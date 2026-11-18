"""
verify_mcp_handshake.py — Teste de Handshake Oficial via SDK MCP
Garante que o servidor FastMCP inicializa, responde ao handshake,
processa a notificação de inicialização e expõe as 3 ferramentas com schemas válidos.
"""

import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT_DIR = Path(__file__).resolve().parent.parent
SERVER_SCRIPT = ROOT_DIR / "server.py"


async def run_handshake():
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_SCRIPT)],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 1. Envia request de inicialização e notificação initialized
            init_res = await asyncio.wait_for(session.initialize(), timeout=10.0)
            assert init_res.serverInfo.name == "antigravity-devtools-design-extractor", (
                f"Nome de servidor incorreto: {init_res.serverInfo.name}"
            )

            # 2. Lista as ferramentas registradas
            tools_res = await asyncio.wait_for(session.list_tools(), timeout=10.0)
            tools_by_name = {t.name: t for t in tools_res.tools}

            required_tools = {
                "extract_cdp_design_telemetry",
                "capture_webgl_and_component_states",
                "compile_living_design_system_html",
            }

            missing = required_tools - set(tools_by_name.keys())
            assert not missing, f"Ferramentas ausentes no servidor: {missing}"

            # 3. Valida a estrutura dos schemas das ferramentas
            for name in required_tools:
                tool = tools_by_name[name]
                assert tool.inputSchema is not None, f"Tool {name} sem inputSchema"
                assert tool.inputSchema.get("type") == "object", f"Tool {name} inputSchema inválido"

            print(f"[PASS] MCP Handshake completo: {len(tools_by_name)} tools operacionais.")


if __name__ == "__main__":
    try:
        asyncio.run(run_handshake())
        sys.exit(0)
    except Exception as exc:
        print(f"[FAIL] Erro no handshake MCP: {exc}", file=sys.stderr)
        sys.exit(1)
