import unittest
import json
import tempfile
import shutil
import threading
import time
import sqlite3
import os
from pathlib import Path
from dispatcher import dispatch_loop, DispatcherConfig, StateStore, cleanup_dead_letter

class TestDispatcherV21(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.watch_dir = Path(self.test_dir) / "watch"
        self.watch_dir.mkdir()
        self.db_path = Path(self.test_dir) / "state.db"
        self.dead_letter = Path(self.test_dir) / "dead_letter"
        
        self.config = DispatcherConfig(
            watch_dirs=[self.watch_dir],
            poll_interval_seconds=1,
            activity_log_path=Path(self.test_dir) / "legacy.jsonl"
        )
        self.state = StateStore(self.db_path)
        
    def tearDown(self):
        time.sleep(1)
        shutil.rmtree(self.test_dir, ignore_errors=True)
        
    def test_sqlite_logging(self):
        # Processa um arquivo
        event_file = self.watch_dir / "qa_verdict_MT-001.json"
        with open(event_file, "w") as f:
            json.dump({"task_id": "MT-001", "verdict": "APPROVED"}, f)
            
        thread = threading.Thread(target=dispatch_loop, args=(self.config, self.state, self.dead_letter), daemon=True)
        thread.start()
        time.sleep(2)
        
        # Verifica se o log foi para o SQLite
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT task_id, dispatched_to FROM dispatch_logs WHERE task_id = ?", ("MT-001",))
            row = cursor.fetchone()
            self.assertIsNotNone(row)
            self.assertEqual(row[1], "vault_archivist")
            
    def test_dead_letter_cleanup(self):
        self.dead_letter.mkdir()
        old_file = self.dead_letter / "old_error.json"
        with open(old_file, "w") as f:
            json.dump({"error": "stale"}, f)
            
        # Simula que o arquivo é antigo (8 dias atrás)
        past_time = time.time() - (8 * 86400)
        os.utime(old_file, (past_time, past_time))
        
        # Executa cleanup
        cleanup_dead_letter(self.dead_letter, max_age_days=7)
        
        self.assertFalse(old_file.exists())
        
    def test_persistence_between_restarts(self):
        event_file = self.watch_dir / "qa_verdict_MT-100.json"
        with open(event_file, "w") as f:
            json.dump({"task_id": "MT-100", "verdict": "REJECTED"}, f)
            
        thread = threading.Thread(target=dispatch_loop, args=(self.config, self.state, self.dead_letter), daemon=True)
        thread.start()
        time.sleep(2)
        
        self.assertTrue(self.state.is_seen(event_file))
        
        # Novo state object
        new_state = StateStore(self.db_path)
        self.assertTrue(new_state.is_seen(event_file))

    def test_robust_read_retry(self):
        """Testa se o dispatcher sobrevive a arquivos temporariamente bloqueados ou vazios."""
        event_file = self.watch_dir / "retry_event.json"
        
        # Simula arquivo que começa vazio e depois é preenchido
        event_file.write_text("") 
        
        # O parse_event deve retornar None inicialmente (robust_read vai tentar 3x)
        from dispatcher import parse_event
        event = parse_event(event_file)
        self.assertIsNone(event)
        
        # Agora preenche o arquivo corretamente
        event_file.write_text(json.dumps({"task_id": "RETRY-1", "test_exit_code": 1}))
        event = parse_event(event_file)
        self.assertIsNotNone(event)
        self.assertEqual(event.task_id, "RETRY-1")

if __name__ == "__main__":
    unittest.main()
