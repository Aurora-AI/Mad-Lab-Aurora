import os
import re
import json
from pathlib import Path

try:
    from src.analyzer import analyze
except ImportError:
    from analyzer import analyze

# Resolve root path of MadLabAurora
ROOT_PATH = Path(r"C:\Projetos\MadLabAurora")

def load_rubric(name):
    rubric_path = Path(__file__).parent.parent / "rubrics" / f"rubric-{name}.json"
    try:
        with open(rubric_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading rubric {name}: {e}")
        return None

def evaluate_trigger_clarity(analysis, content):
    rubric = load_rubric("trigger-clarity")
    score = 0
    details = []

    # Criterion 1: Presence in frontmatter or dedicated section
    has_trigger_meta = "trigger" in analysis.get("frontmatter", {}) or "gatilho" in analysis.get("frontmatter", {})
    has_trigger_heading = any(re.search(r"gatilho|trigger", h, re.IGNORECASE) for h in analysis.get("headings", []))
    if has_trigger_meta or has_trigger_heading:
        score += 5
        details.append("Gatilho presente no frontmatter ou seção dedicada (+5)")
    else:
        details.append("Ausência de gatilho formal (0)")

    # Criterion 2: Explicit keywords or conditions defined
    triggers = analysis.get("triggers", [])
    if len(triggers) > 0 and any(len(t.strip()) > 3 for t in triggers):
        score += 5
        details.append("Gatilhos especificam condições ou palavras-chave claras (+5)")
    else:
        details.append("Gatilhos não parecem conter palavras-chave específicas (0)")

    # Criterion 3: Avoid vague phrases
    vague_phrases = ["quando achar apropriado", "se achar necessário", "caso queira", "se julgar", "quando necessário"]
    has_vague = any(p in content.lower() for p in vague_phrases)
    if not has_vague:
        score += 5
        details.append("Nenhuma linguagem vaga detectada nos gatilhos (+5)")
    else:
        details.append("Linguagem vaga/ambígua detectada nos gatilhos (0)")

    # Criterion 4: Scenario or specific phrase example
    has_example = bool(re.search(r"exemplo|cenário|frase|quando o usuário disser", content, re.IGNORECASE))
    if has_example:
        score += 5
        details.append("Presença de exemplos práticos de acionamento (+5)")
    else:
        details.append("Ausência de exemplos práticos de acionamento (0)")

    return score, details

def evaluate_output_structure(analysis, content):
    score = 0
    details = []

    # Criterion 1: Output section
    has_output_heading = any(re.search(r"saída|output|formato", h, re.IGNORECASE) for h in analysis.get("headings", []))
    if has_output_heading:
        score += 5
        details.append("Seção explícita de output/saída documentada (+5)")
    else:
        details.append("Ausência de seção de output/saída (0)")

    # Criterion 2: Format specification (JSON, Markdown, YAML)
    has_format = bool(re.search(r"format:\s*(?:json|yaml|markdown|md|xml)|formato:\s*(?:json|yaml|markdown|md|xml)", content, re.IGNORECASE)) or \
                 bool(re.search(r"em format[o|a]\s*(?:json|yaml|markdown|md|xml)", content, re.IGNORECASE))
    if has_format:
        score += 5
        details.append("Especificação de formato de arquivo (JSON/YAML/Markdown) encontrada (+5)")
    else:
        details.append("Formato do output não explicitado (0)")

    # Criterion 3: Templates or example blocks
    if analysis.get("has_templates", False):
        score += 5
        details.append("Presença de template ou bloco de exemplo de saída (+5)")
    else:
        details.append("Ausência de bloco de exemplo ou template de saída (0)")

    # Criterion 4: anti-placeholder instructions
    anti_placeholder = ["não omitir", "não use placeholder", "sem placeholder", "complete output", "completamente preenchido", "não truncar"]
    has_anti_placeholder = any(p in content.lower() for p in anti_placeholder)
    if has_anti_placeholder:
        score += 5
        details.append("Instruções explícitas de não usar placeholders (+5)")
    else:
        details.append("Falta de instruções contra placeholders no output (0)")

    return score, details

def evaluate_anti_hallucination(analysis, content):
    score = 0
    details = []

    # Criterion 1: Prohibit assuming contracts/tools without existence
    prohibit_words = ["não assuma", "proibido", "terminantemente proibido", "não invente"]
    has_prohibit = any(w in content.lower() for w in prohibit_words)
    if has_prohibit:
        score += 5
        details.append("Presença de restrições de proibição explícitas (+5)")
    else:
        details.append("Falta de termos proibitivos assertivos (0)")

    # Criterion 2: Mandatory physical scans
    scan_words = ["varredura física", "verifique a existência", "descoberta física", "rastreável"]
    has_scan = any(w in content.lower() for w in scan_words)
    if has_scan:
        score += 5
        details.append("Instrução de varredura física ativa de contratos (+5)")
    else:
        details.append("Falta de instrução de varredura física de contratos (0)")

    # Criterion 3: Fail explicitly if unavailable
    fail_words = ["registrar falha", "falha explícita", "avise", "notifique a indisponibilidade"]
    has_fail = any(w in content.lower() for w in fail_words)
    if has_fail:
        score += 5
        details.append("Tratamento de indisponibilidade de ferramentas/contratos (+5)")
    else:
        details.append("Falta de regras de erro ou indisponibilidade explícita (0)")

    # Criterion 4: Negative constraints
    negative_constraints = ["invariante", "inegociável", "regra absoluta", "restrições negativas"]
    has_neg = any(w in content.lower() for w in negative_constraints)
    if has_neg:
        score += 5
        details.append("Especificação de invariantes/regras absolutas (+5)")
    else:
        details.append("Falta de regras absolutas declaradas (0)")

    return score, details

def evaluate_mode_coverage(analysis, content):
    score = 0
    details = []

    # Criterion 1: Mode section
    has_mode_section = any(re.search(r"modo|mode", h, re.IGNORECASE) for h in analysis.get("headings", []))
    if has_mode_section:
        score += 5
        details.append("Seção dedicada a modos de operação encontrada (+5)")
    else:
        details.append("Ausência de seção de modos de operação (0)")

    # Criterion 2: At least 2 modes defined
    modes_found = len(re.findall(r"modo\s+\d+|mode\s+\d+|express|completo|full|diagnóstico", content, re.IGNORECASE))
    if modes_found >= 2:
        score += 5
        details.append(f"Múltiplos modos de operação detectados ({modes_found} encontrados) (+5)")
    else:
        details.append("Apenas um ou nenhum modo de operação claro (0)")

    # Criterion 3: Clear description of when to use each
    has_use_description = bool(re.search(r"quando utilizar|quando usar|acionado quando|indicado para", content, re.IGNORECASE))
    if has_use_description:
        score += 5
        details.append("Critérios de seleção de modo descritos (+5)")
    else:
        details.append("Sem descrição de quando selecionar cada modo (0)")

    # Criterion 4: Variation in output volume/structure
    has_variation = bool(re.search(r"diferença no output|saída específica|formato de saída para o modo", content, re.IGNORECASE)) or \
                    (has_mode_section and modes_found >= 2 and len(content) > 1500)
    if has_variation:
        score += 5
        details.append("Variação de output/estrutura entre os modos suportada (+5)")
    else:
        details.append("Ausência de variação clara de comportamento/output (0)")

    return score, details

def evaluate_reference_integrity(analysis, content):
    score = 0
    details = []
    
    # Criterion 1: Dedicated reference section
    has_ref_heading = any(re.search(r"referência|reference", h, re.IGNORECASE) for h in analysis.get("headings", []))
    if has_ref_heading:
        score += 5
        details.append("Seção dedicada a referências/suporte encontrada (+5)")
    else:
        details.append("Ausência de seção de referências (0)")

    # Criterion 2: Correct file:// or relative paths syntax
    references = analysis.get("references", [])
    has_proper_syntax = len(references) > 0 and any(("/" in r or "\\" in r) for r in references)
    if has_proper_syntax:
        score += 5
        details.append("Sintaxe adequada de caminhos de arquivos (+5)")
    else:
        details.append("Sintaxe de caminhos ausente ou inválida (0)")

    if not references:
        details.append("Nenhuma referência para validar fisicamente (0/10)")
        return score, details

    # Validate physical existence on disk
    skill_name = analysis.get("name", "")
    skill_dir = ROOT_PATH / ".aurora" / "skills" / skill_name

    broken_count = 0
    for ref in references:
        # Check absolute or relative paths
        path_variants = [
            ROOT_PATH / ref,
            skill_dir / ref,
            ROOT_PATH / ".aurora" / "skills" / ref,
            Path(ref)
        ]
        
        exists = False
        for var in path_variants:
            if var.exists():
                exists = True
                break
                
        if not exists:
            broken_count += 1
            print(f"[SES Scorer] Broken reference found in skill {skill_name}: {ref}")

    broken_pct = (broken_count / len(references)) * 100 if references else 0
    
    # Criterion 3: Less than 15% broken references
    if broken_pct < 15:
        score += 5
        details.append(f"Alta integridade física de referências ({broken_count} quebradas de {len(references)}) (+5)")
    else:
        details.append(f"Muitas referências quebradas ({broken_count} de {len(references)} | {broken_pct:.1f}%) (0)")

    # Criterion 4: Zero broken references (Perfect 100% integrity)
    if broken_count == 0:
        score += 5
        details.append("Excelente: 100% das referências existem fisicamente no filesystem! (+5)")
    else:
        details.append(f"Falta de integridade perfeita (existem {broken_count} referências ausentes) (0)")

    return score, details

def score(skill_content):
    """
    Evaluates the skill content semantic quality against the 5 structural rubrics.
    """
    analysis = analyze(skill_content)
    
    # Calculate rubric scores
    trigger_score, trigger_details = evaluate_trigger_clarity(analysis, skill_content)
    output_score, output_details = evaluate_output_structure(analysis, skill_content)
    anti_halluc_score, anti_halluc_details = evaluate_anti_hallucination(analysis, skill_content)
    mode_score, mode_details = evaluate_mode_coverage(analysis, skill_content)
    ref_score, ref_details = evaluate_reference_integrity(analysis, skill_content)

    total_score = trigger_score + output_score + anti_halluc_score + mode_score + ref_score

    # Construct result payload matching schema and live evaluation needs
    return {
        "score": total_score,
        "rubrics": {
            "trigger-clarity": {
                "score": trigger_score,
                "max": 20,
                "details": trigger_details
            },
            "output-structure": {
                "score": output_score,
                "max": 20,
                "details": output_details
            },
            "anti-hallucination": {
                "score": anti_halluc_score,
                "max": 20,
                "details": anti_halluc_details
            },
            "mode-coverage": {
                "score": mode_score,
                "max": 20,
                "details": mode_details
            },
            "reference-integrity": {
                "score": ref_score,
                "max": 20,
                "details": ref_details
            }
        }
    }
