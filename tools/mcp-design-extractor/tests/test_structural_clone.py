"""
test_structural_clone.py — Teste de Validação dos Portões ME-01, ME-02 e ME-03
(OS-20261020-CDP-STRUCTURAL-CLONE).
"""

import asyncio
import http.server
import json
import os
import socket
import sys
import threading
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
ROOT_DIR = TESTS_DIR.parent
sys.path.insert(0, str(ROOT_DIR))

from server import (
    CDPExtractorEngine,
    compile_living_design_system_html,
)

FIXTURE_PATH = TESTS_DIR / "fixtures" / "typography_fixture.html"


class FixtureHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        return str(FIXTURE_PATH)

    def log_message(self, format, *args):
        pass


def get_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


async def run_suite():
    print("=== [TEST STRUCTURAL CLONE] INICIANDO GATES ME-01, ME-02, ME-03 ===")
    os.environ["CDP_TEST_MODE"] = "1"

    port = get_free_port()
    server = http.server.HTTPServer(("127.0.0.1", port), FixtureHTTPHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    target_url = f"http://127.0.0.1:{port}/typography_fixture.html"
    out_dir = TESTS_DIR / "output" / "structural_test"
    out_dir.mkdir(parents=True, exist_ok=True)

    telemetry_file = out_dir / "design-telemetry.json"
    tokens_file = out_dir / "design-tokens.json"
    html_file = out_dir / "design-system.html"

    try:
        # 1. Executa extração da fixture
        print(f"\n[1/3] Extraindo telemetria da fixture em {target_url}...")
        engine = CDPExtractorEngine(url=target_url)
        telemetry = await engine.execute_telemetry_extraction()
        from dataclasses import asdict
        telemetry_file.write_text(json.dumps(asdict(telemetry), indent=2, ensure_ascii=False), encoding="utf-8")

        telem_data = json.loads(telemetry_file.read_text(encoding="utf-8"))

        # GATE ME-01: Verificação da classificação tipográfica
        print("\n--- Validando GATE ME-01: Classificação Tipográfica ---")
        roles = telem_data.get("typography_roles", {})
        body_role = roles.get("body", {})
        hand_role = roles.get("accent_hand", {})
        display_role = roles.get("display", {})
        mono_role = roles.get("mono", {})

        print(f" -> body_role: {body_role.get('family')}")
        print(f" -> hand_role: {hand_role.get('family')}")
        print(f" -> display_role: {display_role.get('family')}")
        print(f" -> mono_role: {mono_role.get('family')}")

        assert "plus jakarta sans" in body_role.get("family", "").lower(), f"FALHA GATE ME-01: body_role esperado 'Plus Jakarta Sans', obtido '{body_role.get('family')}'"
        assert "faracohand" not in body_role.get("family", "").lower(), "FALHA CRÍTICA ME-01: 'faracohand' contaminou o body_role!"
        assert "faracohand" in hand_role.get("family", "").lower(), f"FALHA GATE ME-01: hand_role esperado 'faracohand', obtido '{hand_role.get('family')}'"
        print(" [GATE ME-01 PASS] Tipografia classificada corretamente sem contaminação.")

        # GATE ME-02: Section Blueprints e Filtros SVG Ativos
        print("\n--- Validando GATE ME-02: Section Blueprints e Filtros SVG ---")
        blueprints = telem_data.get("section_blueprints", [])
        svg_filters = telem_data.get("active_svg_filters", [])

        print(f" -> Blueprints extraídos: {len(blueprints)}")
        print(f" -> Filtros SVG detectados: {len(svg_filters)}")

        assert len(blueprints) >= 3, f"FALHA GATE ME-02: Esperado >= 3 section_blueprints, obtido {len(blueprints)}"
        
        # Verifica se o filtro test-turb-filter tem seletores CSS vinculados
        turb_filter = next((f for f in svg_filters if f.get("id") == "test-turb-filter"), None)
        assert turb_filter is not None, "FALHA GATE ME-02: Filtro 'test-turb-filter' não capturado em active_svg_filters!"
        assert turb_filter.get("is_active") is True, "FALHA GATE ME-02: Filtro não marcado como ativo!"
        print(f" -> Regras vinculadas ao filtro: {turb_filter.get('css_rules')}")
        assert len(turb_filter.get("css_rules", [])) > 0 or len(turb_filter.get("applied_elements", [])) > 0, "FALHA GATE ME-02: Filtro sem elemento ou regra CSS associada!"
        print(" [GATE ME-02 PASS] Blueprints estruturais e regras de filtro SVG auditados com sucesso.")

        # GATE ME-03: Compilação sem Hardcode #f8fafc e com Cores/Fontes Reais
        print("\n--- Validando GATE ME-03: Compilador Living Design System ---")
        res_comp_raw = await compile_living_design_system_html(
            telemetry_path=str(telemetry_file),
            output_html_path=str(html_file),
            output_tokens_path=str(tokens_file),
        )
        compiled_html = html_file.read_text(encoding="utf-8")
        tokens_json = json.loads(tokens_file.read_text(encoding="utf-8"))

        canvas_val = tokens_json["color"]["background"]["canvas"]["$value"]
        assert canvas_val != "#f8fafc", f"FALHA CRÍTICA ME-03: #f8fafc hardcoded detectado nos tokens de fundo! ({canvas_val})"
        assert "#f8fafc" not in compiled_html, "FALHA CRÍTICA ME-03: #f8fafc hardcoded encontrado no HTML compilado!"

        # Verifica presença das fontes reais e classes de filtro geradas
        assert "--ds-font-sans" in compiled_html, "FALHA ME-03: Variável --ds-font-sans ausente no :root"
        assert "--ds-font-hand" in compiled_html, "FALHA ME-03: Variável --ds-font-hand ausente no :root"
        assert "ds-effect-test-turb-filter" in compiled_html, "FALHA ME-03: Classe CSS para o filtro SVG não foi gerada!"
        assert "filter: url(#test-turb-filter)" in compiled_html, "FALHA ME-03: filter: url(#test-turb-filter) não injetado no CSS compilado!"
        print(" [GATE ME-03 PASS] Compilador limpo de hardcode e com fidelidade estética total.")

    finally:
        server.shutdown()
        server.server_close()

    print("\n=== TODOS OS GATES ME-01, ME-02 E ME-03 FORAM APROVADOS COM SUCESSO! ===")


if __name__ == "__main__":
    try:
        asyncio.run(run_suite())
        sys.exit(0)
    except Exception as exc:
        print(f"\n[TEST FAIL] Erro no teste estrutural: {exc}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
