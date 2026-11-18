import asyncio
import json
import shutil
import sys
from pathlib import Path

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
    target_dir = root / "Elysian Consult" / "aori-clone"
    target_dir.mkdir(parents=True, exist_ok=True)
    
    telemetry_path = str(target_dir / "design-telemetry.json")
    visual_dir = str(target_dir / "visual-captures")
    visual_manifest_path = str(target_dir / "visual-captures" / "visual-shader-manifest.json")
    html_path = str(target_dir / "design-system.html")
    tokens_path = str(target_dir / "design-tokens.json")
    
    print(f"=== EXTRAÇÃO AO VIVO: {TARGET_URL} ===")
    
    # 1. Telemetria
    print("[1/3] Extraindo telemetria...")
    res_telem_raw = await extract_cdp_design_telemetry(url=TARGET_URL, output_path=telemetry_path)
    res_telem = json.loads(res_telem_raw)
    print(f" -> Telemetria: {telemetry_path} (Capture ID: {res_telem.get('capture_id')})")
    
    # 2. Shaders e pares visuais
    print("[2/3] Capturando shaders e visuais...")
    res_visual_raw = await capture_webgl_and_component_states(url=TARGET_URL, output_dir=visual_dir, max_components=6)
    res_visual = json.loads(res_visual_raw)
    print(f" -> Shaders GLSL: {res_visual.get('webgl_shaders_captured')}")
    
    # 3. Compilação
    print("[3/3] Compilando Living Design System...")
    res_compile_raw = await compile_living_design_system_html(
        telemetry_path=telemetry_path,
        visual_manifest_path=visual_manifest_path,
        output_html_path=html_path,
        output_tokens_path=tokens_path,
        export_raw_fidelity=True,
    )
    print(f" -> Living Design System compilado: {html_path}")
    print("=== EXTRAÇÃO AO VIVO CONCLUÍDA COM SUCESSO ===")

if __name__ == "__main__":
    asyncio.run(main())
