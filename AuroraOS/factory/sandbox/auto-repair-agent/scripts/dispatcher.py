import time
import json
import logging
import sqlite3
from pathlib import Path
from datetime import datetime, timezone
import sys
import os
import argparse
from typing import Set

# Adiciona o diretório atual e o pai ao sys.path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.append(str(current_dir))
sys.path.append(str(parent_dir))

from contracts import DispatchEvent, DispatcherConfig

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

class StateStore:
    """Gerencia a persistência de estado e auditoria do dispatcher via SQLite."""
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS seen_files (
                    file_path TEXT PRIMARY KEY,
                    processed_at TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS failed_attempts (
                    file_path TEXT PRIMARY KEY,
                    attempts INTEGER DEFAULT 0
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS dispatch_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP,
                    event_type TEXT,
                    os_id TEXT,
                    task_id TEXT,
                    source_file TEXT,
                    dispatched_to TEXT,
                    metadata TEXT
                )
            """)
            # Índices sugeridos pelo QA para performance industrial
            conn.execute("CREATE INDEX IF NOT EXISTS idx_logs_task_id ON dispatch_logs(task_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_logs_timestamp ON dispatch_logs(timestamp)")

    def is_seen(self, file_path: Path) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT 1 FROM seen_files WHERE file_path = ?", (str(file_path),))
            return cursor.fetchone() is not None

    def mark_seen(self, file_path: Path):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO seen_files (file_path, processed_at) VALUES (?, ?)",
                (str(file_path), datetime.now(timezone.utc).isoformat())
            )

    def get_attempts(self, file_path: Path) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT attempts FROM failed_attempts WHERE file_path = ?", (str(file_path),))
            row = cursor.fetchone()
            return row[0] if row else 0

    def increment_attempt(self, file_path: Path):
        attempts = self.get_attempts(file_path) + 1
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO failed_attempts (file_path, attempts) VALUES (?, ?)",
                (str(file_path), attempts)
            )
        return attempts

    def clear_attempts(self, file_path: Path):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM failed_attempts WHERE file_path = ?", (str(file_path),))

    def log_dispatch(self, event: DispatchEvent):
        """Persiste o log de dispatch diretamente no banco de dados."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO dispatch_logs 
                (timestamp, event_type, os_id, task_id, source_file, dispatched_to, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                datetime.now(timezone.utc).isoformat(),
                "DISPATCH_EXECUTED",
                event.os_id,
                event.task_id,
                event.source_file.name,
                event.dispatched_to,
                json.dumps({"source_event": event.event_type})
            ))

def robust_read(file_path: Path, max_retries: int = 3, initial_delay: float = 0.1) -> dict | None:
    """Realiza leitura robusta com retentativas para contornar locks de arquivo (Windows)."""
    delay = initial_delay
    for attempt in range(max_retries):
        try:
            if file_path.stat().st_size == 0:
                time.sleep(delay)  # Aguarda o processo de escrita terminar
                continue
                
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (PermissionError, json.JSONDecodeError, OSError):
            if attempt < max_retries - 1:
                time.sleep(delay)
                delay *= 2  # Backoff exponencial
            else:
                return None
    return None

def parse_event(event_file: Path) -> DispatchEvent | None:
    """Extrai informações de um arquivo JSON para determinar o evento com leitura robusta."""
    try:
        data = robust_read(event_file)
        if not data:
            return None
            
        filename = event_file.name
        
        if filename.startswith("qa_verdict_"):
            task_id = data.get("task_id", "UNKNOWN")
            verdict = data.get("verdict", "")
            if verdict == "REJECTED":
                return DispatchEvent(
                    event_type="QA_REJECTED",
                    source_file=event_file,
                    task_id=task_id,
                    os_id=data.get("os_id", "UNKNOWN"),
                    detected_at=datetime.now(timezone.utc).isoformat(),
                    dispatched_to="repair_loop"
                )
            elif verdict == "APPROVED":
                return DispatchEvent(
                    event_type="QA_APPROVED",
                    source_file=event_file,
                    task_id=task_id,
                    os_id=data.get("os_id", "UNKNOWN"),
                    detected_at=datetime.now(timezone.utc).isoformat(),
                    dispatched_to="vault_archivist"
                )
        elif filename.startswith("repair_result_") or ("status" in data and "patch_diff" in data):
            return DispatchEvent(
                event_type="REPAIR_COMPLETED",
                source_file=event_file,
                task_id=data.get("task_id", "UNKNOWN"),
                os_id="UNKNOWN",
                detected_at=datetime.now(timezone.utc).isoformat(),
                dispatched_to="qa_headless"
            )
        elif filename.startswith("task_result_") or "test_exit_code" in data:
            exit_code = data.get("test_exit_code", 0)
            if exit_code != 0:
                return DispatchEvent(
                    event_type="MICRO_TASK_COMPLETED",
                    source_file=event_file,
                    task_id=data.get("task_id", "UNKNOWN"),
                    os_id="UNKNOWN",
                    detected_at=datetime.now(timezone.utc).isoformat(),
                    dispatched_to="repair_loop"
                )
    except Exception as e:
        logger.error(f"Erro crítico no processamento de {event_file}: {e}")
        
    return None

