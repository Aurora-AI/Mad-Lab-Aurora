"""Executor de sandbox com idempotência e observabilidade."""
from __future__ import annotations

import json
import subprocess
import time
import psutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Imports do sandbox
try:
    from contracts import (
        RepairRequest, RepairResult, RepairState,
        AttemptResult, ActivityEvent, SandboxMode,
    )
except ImportError:
    # Fallback para execuções onde o diretório pai não está no sys.path
    pass


def kill_process_tree(pid: int) -> None:
    """Encerra recursivamente todos os processos filhos (M2)."""
    try:
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)
        for child in children:
            child.terminate()
        psutil.wait_procs(children, timeout=3)
        for child in children:
            if child.is_running():
                child.kill()
        parent.terminate()
        parent.kill()
    except (psutil.NoSuchProcess, Exception):
        pass


def validate_command(cmd: str) -> None:
    """Valida se o comando é seguro para execução local (M2)."""
    forbidden = [";", "&&", "||", "|", "`", "$(", ">", ">>", "<"]
    for char in forbidden:
        if char in cmd:
            raise ValueError(f"Comando contém caracteres proibidos para modo local: {char}")


def execute_in_sandbox(
    cmd_list: list[str],
    mode: SandboxMode,
    timeout_seconds: int = 30,
    work_dir: Path | None = None
) -> tuple[int, str, str, float, dict]:
    """Executa comando coletando métricas de recursos e limpando processos."""
    if mode == SandboxMode.LOCAL_VENV:
        # Validar cada token do comando para evitar injeção básica
        for token in cmd_list:
            validate_command(token)

    stdout, stderr = "", ""
    returncode = 1
    metrics = {"max_rss_mb": 0.0}
    start_time = time.time()
    
    try:
        process = subprocess.Popen(
            cmd_list,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=str(work_dir) if work_dir else None
        )
        
        # Monitoramento de recursos
        try:
            ps_proc = psutil.Process(process.pid)
            while process.poll() is None:
                try:
                    # RSS em MB
                    mem = ps_proc.memory_info().rss / (1024 * 1024)
                    metrics["max_rss_mb"] = max(metrics["max_rss_mb"], mem)
                    
                    # Coletar também de filhos
                    for child in ps_proc.children(recursive=True):
                        mem += child.memory_info().rss / (1024 * 1024)
                    metrics["max_rss_mb"] = max(metrics["max_rss_mb"], mem)
                    
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    break
                
                time.sleep(0.1)
                if (time.time() - start_time) > timeout_seconds:
                    kill_process_tree(process.pid)
                    returncode = 124
                    stderr = "Timeout excedido no executor industrial."
                    break
            
            if returncode != 124:
                stdout, stderr = process.communicate()
                returncode = process.returncode
        except Exception as e:
            kill_process_tree(process.pid)
            stderr = f"Falha no monitoramento: {str(e)}"
            
    except Exception as e:
        stderr = f"Erro ao iniciar processo: {str(e)}"
        returncode = 1
        
    duration = time.time() - start_time
    return returncode, stdout, stderr, duration, metrics


def save_checkpoint(state_path: Path, state: dict) -> None:
    """Salva checkpoint de estado de forma atômica."""
    atomic_write_json(state_path, state)


def atomic_write_json(path: Path, data: dict | Any) -> None:
    """Escreve um JSON de forma atômica usando tempfile + replace."""
    import os
    import tempfile
    
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_path = tempfile.mkstemp(dir=str(path.parent), prefix=path.name + ".tmp")
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
        
        # Retry loop para Windows (contencão de arquivo/antivirus)
        max_retries = 5
        for i in range(max_retries):
            try:
                os.replace(temp_path, str(path))
                break
            except PermissionError:
                if i == max_retries - 1:
                    raise
                time.sleep(0.1)
    except Exception:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise


def load_checkpoint(state_path: Path) -> dict | None:
    """Carrega checkpoint existente para retomada."""
    if state_path.exists():
        return json.loads(state_path.read_text())
    return None


def emit_activity_event(
    activity_path: Path,
    event_type: str,
    os_id: str,
    task_id: str,
    metadata: dict,
) -> None:
    """Emite evento estruturado no activity.jsonl com lock atômico."""
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": event_type,
        "os_id": os_id,
        "actor": "auto-repair-agent",
        "task_id": task_id,
        "metadata": metadata,
    }
    
    lock_path = activity_path.with_suffix(".jsonl.lock")
    
    # Implementação de lock simples e atômica via criação de diretório (cross-platform)
    # ou tentativa de criar arquivo exclusivo.
    timeout = 5
    start = time.time()
    
    while time.time() - start < timeout:
        try:
            # os.open com O_CREAT | O_EXCL é atômico no Windows e Linux
            import os
            fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            try:
                with activity_path.open("a", encoding="utf-8") as f:
                    f.write(json.dumps(event) + "\n")
                break
            finally:
                os.close(fd)
                os.remove(lock_path)
        except FileExistsError:
            time.sleep(0.1)
            continue
    else:
        # Fallback se o lock demorar demais: escreve sem lock (melhor logar do que perder)
        with activity_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event) + "\n")
