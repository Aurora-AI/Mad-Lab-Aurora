import sqlite3
import sys
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("DB-Health-Check")

def verify_db_integrity(db_path: Path) -> bool:
    """Executa verificações de integridade física e lógica no banco SQLite."""
    if not db_path.exists():
        logger.error(f"Arquivo de banco de dados não encontrado: {db_path}")
        return False

    try:
        with sqlite3.connect(f"file:{db_path}?mode=ro", uri=True) as conn:
            # 1. Teste de Integridade Física (SQLite)
            cursor = conn.execute("PRAGMA integrity_check")
            result = cursor.fetchone()[0]
            if result != "ok":
                logger.error(f"Falha na integridade física do SQLite: {result}")
                return False
            
            # 2. Verificação de Tabelas Obrigatórias (Maturidade Industrial)
            required_tables = {"seen_files", "failed_attempts", "dispatch_logs"}
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
            existing_tables = {row[0] for row in cursor.fetchall()}
            
            missing = required_tables - existing_tables
            if missing:
                logger.error(f"Tabelas obrigatórias ausentes: {missing}")
                return False
                
            # 3. Verificação de Índices
            required_indexes = {"idx_logs_task_id", "idx_logs_timestamp"}
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='index'")
            existing_indexes = {row[0] for row in cursor.fetchall()}
            
            missing_idx = required_indexes - existing_indexes
            if missing_idx:
                logger.warning(f"Índices de performance ausentes: {missing_idx}")
                # Índices ausentes não falham o health check, mas emitem alerta.

            # 4. Estatísticas Rápidas
            cursor = conn.execute("SELECT COUNT(*) FROM dispatch_logs")
            log_count = cursor.fetchone()[0]
            logger.info(f"Integridade OK. Total de logs processados: {log_count}")
            
    except sqlite3.Error as e:
        logger.error(f"Erro crítico de acesso ao SQLite: {e}")
        return False
    except Exception as e:
        logger.error(f"Erro inesperado no Health Check: {e}")
        return False

    return True

if __name__ == "__main__":
    # Caminho padrão ou via argumento
    db_file = Path("dispatcher_state.db")
    if len(sys.argv) > 1:
        db_file = Path(sys.argv[1])

    logger.info(f"Iniciando Health Check em: {db_file}")
    if verify_db_integrity(db_file):
        logger.info("STATUS: HEALTHY")
        sys.exit(0)
    else:
        logger.error("STATUS: UNHEALTHY")
        sys.exit(1)
