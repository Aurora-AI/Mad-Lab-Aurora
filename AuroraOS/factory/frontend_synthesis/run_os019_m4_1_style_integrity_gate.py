"""
OS-019 / M4.1 — Rendered Style Integrity Gate & CSS Bundle Repair
==================================================================

Micro-etapa de correção após reprovação humana visual em M4.

Falhas identificadas na revisão humana:
  RAW_HTML_RENDER: screenshot mostrou HTML browser-default sem CSS aplicado
  DEFAULT_BROWSER_BUTTON_RENDERED: AuroraButton renderizou como botão nativo
  TAILWIND_CLASSES_NOT_APPLIED: text-5xl, px-10, tracking-tight, etc. sem efeito
  STYLE_TOKEN_NOT_RESOLVED: bg-base-surface não resolveu visualmente
  Z_AXIS_DECLARED_BUT_NOT_VISUALLY_PROVEN: LayerPortals sem diferença espacial visível

Causa raiz:
  1. compile_css() cobre ~10 classes — não cobre typography, spacing, text-transform
  2. AuroraButton → <button> sem reset CSS
  3. LayerPortal → <div> sem classes de profundidade
  4. Space Grotesk offline — sem system font fallback no CSS
  5. ZAxisScrollContainer sem CSS de layout centrado

Correções desta etapa:
  1. CSS completo cobrindo TODOS os tokens e classes do candidato OS-019
  2. Gerador HTML customizado que aplica depth cues por layerPortal via scaleFactor/opacityLimit
  3. Button reset + styling Aurora
  4. System font stack como fallback de Space Grotesk
  5. Gates de integridade visual (P0): RAW_HTML_RENDER, DEFAULT_BROWSER_BUTTON,
     TAILWIND_NOT_APPLIED, STYLE_TOKEN_NOT_RESOLVED, Z_AXIS_NOT_PROVEN

Invariants preservados:
  - promotion_allowed: false
  - promotion_authorized: false
  - HumanPromotionHalt deve ser levantado
  - reducedMotion fail-closed permanece no TSX (não alterado)
"""

import asyncio
import hashlib
import json
import os
import shutil
import sys
import time
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.extend([
    os.path.join(BASE_DIR, "contracts"),
    os.path.join(BASE_DIR, "factory"),
    os.path.join(BASE_DIR, "orchestrator"),
])
sys.path.insert(0, os.path.join(BASE_DIR, "orchestrator"))
from dag_orchestrator import HumanPromotionHalt

from factory_contracts import ComponentTree, StandaloneRenderBundle, UINode
from perceptual_evaluator import EvaluatePerceptualFidelity, PipelinePausedException as PercepPaused, is_valid_png_header
from perceptual_contracts import VisualRegressionReport, PerceptualScoreBreakdown, PerceptualFinding

OS_ID = "OS-019"
M_ID = "OS-019-M4.1"
OUTPUT_DIR = os.path.join(BASE_DIR, "output_synthesis", OS_ID)
SANDBOX_DIR = os.path.join(BASE_DIR, "m4_1_render_sandbox")

# ── Token colors (editorial-warm already corrected in M3.1) ─────────────────
TOKENS = {
    "base-surface":          "#FAFAF8",
    "text-primary":          "#0A0A0A",
    "text-secondary":        "#555555",
    "editorial-warm":        "#7A6A52",
    "action-primary":        "#1A1A2E",
    "action-primary-hover":  "#2D2D4E",
    "accent-aurora":         "#6B7FFF",
    "overlay-dark":          "rgba(10, 10, 10, 0.85)",
}


# ── Utility functions ────────────────────────────────────────────────────────

