import os
import re
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http import models

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load .env
ENV_PATH = Path("C:/Projetos/Aurora/ElysianLex/.env")
load_dotenv(ENV_PATH)

# Configs
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = "reflexion_ki"
VAULT_REFLEXION_PATH = Path("C:/Projetos/Aurora/Ozzmosis/docs/Vault/Reflexion/KIs")
ANTI_PATTERNS_FILE = Path("C:/Projetos/Aurora/Ozzmosis/docs/Vault/Reflexion/anti-patterns.md")

# Default Embedding Size for reflexion_ki
VECTOR_SIZE = 768

def get_embedding(text: str, model_name="all-mpnet-base-v2"):
    """
    Get embedding for text.
    """
    from sentence_transformers import SentenceTransformer
    if not hasattr(get_embedding, "_model"):
        logger.info(f"Loading embedding model: {model_name}")
        get_embedding._model = SentenceTransformer(model_name)
    
    return get_embedding._model.encode(text).tolist()

def parse_anti_patterns():
    """
    Parses anti-patterns.md to extract metadata and link to KI files.
    """
    if not ANTI_PATTERNS_FILE.exists():
        logger.error(f"Anti-patterns file not found: {ANTI_PATTERNS_FILE}")
        return []

    content = ANTI_PATTERNS_FILE.read_text(encoding="utf-8")
    sections = re.split(r'---', content)
    
    patterns = []
    for section in sections:
        match = re.search(r'## \[(?P<id>.*?)\] (?P<title>.*?)\n', section)
        if match:
            p_id = match.group('id')
            title = match.group('title')
            
            prev_match = re.search(r'\*\*Prevenção:\*\* (?P<prev>.*?)\n', section)
            prevention = prev_match.group('prev') if prev_match else ""
            
            ki_match = re.search(r'\*\*KI:\*\* `(?P<ki_path>.*?)`', section)
            ki_path = ki_match.group('ki_path') if ki_match else ""
            
            patterns.append({
                "id": p_id,
                "title": title,
                "prevention": prevention,
                "ki_path": ki_path
            })
            
    return patterns

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--single", help="Path to a single AntiPatternCandidate JSON file")
    parser.add_argument("--all", action="store_true", help="Ingest all patterns from Vault")
    args = parser.parse_args()

    logger.info("Starting OS-07 Memory Migration...")
    
    client = QdrantClient(url=QDRANT_URL)
    
    # Ensure collection
    collections = client.get_collections().collections
    if not any(c.name == COLLECTION_NAME for c in collections):
        logger.info(f"Creating collection {COLLECTION_NAME}...")
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(size=VECTOR_SIZE, distance=models.Distance.COSINE),
        )

    if args.single:
        ap_path = Path(args.single)
        if not ap_path.exists():
            logger.error(f"File not found: {ap_path}")
            return
        
        with open(ap_path, "r", encoding="utf-8") as f:
            ap_data = json.load(f)
        
        logger.info(f"Ingesting single pattern candidate: {ap_data.get('pattern_id')}")
        text_to_embed = f"Pattern: {ap_data.get('pattern_id')}\nSymptom: {ap_data.get('symptom')}\nFix: {ap_data.get('fix_applied')}"
        vector = get_embedding(text_to_embed)
        
        point = models.PointStruct(
            id=hash(ap_data.get('pattern_id', str(datetime.now()))) % (2**63),
            vector=vector,
            payload={
                **ap_data, 
                "type": "anti_pattern_candidate", 
                "ingested_at": datetime.now().isoformat()
            }
        )
        client.upsert(collection_name=COLLECTION_NAME, points=[point])
        logger.info(f"Successfully ingested candidate: {ap_data.get('pattern_id')}")

    else:
        patterns = parse_anti_patterns()
        logger.info(f"Extracted {len(patterns)} patterns from catalogue.")

        points = []
        for p in patterns:
            try:
                logger.info(f"Processing pattern {p['id']} - {p['title']}")
                text_to_embed = f"Pattern: {p['title']}\nPrevention: {p['prevention']}"
                
                if p['ki_path']:
                    full_ki_path = Path("C:/Projetos/Aurora/Ozzmosis") / p['ki_path']
                    if full_ki_path.exists():
                        ki_content = full_ki_path.read_text(encoding="utf-8")
                        desc_match = re.search(r'## Descrição\n(.*?)\n##', ki_content, re.DOTALL)
                        if desc_match:
                            text_to_embed += f"\nDescription: {desc_match.group(1).strip()}"
                
                vector = get_embedding(text_to_embed)
                
                points.append(models.PointStruct(
                    id=hash(p['id']) % (2**63),
                    vector=vector,
                    payload={
                        **p,
                        "type": "anti_pattern",
                        "ingested_at": datetime.now().isoformat()
                    }
                ))
            except Exception as e:
                logger.error(f"Error processing {p['id']}: {e}")

        if points:
            client.upsert(collection_name=COLLECTION_NAME, points=points)
            logger.info(f"Successfully ingested {len(points)} patterns into {COLLECTION_NAME}.")
        else:
            logger.warning("No patterns found to ingest.")

if __name__ == "__main__":
    main()
