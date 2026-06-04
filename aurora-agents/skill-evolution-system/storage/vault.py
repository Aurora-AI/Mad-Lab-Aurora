import json
import os
from datetime import date, datetime

VAULT_FILE = os.path.join(os.path.dirname(__file__), "..", "vault_log.json")

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        return super().default(obj)

def persist(result):
    with open(VAULT_FILE, "a", encoding='utf-8') as f:
        f.write(json.dumps(result, cls=DateTimeEncoder, ensure_ascii=False) + "\n")
