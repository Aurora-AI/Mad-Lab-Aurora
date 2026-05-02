"""Classificador de modo de sandbox baseado em tokenização de comando."""
from __future__ import annotations

import shlex
from enum import Enum


class SandboxMode(str, Enum):
    MEMORY = "memory"
    WORKTREE = "worktree"
    CONTAINER = "container"


# Binários que exigem container
CONTAINER_BINARIES = frozenset({
    "docker", "docker-compose", "docker compose",
    "psql", "redis-cli", "mongosh", "curl", "wget",
    "uvicorn", "gunicorn", "celery",
})

# Binários que exigem worktree
WORKTREE_BINARIES = frozenset({
    "pytest", "python", "python3", "node", "npm", "npx",
    "vitest", "jest", "tsc", "mypy", "ruff", "uv",
})


def classify_mode(test_cmd: list[str]) -> SandboxMode:
    """Classifica o modo de sandbox baseado no binário principal do comando.

    Args:
        test_cmd: Comando como lista de tokens (ex: ["pytest", "-q", "tests/"])

    Returns:
        SandboxMode adequado para o comando.
    """
    if not test_cmd:
        return SandboxMode.MEMORY

    # Extrair binário principal (primeiro token)
    primary_binary = test_cmd[0].split("/")[-1].split("\\")[-1].lower()

    # Checar container primeiro (mais restritivo)
    if primary_binary in CONTAINER_BINARIES:
        return SandboxMode.CONTAINER

    # Checar worktree
    if primary_binary in WORKTREE_BINARIES:
        return SandboxMode.WORKTREE

    # Fallback seguro: memory (menos permissivo)
    return SandboxMode.MEMORY


def classify_from_string(cmd_string: str) -> SandboxMode:
    """Wrapper para classificar a partir de string (conveniência).

    Usa shlex.split para tokenização segura em vez de substring match.
    """
    try:
        tokens = shlex.split(cmd_string)
    except ValueError:
        # Se shlex falhar (ex: quotes não fechados), fallback seguro
        return SandboxMode.MEMORY
    return classify_mode(tokens)
