#!/usr/bin/env python3
"""
test_landing_reprova.py — Suíte de QA e Validação Adversarial (Sabotage-Driven)
para a Landing Page da Elysian Consult no Mad Lab Aurora.
Verifica conformidade estrita com Doutrina v9.1, Paz Cognitiva, WebMCP e vocabulário óptico.
"""

import json
import re
import sys
from pathlib import Path

LANDING_DIR = Path(__file__).resolve().parent

FORBIDDEN_WORDS = [
    r"\bchurn\b",
    r"\bltv\b",
    r"\bgmroi\b",
    r"\bdataset\b",
    r"\boutlier\b",
    r"\battach\s+rate\b"
]

MANDATORY_TERMS = [
    "Lucro Fantasma",
    "Clientes Evaporando",
    "Caixa Preso",
    "nota fiscal",
    "Diagnóstico de Choque",
    "document.modelContext"
]


def audit_html_file(html_content: str) -> None:
    # 1. Checagem de Zero-Stub
    for stub in ["// TODO", "/* TODO */", "TODO:", "Lorem ipsum", "[PLACEHOLDER]"]:
        if stub in html_content:
            raise AssertionError(f"[ZERO_STUB_VIOLATION] Stub detectado no código: '{stub}'")

    # 2. Checagem de WebMCP (Depreciação de navigator.modelContext)
    if "navigator.modelContext" in html_content:
        raise AssertionError("[WEBMCP_VIOLATION] Uso proibido da API depreciada 'navigator.modelContext'. Use 'document.modelContext'.")

    # 3. Checagem de Termos Proibidos diante do Dono da Ótica
    for pattern in FORBIDDEN_WORDS:
        match = re.search(pattern, html_content, re.IGNORECASE)
        if match:
            raise AssertionError(f"[VOCABULARY_VIOLATION] Termo proibido detectado: '{match.group(0)}'")

    # 4. Checagem de Termos Obrigatórios
    for term in MANDATORY_TERMS:
        if term not in html_content:
            raise AssertionError(f"[MANDATORY_TERM_MISSING] Termo obrigatório ausente: '{term}'")

    # 5. Checagem de atributos declarativos no form WebMCP
    toolname_match = re.search(r'toolname="([^"]+)"', html_content)
    if not toolname_match:
        raise AssertionError("[WEBMCP_VIOLATION] Atributo 'toolname' ausente no formulário.")
    toolname = toolname_match.group(1)
    if len(toolname) > 30:
        raise AssertionError(f"[WEBMCP_VIOLATION] 'toolname' excede o limite de 30 caracteres: '{toolname}' ({len(toolname)} chars)")

    tooldesc_match = re.search(r'tooldescription="([^"]+)"', html_content)
    if not tooldesc_match:
        raise AssertionError("[WEBMCP_VIOLATION] Atributo 'tooldescription' ausente no formulário.")
    tooldesc = tooldesc_match.group(1)
    if len(tooldesc) > 500:
        raise AssertionError(f"[WEBMCP_VIOLATION] 'tooldescription' excede o limite de 500 caracteres ({len(tooldesc)} chars)")

    # 5. Checagem de Grafo Semântico JSON-LD
    json_ld_match = re.search(r'<script type="application/ld\+json">(.*?)</script>', html_content, re.DOTALL)
    if not json_ld_match:
        raise AssertionError("[JSON_LD_MISSING] Bloco JSON-LD não encontrado.")
    
    try:
        json_data = json.loads(json_ld_match.group(1).strip())
        assert "@graph" in json_data, "JSON-LD deve conter chave '@graph'"
        types = [item.get("@type") for item in json_data["@graph"]]
        assert "Organization" in types, "JSON-LD deve conter 'Organization'"
        assert "ProfessionalService" in types, "JSON-LD deve conter 'ProfessionalService'"
        assert "FAQPage" in types, "JSON-LD deve conter 'FAQPage'"
    except Exception as e:
        raise AssertionError(f"[JSON_LD_INVALID] Erro na validação sintática do JSON-LD: {e}")

    # 6. Paz Cognitiva & Acessibilidade
    if "prefers-reduced-motion" not in html_content:
        raise AssertionError("[ACCESSIBILITY_VIOLATION] Suporte a 'prefers-reduced-motion' ausente no CSS.")


