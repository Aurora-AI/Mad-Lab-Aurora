import os
import sys
import google.generativeai as genai
from pathlib import Path

def find_project_root(current_path: Path, target_file: str = "aurora_vault.py") -> Path:
    """Recursively searches for the project root containing the target file."""
    for parent in current_path.parents:
        if (parent / target_file).exists():
            return parent
    return current_path # Fallback

# Add project root to sys.path
PROJECT_ROOT = find_project_root(Path(__file__).resolve())
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

import aurora_vault

def get_gemini_embedding(text: str, model="models/gemini-embedding-2"):
    # Garante que a API Key esteja disponível
    # A senha deve estar no ambiente: AURORA_VAULT_PASSWORD
    api_key = aurora_vault.get_secret("AURORA_GEMINI_API_KEY")
    if not api_key:
        api_key = aurora_vault.get_secret("GEMINI_ELYSIAN_LEX")
        
    if not api_key:
        print("[!] ERROR: No Gemini API Key found in Vault.")
        raise ValueError("AURORA_GEMINI_API_KEY not found in Vault.")
    
    print(f"[*] Using API Key: {api_key[:8]}...{api_key[-4:]}")
    genai.configure(api_key=api_key)
    
    result = genai.embed_content(
        model=model,
        content=text,
        task_type="retrieval_document",
        title="Reflexion KI Ingestion"
    )
    
    return result['embedding']

if __name__ == "__main__":
    # Teste rápido - Requer AURORA_VAULT_PASSWORD no ambiente
    try:
        if "AURORA_VAULT_PASSWORD" not in os.environ:
            print("[!] WARNING: AURORA_VAULT_PASSWORD not found in environment.")
            print("[*] Accessing Vault requires the Commander to set this variable.")
        
        vec = get_gemini_embedding("Aurora System Test")
        print(f"Sucesso: Vector size {len(vec)}")
    except Exception as e:
        print(f"Erro esperado se sem senha: {e}")