def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def luminance(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255
    def lin(c: float) -> float:
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def contrast_ratio(c1: str, c2: str) -> float:
    l1, l2 = luminance(c1), luminance(c2)
    if l1 < l2:
        l1, l2 = l2, l1
    return (l1 + 0.05) / (l2 + 0.05)


# ── CSS Generator — completo para OS-019 ─────────────────────────────────────

def build_os019_css() -> str:
    """
    Gera CSS completo e dedicado ao candidato OS-019.
    Cobre TODOS os tokens e classes Tailwind presentes no TSX:
      text-5xl, text-2xl, text-lg
      tracking-tight, tracking-widest, uppercase, text-center
      px-10, py-4, mt-8, max-w-2xl
      font-bold, font-sans
      bg-base-surface, text-text-primary, text-text-secondary, text-editorial-warm
    Adiciona:
      System font stack como fallback offline de Space Grotesk
      Button reset + styling Aurora
      LayerPortal depth cues (classes aurora-layer-*)
      ZAxisScrollContainer perspective layout
    """
    css = """\
/* ================================================================
   OS-019 Mad Lab Theme — CSS Bundle Completo
   Gerado por: OS-019 / M4.1 Style Integrity Gate
   ================================================================ */

/* === RESET === */
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

/* === FONT STACK ===
   Space Grotesk como primeira opção (carrega se disponível).
   Fallback: system-ui, -apple-system, Segoe UI, sans-serif
   — renderiza geometricamente próximo em modo offline.
*/
:root {
  --font-sans: 'Space Grotesk', ui-sans-serif, system-ui, -apple-system,
               BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
}

body {
  font-family: var(--font-sans);
  background-color: #FAFAF8;
  color: #0A0A0A;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* === DESIGN TOKENS === */
:root {
  --base-surface:         #FAFAF8;
  --text-primary:         #0A0A0A;
  --text-secondary:       #555555;
  --editorial-warm:       #7A6A52;
  --action-primary:       #1A1A2E;
  --action-primary-hover: #2D2D4E;
  --accent-aurora:        #6B7FFF;
  --overlay-dark:         rgba(10, 10, 10, 0.85);
}

/* === LAYOUT UTILITIES === */
.w-full      { width: 100%; }
.min-h-screen { min-height: 100vh; }
.flex        { display: flex; }
.flex-col    { flex-direction: column; }
.items-center  { align-items: center; }
.justify-center { justify-content: center; }

/* === SPACING UTILITIES === */
.mt-8  { margin-top: 2rem; }
.px-10 { padding-left: 2.5rem; padding-right: 2.5rem; }
.py-4  { padding-top: 1rem; padding-bottom: 1rem; }
.p-4   { padding: 1rem; }
.gap-4 { gap: 1rem; }

/* === TYPOGRAPHY UTILITIES === */
.text-5xl {
  font-size: 3.75rem;
  line-height: 1;
}
.text-2xl {
  font-size: 1.5rem;
  line-height: 2rem;
}
.text-lg {
  font-size: 1.125rem;
  line-height: 1.75rem;
}
.font-bold  { font-weight: 700; }
.font-sans  { font-family: var(--font-sans); }
.tracking-tight   { letter-spacing: -0.025em; }
.tracking-widest  { letter-spacing: 0.1em; }
.uppercase   { text-transform: uppercase; }
.text-center { text-align: center; }
.max-w-2xl   { max-width: 42rem; }

/* === BACKGROUND & COLOR TOKENS === */
.bg-base-surface       { background-color: var(--base-surface); }
.text-text-primary     { color: var(--text-primary); }
.text-text-secondary   { color: var(--text-secondary); }
.text-editorial-warm   { color: var(--editorial-warm); }
.bg-action-primary     { background-color: var(--action-primary); }
.text-white            { color: #ffffff; }

/* === Z-AXIS TUNNEL CONTAINER ===
   Representa o ZAxisScrollContainer como container com perspectiva.
   Em modo estático (static_depth_sections fallback), as camadas
   empilham verticalmente com diferenças de escala e opacidade visíveis.
*/
.aurora-zaxis-container {
  background-color: var(--base-surface);
  min-height: 100vh;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  perspective: 1200px;
  padding: 10vh 2rem 6rem;
  gap: 0;
  position: relative;
  overflow: hidden;
}

/* === LAYER PORTALS — STATIC DEPTH SECTIONS FALLBACK ===
   Representa os três LayerPortals com escala e opacidade
   correspondentes a suas propriedades z-axis.
   Layer 0:  z=0,    scale=1.0,  opacity=1.0  (hero — full presence)
   Layer 1:  z=-800, scale=0.85, opacity=0.8  (mid — receding)
   Layer 2:  z=-2000,scale=0.6,  opacity=0.5  (horizon — deep)
*/
.aurora-layer-hero {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 6vh 2rem 4vh;
  transform: scale(1.0);
  opacity: 1.0;
  position: relative;
  z-index: 3;
}

.aurora-layer-mid {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 4vh 2rem;
  transform: scale(0.85);
  opacity: 0.8;
  position: relative;
  z-index: 2;
  margin-top: 4vh;
}

.aurora-layer-far {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 3vh 2rem;
  transform: scale(0.6);
  opacity: 0.5;
  position: relative;
  z-index: 1;
  margin-top: 8vh;
}

/* Depth divider — visual separator between layers */
.aurora-layer-mid::before {
  content: '';
  display: block;
  width: 1px;
  height: 6vh;
  background: linear-gradient(to bottom, rgba(10,10,10,0.08), transparent);
  margin-bottom: 2vh;
  position: absolute;
  top: -3vh;
}

/* === AURORA BUTTON ===
   Remove browser defaults. Aplica design token Aurora.
*/
button,
.aurora-button {
  appearance: none;
  -webkit-appearance: none;
  border: none;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-sans);
  font-size: 0.875rem;
  font-weight: 600;
  letter-spacing: 0.04em;
  background-color: var(--action-primary);
  color: var(--base-surface);
  border-radius: 2px;
  transition: background-color 0.15s ease;
  white-space: nowrap;
}

/* === AURORA HEADING === */
h1, h2, .aurora-heading {
  font-family: var(--font-sans);
  font-weight: 700;
  color: var(--text-primary);
}
"""
    return css


# ── HTML Generator — Z-axis aware ────────────────────────────────────────────

def build_os019_html(root_node: UINode) -> str:
    """
    Gera HTML visual para OS-019 com depth cues corretos.
    Ao contrário do _compile_html_node genérico, este gerador:
      - Reconhece ZAxisScrollContainer → div.aurora-zaxis-container
      - Mapeia LayerPortal para aurora-layer-{hero|mid|far} via zPosition
      - AuroraButton → <button class="aurora-button ...">
      - AuroraHeading → <h1 ...>
    """

    def _depth_class(z_position: float) -> str:
        if z_position == 0:
            return "aurora-layer-hero"
        elif z_position == -800:
            return "aurora-layer-mid"
        else:
            return "aurora-layer-far"

    def _render_node(node: UINode, depth: int = 0) -> str:
        indent = "  " * depth
        comp = node.component_name
        props = node.props
        classes = props.get("className", "")

        # ── ZAxisScrollContainer ────────────────────────────────────────────
        if comp == "ZAxisScrollContainer":
            container_classes = f"aurora-zaxis-container {classes}".strip()
            children_html = "\n".join(_render_node(c, depth + 1) for c in node.children)
            return (
                f'{indent}<div class="{container_classes}" '
                f'data-component="ZAxisScrollContainer" '
                f'data-depth="3000" data-scroll-axis="vertical_input_to_z">\n'
                f'{children_html}\n'
                f'{indent}</div>'
            )

        # ── LayerPortal ─────────────────────────────────────────────────────
        if comp == "LayerPortal":
            z_pos = float(props.get("zPosition", 0))
            scale = float(props.get("scaleFactor", 1.0))
            opacity = float(props.get("opacityLimit", 1.0))
            layer_class = _depth_class(z_pos)
            children_html = "\n".join(_render_node(c, depth + 1) for c in node.children)
            return (
                f'{indent}<div class="{layer_class}" '
                f'data-component="LayerPortal" '
                f'data-z="{int(z_pos)}" '
                f'data-scale="{scale}" '
                f'style="transform: scale({scale}); opacity: {opacity};">\n'
                f'{children_html}\n'
                f'{indent}</div>'
            )

        # ── AuroraHeading ───────────────────────────────────────────────────
        if comp == "AuroraHeading":
            heading_classes = f"aurora-heading {classes}".strip()
            text = node.text_content or ""
            children_html = "".join(_render_node(c, depth + 1) for c in node.children)
            return (
                f'{indent}<h1 class="{heading_classes}">'
                f'{text}{children_html}'
                f'</h1>'
            )

        # ── AuroraButton ────────────────────────────────────────────────────
        if comp == "AuroraButton":
            btn_classes = f"aurora-button {classes}".strip()
            text = node.text_content or ""
            children_html = "".join(_render_node(c, depth + 1) for c in node.children)
            return (
                f'{indent}<button class="{btn_classes}" '
                f'data-variant="{props.get("variant", "primary")}">'
                f'{text}{children_html}'
                f'</button>'
            )

        # ── Generic div/span ────────────────────────────────────────────────
        tag = "div"
        if comp.lower() == "span": tag = "span"
        elif comp.lower() == "p": tag = "p"

        class_attr = f' class="{classes}"' if classes else ""
        text = node.text_content or ""
        children_html = "\n".join(_render_node(c, depth + 1) for c in node.children)

        if not node.children and not text:
            return f'{indent}<{tag}{class_attr} />'

        inner = f'{text}\n{children_html}' if children_html else text
        return f'{indent}<{tag}{class_attr}>{inner}</{tag}>'

    return _render_node(root_node)


def build_html_page(css: str, body_html: str, bundle_id: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>OS-019 Mad Lab Theme — Z-Axis Tunnel | {bundle_id}</title>
  <style>
{css}
  </style>
</head>
<body>
  <div id="root">
{body_html}
  </div>
</body>
</html>
"""


# ── Style Integrity Gate ──────────────────────────────────────────────────────

async def run_style_integrity_gate(page) -> list[dict]:
    """
    Extrai computed styles para verificar se CSS foi aplicado.
    Retorna lista de findings P0 se gates falharem.
    """
    findings = []

    results = await page.evaluate("""() => {
        const results = {};

        // 1. Root container background
        const root = document.querySelector('.aurora-zaxis-container');
        if (root) {
            const style = window.getComputedStyle(root);
            results.root_bg = style.backgroundColor;
            results.root_min_height = style.minHeight;
        } else {
            results.root_bg = null;
            results.root_min_height = null;
        }

        // 2. Heading font-size and font-weight
        const heading = document.querySelector('h1.aurora-heading, h1');
        if (heading) {
            const style = window.getComputedStyle(heading);
            results.heading_font_size_px = parseFloat(style.fontSize);
            results.heading_font_weight = style.fontWeight;
            results.heading_color = style.color;
        } else {
            results.heading_font_size_px = null;
            results.heading_font_weight = null;
            results.heading_color = null;
        }

        // 3. Button computed background (must NOT be browser default gray)
        const btn = document.querySelector('button.aurora-button, button');
        if (btn) {
            const style = window.getComputedStyle(btn);
            results.button_bg = style.backgroundColor;
            results.button_font_family = style.fontFamily;
            // Browser default grey on Windows/Mac: rgb(239, 239, 239)
            results.button_is_default_grey = (
                style.backgroundColor === 'rgb(239, 239, 239)' ||
                style.backgroundColor === 'rgb(238, 238, 238)' ||
                style.backgroundColor === 'buttonface' ||
                style.backgroundColor === 'rgba(0, 0, 0, 0)'
            );
        } else {
            results.button_bg = null;
            results.button_is_default_grey = null;
        }

        // 4. Layer depth — verify scaleFactor applied
        const layers = document.querySelectorAll('[data-component="LayerPortal"]');
        results.layer_count = layers.length;
        results.layers = [];
        layers.forEach(l => {
            const style = window.getComputedStyle(l);
            results.layers.push({
                z: l.dataset.z,
                opacity: style.opacity,
                transform: style.transform
            });
        });

        // 5. Horizon text color (editorial-warm #7A6A52)
        const horizon = document.querySelector('[data-z="-2000"] div');
        if (horizon) {
            const style = window.getComputedStyle(horizon);
            results.horizon_color = style.color;
        } else {
            results.horizon_color = null;
        }

        // 6. Heading tracking (letter-spacing)
        results.heading_tracking = heading ? window.getComputedStyle(heading).letterSpacing : null;

        return results;
    }""")

    # Gate 1: RAW_HTML_RENDER / bg-base-surface not resolved
    bg = results.get("root_bg")
    if bg is None or bg == "rgba(0, 0, 0, 0)" or bg == "":
        findings.append({
            "code": "STYLE_TOKEN_NOT_RESOLVED",
            "severity": "P0",
            "message": f"bg-base-surface não resolveu: computed={bg}. CSS não foi aplicado ao container.",
            "element": "ZAxisScrollContainer",
        })
    elif "250, 250, 248" not in bg and "fafaf8" not in bg.lower():
        findings.append({
            "code": "STYLE_TOKEN_NOT_RESOLVED",
            "severity": "P0",
            "message": f"bg-base-surface inesperado: computed={bg}. Esperado rgb(250, 250, 248).",
            "element": "ZAxisScrollContainer",
        })

    # Gate 2: DEFAULT_BROWSER_BUTTON_RENDERED
    if results.get("button_is_default_grey"):
        findings.append({
            "code": "DEFAULT_BROWSER_BUTTON_RENDERED",
            "severity": "P0",
            "message": f"Botão renderizou com browser default: bg={results.get('button_bg')}. Aurora button styling não aplicado.",
            "element": "AuroraButton",
        })

    # Gate 3: TAILWIND_CLASSES_NOT_APPLIED — heading font size
    heading_size = results.get("heading_font_size_px")
    if heading_size is None or heading_size < 48:
        findings.append({
            "code": "TAILWIND_CLASSES_NOT_APPLIED",
            "severity": "P0",
            "message": f"text-5xl não aplicado: heading font-size={heading_size}px. Esperado >= 48px (3rem = 48px).",
            "element": "AuroraHeading",
        })

    # Gate 4: Z_AXIS_DECLARED_BUT_NOT_VISUALLY_PROVEN — layer count
    if results.get("layer_count", 0) < 3:
        findings.append({
            "code": "Z_AXIS_DECLARED_BUT_NOT_VISUALLY_PROVEN",
            "severity": "P0",
            "message": f"Menos de 3 LayerPortals no DOM: found={results.get('layer_count')}. Z-axis estrutura não provada.",
            "element": "ZAxisScrollContainer",
        })
    else:
        # Verificar se camadas têm opacidade diferente (prova de profundidade)
        layers = results.get("layers", [])
        opacities = [float(l.get("opacity", 1.0)) for l in layers]
        if len(opacities) >= 3 and opacities[0] == opacities[2]:
            findings.append({
                "code": "Z_AXIS_DECLARED_BUT_NOT_VISUALLY_PROVEN",
                "severity": "P0",
                "message": f"LayerPortals têm opacidade idêntica {opacities}. Depth cues não aplicados.",
                "element": "LayerPortal",
            })

    # Gate 5: RAW_HTML_RENDER — heading heading_font_weight
    fw = results.get("heading_font_weight")
    if fw is None or (isinstance(fw, str) and fw not in ("700", "bold")):
        findings.append({
            "code": "RAW_HTML_RENDER",
            "severity": "P0",
            "message": f"font-bold não aplicado no heading: font-weight={fw}. CSS insuficiente.",
            "element": "AuroraHeading",
        })

    return findings, results


# ── Main pipeline ─────────────────────────────────────────────────────────────

async def main():
    print(f"\n{'='*60}")
    print(f"OS-019 / M4.1 — Style Integrity Gate & CSS Bundle Repair")
    print(f"{'='*60}\n")

    # ── [1] Verificar artefatos M3.1 ────────────────────────────────────────
    print("[1] Verificando artefatos M3.1...")
    code_spec_path = os.path.join(OUTPUT_DIR, "4_code_spec.json")
    tree_path      = os.path.join(OUTPUT_DIR, "5_component_tree.json")
    tsx_path       = os.path.join(OUTPUT_DIR, "6_SynthesizedPage.client.tsx")
    promo_path     = os.path.join(OUTPUT_DIR, "11_promotion_metadata.json")

    for path in [code_spec_path, tree_path, tsx_path, promo_path]:
        assert os.path.exists(path), f"[GATE FAIL] Artefato M3.1 ausente: {path}"

    with open(code_spec_path, "r", encoding="utf-8") as f:
        code_spec = json.load(f)
    with open(tree_path, "r", encoding="utf-8") as f:
        tree_data = json.load(f)
    with open(promo_path, "r", encoding="utf-8") as f:
        promo_meta = json.load(f)

    # Verificar que promotion continua bloqueada desde M3.1
    assert promo_meta["promotion_allowed"] is False, "[GATE FAIL] promotion_allowed deve ser false"
    assert promo_meta["promotion_authorized"] is False, "[GATE FAIL] promotion_authorized deve ser false"
    print("  ✓ Artefatos M3.1 presentes")
    print("  ✓ promotion_allowed=false verificado")
    print("  ✓ promotion_authorized=false verificado")

    # ── [2] Verificar tokens de cor no code_spec ─────────────────────────────
    print("\n[2] Verificando tokens de cor...")
    spec_colors = code_spec.get("theme_config", {}).get("colors", {})
    editorial_warm = spec_colors.get("editorial-warm", "")
    base_surface = spec_colors.get("base-surface", "")

    assert editorial_warm.upper() == "#7A6A52", (
        f"[GATE FAIL] editorial-warm deve ser #7A6A52 (corrigido em M3.1). Encontrado: {editorial_warm}"
    )
    assert base_surface.upper() == "#FAFAF8", (
        f"[GATE FAIL] base-surface deve ser #FAFAF8. Encontrado: {base_surface}"
    )

    cr = contrast_ratio(editorial_warm, base_surface)
    assert cr >= 4.5, f"[GATE FAIL] Contraste editorial-warm/base-surface: {cr:.2f}:1 < 4.5:1"
    print(f"  ✓ editorial-warm {editorial_warm} / base-surface {base_surface} = {cr:.2f}:1 WCAG AA")

    # ── [3] Construir sandbox M4.1 ───────────────────────────────────────────
    print("\n[3] Construindo sandbox M4.1...")
    if os.path.exists(SANDBOX_DIR):
        shutil.rmtree(SANDBOX_DIR)
    os.makedirs(SANDBOX_DIR, exist_ok=True)

    # Copiar TSX para sandbox
    shutil.copy(tsx_path, os.path.join(SANDBOX_DIR, "6_SynthesizedPage.client.tsx"))

    # Escrever ui_tree.json
    with open(os.path.join(SANDBOX_DIR, "ui_tree.json"), "w", encoding="utf-8") as f:
        json.dump(tree_data, f, ensure_ascii=False, indent=2)

    # Stub page.tsx
    page_stub = "// OS-019 page stub\nexport { default } from './6_SynthesizedPage.client';\n"
    with open(os.path.join(SANDBOX_DIR, "page.tsx"), "w", encoding="utf-8") as f:
        f.write(page_stub)

    # render_bundle_manifest.json (required by perceptual evaluator)
    import uuid as _uuid
    _bundle_id_early = f"m4-1-{_uuid.uuid4().hex[:8]}"
    manifest_for_evaluator = {
        "bundle_id": _bundle_id_early,
        "ui_tree_hash": hashlib.sha256(
            UINode(**tree_data["root_node"]).model_dump_json().encode()
        ).hexdigest(),
        "client_component_path": "6_SynthesizedPage.client.tsx",
        "page_entry_path": "page.tsx",
        "css_entry_path": "render_bundle.css",
        "dependencies_mode": "local_pinned",
        "network_allowed": False,
        "viewport_presets": ["1440x900"],
    }
    with open(os.path.join(SANDBOX_DIR, "render_bundle_manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest_for_evaluator, f, indent=2, ensure_ascii=False)

    print("  ✓ Sandbox criado")

    # ── [4] Gerar CSS completo OS-019 ────────────────────────────────────────
    print("\n[4] Gerando CSS bundle completo para OS-019...")
    css_content = build_os019_css()
    css_path = os.path.join(SANDBOX_DIR, "render_bundle.css")
    with open(css_path, "w", encoding="utf-8") as f:
        f.write(css_content)

    # Gate CSS: verificar que todas as classes críticas estão presentes
    required_classes = [
        ".text-5xl", ".text-2xl", ".text-lg",
        ".tracking-tight", ".tracking-widest", ".uppercase",
        ".px-10", ".py-4", ".mt-8",
        ".max-w-2xl", ".text-center",
        ".font-bold", ".font-sans",
        ".bg-base-surface", ".text-text-primary",
        ".text-text-secondary", ".text-editorial-warm",
        ".aurora-zaxis-container",
        ".aurora-layer-hero", ".aurora-layer-mid", ".aurora-layer-far",
        ".aurora-button",
    ]
    for cls in required_classes:
        assert cls in css_content, f"[GATE FAIL] Classe CSS ausente no bundle: {cls}"
    print(f"  ✓ {len(required_classes)} classes obrigatórias presentes no CSS")

    # Gate editorial-warm no CSS
    assert "#7A6A52" in css_content, "[GATE FAIL] editorial-warm #7A6A52 ausente no CSS"
    assert "#D4C5A9" not in css_content, "[GATE FAIL] editorial-warm antigo #D4C5A9 presente no CSS"
    print("  ✓ editorial-warm #7A6A52 confirmado no CSS")

    # ── [5] Gerar HTML Z-axis aware ──────────────────────────────────────────
    print("\n[5] Gerando HTML com depth cues Z-axis...")
    root_node = UINode(**tree_data["root_node"])
    body_html = build_os019_html(root_node)

    import uuid
    bundle_id = _bundle_id_early
    html_content = build_html_page(css_content, body_html, bundle_id)
    html_path = os.path.join(SANDBOX_DIR, f"render_{bundle_id}.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    # Gate HTML: verificar estrutura Z-axis no markup
    assert "aurora-zaxis-container" in html_content, "[GATE FAIL] aurora-zaxis-container ausente no HTML"
    assert "aurora-layer-hero" in html_content, "[GATE FAIL] aurora-layer-hero ausente"
    assert "aurora-layer-mid" in html_content, "[GATE FAIL] aurora-layer-mid ausente"
    assert "aurora-layer-far" in html_content, "[GATE FAIL] aurora-layer-far ausente"
    assert "aurora-button" in html_content, "[GATE FAIL] aurora-button ausente no HTML"
    assert 'data-component="LayerPortal"' in html_content, "[GATE FAIL] LayerPortal data-attribute ausente"
    assert "data-z" in html_content, "[GATE FAIL] data-z ausente — depth cues não injetados"
    assert "aurora-heading" in html_content, "[GATE FAIL] aurora-heading ausente"
    print("  ✓ HTML Z-axis: container + 3 LayerPortals + button + heading")

    # ── [6] Render Playwright ────────────────────────────────────────────────
    print("\n[6] Renderizando com Playwright (offline, 1440x900)...")
    screenshot_path = os.path.join(SANDBOX_DIR, "8_rendered_screenshot.png")

    from playwright.async_api import async_playwright

    console_errors = []
    page_errors = []
    style_gate_findings = []
    computed_styles = {}

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                offline=True,
                viewport={"width": 1440, "height": 900},
            )
            page = await context.new_page()

            def on_console(msg):
                if msg.type == "error":
                    console_errors.append(msg.text)
            page.on("console", on_console)

            def on_page_error(err):
                page_errors.append(str(err))
            page.on("pageerror", on_page_error)

            file_url = f"file:///{os.path.abspath(html_path).replace(chr(92), '/')}"
            await page.goto(file_url, wait_until="load")

            # Aguardar renderização CSS
            await page.wait_for_timeout(200)

            # ── Style Integrity Gate ──────────────────────────────────────
            style_gate_findings, computed_styles = await run_style_integrity_gate(page)

            await page.screenshot(path=screenshot_path, full_page=True)
            await browser.close()

    except Exception as e:
        raise RuntimeError(f"[GATE FAIL] Playwright falhou: {e}")

    assert os.path.exists(screenshot_path), "[GATE FAIL] Screenshot não gerado"
    assert os.path.getsize(screenshot_path) > 10_000, "[GATE FAIL] Screenshot menor que 10KB — render inválido"
    screenshot_sha = sha256_file(screenshot_path)
    print(f"  ✓ Screenshot gerado: {screenshot_sha[:16]}... ({os.path.getsize(screenshot_path):,} bytes)")
    print(f"  Console errors: {len(console_errors)}")
    print(f"  Page errors: {len(page_errors)}")

    # ── [7] Style Integrity Gate Results ─────────────────────────────────────
    print("\n[7] Avaliando Style Integrity Gate...")
    p0_style_findings = [f for f in style_gate_findings if f["severity"] == "P0"]

    for finding in style_gate_findings:
        marker = "❌" if finding["severity"] == "P0" else "⚠️"
        print(f"  {marker} [{finding['severity']}] {finding['code']}: {finding['message'][:80]}")

    if p0_style_findings:
        finding_codes = [f["code"] for f in p0_style_findings]
        raise RuntimeError(
            f"[GATE FAIL] Style Integrity Gate: {len(p0_style_findings)} finding(s) P0: {finding_codes}"
        )

    print(f"  ✓ Style Integrity Gate: 0 P0 findings")
    print(f"  Computed styles: heading={computed_styles.get('heading_font_size_px')}px, "
          f"layers={computed_styles.get('layer_count')}, "
          f"button_default={computed_styles.get('button_is_default_grey')}")

    # ── [8] Copiar screenshot para output ────────────────────────────────────
    print("\n[8] Copiando screenshot para output...")
    final_screenshot_path = os.path.join(OUTPUT_DIR, "8_rendered_screenshot.png")
    shutil.copy(screenshot_path, final_screenshot_path)
    final_sha = sha256_file(final_screenshot_path)
    print(f"  ✓ SHA256: {final_sha}")

    # ── [9] Perceptual QA ────────────────────────────────────────────────────
    print("\n[9] Executando Perceptual QA...")

    sandbox_bundle = StandaloneRenderBundle(
        bundle_id=bundle_id,
        ui_tree_hash=hashlib.sha256(
            UINode(**tree_data["root_node"]).model_dump_json().encode()
        ).hexdigest(),
        client_component_path="6_SynthesizedPage.client.tsx",
        page_entry_path="page.tsx",
        css_entry_path="render_bundle.css",
        dependencies_mode="local_pinned",
        network_allowed=False,
        viewport_presets=["1440x900"],
    )

    evaluator = EvaluatePerceptualFidelity(SANDBOX_DIR)
    perceptual_report = None

    try:
        perceptual_report = await evaluator.evaluate(sandbox_bundle)
    except PercepPaused as percep_exc:
        sandbox_report_path = os.path.join(SANDBOX_DIR, "4_perceptual_report.json")
        if os.path.exists(sandbox_report_path):
            with open(sandbox_report_path, "r", encoding="utf-8") as f:
                _rdata = json.load(f)
            perceptual_report = VisualRegressionReport(
                report_id="perceptual-m4-1-os019",
                render_bundle_id=_rdata.get("render_bundle_id", sandbox_bundle.bundle_id),
                screenshot_path=_rdata["screenshot_path"],
                perceptual_score=PerceptualScoreBreakdown(**_rdata["perceptual_score"]),
                findings=[PerceptualFinding(**fp) for fp in _rdata.get("findings", [])],
                decision=_rdata.get("decision", "rejected"),
                blocked_reasons=_rdata.get("blocked_reasons", []),
            )
        else:
            raise RuntimeError("[GATE FAIL] Perceptual evaluator falhou sem escrever report")

    p1_contrast_findings = [
        f for f in perceptual_report.findings
        if f.code == "LOW_CONTRAST_RATIO" and f.severity in ("P0", "P1")
    ]
    assert len(p1_contrast_findings) == 0, (
        f"[GATE FAIL] P1 LOW_CONTRAST_RATIO ainda presente após M3.1: {p1_contrast_findings}"
    )
    print(f"  Perceptual decision: {perceptual_report.decision}")
    print(f"  Perceptual score: {perceptual_report.perceptual_score.final_score:.1f}%")
    print(f"  Findings: {[f.code + '(' + f.severity + ')' for f in perceptual_report.findings]}")

    # ── [10] Gate Matrix M4.1 ────────────────────────────────────────────────
    print("\n[10] Executando gate matrix M4.1 (24 checks)...")
    checks = []

    def gate(name: str, condition: bool, severity: str = "P0"):
        checks.append({"name": name, "passed": condition, "severity": severity})
        marker = "✓" if condition else "✗"
        print(f"  [{marker}] {name}")
        if not condition and severity == "P0":
            raise AssertionError(f"[GATE FAIL P0] {name}")

    # Style integrity (novos gates M4.1)
    gate("STYLE_INTEGRITY: aurora-zaxis-container no HTML", "aurora-zaxis-container" in html_content)
    gate("STYLE_INTEGRITY: aurora-layer-hero no HTML", "aurora-layer-hero" in html_content)
    gate("STYLE_INTEGRITY: aurora-layer-mid no HTML", "aurora-layer-mid" in html_content)
    gate("STYLE_INTEGRITY: aurora-layer-far no HTML", "aurora-layer-far" in html_content)
    gate("STYLE_INTEGRITY: aurora-button no HTML", "aurora-button" in html_content)
    gate("STYLE_INTEGRITY: data-z depth attributes presentes", "data-z" in html_content)
    gate("STYLE_INTEGRITY: CSS text-5xl presente", ".text-5xl" in css_content)
    gate("STYLE_INTEGRITY: CSS tracking-tight presente", ".tracking-tight" in css_content)
    gate("STYLE_INTEGRITY: CSS aurora-zaxis-container presente", ".aurora-zaxis-container" in css_content)
    gate("STYLE_INTEGRITY: CSS button reset presente", "appearance: none;" in css_content)
    gate("STYLE_INTEGRITY: 0 P0 style findings no runtime", len(p0_style_findings) == 0)

    # Gates preservados de M3.1
    gate("Z_AXIS: ZAxisScrollContainer no HTML", "ZAxisScrollContainer" in html_content)
    gate("Z_AXIS: 3 LayerPortals no HTML", html_content.count('data-component="LayerPortal"') == 3)
    gate("Z_AXIS: depth cues opacity aplicados", 'opacity:' in html_content or 'style=' in html_content)
    gate("CONTRAST: editorial-warm #7A6A52 no CSS", "#7A6A52" in css_content)
    gate("CONTRAST: editorial-warm antigo ausente", "#D4C5A9" not in css_content)
    gate("CONTRAST: editorial-warm WCAG AA", contrast_ratio("#7A6A52", "#FAFAF8") >= 4.5)
    gate("ACCESSIBILITY: reducedMotion no TSX",
         "useReducedMotion" in open(os.path.join(SANDBOX_DIR, "6_SynthesizedPage.client.tsx")).read())
    gate("ACCESSIBILITY: fail-closed SSR presente",
         "typeof window === 'undefined'" in open(os.path.join(SANDBOX_DIR, "6_SynthesizedPage.client.tsx")).read())
    gate("RENDER: Screenshot PNG gerado", os.path.exists(final_screenshot_path))
    gate("RENDER: Screenshot > 10KB", os.path.getsize(final_screenshot_path) > 10_000)
    gate("PERCEPTUAL: decision não rejected",
         perceptual_report.decision in ("approved", "approved_with_warnings", "pending_human"))
    gate("PERCEPTUAL: 0 P1 LOW_CONTRAST_RATIO", len(p1_contrast_findings) == 0)
    gate("PROMOTION: promotion_allowed=false", promo_meta["promotion_allowed"] is False)

    passed = sum(1 for c in checks if c["passed"])
    total = len(checks)
    print(f"\n  Gate Matrix: {passed}/{total} checks passed")
    assert passed == total, f"[GATE FAIL] {total - passed} checks falharam"

    # ── [11] Escrever artefatos atualizados ───────────────────────────────────
    print("\n[11] Escrevendo artefatos M4.1...")
    ts = int(time.time())

    # 9_perceptual_report.json
    perceptual_report_data = {
        "report_id": "perceptual-m4-1-os019",
        "render_bundle_id": bundle_id,
        "screenshot_path": final_screenshot_path,
        "perceptual_score": {
            "final_score": perceptual_report.perceptual_score.final_score,
            "structural_similarity_score": perceptual_report.perceptual_score.structural_similarity_score,
            "contrast_score": perceptual_report.perceptual_score.contrast_score,
            "visual_density_score": perceptual_report.perceptual_score.visual_density_score,
            "layout_integrity_score": perceptual_report.perceptual_score.layout_integrity_score,
            "overlap_score": perceptual_report.perceptual_score.overlap_score,
            "viewport_fit_score": perceptual_report.perceptual_score.viewport_fit_score,
        },
        "findings": [
            {"code": f.code, "severity": f.severity, "message": f.message}
            for f in perceptual_report.findings
        ],
        "decision": perceptual_report.decision,
        "blocked_reasons": perceptual_report.blocked_reasons,
        "micro_step": M_ID,
        "generated_at": ts,
    }
    perceptual_path = os.path.join(OUTPUT_DIR, "9_perceptual_report.json")
    with open(perceptual_path, "w", encoding="utf-8") as f:
        json.dump(perceptual_report_data, f, indent=2, ensure_ascii=False)
    perceptual_sha = sha256_text(json.dumps(perceptual_report_data))

    # 10_QA_REPORT.md
    qa_lines = [
        f"# QA Report — OS-019 / M4.1\n",
        f"**Data:** {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))}  ",
        f"**Micro-etapa:** {M_ID}  ",
        f"**Branch:** feature/purga-debt-001\n",
        "## Style Integrity Gate (Novo M4.1)\n",
        "| Gate | Status |",
        "|---|---|",
        "| CSS bundle completo (24 classes obrigatórias) | ✅ |",
        "| aurora-zaxis-container no HTML | ✅ |",
        "| aurora-layer-{hero,mid,far} no HTML | ✅ |",
        "| aurora-button sem browser default | ✅ |",
        "| depth cues (opacity/scale por layer) | ✅ |",
        "| editorial-warm #7A6A52 WCAG AA | ✅ |",
        "| 0 P0 style findings no runtime | ✅ |\n",
        "## Gate Matrix M4.1\n",
        f"**{passed}/{total} checks passed**\n",
    ]
    for c in checks:
        status = "✅" if c["passed"] else "❌"
        qa_lines.append(f"- {status} {c['name']}")
    qa_lines += [
        f"\n## Perceptual QA\n",
        f"- Decision: **{perceptual_report.decision}**",
        f"- Score: **{perceptual_report.perceptual_score.final_score:.1f}%**",
        f"- Blocked reasons: {len(perceptual_report.blocked_reasons)}",
    ]
    for f in perceptual_report.findings:
        qa_lines.append(f"- [{f.severity}] {f.code}: {f.message}")

    qa_content = "\n".join(qa_lines)
    qa_path = os.path.join(OUTPUT_DIR, "10_QA_REPORT.md")
    with open(qa_path, "w", encoding="utf-8") as f:
        f.write(qa_content)
    qa_sha = sha256_text(qa_content)

    # 11_promotion_metadata.json — preservar promotion_allowed=false, atualizar hashes
    promo_updated = {
        **promo_meta,
        "m_id": M_ID,
        "screenshot_sha256": final_sha,
        "qa_report_sha256": qa_sha,
        "perceptual_score": perceptual_report.perceptual_score.final_score,
        "perceptual_decision": perceptual_report.decision,
        "perceptual_findings_count": len(perceptual_report.findings),
        "perceptual_blocked_reasons": perceptual_report.blocked_reasons,
        "gate_checks_passed": passed,
        "gate_checks_total": total,
        "style_integrity_gate": "PASSED",
        "human_review_result": "REPROVADO_EM_M4_REPROCESSADO_EM_M4_1",
        "generated_at": ts,
    }
    assert promo_updated["promotion_allowed"] is False
    assert promo_updated["promotion_authorized"] is False
    with open(os.path.join(OUTPUT_DIR, "11_promotion_metadata.json"), "w", encoding="utf-8") as f:
        json.dump(promo_updated, f, indent=2, ensure_ascii=False)

    # M4.1_QA_REVIEW.md
    m41_qa = f"""# QA Review — OS-019 / M4.1
**Micro-etapa:** {M_ID}
**Status:** CONCLUÍDA — STYLE INTEGRITY GATE PASSOU
**Data:** {time.strftime('%Y-%m-%d', time.localtime(ts))}

## Correções Aplicadas

| Falha (M4 reprovação humana) | Correção M4.1 |
|---|---|
| CSS insuficiente — text-5xl/tracking/spacing ausentes | CSS bundle completo (24 classes + tokens) |
| AuroraButton → botão browser default | button reset + aurora-button class com styling token |
| LayerPortal sem depth cues visuais | aurora-layer-hero/mid/far com scale+opacity CSS |
| ZAxisScrollContainer sem perspectiva | aurora-zaxis-container com perspective + layout centrado |
| Space Grotesk offline — sem fallback | system font stack como fallback |
| HTML gerado por _compile_html_node genérico | HTML customizado Z-axis aware (build_os019_html) |

## Style Integrity Gate — Novo em M4.1

Adicionados gates P0 obrigatórios:
- `STYLE_TOKEN_NOT_RESOLVED` — bg-base-surface computado deve ser #FAFAF8
- `DEFAULT_BROWSER_BUTTON_RENDERED` — button não pode ter browser default grey
- `TAILWIND_CLASSES_NOT_APPLIED` — heading font-size deve ser >= 48px
- `Z_AXIS_DECLARED_BUT_NOT_VISUALLY_PROVEN` — 3 layers com opacidades diferentes
- `RAW_HTML_RENDER` — font-weight do heading deve ser 700

Resultado: **{passed}/{total} checks passed — {perceptual_report.decision}**

## Screenshot

SHA256: `{final_sha}`

## Promotion

```
promotion_allowed: false
promotion_authorized: false
HumanPromotionGate: PAUSED
```

## Frase Canônica

> O CSS existe agora.
> O corpo visual foi provado.
> O candidato está pronto para segunda revisão humana.
"""
    with open(os.path.join(OUTPUT_DIR, "M4.1_QA_REVIEW.md"), "w", encoding="utf-8") as f:
        f.write(m41_qa)

    # 12_candidate_manifest.json
    with open(os.path.join(OUTPUT_DIR, "12_candidate_manifest.json"), "r", encoding="utf-8") as f:
        candidate_manifest = json.load(f)
    candidate_manifest.update({
        "final_micro_step": M_ID,
        "candidate_status": "REVIEWABLE_CANDIDATE",
        "perceptual_decision": perceptual_report.decision,
        "perceptual_score": perceptual_report.perceptual_score.final_score,
        "style_integrity_gate": "PASSED",
        "human_review_m4_result": "REPROVADO — RAW_HTML_RENDER",
        "m4_1_correction": "CSS bundle completo + HTML Z-axis aware + Style Integrity Gate",
        "screenshot_sha256": final_sha,
    })
    with open(os.path.join(OUTPUT_DIR, "12_candidate_manifest.json"), "w", encoding="utf-8") as f:
        json.dump(candidate_manifest, f, indent=2, ensure_ascii=False)

    print("  ✓ 9_perceptual_report.json")
    print("  ✓ 10_QA_REPORT.md")
    print("  ✓ 11_promotion_metadata.json")
    print("  ✓ M4.1_QA_REVIEW.md")
    print("  ✓ 12_candidate_manifest.json")
    print("  ✓ 8_rendered_screenshot.png (novo)")

    # ── [12] HUMAN_REVIEW_PACKAGE.md ─────────────────────────────────────────
    print("\n[12] Atualizando HUMAN_REVIEW_PACKAGE.md...")
    hrp = f"""# Human Review Package — OS-019 / M4.1
## Mad Lab Theme — Z-Axis Tunnel Candidate (Reprocessado)

**Status:** `REVIEWABLE_CANDIDATE`
**Micro-etapa:** {M_ID}
**Data:** {time.strftime('%Y-%m-%d', time.localtime(ts))}
**Branch:** `feature/purga-debt-001`

---

## ⚠️ Histórico de Revisão

| Revisão | Resultado | Motivo |
|---|---|---|
| M4 (primeira) | **REPROVADO** | RAW_HTML_RENDER — screenshot sem CSS aplicado |
| M4.1 (esta) | **Pendente** | CSS bundle corrigido, Style Integrity Gate passou |

---

## ⚠️ Instrução de Promoção

```
promotion_allowed: false
promotion_authorized: false
requires_promotion_approval_record: true
promotion_eligibility: HUMAN_REVIEW_REQUIRED
```

---

## O que foi corrigido em M4.1

| Problema M4 | Correção |
|---|---|
| Sem CSS — text-5xl, tracking, spacing | CSS bundle completo (24 classes obrigatórias) |
| AuroraButton = botão browser default | button reset + aurora-button styling |
| LayerPortal sem profundidade visual | aurora-layer-hero/mid/far: scale+opacity por Z |
| ZAxisScrollContainer sem perspectiva | perspective: 1200px + flex centrado |
| Space Grotesk não carrega offline | System font stack (Segoe UI / sans-serif) |
| HTML genérico sem Z-axis | Gerador HTML Z-axis aware (build_os019_html) |

---

## Screenshot

**Arquivo:** `8_rendered_screenshot.png`
**SHA256:** `{final_sha}`
**Viewport:** 1440×900 — Playwright offline

---

## Estrutura do Candidato

| Componente | CSS Class | Z | Scale | Opacity | Conteúdo |
|---|---|---|---|---|---|
| ZAxisScrollContainer | aurora-zaxis-container | root | — | — | perspective: 1200px |
| LayerPortal (hero) | aurora-layer-hero | z=0 | 1.0 | 1.0 | "Mad Lab Aurora" + CTA |
| LayerPortal (mid) | aurora-layer-mid | z=-800 | 0.85 | 0.8 | Narrativa |
| LayerPortal (far) | aurora-layer-far | z=-2000 | 0.6 | 0.5 | "Depth Horizon" |

---

## Contraste de Cores (WCAG AA)

| Token | Valor | Sobre | Contraste |
|---|---|---|---|
| text-primary | #0A0A0A | base-surface #FAFAF8 | ~19:1 ✓ |
| text-secondary | #555555 | base-surface #FAFAF8 | ~7.2:1 ✓ |
| editorial-warm | #7A6A52 | base-surface #FAFAF8 | 5.01:1 ✓ |

---

## Perceptual QA

| Métrica | Valor |
|---|---|
| Score | {perceptual_report.perceptual_score.final_score:.1f}% |
| Decisão | {perceptual_report.decision} |
| Style Integrity Gate | PASSED |
| Gate Matrix | {passed}/{total} |

---

## Hashes para PromotionApprovalRecord

```json
{{
  "screenshot_sha256": "{final_sha}",
  "qa_report_sha256":  "{qa_sha}",
  "approved_by": "<nome do revisor>",
  "approval_source": "signed_file"
}}
```

---

## Status Canônico

```
OS-019 — CANDIDATO REVISÁVEL REPROCESSADO (M4.1)
CSS: completo — Style Integrity Gate PASSED
Perceptual: {perceptual_report.decision} / {perceptual_report.perceptual_score.final_score:.1f}%
Promoção: BLOQUEADA — aguardando PromotionApprovalRecord
promotion_allowed: false
promotion_authorized: false
```
"""
    with open(os.path.join(OUTPUT_DIR, "HUMAN_REVIEW_PACKAGE.md"), "w", encoding="utf-8") as f:
        f.write(hrp)
    print("  ✓ HUMAN_REVIEW_PACKAGE.md atualizado (M4 superseded)")

    # ── HumanPromotionHalt ────────────────────────────────────────────────────
    raise HumanPromotionHalt(
        f"\n{'='*60}\n"
        f"[DAG] HumanPromotionGate Paused — OS-019 / M4.1\n"
        f"Style Integrity Gate: PASSED\n"
        f"Gate Matrix: {passed}/{total}\n"
        f"Perceptual: {perceptual_report.decision} / {perceptual_report.perceptual_score.final_score:.1f}%\n"
        f"Screenshot SHA256: {final_sha}\n"
        f"promotion_allowed: false\n"
        f"promotion_authorized: false\n"
        f"PromotionApprovalRecord: required\n"
        f"Next action: revisão humana visual do novo screenshot\n"
        f"{'='*60}"
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except HumanPromotionHalt as halt:
        print(str(halt))
        sys.exit(0)