def route_event(event: DispatchEvent):
    logger.info(f"Roteando evento {event.event_type} para {event.dispatched_to} (Task: {event.task_id})")
    if event.dispatched_to == "repair_loop":
        logger.info(f"-> Acionando auto-repair-agent para a task {event.task_id}")
    elif event.dispatched_to == "qa_headless":
        logger.info(f"-> Acionando QA Headless para a task {event.task_id}")

def cleanup_dead_letter(dead_letter_dir: Path, max_age_days: int = 7):
    """Remove arquivos antigos da quarentena para evitar transbordamento."""
    if not dead_letter_dir.exists():
        return
    
    now = time.time()
    removed_count = 0
    for f in dead_letter_dir.glob("*.json"):
        if f.is_file():
            if now - f.stat().st_mtime > (max_age_days * 86400):
                try:
                    f.unlink()
                    removed_count += 1
                except Exception as e:
                    logger.error(f"Erro ao remover {f}: {e}")
    
    if removed_count > 0:
        logger.info(f"Limpeza de quarentena concluída: {removed_count} arquivos removidos.")

def handle_dead_letter(event_file: Path, dead_letter_dir: Path):
    dead_letter_dir.mkdir(parents=True, exist_ok=True)
    target = dead_letter_dir / event_file.name
    logger.warning(f"Movendo {event_file} para DEAD-LETTER: {target}")
    try:
        if target.exists():
            target.unlink()
        event_file.rename(target)
    except Exception as e:
        logger.error(f"Erro ao mover para dead-letter: {e}")

def dispatch_loop(config: DispatcherConfig, state: StateStore, dead_letter_dir: Path):
    """Loop de polling v2.2 - Otimizado com índices e cleanup silencioso."""
    logger.info(f"Iniciando Dispatcher v2.2 (Final). Monitorando {len(config.watch_dirs)} diretórios...")
    
    iteration_count = 0
    try:
        while True:
            iteration_count += 1
            
            if iteration_count % 100 == 0:
                cleanup_dead_letter(dead_letter_dir)

            for watch_dir in config.watch_dirs:
                if not watch_dir.exists():
                    continue
                    
                for event_file in watch_dir.glob("*.json"):
                    try:
                        if not state.is_seen(event_file):
                            event = parse_event(event_file)
                            if event:
                                route_event(event)
                                state.log_dispatch(event)
                                state.mark_seen(event_file)
                                state.clear_attempts(event_file)
                            else:
                                attempts = state.increment_attempt(event_file)
                                if attempts >= 5:
                                    handle_dead_letter(event_file, dead_letter_dir)
                                    state.mark_seen(event_file)
                    except Exception as e:
                        logger.error(f"Erro inesperado ao processar {event_file}: {e}")
                        # Não marca como visto para permitir retentativa se não foi um erro de quarentena
                                
            time.sleep(config.poll_interval_seconds)
    except KeyboardInterrupt:
        logger.info("Encerrando Dispatcher graciosamente.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--watch-dir", type=str, required=True, help="Diretório para monitorar")
    parser.add_argument("--db-path", type=str, default="dispatcher_state.db", help="Caminho do banco SQLite")
    parser.add_argument("--dead-letter", type=str, default="dead_letter", help="Diretório de dead-letter")
    parser.add_argument("--interval", type=int, default=5, help="Intervalo de polling em segundos")
    
    args = parser.parse_args()
    
    watch_dirs = [Path(args.watch_dir)]
    for w in watch_dirs:
        w.mkdir(parents=True, exist_ok=True)
        
    config = DispatcherConfig(
        watch_dirs=watch_dirs,
        poll_interval_seconds=args.interval,
        activity_log_path=Path("legacy_activity.jsonl")
    )
    
    state = StateStore(Path(args.db_path))
    dead_letter_dir = Path(args.dead_letter)
    
    dispatch_loop(config, state, dead_letter_dir)
