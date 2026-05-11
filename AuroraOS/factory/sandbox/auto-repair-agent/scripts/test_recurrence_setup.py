import os
import sys
import json
from pathlib import Path
from qdrant_client import QdrantClient
from qdrant_client.http import models
from datetime import datetime, timezone

# Add parent dir for imports
sys.path.append(str(Path(__file__).parent.parent))

QDRANT_URL = os.getenv("QDRANT_URL", "http://127.0.0.1:6333")
COLLECTION_NAME = "reflexion_ki"

def setup_mock_data():
    client = QdrantClient(url=QDRANT_URL)
    
    # 1. Padrao recorrente (4 ocorrencias)
    point_recurrent = models.PointStruct(
        id=999999,
        vector=[0.1] * 3072, # Dummy vector
        payload={
            "type": "anti_pattern_candidate",
            "pattern_id": "KI-MOCK-RECURRENT",
            "category": "CI",
            "occurrences": 4,
            "ingested_at": datetime.now(timezone.utc).isoformat(),
            "domains": ["UnitTests", "Mocking"]
        }
    )
    
    # 2. Padrao isolado (1 ocorrencia)
    point_isolated = models.PointStruct(
        id=999998,
        vector=[0.2] * 3072,
        payload={
            "type": "anti_pattern_candidate",
            "pattern_id": "KI-MOCK-ISOLATED",
            "category": "IA",
            "occurrences": 1,
            "ingested_at": datetime.now(timezone.utc).isoformat(),
            "domains": ["PromptInjection"]
        }
    )
    
    client.upsert(collection_name=COLLECTION_NAME, points=[point_recurrent, point_isolated])
    print("Mock data upserted to Qdrant.")

if __name__ == "__main__":
    setup_mock_data()
