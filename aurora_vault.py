from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Iterable, Sequence
try:
    import tomllib
except ImportError:
    import tomli as tomllib
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet


SYSTEM_NAMESPACE = "system"
DEFAULT_NAMESPACES = (SYSTEM_NAMESPACE,)
NAMESPACE_ALIASES = {
    "global": SYSTEM_NAMESPACE,
}

KEY_PREFIX = "AURORA_PROTECTED_KEY_V1:"
KDF_ITERATIONS = 100_000


class AuroraVaultError(RuntimeError):
    """Base error for AuroraVault failures."""


class AuroraVaultDependencyError(AuroraVaultError):
    """Raised when SQLCipher support is not available."""


class AuroraVaultConfigurationError(AuroraVaultError):
    """Raised when the vault cannot be configured securely."""


class AuroraVaultSecretNotFoundError(AuroraVaultError):
    """Raised when a requested secret does not exist in the vault."""


def _default_database_path() -> Path:
    return Path(__file__).resolve().with_name("aurora_vault.db")


def _decrypt_protected_key(payload: str) -> str:
    """Decrypts a protected master key using the user password."""
    password = os.getenv("AURORA_VAULT_PASSWORD")
    if not password:
        # Fallback to interactive input if in a TTY or explicitly allowed
        import getpass
        try:
            password = getpass.getpass("AuroraVault password required: ")
        except Exception:
            raise AuroraVaultConfigurationError(
                "AuroraVault password required but environment variable AURORA_VAULT_PASSWORD is not set."
            )

    try:
        # Format: PREFIX:SALT_B64:ENCRYPTED_B64
        parts = payload.removeprefix(KEY_PREFIX).split(":")
        if len(parts) != 2:
            raise ValueError("Invalid protected key format.")
        
        salt = base64.b64decode(parts[0])
        encrypted_data = parts[1].encode()

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=KDF_ITERATIONS,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        f = Fernet(key)
        return f.decrypt(encrypted_data).decode()
    except Exception as exc:
        msg = str(exc)
        # Se for erro de token inválido (senha errada), fornece feedback claro
        if "InvalidToken" in type(exc).__name__:
            msg = "Senha incorreta ou chave corrompida."
        raise AuroraVaultConfigurationError(f"Failed to decrypt Master Key: {msg}") from exc


def _read_master_key_from_file(path_value: str | None) -> str:
    if not path_value:
        return ""
    key_path = Path(path_value).expanduser().resolve()
    if not key_path.exists():
        raise AuroraVaultConfigurationError(f"Master key file not found: {key_path}")
    
    content = key_path.read_text(encoding="utf-8").strip()
    if content.startswith(KEY_PREFIX):
        return _decrypt_protected_key(content)
    return content


def resolve_master_key() -> str:
    key_file_path = os.getenv("AURORA_MASTER_KEY_FILE")
    if key_file_path:
        return _read_master_key_from_file(key_file_path)
    
    key = (os.getenv("AURORA_MASTER_KEY") or "").strip()
    if key.startswith(KEY_PREFIX):
        return _decrypt_protected_key(key)
    if key:
        return key
    
    raise AuroraVaultConfigurationError(
        "AuroraVault master key is missing. Configure AURORA_MASTER_KEY_FILE or AURORA_MASTER_KEY."
    )


def _normalize_namespaces(namespaces: Sequence[str] | None) -> tuple[str, ...]:
    raw = namespaces or DEFAULT_NAMESPACES
    normalized = []
    for item in raw:
        if not item or not item.strip():
            continue
        value = item.strip()
        normalized.append(NAMESPACE_ALIASES.get(value, value))
    normalized = tuple(dict.fromkeys(normalized))
    return normalized or DEFAULT_NAMESPACES


def _escape_pragma(value: str) -> str:
    return value.replace("'", "''")


@dataclass(slots=True)
class AuroraSecretRecord:
    namespace: str
    name: str
    value: str | None = None


