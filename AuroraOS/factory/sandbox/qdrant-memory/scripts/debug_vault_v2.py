import sys
from pathlib import Path
import sqlcipher3

def test_vault(db_path, master_key):
    print(f"Testing {db_path} with key {master_key[:5]}...")
    try:
        conn = sqlcipher3.connect(str(db_path))
        # Try both direct and hex
        try:
            conn.execute(f"PRAGMA key = '{master_key}';")
            conn.execute("SELECT count(*) FROM sqlite_master").fetchone()
            print("SUCCESS with direct key!")
            return True
        except:
            pass
            
        try:
            conn.execute(f"PRAGMA key = \"x'{master_key}'\";")
            conn.execute("SELECT count(*) FROM sqlite_master").fetchone()
            print("SUCCESS with hex key!")
            return True
        except:
            pass
            
        return False
    except Exception as e:
        print(f"FAILED: {e}")
        return False

if __name__ == "__main__":
    db = sys.argv[1]
    key = sys.argv[2]
    test_vault(db, key)
