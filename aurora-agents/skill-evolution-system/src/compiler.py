import re
import yaml

def compile_skill(skill_content, patterns):
    """
    Evolves a skill's markdown representation by resolving metadata deficiencies 
    and missing sections identified by extracted patterns.
    """
    if not skill_content:
        return skill_content

    # 1. Parse frontmatter and find matches
    frontmatter_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", skill_content, re.DOTALL)
    
    metadata = {}
    body_content = skill_content
    
    if frontmatter_match:
        yaml_text = frontmatter_match.group(1)
        body_content = skill_content[frontmatter_match.end():]
        try:
            metadata = yaml.safe_load(yaml_text) or {}
        except Exception:
            # Simple fallback regex parser
            for line in yaml_text.splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    metadata[k.strip()] = v.strip().strip("'\"")

    # 2. Inject missing frontmatter fields
    injected_keys = []
    for key in patterns.get("required_frontmatter_keys", []):
        if key not in metadata:
            if key == "version":
                metadata["version"] = "1.0.0-evolved"
            elif key == "domain":
                metadata["domain"] = "general"
            elif key == "classification":
                metadata["classification"] = "local-agents"
            elif key == "status":
                metadata["status"] = "draft"
            elif key == "description":
                metadata["description"] = "Evolved local agent skill."
            else:
                metadata[key] = "auto-generated"
            injected_keys.append(key)

    # Reconstruct frontmatter block
    new_yaml = "---\n"
    for k, v in metadata.items():
        if isinstance(v, list):
            new_yaml += f"{k}: {v}\n"
        elif isinstance(v, str) and "\n" in v:
            # block string
            new_yaml += f"{k}: |\n"
            for line in v.splitlines():
                new_yaml += f"  {line}\n"
        else:
            new_yaml += f"{k}: {v}\n"
    new_yaml += "---\n"

    # 3. Check and inject missing headings
    new_sections = []
    
    # Check "Modos de Operação"
    has_modes = any(re.search(r"modo|mode", h, re.IGNORECASE) for h in re.findall(r"^#+\s+(.+)$", body_content, re.MULTILINE))
    if not has_modes:
        new_sections.append("""
## Modos de Operação

Esta skill opera nos seguintes modos de acordo com o contexto da tarefa:

### Modo 1 — Execução Expressa
*   Indicado para tarefas simples e diretas.
*   **Comportamento:** O output é condensado e imediato, focando na resposta rápida.

### Modo 2 — Auditoria Completa
*   Indicado para revisões amplas, designs complexos ou diagnósticos de código.
*   **Comportamento:** Processamento detalhado, checklist passo a passo e templates de conformidade explícitos.
""")

    # Check "Referências" section
    has_refs = any(re.search(r"referência|reference", h, re.IGNORECASE) for h in re.findall(r"^#+\s+(.+)$", body_content, re.MULTILINE))
    if not has_refs:
        new_sections.append("""
## Referências

*   [MANUAL_DA_AGENCIA.md](file:///C:/Projetos/MadLabAurora/docs/Vault/Raw/MANUAL_DA_AGENCIA.md)
*   [designmanualposthero.md](file:///C:/Projetos/MadLabAurora/.agents/rules/designmanualposthero.md)
""")

    # Check anti-hallucination / physical scan constraints in text
    has_anti_halluc = "varredura física" in body_content.lower() or "não assuma" in body_content.lower()
    if not has_anti_halluc:
        new_sections.append("""
## Regras Invariantes (Anti-Alucinação)

> [!IMPORTANT]
> - **DESCOBERTA FÍSICA DE CONTRATOS:** Fica terminantemente proibido assumir utilitários, scripts ou contratos por mera dedução lógica. O agente deve realizar uma varredura física ativa para verificar caminhos e ferramentas no filesystem.
> - **NÃO utilizar placeholders** ou trechos de código truncados no output.
""")

    # Append new sections to the body
    body_evolved = body_content
    for section in new_sections:
        body_evolved = body_evolved.rstrip() + "\n\n" + section.strip() + "\n"

    return new_yaml + body_evolved
