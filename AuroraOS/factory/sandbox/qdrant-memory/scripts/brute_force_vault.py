import sqlcipher3
from pathlib import Path

def test_config(db_path, key, pragmas):
    try:
        conn = sqlcipher3.connect(str(db_path))
        conn.execute(f"PRAGMA key = '{key}';")
        for p in pragmas:
            conn.execute(p)
        # Test read
        conn.execute("SELECT count(*) FROM sqlite_master").fetchone()
        print(f"SUCCESS with pragmas: {pragmas}")
        return True
    except Exception:
        return False
    finally:
        try: conn.close()
        except: pass

db = "C:/Projetos/Aurora/aurora_vault.db"
key = "S6MXFOtQZbpvje5cwGyU0EC3AxnLY82u"

configs = [
    [],
    ["PRAGMA cipher_compatibility = 3;"],
    ["PRAGMA cipher_compatibility = 4;"],
    ["PRAGMA kdf_iter = 64000;"],
    ["PRAGMA cipher_page_size = 1024;"],
    ["PRAGMA cipher_page_size = 4096;"],
    ["PRAGMA cipher_hmac_algorithm = 'HMAC_SHA1';"],
    ["PRAGMA cipher_kdf_algorithm = 'PBKDF2_HMAC_SHA1';"]
]

for cfg in configs:
    if test_config(db, key, cfg):
        break
else:
    print("All standard configs failed.")
