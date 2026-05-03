import os
import logging
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

QDRANT_URL = "http://127.0.0.1:6333"
COLLECTION_NAME = "reflexion_ki"
MODEL_NAME = "all-MiniLM-L6-v2"

def test_search(query: str):
    logger.info(f"Querying Qdrant for: '{query}'")
    client = QdrantClient(url=QDRANT_URL)
    model = SentenceTransformer(MODEL_NAME)
    
    vector = model.encode(query).tolist()
    
    results = client.query(
        collection_name=COLLECTION_NAME,
        query_vector=vector,
        limit=3
    )
    
    print("\n--- Search Results ---")
    for i, res in enumerate(results):
        print(f"{i+1}. [{res.payload.get('id')}] {res.payload.get('title')} (Score: {res.score:.4f})")
        print(f"   Prevention: {res.payload.get('prevention')}")
        print("-" * 20)

if __name__ == "__main__":
    test_search("missing structural validation in t22")
    test_search("asgi server app initialization error")
