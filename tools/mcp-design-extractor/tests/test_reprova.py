"""
test_reprova.py — Suíte de Sabotagem Adversarial e Degradação Graciosa.
Valida rigorosamente:
1. 4 Cenários Negativos (Ataques e anomalias que DEVEM levantar exceções estritas);
2. 2 Cenários de Degradação Graciosa (Capacidades opcionais ausentes que NÃO devem falhar).
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

from security import (
    InvalidSchemeError,
    SSRFSecurityError,
    validate_url,
)
from server import (
    capture_webgl_and_component_states,
    compile_living_design_system_html,
)


class SimplePageHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        html = "<html><body><h1>Página Simples sem WebGL</h1><p>Apenas texto.</p></body></html>"
        self.wfile.write(html.encode("utf-8"))

    def log_message(self, format, *args):
        pass


def get_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


async def run_adversarial_suite():
    print("=== [REPROVA] INICIANDO SUÍTE ADVERSARIAL ===")

    # --------------------------------------------------------------------------
    # CENÁRIOS NEGATIVOS (Devem levantar exceções estritas de segurança)
    # --------------------------------------------------------------------------

    # S1: Tentativa de SSRF em IP privado sem modo de teste
    print("\n[NEGATIVO S1] Testando bloqueio de IP privado RFC 1918 (http://192.168.1.1)...")
    old_mode = os.environ.pop("CDP_TEST_MODE", None)
    try:
        validate_url("http://192.168.1.1/admin")
        raise AssertionError("FALHA: SSRF para 192.168.1.1 não foi bloqueado!")
    except SSRFSecurityError as e:
        print(f" -> Interceptado com sucesso: {e}")

    print("[NEGATIVO S1b] Testando bloqueio de loopback (http://127.0.0.1) em produção...")
    try:
        validate_url("http://127.0.0.1:8080/secret")
        raise AssertionError("FALHA: Loopback 127.0.0.1 não foi bloqueado sem flag de teste!")
    except SSRFSecurityError as e:
        print(f" -> Interceptado com sucesso: {e}")

    # S2: Esquemas proibidos (file://, javascript:)
    print("\n[NEGATIVO S2] Testando rejeição de esquemas proibidos...")
    for mal_url in ["file:///etc/passwd", "javascript:alert(1)", "data:text/html,<h1>XSS</h1>"]:
        try:
            validate_url(mal_url)
            raise AssertionError(f"FALHA: Esquema malicioso '{mal_url}' não foi rejeitado!")
        except InvalidSchemeError as e:
            print(f" -> Interceptado com sucesso ({mal_url}): {e}")

    # S3: Domínio inexistente / falha de resolução DNS
    print("\n[NEGATIVO S3] Testando falha de DNS para domínio fantasma...")
    try:
        validate_url("http://non-existent-subdomain-129384712039.com")
        raise AssertionError("FALHA: Domínio inexistente não levantou erro de DNS!")
    except SSRFSecurityError as e:
        print(f" -> Interceptado com sucesso: {e}")

    # S4: Arquivo de telemetria inexistente na compilação
    print("\n[NEGATIVO S4] Testando compilação com arquivo de telemetria ausente...")
    try:
        await compile_living_design_system_html(telemetry_path="caminho_inexistente_123.json")
        raise AssertionError("FALHA: Compilador não levantou FileNotFoundError para arquivo ausente!")
    except FileNotFoundError as e:
        print(f" -> Interceptado com sucesso: {e}")

    # S5: Sanitização de variáveis CSS contra quebra de tag </style> e injeção XSS
    print("\n[NEGATIVO S5] Testando sanitização de injeção em variáveis CSS e payload adulterado...")
    crafted_payload = {
        "schema_version": "cdp.telemetry.v1",
        "capture_id": "cap_crafted_999",
        "source_url": "https://attacker.com/<script>alert(1)</script>",
        "typography_scale": [
            {"fontFamily": "'Comic Sans', sans-serif; } </style><script>alert('font_xss')</script><style>"}
        ],
        "surfaces_and_shadows": [
            {
                "boxShadow": "none; } </style><script>alert('shadow_xss')</script><style>",
                "backdropFilter": "none; } </style><script>alert('filter_xss')</script><style>",
            }
        ],
        "easing_curves": ["ease; } </style><script>alert('ease_xss')</script><style>"],
        "color_palette": {},
    }
    scratch_reprova = TESTS_DIR / "output" / "reprova_s5"
    scratch_reprova.mkdir(parents=True, exist_ok=True)
    crafted_json = scratch_reprova / "crafted_telemetry.json"
    crafted_html = scratch_reprova / "crafted_living.html"
    crafted_tokens = scratch_reprova / "crafted_tokens.json"

    crafted_json.write_text(json.dumps(crafted_payload), encoding="utf-8")
    await compile_living_design_system_html(
        telemetry_path=str(crafted_json),
        output_html_path=str(crafted_html),
        output_tokens_path=str(crafted_tokens),
    )

    generated_html = crafted_html.read_text(encoding="utf-8")
    assert "<script>alert(1)</script>" not in generated_html, "FALHA: Script tag não sanitizada no body/title!"
    assert "</style><script>" not in generated_html, "FALHA: Quebra de </style> permitiu injeção de script!"
    assert "alert('font_xss')" not in generated_html, "FALHA: Payload font_xss vazou para o HTML!"
    assert "alert('shadow_xss')" not in generated_html, "FALHA: Payload shadow_xss vazou para o HTML!"
    assert "alert('ease_xss')" not in generated_html, "FALHA: Payload ease_xss vazou para o HTML!"
    print(" -> Sanitização de CSS e source_url OK: Zero quebras de contexto ou vazamento de tags script.")

    # --------------------------------------------------------------------------
    # CENÁRIOS DE DEGRADAÇÃO GRACIOSA (Devem suceder sem erro)
    # --------------------------------------------------------------------------

    # Restaura modo de teste para executar a fixture local sem WebGL
    os.environ["CDP_TEST_MODE"] = "1"
    port = get_free_port()
    server = http.server.HTTPServer(("127.0.0.1", port), SimplePageHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    try:
        # D1: Página estática comum sem WebGL
        print("\n[DEGRADAÇÃO D1] Testando página estática sem WebGL (esperado sucesso estruturado)...")
        test_url = f"http://127.0.0.1:{port}/"
        out_dir = TESTS_DIR / "output" / "degradation"
        out_dir.mkdir(parents=True, exist_ok=True)

        res_raw = await capture_webgl_and_component_states(
            url=test_url, output_dir=str(out_dir), max_components=2
        )
        res = json.loads(res_raw)

        assert res["status"] == "success", "Degradação falhou: status não foi success"
        assert res["webgl_supported"] is False, "D1 falhou: webgl_supported deveria ser False"
        assert res["webgl_shaders_captured"] == 0, "D1 falhou: nenhum shader deveria ser capturado"
        print(" -> Degradação graciosa D1 OK: WebGL ausente reportado sem erro de execução.")

    finally:
        server.shutdown()
        server.server_close()
        if old_mode is not None:
            os.environ["CDP_TEST_MODE"] = old_mode
        else:
            os.environ.pop("CDP_TEST_MODE", None)

    print("\n=== [REPROVA PASS] TODOS OS CENÁRIOS ADVERSARIAIS E DE DEGRADAÇÃO FORAM VALIDADOS COM SUCESSO. ===")


if __name__ == "__main__":
    try:
        asyncio.run(run_adversarial_suite())
        sys.exit(0)
    except Exception as exc:
        print(f"\n[REPROVA FAIL] Quebra inesperada na suíte adversarial: {exc}", file=sys.stderr)
        sys.exit(1)
