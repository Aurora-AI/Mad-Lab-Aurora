import os
import base64
import secrets
import sqlite3
from pathlib import Path
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import sqlcipher3

# Configurações de Criptografia
KDF_ITERATIONS = 100_000
KEY_PREFIX = "AURORA_PROTECTED_KEY_V1:"

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=KDF_ITERATIONS,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt_master_key(master_key: str, password: str) -> str:
    salt = os.urandom(16)
    key = derive_key(password, salt)
    f = Fernet(key)
    encrypted = f.encrypt(master_key.encode())
    
    salt_b64 = base64.b64encode(salt).decode()
    payload = f"{KEY_PREFIX}{salt_b64}:{encrypted.decode()}"
    return payload

def rebuild_vault(db_path: Path, master_key: str, env_content: str):
    if db_path.exists():
        db_path.unlink()
        
    conn = sqlcipher3.dbapi2.connect(str(db_path))
    conn.execute(f"PRAGMA key='{master_key}'")
    
    # Schema Aurora V1
    conn.execute("""
        CREATE TABLE aurora_secrets (
            namespace TEXT NOT NULL,
            name TEXT NOT NULL,
            value TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (namespace, name)
        )
    """)
    
    count = 0
    for line in env_content.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if line.startswith("export "):
            line = line.removeprefix("export ").strip()
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("\"'")
        
        conn.execute(
            "INSERT OR REPLACE INTO aurora_secrets (namespace, name, value) VALUES (?, ?, ?)",
            ("system", key, value)
        )
        count += 1
        
    conn.commit()
    conn.close()
    return count

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--password", required=True)
    parser.add_argument("--env-content", required=True)
    parser.add_argument("--db-path", default="aurora_vault.db")
    parser.add_argument("--key-file", default="master.key")
    
    args = parser.parse_args()
    
    db_path = Path(args.db_path)
    key_file = Path(args.key_file)
    
    new_master_key = secrets.token_urlsafe(32)
    protected_payload = encrypt_master_key(new_master_key, password=args.password)
    
    print(f"[*] Gerando Chave Mestra Protegida em: {key_file}")
    key_file.write_text(protected_payload, encoding="utf-8")
    
    print(f"[*] Reconstruindo Vault em: {db_path}")
    imported_count = rebuild_vault(db_path, new_master_key, args.env_content)
    
    print(f"[+] Sucesso: {imported_count} segredos importados para o novo Vault.")