class AuroraVault:
    """Central SQLCipher-backed source of truth for Aurora secrets."""

    def __init__(self, database_path: str | Path | None = None, master_key: str | None = None):
        self.database_path = Path(database_path or _default_database_path()).expanduser().resolve()
        self.master_key = (master_key or resolve_master_key()).strip()
        if not self.master_key:
            raise AuroraVaultConfigurationError("AuroraVault master key resolved to an empty value.")
        self._dbapi = self._load_sqlcipher()
        self._schema_variant = "tenant"
        self._connection = self._connect()
        self._ensure_schema()

    @staticmethod
    def _load_sqlcipher():
        try:
            import sqlcipher3  # type: ignore[import-not-found]
        except ImportError as exc:
            raise AuroraVaultDependencyError(
                "sqlcipher3 is required to operate AuroraVault. Install sqlcipher3-wheels in the runtime."
            ) from exc
        return sqlcipher3.dbapi2

    def _connect(self):
        connection = self._dbapi.connect(str(self.database_path))
        connection.row_factory = self._dbapi.Row
        connection.execute(f"PRAGMA key='{_escape_pragma(self.master_key)}'")
        connection.execute("PRAGMA foreign_keys=ON")
        try:
            connection.execute("SELECT count(*) FROM sqlite_master").fetchone()
        except Exception as exc:  # pragma: no cover - depends on SQLCipher runtime
            raise AuroraVaultConfigurationError(
                "Failed to open AuroraVault. Verify the master key and the encrypted database path."
            ) from exc
        return connection

    def _ensure_schema(self) -> None:
        table = self._connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'aurora_secrets'"
        ).fetchone()
        if table is None:
            self._connection.execute(
                """
                CREATE TABLE aurora_secrets (
                    tenant_id TEXT NOT NULL,
                    key TEXT NOT NULL,
                    value JSON NOT NULL,
                    PRIMARY KEY (tenant_id, key)
                )
                """
            )
            self._connection.commit()
            self._schema_variant = "tenant"
            return

        columns = {
            str(row["name"])
            for row in self._connection.execute("PRAGMA table_info(aurora_secrets)").fetchall()
        }
        if {"tenant_id", "key", "value"}.issubset(columns):
            self._schema_variant = "tenant"
            return
        if {"namespace", "name", "value"}.issubset(columns):
            self._schema_variant = "namespace"
            return
        raise AuroraVaultConfigurationError(
            "Unsupported AuroraVault schema. Expected tenant_id/key/value or namespace/name/value columns."
        )

    def _namespace_column(self) -> str:
        return "tenant_id" if self._schema_variant == "tenant" else "namespace"

    def _name_column(self) -> str:
        return "key" if self._schema_variant == "tenant" else "name"

    def _value_select_expr(self) -> str:
        return "json_extract(value, '$')" if self._schema_variant == "tenant" else "value"

    def _serialize_value(self, value: str) -> str:
        if self._schema_variant == "tenant":
            return json.dumps(value, ensure_ascii=True)
        return value

    def list_secret_names(self, namespaces: Sequence[str] | None = None) -> list[AuroraSecretRecord]:
        rows: list[AuroraSecretRecord] = []
        namespace_column = self._namespace_column()
        name_column = self._name_column()
        for namespace in _normalize_namespaces(namespaces):
            cursor = self._connection.execute(
                f"""
                SELECT {namespace_column} AS namespace, {name_column} AS name
                FROM aurora_secrets
                WHERE {namespace_column} = ?
                ORDER BY {name_column} ASC
                """,
                (namespace,),
            )
            rows.extend(
                AuroraSecretRecord(
                    namespace=row["namespace"],
                    name=row["name"],
                )
                for row in cursor.fetchall()
            )
        return rows

    def get_secret(
        self,
        name: str,
        *,
        namespaces: Sequence[str] | None = None,
        default: str | None = None,
        required: bool = False,
    ) -> str | None:
        namespace_column = self._namespace_column()
        name_column = self._name_column()
        value_expr = self._value_select_expr()
        for namespace in _normalize_namespaces(namespaces):
            row = self._connection.execute(
                f"""
                SELECT {value_expr} AS value
                FROM aurora_secrets
                WHERE {namespace_column} = ? AND {name_column} = ?
                """,
                (namespace, name),
            ).fetchone()
            if row is not None:
                value = row["value"]
                if value is None:
                    continue
                return str(value)

        if required:
            raise AuroraVaultSecretNotFoundError(
                f"Secret '{name}' was not found in namespaces {', '.join(_normalize_namespaces(namespaces))}."
            )
        return default

    def set_secret(self, name: str, value: str, *, namespace: str = SYSTEM_NAMESPACE) -> None:
        normalized_namespace = _normalize_namespaces((namespace,))[0]
        namespace_column = self._namespace_column()
        name_column = self._name_column()
        if self._schema_variant == "tenant":
            self._connection.execute(
                f"""
                INSERT INTO aurora_secrets ({namespace_column}, {name_column}, value)
                VALUES (?, ?, json(?))
                ON CONFLICT({namespace_column}, {name_column})
                DO UPDATE SET value = excluded.value
                """,
                (normalized_namespace, name, self._serialize_value(value)),
            )
        else:
            self._connection.execute(
                f"""
                INSERT INTO aurora_secrets ({namespace_column}, {name_column}, value, updated_at)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT({namespace_column}, {name_column})
                DO UPDATE SET value = excluded.value, updated_at = CURRENT_TIMESTAMP
                """,
                (normalized_namespace, name, value),
            )
        self._connection.commit()

    def delete_secret(self, name: str, *, namespace: str = SYSTEM_NAMESPACE) -> None:
        normalized_namespace = _normalize_namespaces((namespace,))[0]
        namespace_column = self._namespace_column()
        name_column = self._name_column()
        self._connection.execute(
            f"DELETE FROM aurora_secrets WHERE {namespace_column} = ? AND {name_column} = ?",
            (normalized_namespace, name),
        )
        self._connection.commit()

    def import_env_file(self, env_path: str | Path, *, namespace: str = SYSTEM_NAMESPACE) -> list[str]:
        path = Path(env_path).expanduser().resolve()
        if not path.exists():
            raise AuroraVaultConfigurationError(f"Env file not found: {path}")

        imported: list[str] = []
        if path.suffix.lower() == ".toml":
            loaded = tomllib.loads(path.read_text(encoding="utf-8"))
            pending: list[tuple[str, str]] = []

            def visit(prefix: str, payload: object) -> None:
                if isinstance(payload, dict):
                    for child_key, child_value in payload.items():
                        child_prefix = f"{prefix}.{child_key}" if prefix else str(child_key)
                        visit(child_prefix, child_value)
                    return
                if isinstance(payload, (str, int, float, bool)):
                    pending.append((prefix, str(payload)))

            visit("", loaded)
        else:
            pending = []
            for raw_line in path.read_text(encoding="utf-8").splitlines():
                line = raw_line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                if line.startswith("export "):
                    line = line.removeprefix("export ").strip()
                key, value = line.split("=", 1)
                pending.append((key.strip(), value.strip().strip("\"'")))

        for name, secret_value in pending:
            if not name or not secret_value:
                continue
            self.set_secret(name=name, value=secret_value, namespace=namespace)
            imported.append(name)
        return imported

    def close(self) -> None:
        self._connection.close()