def run_baseline_and_reprova():
    html_path = LANDING_DIR / "index.html"
    assert html_path.exists(), f"Arquivo não encontrado: {html_path}"
    raw_content = html_path.read_text(encoding="utf-8")

    print("=== [QA-REVIEW] INICIANDO AUDITORIA DA LANDING PAGE ELYSIAN ===")
    
    # 1. Baseline Test (deve passar com EXIT 0)
    print("\n[TEST 1] Verificando baseline da landing page de produção...")
    audit_html_file(raw_content)
    print(" -> Baseline PASS: Zero-stub, vocabulário limpo, WebMCP e JSON-LD 100% em conformidade.")

    # 2. Verificação de Arquivos da Arquitetura Dual-Surface
    print("\n[TEST 2] Verificando artefatos Dual-Surface e endpoints de descoberta...")
    assert (LANDING_DIR / "index.md").exists(), "index.md ausente"
    assert (LANDING_DIR / "llms.txt").exists(), "llms.txt ausente"
    assert (LANDING_DIR / ".well-known" / "agent-card.json").exists(), "agent-card.json ausente"
    assert (LANDING_DIR / "robots.txt").exists(), "robots.txt ausente"
    print(" -> Dual-Surface PASS: index.md, llms.txt, agent-card.json e robots.txt confirmados.")

    # 3. Suíte de Sabotagem (Reprova - cenários forçados)
    print("\n[SUÍTE REPROVA] Testando 4 cenários adversariais (esperado EXIT=1 induzido)...")

    # Cenário S1: Injeção de termo proibido (churn)
    print(" -> [S1] Injetando jargão proibido 'churn'...")
    try:
        audit_html_file(raw_content + " <p>Nossa taxa de churn é zero.</p>")
        raise RuntimeError("FALHA: O validador deveria ter barrado o termo proibido 'churn'.")
    except AssertionError as e:
        assert "[VOCABULARY_VIOLATION]" in str(e)
        print("    -> Interceptado com sucesso.")

    # Cenário S2: Uso de API depreciada navigator.modelContext
    print(" -> [S2] Injetando 'navigator.modelContext' depreciado...")
    try:
        audit_html_file(raw_content.replace("document.modelContext", "navigator.modelContext"))
        raise RuntimeError("FALHA: O validador deveria ter barrado 'navigator.modelContext'.")
    except AssertionError as e:
        assert "[WEBMCP_VIOLATION]" in str(e)
        print("    -> Interceptado com sucesso.")

    # Cenário S3: Quebra de JSON-LD
    print(" -> [S3] Injetando JSON-LD corrompido...")
    try:
        bad_json = raw_content.replace('"@graph":', '"@graph_invalido":')
        audit_html_file(bad_json)
        raise RuntimeError("FALHA: O validador deveria ter barrado JSON-LD corrompido.")
    except AssertionError as e:
        assert "[JSON_LD_INVALID]" in str(e)
        print("    -> Interceptado com sucesso.")

    # Cenário S4: Toolname acima do limite de 30 caracteres
    print(" -> [S4] Injetando toolname com mais de 30 caracteres...")
    try:
        bad_tool = raw_content.replace('toolname="simulate_optical_leak"', 'toolname="simulate_optical_leakage_very_long_invalid_name"')
        audit_html_file(bad_tool)
        raise RuntimeError("FALHA: O validador deveria ter barrado toolname com >30 caracteres.")
    except AssertionError as e:
        assert "[WEBMCP_VIOLATION]" in str(e)
        print("    -> Interceptado com sucesso.")

    print("\n=== [QA-REVIEW PASS] TODOS OS TESTES E SABOTAGENS FORAM CONCLUÍDOS COM SUCESSO. ===")


if __name__ == "__main__":
    run_baseline_and_reprova()
