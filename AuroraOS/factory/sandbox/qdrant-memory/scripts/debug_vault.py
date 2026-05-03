import sys
from pathlib import Path
import sqlcipher3

def test_vault(db_path, master_key):
    print(f"Testing {db_path} with key...")
    try:
        conn = sqlcipher3.connect(str(db_path))
        conn.execute(f"PRAGMA key = '{master_key}';")
        # Try to read something
        res = conn.execute("SELECT count(*) FROM sqlite_master").fetchone()
        print(f"SUCCESS! Found {res[0]} items in sqlite_master")
        
        # Check for aurora_secrets table
        res = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='aurora_secrets'").fetchone()
        if res:
            print("Found aurora_secrets table!")
            # List some keys if possible
            secrets = conn.execute("SELECT tenant_id, key FROM aurora_secrets LIMIT 5").fetchall()
            for s in secrets:
                print(f"  Secret: {s[0]}:{s[1]}")
        else:
            print("aurora_secrets table NOT found.")
        conn.close()
        return True
    except Exception as e:
        print(f"FAILED: {e}")
        return False

if __name__ == "__main__":
    key = "S6MXFOtQZbpvje5cwGyU0EC3AxnLY82u"
    if len(sys.argv) > 1:
        test_vault(sys.argv[1], key)
    else:
        # Default searches
        paths = [
            "C:/Projetos/Aurora/aurora_vault.db",
            "C:/Projetos/Aurora/CRM/apps/crm-core/data/aurora_aios.db",
            "C:/Projetos/Aurora/ElysianLex/lex_core.db",
            "C:/Projetos/Aurora/CRM/apps/crm-core/crm_core.db"
        ]
        for p in paths:
            if Path(p).exists():
                test_vault(p, key)
            else:
                print(f"Path does not exist: {p}")