@lru_cache(maxsize=1)
def get_default_vault() -> AuroraVault:
    return AuroraVault()


def get_secret(
    name: str,
    *,
    namespaces: Sequence[str] | None = None,
    default: str | None = None,
    required: bool = False,
) -> str | None:
    return get_default_vault().get_secret(
        name,
        namespaces=namespaces,
        default=default,
        required=required,
    )


def set_secret(name: str, value: str, *, namespace: str = SYSTEM_NAMESPACE) -> None:
    get_default_vault().set_secret(name, value, namespace=namespace)


def delete_secret(name: str, *, namespace: str = SYSTEM_NAMESPACE) -> None:
    get_default_vault().delete_secret(name, namespace=namespace)


def _parse_namespaces(value: str | None) -> tuple[str, ...]:
    if not value:
        return DEFAULT_NAMESPACES
    return _normalize_namespaces([part for part in value.split(",")])


def _cmd_get(args: argparse.Namespace) -> int:
    value = get_secret(
        args.name,
        namespaces=_parse_namespaces(args.namespaces),
        default=None,
        required=not args.optional,
    )
    payload = {"ok": value is not None, "name": args.name, "value": value}
    print(json.dumps(payload, ensure_ascii=True))
    return 0


def _cmd_set(args: argparse.Namespace) -> int:
    vault = get_default_vault()
    vault.set_secret(args.name, args.value, namespace=args.namespace)
    print(json.dumps({"ok": True, "name": args.name, "namespace": args.namespace}, ensure_ascii=True))
    return 0


def _cmd_delete(args: argparse.Namespace) -> int:
    vault = get_default_vault()
    vault.delete_secret(args.name, namespace=args.namespace)
    print(json.dumps({"ok": True, "name": args.name, "namespace": args.namespace}, ensure_ascii=True))
    return 0


def _cmd_import_env(args: argparse.Namespace) -> int:
    vault = get_default_vault()
    imported = vault.import_env_file(args.path, namespace=args.namespace)
    print(
        json.dumps(
            {"ok": True, "namespace": args.namespace, "imported": imported, "count": len(imported)},
            ensure_ascii=True,
        )
    )
    return 0


def _cmd_list(args: argparse.Namespace) -> int:
    vault = get_default_vault()
    rows = vault.list_secret_names(_parse_namespaces(args.namespaces))
    print(
        json.dumps(
            {
                "ok": True,
                "records": [{"namespace": row.namespace, "name": row.name} for row in rows],
            },
            ensure_ascii=True,
        )
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AuroraVault CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    get_parser = subparsers.add_parser("get", help="Read a secret from AuroraVault")
    get_parser.add_argument("--name", required=True)
    get_parser.add_argument("--namespaces", default="global")
    get_parser.add_argument("--optional", action="store_true")
    get_parser.set_defaults(func=_cmd_get)

    set_parser = subparsers.add_parser("set", help="Write a secret to AuroraVault")
    set_parser.add_argument("--name", required=True)
    set_parser.add_argument("--value", required=True)
    set_parser.add_argument("--namespace", default="global")
    set_parser.set_defaults(func=_cmd_set)

    delete_parser = subparsers.add_parser("delete", help="Delete a secret from AuroraVault")
    delete_parser.add_argument("--name", required=True)
    delete_parser.add_argument("--namespace", default="global")
    delete_parser.set_defaults(func=_cmd_delete)

    import_parser = subparsers.add_parser("import-env", help="Import secrets from an env file")
    import_parser.add_argument("--path", required=True)
    import_parser.add_argument("--namespace", default="global")
    import_parser.set_defaults(func=_cmd_import_env)

    list_parser = subparsers.add_parser("list", help="List secret names in AuroraVault")
    list_parser.add_argument("--namespaces", default="global")
    list_parser.set_defaults(func=_cmd_list)

    return parser


def main(argv: Iterable[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    try:
        return int(args.func(args))
    except AuroraVaultError as exc:
        print(json.dumps({"ok": False, "error": exc.__class__.__name__, "message": str(exc)}, ensure_ascii=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
