import google.generativeai as genai
import sys

def test_key(api_key):
    try:
        genai.configure(api_key=api_key)
        model = "models/text-embedding-004"
        result = genai.embed_content(
            model=model,
            content="Teste de integridade Aurora OS-07",
            task_type="retrieval_document"
        )
        print("Sucesso! A chave é uma GOOGLE_API_KEY funcional.")
        print(f"Dimensões do embedding: {len(result['embedding'])}")
        return True
    except Exception as e:
        print(f"Falha ao usar como Google API Key: {e}")
        return False

if __name__ == "__main__":
    test_key("S6MXFOtQZbpvje5cwGyU0EC3AxnLY82u")
