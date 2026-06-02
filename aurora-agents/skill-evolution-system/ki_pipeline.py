import os
import re
import yaml
import json
from datetime import datetime
from pathlib import Path

# Paths Setup
PROJECT_ROOT = Path(r"C:\Projetos\MadLabAurora")
CANDIDATES_DIR = PROJECT_ROOT / "docs" / "Vault" / "KIs" / "candidates"
APPROVED_DIR = PROJECT_ROOT / "docs" / "Vault" / "KIs" / "approved"
MANIFEST_PATH = PROJECT_ROOT / "docs" / "Vault" / "vault_manifest.json"

def slugify(text):
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return text.strip("-")

def parse_ki(file_content):
    frontmatter_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", file_content, re.DOTALL)
    if not frontmatter_match:
        return None, file_content
    
    yaml_text = frontmatter_match.group(1)
    body = file_content[frontmatter_match.end():]
    try:
        metadata = yaml.safe_load(yaml_text) or {}
    except Exception:
        # manual fallback
        metadata = {}
        for line in yaml_text.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                metadata[k.strip()] = v.strip().strip("'\"")
    return metadata, body

def get_next_ki_id():
    max_id = 0
    if not APPROVED_DIR.exists():
        APPROVED_DIR.mkdir(parents=True, exist_ok=True)
        return "KI-MADLAB-001"
        
    for item in APPROVED_DIR.glob("KI-MADLAB-*.md"):
        match = re.match(r"KI-MADLAB-(\d+)", item.name)
        if match:
            num = int(match.group(1))
            if num > max_id:
                max_id = num
    
    next_id = max_id + 1
    return f"KI-MADLAB-{next_id:03d}"

def validate_ki(metadata, body):
    errors = []
    
    # Required metadata fields
    required_fields = ["title", "domain", "evidence_type", "applicable_to"]
    for f in required_fields:
        if f not in metadata or not metadata[f]:
            errors.append(f"Falta o campo obrigatório de metadados: '{f}'")
            
    # Required body sections
    required_sections = [
        "## O Aprendizado",
        "## Por Que Isso É Um KI",
        "## Aplicação Prática",
        "## Evidência de Origem"
    ]
    for s in required_sections:
        if s not in body:
            errors.append(f"Falta a seção obrigatória do corpo: '{s}'")
            
    return len(errors) == 0, errors

def update_manifest(approved_files):
    if not MANIFEST_PATH.exists():
        return
        
    try:
        with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
            
        for section in manifest:
            if section.get("vault_section") == "KIs":
                sub = section.setdefault("sub_sections", {})
                approved_sub = sub.setdefault("approved", {})
                approved_sub["count"] = len(approved_files)
                approved_sub["items"] = approved_files
                break
                
        with open(MANIFEST_PATH, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        print("[KI Pipeline] vault_manifest.json atualizado com sucesso.")
    except Exception as e:
        print(f"[KI Pipeline] Erro ao atualizar manifesto: {e}")

def run_ki_pipeline():
    print("--- INICIANDO PIPELINE DE KIS ---")
    if not CANDIDATES_DIR.exists():
        print(f"Diretório de candidatos {CANDIDATES_DIR} não existe.")
        return []

    promoted_kis = []
    
    # Scan all markdown candidates except README.md
    for file_path in CANDIDATES_DIR.glob("*.md"):
        if file_path.name.lower() == "readme.md":
            continue
            
        print(f"Processando candidato: {file_path.name}...")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            metadata, body = parse_ki(content)
            if not metadata:
                print(f"  [RECUSADO] {file_path.name}: Não possui frontmatter YAML válido.")
                continue
                
            valid, errors = validate_ki(metadata, body)
            if not valid:
                print(f"  [RECUSADO] {file_path.name} falhou na validação:")
                for err in errors:
                    print(f"    - {err}")
                continue
                
            # Promote candidate
            ki_id = get_next_ki_id()
            slug = slugify(metadata["title"])
            new_filename = f"{ki_id}-{slug}.md"
            new_path = APPROVED_DIR / new_filename
            
            # Update metadata
            metadata["ki_id"] = ki_id
            metadata["approved_at"] = datetime.now().strftime("%Y-%m-%d")
            metadata["approved_by"] = "antigravity-ki-pipeline"
            metadata["status"] = "approved"
            
            # Build evolved file
            new_frontmatter = "---\n"
            for k, v in metadata.items():
                if isinstance(v, list):
                    new_frontmatter += f"{k}: {json.dumps(v, ensure_ascii=False)}\n"
                else:
                    new_frontmatter += f"{k}: \"{v}\"\n"
            new_frontmatter += "---\n"
            
            # Build body title
            body_cleaned = body.strip()
            # If body has a title #, replace or prepend
            if not body_cleaned.startswith("# "):
                body_cleaned = f"# {ki_id} — {metadata['title']}\n\n" + body_cleaned
            else:
                # Replace the first title
                body_cleaned = re.sub(r"^#\s+.*?\n", f"# {ki_id} — {metadata['title']}\n", body_cleaned, count=1)
                
            with open(new_path, 'w', encoding='utf-8') as f:
                f.write(new_frontmatter + "\n" + body_cleaned + "\n")
                
            # Delete original candidate
            file_path.unlink()
            print(f"  [PROMOVIDO] {file_path.name} -> {new_filename} ({ki_id})")
            promoted_kis.append(new_filename)
            
        except Exception as e:
            print(f"  [ERRO] Falha ao processar {file_path.name}: {e}")
            
    # Update vault_manifest.json with all approved KIs currently in the directory
    all_approved = []
    if APPROVED_DIR.exists():
        # Get sorted list of all MD files except README.md
        all_approved = [f.name for f in APPROVED_DIR.glob("*.md") if f.name.lower() != "readme.md"]
        all_approved.sort()
        update_manifest(all_approved)
        
    print(f"--- PIPELINE DE KIS CONCLUÍDO: {len(promoted_kis)} KIs PROMOVIDOS ---")
    return promoted_kis

if __name__ == "__main__":
    run_ki_pipeline()
