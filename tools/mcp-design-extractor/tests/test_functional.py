"""
test_functional.py — Teste Funcional Ponta a Ponta contra Fixture Controlada.
Valida extração de tokens em :root, @keyframes, curvas cubic-bezier,
deltas forçados de :hover via CDP, interceptação de Shaders WebGL e compilação HTML.
"""

import asyncio
import http.server
import json
import os
import socket
import sys
import threading
from pathlib import Path

# Habilita o modo de teste interno estritamente para este processo
os.environ["CDP_TEST_MODE"] = "1"

TESTS_DIR = Path(__file__).resolve().parent
ROOT_DIR = TESTS_DIR.parent
FIXTURE_PATH = TESTS_DIR / "fixtures" / "sample_page.html"

sys.path.insert(0, str(ROOT_DIR))
from server import (
    extract_cdp_design_telemetry,
    capture_webgl_and_component_states,
    compile_living_design_system_html,
)


class FixtureHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        return str(FIXTURE_PATH)

    def log_message(self, format, *args):
        pass  # Silencia logs de requisição no terminal de teste


def get_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


async def run_functional_suite():
    port = get_free_port()
    server = http.server.HTTPServer(("127.0.0.1", port), FixtureHTTPHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    target_url = f"http://127.0.0.1:{port}/sample_page.html"
    out_dir = TESTS_DIR / "output"
    out_dir.mkdir(parents=True, exist_ok=True)

    telemetry_path = str(out_dir / "design-telemetry.json")
    visual_manifest_dir = str(out_dir / "visual-captures")
    visual_manifest_path = str(out_dir / "visual-captures" / "visual-shader-manifest.json")
    html_output_path = str(out_dir / "design-system.html")
    tokens_output_path = str(out_dir / "design-tokens.json")

    try:
        # 1. Executa extração de telemetria CDP
        print(f"[TEST 1/3] Executando extract_cdp_design_telemetry em {target_url}...")
        res_raw1 = await extract_cdp_design_telemetry(url=target_url, output_path=telemetry_path)
        res1 = json.loads(res_raw1)
        assert res1["status"] == "success", "Falha na extração de telemetria"
        assert res1["capture_id"].startswith("cap_"), "Capture ID malformado"

        telemetry_data = json.loads(Path(telemetry_path).read_text(encoding="utf-8"))
        vars_map = telemetry_data["css_custom_properties"]
        assert "--fixture-bg" in vars_map, "Variável --fixture-bg não extraída"
        assert "--fixture-accent" in vars_map, "Variável --fixture-accent não extraída"

        keyframes = [k["name"] for k in telemetry_data["keyframes"]]
        assert "fixturePulse" in keyframes, f"Keyframe fixturePulse não extraído: {keyframes}"

        easings = telemetry_data["easing_curves"]
        assert any("0.16" in e for e in easings), f"Curva cubic-bezier não encontrada em: {easings}"
        print(f" -> Telemetria OK: {len(vars_map)} vars, {len(keyframes)} keyframes, {len(easings)} easings.")

        # 2. Executa captura de shaders WebGL e pares 2x DPI
        print(f"[TEST 2/3] Executando capture_webgl_and_component_states...")
        res_raw2 = await capture_webgl_and_component_states(
            url=target_url, output_dir=visual_manifest_dir, max_components=4
        )
        res2 = json.loads(res_raw2)
        assert res2["status"] == "success", "Falha na captura de shaders/visuais"
        assert res2["webgl_supported"] is True, "WebGL não foi detectado"
        assert res2["webgl_shaders_captured"] >= 2, f"Esperado >= 2 shaders, obtido {res2['webgl_shaders_captured']}"

        manifest_data = json.loads(Path(visual_manifest_path).read_text(encoding="utf-8"))
        assert len(manifest_data["component_visual_pairs"]) > 0, "Nenhum par visual 2x DPI capturado"
        print(f" -> Shaders e Visuais OK: {len(manifest_data['webgl_shaders'])} shaders GLSL capturados.")

        # 3. Compila o Living Design System em HTML e tokens
        print(f"[TEST 3/3] Compilando design-system.html e design-tokens.json...")
        res_raw3 = await compile_living_design_system_html(
            telemetry_path=telemetry_path,
            visual_manifest_path=visual_manifest_path,
            output_html_path=html_output_path,
            output_tokens_path=tokens_output_path,
            export_raw_fidelity=True,
        )
        res3 = json.loads(res_raw3)
        assert res3["status"] == "compiled", "Falha na compilação do design system"

        tokens_json = json.loads(Path(tokens_output_path).read_text(encoding="utf-8"))
        assert tokens_json["schema_version"] == "w3c.design-tokens.v1", "Schema tokens incorreto"
        assert "color" in tokens_json and "typography" in tokens_json, "Contrato tokens incompleto"

        html_text = Path(html_output_path).read_text(encoding="utf-8")
        assert "AURORA LIVING DESIGN SYSTEM" in html_text, "Header do Living Design System ausente"
        assert "toolname=\"simulate_roi\"" in html_text, "Formulário WebMCP ausente no HTML"
        assert "<script src=" not in html_text, "Script externo indevidamente injetado no HTML"
        print(" -> Compilação OK: HTML e tokens JSON gerados em estrita conformidade.")

        print("\n[PASS] TODOS OS TESTES FUNCIONAIS FORAM CONCLUÍDOS COM SUCESSO ABSOLUTO.")

    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    try:
        asyncio.run(run_functional_suite())
        sys.exit(0)
    except Exception as exc:
        print(f"\n[FAIL] Erro nos testes funcionais: {exc}", file=sys.stderr)
        sys.exit(1)
