from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
import sys

def setup():
    client = QdrantClient(host="localhost", port=6333)
    
    collection_name = "reflexion_ki"
    
    # Verifica se já existe
    collections = client.get_collections().collections
    print(f"Recriando coleção '{collection_name}' (3072d, Cosine)...")
    if any(c.name == collection_name for c in collections):
        client.delete_collection(collection_name)
        
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=3072, distance=Distance.COSINE),
    )
    print("Sucesso: Memória vetorial inicializada.")

if __name__ == "__main__":
    try:
        setup()
    except Exception as e:
        print(f"Erro ao conectar ao Qdrant: {e}")
        sys.exit(1)
