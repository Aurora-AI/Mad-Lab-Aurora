import asyncio
import json
import logging
import sqlite3
from pathlib import Path
from datetime import datetime, timezone
import sys
import os
import argparse
from typing import Set
from nats.aio.client import Client as NATS

# Adiciona o diretório atual e o pai ao sys.path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.append(str(current_dir))
sys.path.append(str(parent_dir))

try:
    from contracts import DispatchEvent, DispatcherConfig
except ImportError:
    # Fallback para desenvolvimento local
    from pydantic import BaseModel
    class DispatchEvent(BaseModel):
        event_type: str
        source_file: Path
        task_id: str
        os_id: str
        detected_at: str
        dispatched_to: str

    class DispatcherConfig(BaseModel):
        watch_dirs: list[Path]
        poll_interval_seconds: int
        activity_log_path: Path

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

async def publish_telemetry(nc: NATS, event: DispatchEvent):
    """Publica métricas no barramento NATS para consumo do Dashboard."""
    if not nc or not nc.is_connected:
        return
    
    try:
        payload = {
            "event_type": event.event_type,
            "task_id": event.task_id,
            "os_id": event.os_id,
            "dispatched_to": event.dispatched_to,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        await nc.publish("aurora.telemetry.metrics", json.dumps(payload).encode())
    except Exception as e:
        logger.error(f"Erro ao publicar telemetria: {e}")

def robust_read(file_path: Path, max_retries: int = 3, initial_delay: float = 0.1) -> dict | None:
    delay = initial_delay
    for attempt in range(max_retries):
        try:
            if not file_path.exists() or file_path.stat().st_size == 0:
                time.sleep(delay)
                continue
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            if attempt < max_retries - 1:
                time.sleep(delay)
                delay *= 2
            else:
                return None
    return None

import time # Mantido para robust_read por enquanto

def parse_event(event_file: Path) -> DispatchEvent | None:
    try:
        data = robust_read(event_file)
        if not data: return None
        
        filename = event_file.name
        if filename.startswith("qa_verdict_"):
            verdict = data.get("verdict", "")
            return DispatchEvent(
                event_type=f"QA_{verdict}",
                source_file=event_file,
                task_id=data.get("task_id", "UNKNOWN"),
                os_id=data.get("os_id", "UNKNOWN"),
                detected_at=datetime.now(timezone.utc).isoformat(),
                dispatched_to="vault_archivist" if verdict == "APPROVED" else "repair_loop"
            )
        elif filename.startswith("repair_result_") or "patch_diff" in data:
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
            return DispatchEvent(
                event_type="MICRO_TASK_COMPLETED",
                source_file=event_file,
                task_id=data.get("task_id", "UNKNOWN"),
                os_id="UNKNOWN",
                detected_at=datetime.now(timezone.utc).isoformat(),
                dispatched_to="repair_loop" if exit_code != 0 else "none"
            )
    except Exception as e:
        logger.error(f"Erro no parse de {event_file}: {e}")
    return None

async def dispatch_loop(config: DispatcherConfig, state: StateStore, dead_letter_dir: Path, nats_url: str):
    nc = NATS()
    try:
        await nc.connect(nats_url)
        logger.info(f"Conectado ao NATS em {nats_url}")
    except Exception as e:
        logger.warning(f"Não foi possível conectar ao NATS: {e}. Operando em modo offline (DB apenas).")
        nc = None

    logger.info(f"Iniciando Dispatcher v2.3 (Async/NATS). Monitorando {len(config.watch_dirs)} diretórios...")
    
    iteration = 0
    try:
        while True:
            iteration += 1
            for watch_dir in config.watch_dirs:
                if not watch_dir.exists(): continue
                for event_file in watch_dir.glob("*.json"):
                    if not state.is_seen(event_file):
                        event = parse_event(event_file)
                        if event:
                            logger.info(f"Evento detectado: {event.event_type} -> {event.dispatched_to}")
                            state.log_dispatch(event)
                            if nc: await publish_telemetry(nc, event)
                            state.mark_seen(event_file)
                            state.clear_attempts(event_file)
                        else:
                            attempts = state.increment_attempt(event_file)
                            if attempts >= 5:
                                dead_letter_dir.mkdir(parents=True, exist_ok=True)
                                event_file.rename(dead_letter_dir / event_file.name)
                                state.mark_seen(event_file)
            await asyncio.sleep(config.poll_interval_seconds)
    except asyncio.CancelledError:
        logger.info("Encerrando Dispatcher...")
    finally:
        if nc: await nc.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--watch-dir", type=str, required=True)
    parser.add_argument("--db-path", type=str, default="dispatcher_state.db")
    parser.add_argument("--nats-url", type=str, default="nats://localhost:4222")
    args = parser.parse_args()
    
    config = DispatcherConfig(
        watch_dirs=[Path(args.watch_dir)],
        poll_interval_seconds=2,
        activity_log_path=Path("legacy.jsonl")
    )
    state = StateStore(Path(args.db_path))
    
    try:
        asyncio.run(dispatch_loop(config, state, Path("dead_letter"), args.nats_url))
    except KeyboardInterrupt:
        pass
