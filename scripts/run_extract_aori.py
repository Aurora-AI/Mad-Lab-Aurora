import asyncio
import json
import shutil
import sys
from pathlib import Path

# Adiciona o diretório do extrator ao sys.path
EXTRACTOR_DIR = Path(__file__).resolve().parent.parent / "tools" / "mcp-design-extractor"
sys.path.insert(0, str(EXTRACTOR_DIR))

from server import (
    extract_cdp_design_telemetry,
    capture_webgl_and_component_states,
    compile_living_design_system_html,
)

TARGET_URL = "https://aoricreative.com/"

async def main():
    root = Path(__file__).resolve().parent.parent
    
    telemetry_path = str(root / "design-telemetry.json")
    visual_dir = str(root / ".antigravity" / "visual-captures")
    visual_manifest_path = str(root / ".antigravity" / "visual-captures" / "visual-shader-manifest.json")
    html_path = str(root / "design-system.html")
    tokens_path = str(root / "design-tokens.json")
    
    print(f"=== INICIANDO EXTRAÇÃO DO LIVING DESIGN SYSTEM ===")
    print(f"Alvo: {TARGET_URL}\n")
    
    # 1. Extração de Telemetria Bruta via CDP
    print(f"[1/3] Extraindo telemetria bruta via CDP...")
    res_telem_raw = await extract_cdp_design_telemetry(url=TARGET_URL, output_path=telemetry_path)
    res_telem = json.loads(res_telem_raw)
    print(f" -> Telemetria salva em: {telemetry_path}")
    print(f" -> Capture ID: {res_telem.get('capture_id')}")
    print(f" -> Variáveis CSS encontradas: {res_telem.get('css_variables_count')}")
    print(f" -> Deltas de interação medidos: {res_telem.get('hover_deltas_count')}\n")
    
    # 2. Captura de Shaders GLSL e Componentes 2x DPI
    print(f"[2/3] Capturando WebGL shaders e screenshots 2x DPI...")
    res_visual_raw = await capture_webgl_and_component_states(url=TARGET_URL, output_dir=visual_dir, max_components=8)
    res_visual = json.loads(res_visual_raw)
    print(f" -> Manifesto visual salvo em: {visual_manifest_path}")
    print(f" -> WebGL suportado: {res_visual.get('webgl_supported')}")
    print(f" -> Shaders GLSL interceptados: {res_visual.get('webgl_shaders_captured')}")
    print(f" -> Pares de screenshots capturados: {res_visual.get('component_screenshot_pairs')}\n")
    
    # 3. Compilação do Living Design System
    print(f"[3/3] Compilando Living Design System em HTML e design-tokens.json...")
    res_compile_raw = await compile_living_design_system_html(
        telemetry_path=telemetry_path,
        visual_manifest_path=visual_manifest_path,
        output_html_path=html_path,
        output_tokens_path=tokens_path,
        export_raw_fidelity=True,
    )
    res_compile = json.loads(res_compile_raw)
    print(f" -> Living Design System compilado em: {html_path}")
    print(f" -> Design Tokens salvos em: {tokens_path}")
    if "design_system_raw_html_path" in res_compile:
        print(f" -> Raw fidelity exportado em: {res_compile['design_system_raw_html_path']}")
        
    # 4. Arquivamento em Referências/Sites/aoricreative
    archive_dir = root / "Referências" / "Sites" / "aoricreative"
    archive_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(telemetry_path, archive_dir / "design-telemetry.json")
    shutil.copy2(tokens_path, archive_dir / "design-tokens.json")
    shutil.copy2(html_path, archive_dir / "design-system.html")
    raw_html = root / "design-system-raw.html"
    if raw_html.exists():
        shutil.copy2(raw_html, archive_dir / "design-system-raw.html")
    if Path(visual_manifest_path).exists():
        vis_dest = archive_dir / "visual-captures"
        if vis_dest.exists():
            shutil.rmtree(vis_dest)
        shutil.copytree(Path(visual_dir), vis_dest)
    print(f"\n -> Cópia de arquivo persistida em: {archive_dir}")
    print(f"\n=== EXTRAÇÃO CONCLUÍDA COM SUCESSO ===")

if __name__ == "__main__":
    asyncio.run(main())
