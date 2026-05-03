from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
import sys

def setup():
    client = QdrantClient(host="localhost", port=6333)
    
    collection_name = "reflexion_ki"
    
    # Verifica se já existe
    collections = client.get_collections().collections
    if any(c.name == collection_name for c in collections):
        print(f"Coleção '{collection_name}' já existe. Ignorando criação.")
        return

    print(f"Criando coleção '{collection_name}' (768d, Cosine)...")
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=768, distance=Distance.COSINE),
    )
    print("Sucesso: Memória vetorial inicializada.")

if __name__ == "__main__":
    try:
        setup()
    except Exception as e:
        print(f"Erro ao conectar ao Qdrant: {e}")
        sys.exit(1)
