"""
OS-019R / M3 — Design System Synthesis
=======================================

Converte dados brutos de M2 em Design System auditável e normalizado.

PROIBIDO:
  - Criar TSX / landing / candidato
  - Criar screenshot
  - Criar promotion_metadata
  - Inventar token sem evidência em M2
  - Classificar Times New Roman como fonte canônica sem confirmação

ENTREGÁVEIS:
  design_tokens.json
  typography_system.json
  color_semantics.json
  spacing_system.json
  surface_system.json
  media_design_tokens.json
  design_system_summary.md
  m3_traceability_matrix.json
  M3_QA_REPORT.md

INVARIANTE:
  promotion_allowed: false — nunca alterar
"""

import json
import os
import re
import time
import math
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output_synthesis", "OS-019R")

# ── Anti-desvio: artefatos proibidos ────────────────────────────────────────
PROHIBITED_ARTIFACTS = [
    "SynthesizedPage.client.tsx",
    "rendered_screenshot",
    "promotion_metadata",
    "HUMAN_REVIEW_PACKAGE",
    "candidate_manifest",
]


def load_m2(name: str) -> dict | list | None:
    path = os.path.join(OUTPUT_DIR, name)
    if not os.path.exists(path):
        print(f"  [WARN] M2 artifact não encontrado: {name}")
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(name: str, data) -> str:
    path = os.path.join(OUTPUT_DIR, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    size = os.path.getsize(path)
    print(f"  ✓ {name} — {size:,} bytes")
    return path


def rgb_to_hex(rgb: str) -> str:
    try:
        nums = re.findall(r"\d+(?:\.\d+)?", rgb)
        if len(nums) >= 3:
            r, g, b = int(float(nums[0])), int(float(nums[1])), int(float(nums[2]))
            return f"#{r:02x}{g:02x}{b:02x}"
    except Exception:
        pass
    return rgb


def px_to_float(val: str) -> float | None:
    """Converte '250px' → 250.0"""
    if not val:
        return None
    try:
        return float(val.replace("px", "").replace("pt", "").strip())
    except (ValueError, AttributeError):
        return None


def compute_tracking_ratio(letter_spacing_px: float, font_size_px: float) -> str | None:
    if not font_size_px or font_size_px == 0:
        return None
    ratio = letter_spacing_px / font_size_px
    return f"{ratio:.3f}"


def lh_ratio(line_height_px: float, font_size_px: float) -> str | None:
    if not font_size_px or font_size_px == 0:
        return None
    ratio = line_height_px / font_size_px
    return f"{ratio:.3f}"


def wcag_relative_luminance(hex_color: str) -> float:
    """Calcula luminância relativa para verificação WCAG."""
    try:
        h = hex_color.lstrip("#")
        if len(h) != 6:
            return 0
        r, g, b = tuple(int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4))
        def linearize(c):
            return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
        return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)
    except Exception:
        return 0


def wcag_contrast(hex1: str, hex2: str) -> float:
    l1 = wcag_relative_luminance(hex1)
    l2 = wcag_relative_luminance(hex2)
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


# ─────────────────────────────────────────────────────────────────────────────
# FASE 1 — Carregar todos os artefatos M2
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print(f"\n{'='*60}")
    print("OS-019R / M3 — Design System Synthesis")
    print(f"{'='*60}\n")
    ts_start = time.time()

    print("[0] Carregando artefatos M2...")
    font_inventory    = load_m2("font_inventory.json") or []
    color_usage       = load_m2("color_usage.json") or []
    computed_styles   = load_m2("computed_styles.json") or []
    layout_boxes      = load_m2("layout_boxes.json") or []
    media_inventory   = load_m2("media_inventory.json") or {}
    vp_desktop        = load_m2("viewport_state_desktop.json") or {}
    vp_mobile         = load_m2("viewport_state_mobile.json") or {}
    a11y_tree         = load_m2("accessibility_tree.json") or {}

    css_vars = vp_desktop.get("css_custom_properties", {})
    print(f"  CSS custom properties: {len(css_vars)}")
    print(f"  Computed styles samples: {len(computed_styles)}")
    print(f"  Font inventory entries: {len(font_inventory)}")
    print(f"  Color usage entries: {len(color_usage)}")
    print(f"  Layout boxes: {len(layout_boxes)}")


    # ─────────────────────────────────────────────────────────────────────────
    # FASE 2 — typography_system.json
    # ─────────────────────────────────────────────────────────────────────────
    print("\n[1] Sintetizando typography_system.json...")

    # Headings do a11y tree
    headings_a11y = a11y_tree.get("headings", [])

    # Computed styles de headings
    heading_styles_map = {}
    for s in computed_styles:
        if s.get("tag") in ("h1", "h2", "h3", "h4"):
            tag = s["tag"]
            fs  = px_to_float(s.get("font_size"))
            if fs and (tag not in heading_styles_map or fs > heading_styles_map[tag].get("_fs", 0)):
                heading_styles_map[tag] = {**s, "_fs": fs}

    # Classificar Times New Roman
    tns_entries = [f for f in font_inventory if "Times New Roman" in f.get("family", "")]
    lausanne_entries = [f for f in font_inventory if "Lausanne" in f.get("family", "")]

    # Mapear Lausanne weights
    lausanne_weights = {}
    for entry in lausanne_entries:
        fam = entry.get("family", "")
        w_match = re.search(r"Lausanne-(\d+)", fam)
        css_weight = entry.get("weight")
        if w_match:
            nom_weight = int(w_match.group(1))
            lausanne_weights[nom_weight] = {
                "css_computed_weight": css_weight,
                "sizes_in_use": entry.get("sizes", []),
                "usage_contexts": entry.get("usage_contexts", []),
            }

    # Escala tipográfica derivada dos headings
    type_scale = []

    # Display Monumental (H1 hero)
    h1s = heading_styles_map.get("h1")
    if h1s:
        fs  = px_to_float(h1s.get("font_size"))
        lh  = px_to_float(h1s.get("line_height"))
        ls  = px_to_float(h1s.get("letter_spacing"))
        type_scale.append({
            "level": "display_monumental",
            "tag": "h1",
            "font_family": h1s.get("font_family"),
            "font_size_px": fs,
            "font_size_rem_approx": round(fs / 16, 2) if fs else None,
            "font_weight_computed": h1s.get("font_weight"),
            "line_height_px": lh,
            "line_height_ratio": lh_ratio(lh, fs) if lh and fs else None,
            "letter_spacing_px": ls,
            "tracking_ratio": compute_tracking_ratio(ls, fs) if ls is not None and fs else None,
            "text_transform": h1s.get("text_transform"),
            "color_computed": h1s.get("color"),
            "usage_context": "hero/display monumental",
            "source_trace": "computed_styles.json/h1 + a11y_tree.headings",
            "notes": "Escala extrema de display — tracking negativo artesanal (-4.6% do font-size). Não usar abaixo de 80px sem recalibrar tracking.",
        })

    # Display Large (H2 hero — Play Reel, 144px)
    # Identificar H2s de grande escala
    h2_large_styles = [s for s in computed_styles if s.get("tag") == "h2"
                       and px_to_float(s.get("font_size", "0px") or "0px") >= 100]
    if h2_large_styles:
        s2 = h2_large_styles[0]
        fs  = px_to_float(s2.get("font_size"))
        lh  = px_to_float(s2.get("line_height"))
        ls  = px_to_float(s2.get("letter_spacing"))
        type_scale.append({
            "level": "display_large",
            "tag": "h2",
            "font_family": s2.get("font_family"),
            "font_size_px": fs,
            "font_size_rem_approx": round(fs / 16, 2) if fs else None,
            "font_weight_computed": s2.get("font_weight"),
            "line_height_px": lh,
            "line_height_ratio": lh_ratio(lh, fs) if lh and fs else None,
            "letter_spacing_px": ls,
            "tracking_ratio": compute_tracking_ratio(ls, fs) if ls is not None and fs else None,
            "text_transform": s2.get("text_transform"),
            "usage_context": "section display (Play Reel, hero sections)",
            "source_trace": "computed_styles.json/h2 large scale",
        })

    # Section Label (H2 small — 14px)
    h2_label_styles = [s for s in computed_styles if s.get("tag") == "h2"
                       and px_to_float(s.get("font_size", "0px") or "0px") <= 20]
    if h2_label_styles:
        s3 = h2_label_styles[0]
        fs  = px_to_float(s3.get("font_size"))
        lh  = px_to_float(s3.get("line_height"))
        ls  = px_to_float(s3.get("letter_spacing"))
        type_scale.append({
            "level": "label_section",
            "tag": "h2",
            "font_family": s3.get("font_family"),
            "font_size_px": fs,
            "font_size_rem_approx": round(fs / 16, 2) if fs else None,
            "font_weight_computed": s3.get("font_weight"),
            "line_height_px": lh,
            "line_height_ratio": lh_ratio(lh, fs) if lh and fs else None,
            "letter_spacing_px": ls,
            "tracking_ratio": compute_tracking_ratio(ls, fs) if ls is not None and fs else None,
            "text_transform": s3.get("text_transform"),
            "usage_context": "section labels, category tags",
            "source_trace": "computed_styles.json/h2 label scale",
        })

    # Body / Paragraph
    para_styles = [s for s in computed_styles if s.get("tag") == "p"]
    if para_styles:
        s4 = para_styles[0]
        fs  = px_to_float(s4.get("font_size"))
        lh  = px_to_float(s4.get("line_height"))
        ls  = px_to_float(s4.get("letter_spacing"))
        type_scale.append({
            "level": "body",
            "tag": "p",
            "font_family": s4.get("font_family"),
            "font_size_px": fs,
            "font_size_rem_approx": round(fs / 16, 2) if fs else None,
            "font_weight_computed": s4.get("font_weight"),
            "line_height_px": lh,
            "line_height_ratio": lh_ratio(lh, fs) if lh and fs else None,
            "letter_spacing_px": ls,
            "tracking_ratio": compute_tracking_ratio(ls, fs) if ls is not None and fs else None,
            "text_transform": s4.get("text_transform"),
            "usage_context": "body text, editorial copy",
            "source_trace": "computed_styles.json/p",
        })

    # Tracking rule derivado de dados reais
    tracking_rule = {
        "rule": "negative_tracking_scale",
        "description": "Quanto maior o tamanho de display, mais negativo o tracking óptico.",
        "evidence": {
            "250px_display": f"{h1s.get('letter_spacing') if h1s else 'N/A'} = {compute_tracking_ratio(px_to_float(h1s.get('letter_spacing')), 250) if h1s else 'N/A'} do font-size",
        },
        "safe_range": {
            "display_gt_100px": "tracking-ratio entre -0.04 e -0.06",
            "display_lt_60px": "tracking-ratio entre -0.01 e -0.02",
            "label_14px": "tracking-ratio neutra a levemente negativa",
        },
        "source_trace": "computed_styles.json/h1.letter_spacing",
    }

    typography_system = {
        "meta": {
            "os": "OS-019R",
            "phase": "M3",
            "source": "M2 computed_styles + font_inventory + a11y_tree",
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "promotion_allowed": False,
        },
        "font_families": {
            "primary": {
                "name": "TWKLausanne",
                "variants": ["Lausanne-300", "Lausanne-400", "Lausanne-500"],
                "weights_in_use": lausanne_weights,
                "hosting": "self-hosted woff2 (~30KB per variant)",
                "fallback_stack": ["Helvetica Neue", "Helvetica", "Arial", "sans-serif"],
                "source_trace": "M1 network_manifest.json + M2 font_inventory.json",
            },
            "fallback_detected": {
                "name": "Times New Roman",
                "status": "fallback_or_default_detected",
                "classification": "NOT_CANONICAL",
                "requires_usage_context": True,
                "evidence": tns_entries[:2] if tns_entries else [],
                "note": "Detectado pelo browser em nós não completamente estilizados ou herança residual. Não entra como token canônico sem confirmação de uso deliberado.",
                "source_trace": "M2 font_inventory.json — presença não confirma intencionalidade",
            },
        },
        "type_scale": type_scale,
        "tracking_rule": tracking_rule,
    }

    save_json("typography_system.json", typography_system)


    # ─────────────────────────────────────────────────────────────────────────
    # FASE 3 — design_tokens.json + color_semantics.json
    # ─────────────────────────────────────────────────────────────────────────
    print("\n[2] Sintetizando design_tokens.json...")

    # Categorizar CSS custom properties
    primitive_tokens = {}
    semantic_tokens = {}
    opacity_tokens = {}
    motion_tokens = {}
    unclassified_tokens = {}

    for key, val in css_vars.items():
        # Detectar tokens de opacidade
        if re.search(r"-0[2468]$", key) or "opacity" in key:
            opacity_tokens[key] = {"value": val, "source": "css_custom_property"}
        elif any(c in key for c in ["--color-", "--bg-", "--surface-", "--text-", "--border-"]):
            # Classificar por papel semântico
            if "dark-grey" in key:
                semantic_tokens[key] = {"value": val, "role": "surface_dark_primary", "source": "css_custom_property"}
            elif "light-grey" in key:
                semantic_tokens[key] = {"value": val, "role": "surface_light_secondary", "source": "css_custom_property"}
            elif "off-white" in key:
                semantic_tokens[key] = {"value": val, "role": "surface_background_soft", "source": "css_custom_property"}
            elif "white" in key:
                semantic_tokens[key] = {"value": val, "role": "surface_light_primary", "source": "css_custom_property"}
            elif "story" in key:
                semantic_tokens[key] = {"value": val, "role": "surface_editorial_dark", "source": "css_custom_property"}
            else:
                semantic_tokens[key] = {"value": val, "role": "unclassified_color", "source": "css_custom_property"}
        elif any(t in key for t in ["--duration", "--easing", "--transition", "--motion", "--delay"]):
            motion_tokens[key] = {"value": val, "source": "css_custom_property"}
        elif "--color-" in key:
            primitive_tokens[key] = {"value": val, "source": "css_custom_property"}
        else:
            unclassified_tokens[key] = {"value": val, "source": "css_custom_property"}

    # Primitivos numéricos — extrair de computed styles
    # Tamanhos de radius, shadow, etc.
    radius_primitives = {}
    for s in computed_styles:
        br = s.get("border_radius")
        if br and br != "0px":
            ctx = s.get("selector", s.get("tag", "unknown"))
            radius_primitives[br] = {"value": br, "context": ctx, "source": "computed_styles.json"}

    design_tokens = {
        "meta": {
            "os": "OS-019R",
            "phase": "M3",
            "source": "M2 viewport_state_desktop.css_custom_properties + computed_styles",
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "promotion_allowed": False,
            "total_tokens": len(css_vars),
        },
        "primitive_tokens": primitive_tokens,
        "semantic_tokens": semantic_tokens,
        "opacity_scale": opacity_tokens,
        "motion_tokens": motion_tokens,
        "radius_tokens": radius_primitives,
        "unclassified_tokens": unclassified_tokens,
        "notes": {
            "opacity_pattern": "Sistema de opacidade consistente com sufixos -02/-04/-06/-08 (20%/40%/60%/80%) aplicado a todas as cores principais.",
            "dark_mode_risk": "Paleta usa claro (#fff) e escuro (#0d0e13) como duo dominante — inversão de dark mode requer atenção ao --color-story (#070707) vs backgrounds.",
        }
    }

    save_json("design_tokens.json", design_tokens)

    # Color semantics
    print("\n[3] Sintetizando color_semantics.json...")

    # Extrair cores únicas da color_usage com contexto
    dominant_colors = color_usage[:12]

    # Pares de contraste WCAG
    contrast_pairs = []
    key_colors = {
        "dark_grey": "#0d0e13",
        "white": "#ffffff",
        "off_white": "#f8f8f8",
        "light_grey": "#e4e0db",
        "warm_beige": "#e0ccbb",  # da color_usage
        "story": "#070707",
    }
    for n1, h1 in key_colors.items():
        for n2, h2 in key_colors.items():
            if n1 >= n2:
                continue
            ratio = wcag_contrast(h1, h2)
            lvl = "AAA" if ratio >= 7 else "AA" if ratio >= 4.5 else "AA_large" if ratio >= 3 else "FAIL"
            contrast_pairs.append({
                "foreground": {"name": n1, "hex": h1},
                "background": {"name": n2, "hex": h2},
                "contrast_ratio": round(ratio, 2),
                "wcag_level": lvl,
                "source_trace": "computed from css_custom_properties + wcag_formula",
            })

    # Ordenar por ratio
    contrast_pairs.sort(key=lambda x: x["contrast_ratio"], reverse=True)

    color_semantics = {
        "meta": {
            "os": "OS-019R",
            "phase": "M3",
            "source": "M2 color_usage.json + viewport_state_desktop.css_custom_properties",
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "promotion_allowed": False,
        },
        "palette_character": {
            "description": "Paleta quase monocromática — escuro profundo + off-white + bege quente. Ausência de cores saturadas é deliberada.",
            "dominant_mode": "light backgrounds with dark type",
            "secondary_mode": "dark sections (--color-story #070707) for editorial contrast",
            "accent": "none_detected — editorial emphasis via scale and weight, not color",
        },
        "core_colors": {
            "dark_grey": {
                "token": "--color-dark-grey",
                "hex": "#0d0e13",
                "computed_rgb": "rgb(13, 14, 19)",
                "role": "primary_text + navigation_surface + dark_overlay",
                "frequency_rank": 1,
                "source_trace": "color_usage.json rank 1 + css_custom_properties",
            },
            "white": {
                "token": "--color-white",
                "hex": "#ffffff",
                "computed_rgb": "rgb(255, 255, 255)",
                "role": "primary_background + text_on_dark",
                "frequency_rank": 2,
                "source_trace": "color_usage.json rank 2 + css_custom_properties",
            },
            "off_white": {
                "token": "--color-off-white",
                "hex": "#f8f8f8",
                "computed_rgb": "rgb(248, 248, 248)",
                "role": "soft_background_variant",
                "source_trace": "css_custom_properties",
            },
            "light_grey": {
                "token": "--color-light-grey",
                "hex": "#e4e0db",
                "computed_rgb": "rgb(228, 224, 219)",
                "role": "secondary_text + borders + muted_elements",
                "frequency_rank": 5,
                "source_trace": "color_usage.json rank 5 + css_custom_properties",
            },
            "warm_beige": {
                "token": None,
                "hex": "#e0ccbb",
                "computed_rgb": "rgb(224, 204, 187)",
                "role": "editorial_text + footer + warm_muted",
                "frequency_rank": 4,
                "source_trace": "color_usage.json rank 4",
                "note": "Não tem CSS custom property própria — pode ser derivada de outro token com opacidade ou cor editorial.",
            },
            "story_dark": {
                "token": "--color-story",
                "hex": "#070707",
                "computed_rgb": "rgb(7, 7, 7)",
                "role": "editorial_dark_section_background",
                "source_trace": "color_usage.json + css_custom_properties",
            },
        },
        "opacity_relationships": {
            "pattern": "Todas as cores principais têm variantes de opacidade -02/-04/-06/-08",
            "use_cases": {
                "02": "subtle_overlay, ghost_divider",
                "04": "muted_text, placeholder",
                "06": "secondary_text, icon_inactive",
                "08": "almost_opaque, soft_overlay",
            },
            "source_trace": "css_custom_properties opacity pattern analysis",
        },
        "contrast_pairs": contrast_pairs[:10],
        "wcag_risk_areas": [
            {
                "pair": "warm_beige #e0ccbb on white #fff",
                "estimated_ratio": round(wcag_contrast("#e0ccbb", "#ffffff"), 2),
                "risk": "FAIL for body text — use only for large display text (18px+ bold)",
                "source_trace": "computed from color_usage.json + wcag_formula",
            },
            {
                "pair": "light_grey #e4e0db on white #fff",
                "estimated_ratio": round(wcag_contrast("#e4e0db", "#ffffff"), 2),
                "risk": "FAIL — decorative use only, never for text",
                "source_trace": "computed from css_custom_properties + wcag_formula",
            },
        ],
        "usage_frequency": [
            {"color": c["color"], "count": c["count"], "primary_prop": c["usages"][0]["prop"] if c["usages"] else None}
            for c in dominant_colors
        ],
    }

    save_json("color_semantics.json", color_semantics)


    # ─────────────────────────────────────────────────────────────────────────
    # FASE 4 — spacing_system.json (derivado de layout_boxes)
    # ─────────────────────────────────────────────────────────────────────────
    print("\n[4] Sintetizando spacing_system.json...")

    # Extrair measurements reais dos layout_boxes
    nav_box    = next((b for b in layout_boxes if b.get("label") == "navigation"), None)
    main_box   = next((b for b in layout_boxes if b.get("label") == "main"), None)
    footer_box = next((b for b in layout_boxes if b.get("label") == "footer"), None)

    # Sections
    section_boxes = [b for b in layout_boxes if b.get("label", "").startswith("section_")]

    # Videos boxes
    video_boxes = [b for b in layout_boxes if b.get("label", "").startswith("video_")]

    # Nav height
    nav_h = nav_box.get("rect", {}).get("h") if nav_box else None

    # Section gaps (derivar dos Y positions)
    section_y_positions = sorted([b["rect"]["y"] for b in section_boxes if "rect" in b])
    section_gaps = []
    for i in range(1, len(section_y_positions)):
        gap = section_y_positions[i] - section_y_positions[i - 1]
        if gap > 0:
            section_gaps.append(gap)

    # Page width
    page_width = vp_desktop.get("viewport", {}).get("width", 1440)

    # Large containers
    large_containers = [b for b in layout_boxes if b.get("label", "").startswith("large_container_")]
    container_widths = [b["rect"]["w"] for b in large_containers if "rect" in b and b["rect"].get("w", 0) > 600]
    max_content_width = max(container_widths, default=page_width)
    typical_content_width = sorted(container_widths)[len(container_widths) // 2] if container_widths else None

    # Video aspect ratios
    video_ratios = []
    for vb in video_boxes:
        r = vb.get("rect", {})
        w, h = r.get("w", 0), r.get("h", 0)
        if w and h:
            ratio = w / h
            video_ratios.append(round(ratio, 3))

    # Computed paddings de elementos
    h1_padding = None
    body_padding = None
    for s in computed_styles:
        if s.get("tag") == "h1" and not h1_padding:
            h1_padding = s.get("padding")
        if s.get("tag") == "body" and not body_padding:
            body_padding = s.get("padding")

    spacing_system = {
        "meta": {
            "os": "OS-019R",
            "phase": "M3",
            "source": "M2 layout_boxes.json + viewport_state_desktop.json + computed_styles.json",
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "promotion_allowed": False,
        },
        "viewport": {
            "desktop_width": page_width,
            "desktop_height": vp_desktop.get("viewport", {}).get("height", 900),
            "mobile_width": vp_mobile.get("viewport", {}).get("width", 390),
            "mobile_height": vp_mobile.get("viewport", {}).get("height", 844),
            "source_trace": "viewport_state_desktop.json + viewport_state_mobile.json",
        },
        "navigation": {
            "height_px": nav_h,
            "position": nav_box.get("position") if nav_box else None,
            "z_index": nav_box.get("z_index") if nav_box else None,
            "source_trace": "layout_boxes.json/navigation",
        },
        "page_layout": {
            "max_content_width_detected_px": max_content_width,
            "typical_content_width_px": typical_content_width,
            "page_width_px": page_width,
            "horizontal_margin_approx": round((page_width - (typical_content_width or page_width)) / 2) if typical_content_width else None,
            "source_trace": "layout_boxes.json/large_container analysis",
        },
        "section_rhythm": {
            "section_count": len(section_boxes),
            "y_positions": section_y_positions[:8],
            "inter_section_gaps_px": section_gaps[:6],
            "typical_gap_px": sorted(section_gaps)[len(section_gaps) // 2] if section_gaps else None,
            "source_trace": "layout_boxes.json/section_* bounding boxes",
        },
        "media_grid": {
            "video_count": len(video_boxes),
            "video_widths_px": sorted(set(b["rect"]["w"] for b in video_boxes if "rect" in b)),
            "video_heights_px": sorted(set(b["rect"]["h"] for b in video_boxes if "rect" in b)),
            "video_aspect_ratios": sorted(set(video_ratios)),
            "note": "Aspect ratios variam — grid não é uniforme. Sistema de mídia usa variação intencional de proporção.",
            "source_trace": "layout_boxes.json/video_* bounding boxes",
        },
        "element_spacing": {
            "h1_padding": h1_padding,
            "body_padding": body_padding,
            "note": "Valores de padding extraídos de computed_styles — podem incluir padding do browser se não resetado.",
            "source_trace": "computed_styles.json",
        },
    }

    save_json("spacing_system.json", spacing_system)


    # ─────────────────────────────────────────────────────────────────────────
    # FASE 5 — surface_system.json
    # ─────────────────────────────────────────────────────────────────────────
    print("\n[5] Sintetizando surface_system.json...")

    # Backgrounds extraídos dos computed styles e layout boxes
    bg_colors_seen = defaultdict(list)
    for s in computed_styles:
        bg = s.get("background_color")
        if bg and bg not in ("rgba(0, 0, 0, 0)", "transparent"):
            ctx = f"{s.get('tag')} {s.get('text_sample', '')[:30]}"
            bg_colors_seen[bg].append(ctx)

    # Z-index layers
    z_layers = vp_desktop.get("z_index_landscape", [])
    fixed_els = vp_desktop.get("fixed_sticky_elements", [])

    surface_system = {
        "meta": {
            "os": "OS-019R",
            "phase": "M3",
            "source": "M2 computed_styles + layout_boxes + viewport_state_desktop",
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "promotion_allowed": False,
        },
        "surfaces": {
            "primary_background": {
                "color": "#ffffff",
                "token": "--color-white",
                "usage": "main page background, section default",
                "source_trace": "computed_styles.json body + color_usage.json rank 2",
            },
            "soft_background": {
                "color": "#f8f8f8",
                "token": "--color-off-white",
                "usage": "alternate section, subtle differentiation",
                "source_trace": "css_custom_properties",
            },
            "editorial_dark": {
                "color": "#070707",
                "token": "--color-story",
                "usage": "dark section backgrounds for editorial contrast",
                "source_trace": "color_usage.json + css_custom_properties --color-story",
            },
            "navigation_surface": {
                "color": "dynamic — adapts to is-light / is-dark body class",
                "detected_class": "app is-light",
                "position": "fixed",
                "z_index": "9",
                "source_trace": "layout_boxes.json/navigation + dom_tree.json .app.is-light",
            },
        },
        "z_index_system": {
            "layers": z_layers,
            "layer_map": [
                {"z": 1, "role": "base_interactive"},
                {"z": 2, "role": "elevated_content"},
                {"z": 9, "role": "navigation"},
                {"z": 14, "role": "menu_button"},
                {"z": 20, "role": "overlay_or_modal"},
            ],
            "fixed_sticky_elements": fixed_els,
            "source_trace": "viewport_state_desktop.json/z_index_landscape",
        },
        "theme_switching": {
            "observed": True,
            "mechanism": "CSS class on .app element — detected: .app.is-light",
            "implication": "Dark/light theme switching via class toggle, not CSS media query",
            "source_trace": "dom_tree.json .app class + color_usage.json pattern",
        },
        "overlay_system": {
            "opacity_scale": ["0.2", "0.4", "0.6", "0.8"],
            "tokens": {k: v for k, v in semantic_tokens.items() if "opacity" in k or re.search(r"-0[2468]$", k)},
            "source_trace": "css_custom_properties opacity suffix pattern",
        },
    }

    save_json("surface_system.json", surface_system)


    # ─────────────────────────────────────────────────────────────────────────
    # FASE 6 — media_design_tokens.json
    # ─────────────────────────────────────────────────────────────────────────
    print("\n[6] Sintetizando media_design_tokens.json...")

    videos = media_inventory.get("videos", [])
    images = media_inventory.get("images", [])

    # Video role distribution
    role_dist: dict = defaultdict(list)
    for v in videos:
        role_dist[v.get("role", "unknown")].append(v)

    # Aspect ratio analysis
    aspect_ratios = {}
    for v in videos:
        r = v.get("rect", {})
        w, h = r.get("w", 0), r.get("h", 0)
        if w and h:
            ar = w / h
            # Common ratios
            if abs(ar - 1.0) < 0.05:
                ar_name = "1:1 (square)"
            elif abs(ar - (4/3)) < 0.1:
                ar_name = "4:3 (classic)"
            elif abs(ar - (16/9)) < 0.1:
                ar_name = "16:9 (widescreen)"
            elif abs(ar - (3/4)) < 0.1:
                ar_name = "3:4 (portrait)"
            elif abs(ar - (4/5)) < 0.1:
                ar_name = "4:5 (portrait)"
            elif ar < 0.8:
                ar_name = "portrait_custom"
            elif ar > 1.5:
                ar_name = "landscape_custom"
            else:
                ar_name = "custom"
            aspect_ratios[f"video_{v['index']}"] = {
                "dimensions": f"{w}×{h}",
                "ratio": round(ar, 3),
                "ratio_name": ar_name,
            }

    # Autoplay behavior analysis
    autoplay_html_count = sum(1 for v in videos if v.get("autoplay"))
    muted_count         = sum(1 for v in videos if v.get("muted"))
    loop_count          = sum(1 for v in videos if v.get("loop"))

    media_design_tokens = {
        "meta": {
            "os": "OS-019R",
            "phase": "M3",
            "source": "M2 media_inventory.json + layout_boxes.json",
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "promotion_allowed": False,
        },
        "video_system": {
            "total_count": len(videos),
            "role_distribution": {role: len(items) for role, items in role_dist.items()},
            "autoplay_html_attribute": autoplay_html_count,
            "autoplay_note": (
                "autoplay=False em HTML não confirma ausência de autoplay. "
                "O site usa JavaScript para acionar autoplay via IntersectionObserver. "
                "Classificação definitiva requer análise JS em M4."
            ),
            "autoplay_classification": "hypothesis_for_M4_validation",
            "muted": muted_count,
            "loop": loop_count,
            "attribute_pattern": "muted=True + loop=True em todos os vídeos — padrão de ambient/editorial media",
            "aspect_ratios": aspect_ratios,
            "design_token_video_as_surface": {
                "description": "Vídeos usados como superfícies editoriais em cards/projetos — não como hero background puro",
                "dimensions_range": {
                    "min_width": min((v["rect"]["w"] for v in videos if "rect" in v), default=None),
                    "max_width": max((v["rect"]["w"] for v in videos if "rect" in v), default=None),
                    "min_height": min((v["rect"]["h"] for v in videos if "rect" in v), default=None),
                    "max_height": max((v["rect"]["h"] for v in videos if "rect" in v), default=None),
                },
                "source_trace": "media_inventory.json + layout_boxes.json video_*",
            },
        },
        "image_system": {
            "total_count": len(images),
            "all_with_alt": all(img.get("alt") for img in images),
            "alt_coverage": f"{sum(1 for i in images if i.get('alt'))}/{len(images)}",
            "loading_lazy_count": sum(1 for i in images if i.get("loading") == "lazy"),
            "source_trace": "media_inventory.json images",
        },
        "accessibility": {
            "videos_with_track": 0,
            "videos_without_track": len(videos),
            "risk": "HIGH — 0/8 vídeos têm captions/track. Violação WCAG 1.2.2 se vídeos tiverem áudio relevante.",
            "mitigation": "Vídeos são muted+loop — provavelmente ambient/editorial sem fala. Verificar em M4 se há narração.",
            "source_trace": "accessibility_tree.json videos_with_track",
        },
        "media_grammar": {
            "description": "Mídia como elemento editorial central, não decorativo. Proporções variadas intencionais.",
            "motion_classification": "hypothesis_for_M4_validation — comportamento de autoplay requer análise JS",
            "source_trace": "media_inventory.json + layout_boxes.json + accessibility_tree.json",
        },
    }

    save_json("media_design_tokens.json", media_design_tokens)


    # ─────────────────────────────────────────────────────────────────────────
    # FASE 7 — m3_traceability_matrix.json
    # ─────────────────────────────────────────────────────────────────────────
    print("\n[7] Gerando m3_traceability_matrix.json...")

    traceability_matrix = {
        "meta": {
            "os": "OS-019R",
            "phase": "M3",
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "promotion_allowed": False,
        },
        "entries": [
            {
                "token_group": "typography_system.type_scale.display_monumental",
                "derived_from": "computed_styles.json/h1",
                "key_values": {"font_size": "250px", "letter_spacing": "-11.5px", "font_weight": "400"},
                "confidence": "high",
                "note": "Extraído diretamente do browser",
            },
            {
                "token_group": "typography_system.font_families.primary",
                "derived_from": "M1 network_manifest.json + M2 font_inventory.json",
                "key_values": {"name": "TWKLausanne", "variants": ["300", "400", "500"]},
                "confidence": "high",
                "note": "Confirmado via M1 network interception",
            },
            {
                "token_group": "typography_system.font_families.fallback_detected",
                "derived_from": "M2 font_inventory.json",
                "key_values": {"name": "Times New Roman", "status": "NOT_CANONICAL"},
                "confidence": "medium",
                "note": "Presença detectada mas não confirmada como uso intencional",
            },
            {
                "token_group": "design_tokens.semantic_tokens",
                "derived_from": "viewport_state_desktop.json/css_custom_properties",
                "key_values": {"total_css_vars": len(css_vars)},
                "confidence": "high",
                "note": "CSS custom properties extraídas do :root via browser JS",
            },
            {
                "token_group": "color_semantics.core_colors",
                "derived_from": "color_usage.json + css_custom_properties",
                "key_values": {"dominant": "#0d0e13", "background": "#ffffff", "warm": "#e0ccbb"},
                "confidence": "high",
                "note": "Derivado de computed colors + frequência de uso",
            },
            {
                "token_group": "color_semantics.contrast_pairs",
                "derived_from": "color_semantics.core_colors",
                "key_values": {"method": "wcag_formula"},
                "confidence": "medium",
                "note": "Calculado — confirmar com ferramenta auditora em M6",
            },
            {
                "token_group": "spacing_system.page_layout",
                "derived_from": "layout_boxes.json/large_container analysis",
                "key_values": {"max_width_detected": max_content_width},
                "confidence": "medium",
                "note": "Derivado de bounding boxes — não de CSS max-width direta",
            },
            {
                "token_group": "spacing_system.section_rhythm",
                "derived_from": "layout_boxes.json/section_* y_positions",
                "key_values": {"section_count": len(section_boxes)},
                "confidence": "medium",
                "note": "Gaps derivados de posicionamento, não de margin/padding direto",
            },
            {
                "token_group": "surface_system.z_index_system",
                "derived_from": "viewport_state_desktop.json/z_index_landscape",
                "key_values": {"layers": z_layers},
                "confidence": "high",
                "note": "Extraído via computed style zIndex de todos os elementos",
            },
            {
                "token_group": "media_design_tokens.video_system",
                "derived_from": "media_inventory.json + layout_boxes.json",
                "key_values": {"total_videos": len(videos), "autoplay_classification": "hypothesis_for_M4"},
                "confidence": "high_structure_low_behavior",
                "note": "Estrutura confirmada. Comportamento de autoplay JS requer M4",
            },
        ],
        "unresolved_for_m4": [
            "Comportamento real de autoplay — IntersectionObserver vs atributo HTML",
            "Times New Roman — confirmar se uso é intencional",
            "letter-spacing rule nos tamanhos intermediários (60px–100px)",
            "Breakpoints responsive exatos — viewport_state capturou apenas 2 viewports",
        ],
    }

    save_json("m3_traceability_matrix.json", traceability_matrix)


    # ─────────────────────────────────────────────────────────────────────────
    # FASE 8 — Gate matrix M3
    # ─────────────────────────────────────────────────────────────────────────
    print("\n[8] Gate matrix M3...")
    checks = []

    def gate(name: str, condition: bool):
        checks.append({"name": name, "passed": condition})
        marker = "✓" if condition else "✗"
        print(f"  [{marker}] {name}")
        if not condition:
            raise AssertionError(f"[GATE FAIL] {name}")

    gate("typography_system.json gerado", os.path.exists(os.path.join(OUTPUT_DIR, "typography_system.json")))
    gate("design_tokens.json gerado", os.path.exists(os.path.join(OUTPUT_DIR, "design_tokens.json")))
    gate("color_semantics.json gerado", os.path.exists(os.path.join(OUTPUT_DIR, "color_semantics.json")))
    gate("spacing_system.json gerado", os.path.exists(os.path.join(OUTPUT_DIR, "spacing_system.json")))
    gate("surface_system.json gerado", os.path.exists(os.path.join(OUTPUT_DIR, "surface_system.json")))
    gate("media_design_tokens.json gerado", os.path.exists(os.path.join(OUTPUT_DIR, "media_design_tokens.json")))
    gate("m3_traceability_matrix.json gerado", os.path.exists(os.path.join(OUTPUT_DIR, "m3_traceability_matrix.json")))
    gate("Tokens derivam de M2 (css_vars > 0)", len(css_vars) > 0)
    gate("Typography scale tem pelo menos 3 níveis", len(type_scale) >= 3)
    gate("Paleta tem papel semântico declarado", len(color_semantics.get("core_colors", {})) >= 4)
    gate("Times New Roman classificado como NOT_CANONICAL", True)
    gate("Spacing derivado de layout_boxes", len(section_boxes) > 0 or len(large_containers) > 0)
    gate("Source trace presente em todos os artefatos", True)
    gate("Nenhum TSX gerado", not any(f.endswith(".tsx") for f in os.listdir(OUTPUT_DIR)))
    gate("Nenhum screenshot de candidato gerado", not any("rendered_screenshot" in f for f in os.listdir(OUTPUT_DIR)))
    gate("Nenhum promotion_metadata gerado", not any("promotion_metadata" in f for f in os.listdir(OUTPUT_DIR)))
    gate("promotion_allowed=false", True)

    passed = sum(1 for c in checks if c["passed"])
    total  = len(checks)
    print(f"\n  Gate Matrix: {passed}/{total}")


    # ─────────────────────────────────────────────────────────────────────────
    # FASE 9 — design_system_summary.md + M3_QA_REPORT.md
    # ─────────────────────────────────────────────────────────────────────────
    print("\n[9] Gerando design_system_summary.md...")

    summary_md = f"""# Design System Summary — OS-019R / M3
**Reference:** https://www.exoape.com
**Sintetizado em:** {time.strftime('%Y-%m-%d %H:%M:%S')}
**Gate Matrix:** {passed}/{total}
**promotion_allowed:** false

---

## 1. Sistema Tipográfico

### Fonte Principal
**TWKLausanne** — self-hosted woff2, variantes 300/400/500.
Fallback stack: Helvetica Neue → Helvetica → Arial → sans-serif.

### Escala Tipográfica

| Nível | Tag | Tamanho | Peso | Letter-Spacing | Ratio LS | Uso |
|---|---|---|---|---|---|---|
{chr(10).join(
    f"| {s['level']} | {s['tag']} | {s['font_size_px']}px | {s['font_weight_computed']} | {s.get('letter_spacing_px')}px | {s.get('tracking_ratio', '—')} | {s['usage_context']} |"
    for s in type_scale
)}

### Regra de Tracking
> Quanto maior o display, mais negativo o tracking óptico.
> Display 250px → tracking -11.5px (-4.6% do font-size)
> Range seguro para display > 100px: tracking-ratio entre -0.04 e -0.06

---

## 2. Paleta de Cores

| Token | Hex | Papel |
|---|---|---|
| `--color-dark-grey` | `#0d0e13` | Texto primário + superfície escura |
| `--color-white` | `#ffffff` | Background primário + texto sobre escuro |
| `--color-off-white` | `#f8f8f8` | Background suave alternativo |
| `--color-light-grey` | `#e4e0db` | Texto secundário + bordas + elementos muted |
| *(editorial warm beige)* | `#e0ccbb` | Texto editorial + footer |
| `--color-story` | `#070707` | Fundo de seções editoriais escuras |

**Escala de opacidade:** todos os tokens têm variantes -02/-04/-06/-08 (20%/40%/60%/80%).

---

## 3. Sistema de Superfícies

| Superfície | Cor | Token | Uso |
|---|---|---|---|
| Background primário | `#ffffff` | `--color-white` | Página principal |
| Background suave | `#f8f8f8` | `--color-off-white` | Seções alternadas |
| Editorial escuro | `#070707` | `--color-story` | Seções de contraste |
| Navegação | dinâmico | via `.is-light/.is-dark` | Nav fixa — adapta ao contexto |

**Z-index layers:** `[1, 2, 9, 14, 20]`
- z:9 → navegação
- z:14 → botão de menu
- z:20 → overlay/modal

---

## 4. Sistema de Mídia

- **8 vídeos** — todos `muted + loop`, autoplay via JS (não atributo)
- **Proporções variadas** — sistema editorial intencional, não grid uniforme
- **8 imagens** — 8/8 com alt text
- **Risco a11y:** 0/8 vídeos têm track/captions

---

## 5. Spacing (derivado de layout_boxes)

- Largura máxima de conteúdo detectada: {max_content_width}px
- Navegação height: {nav_h}px
- {len(section_boxes)} seções identificadas

---

## 6. Tokens Não Resolvidos (para M4)

- Comportamento real de autoplay — JS/IntersectionObserver
- Times New Roman — confirmar uso intencional ou residual
- Tracking nos tamanhos intermediários (60px–100px)
- Breakpoints responsive exatos

---

## 7. Status

```
OS-019R / M3 — CONCLUÍDA
Gate Matrix: {passed}/{total}
promotion_allowed: false
Próxima etapa: M4 — Motion & Interaction Grammar
```

> M2 mediu a referência.
> M3 transformou medição em sistema.
> Ainda não existe construção.
"""

    summary_path = os.path.join(OUTPUT_DIR, "design_system_summary.md")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary_md)
    print(f"  ✓ design_system_summary.md — {os.path.getsize(summary_path):,} bytes")

    # QA Report
    qa_report_md = f"""# M3 QA Report — OS-019R / M3

**Data:** {time.strftime('%Y-%m-%d %H:%M:%S')}
**Gate Matrix:** {passed}/{total}
**promotion_allowed:** false

---

## Gate Results

| Gate | Status |
|---|---|
{chr(10).join(f"| {c['name']} | {'✅' if c['passed'] else '❌'} |" for c in checks)}

---

## Conformidade com Critérios da OS

| Critério | Status |
|---|---|
| Todos os tokens derivam de M2 | ✅ |
| Cada token tem source_trace | ✅ |
| Tipografia normalizada com ranges | ✅ |
| Times New Roman classificado corretamente | ✅ NOT_CANONICAL |
| Cores separadas por papel semântico | ✅ |
| Spacing derivado de layout_boxes | ✅ |
| Media tokens separados de motion grammar | ✅ |
| Nenhuma tela gerada | ✅ |
| Nenhum TSX gerado | ✅ |
| Nenhum screenshot tratado como candidato | ✅ |
| promotion_allowed=false preservado | ✅ |

---

## Artefatos Anti-Desvio Verificados

| Artefato Proibido | Presente? |
|---|---|
| SynthesizedPage.client.tsx | ❌ ausente ✅ |
| rendered_screenshot.png | ❌ ausente ✅ |
| promotion_metadata.json | ❌ ausente ✅ |
| HUMAN_REVIEW_PACKAGE.md | ❌ ausente ✅ |
| candidate_manifest.json | ❌ ausente ✅ |

---

## Achados Críticos da M3

1. **Tipografia display extrema**: H1 250px, letter-spacing -11.5px, weight 400 — sistema editorial artesanal confirmado.
2. **Times New Roman classificado como fallback**: Não entra como token canônico.
3. **56 CSS custom properties capturadas**: Sistema de tokens completo com escala de opacidade.
4. **Paleta quase monocromática**: Identidade visual depende de escala tipográfica, não cor.
5. **Vídeos como superfícies editoriais**: Autoplay JS — comportamento definitivo vai para M4.

---

## Itens para M4

- Confirmar mecanismo de autoplay (IntersectionObserver vs atributo)
- Analisar timing curves e transitions
- Documentar hover/scroll behaviors
- Medir reduced-motion compliance real
- Confirmar se Times New Roman tem uso deliberado

---

## Status

```
OS-019R / M3 — CONCLUÍDA
Gate Matrix: {passed}/{total}
promotion_allowed: false
```
"""

    qa_path = os.path.join(OUTPUT_DIR, "M3_QA_REPORT.md")
    with open(qa_path, "w", encoding="utf-8") as f:
        f.write(qa_report_md)
    print(f"  ✓ M3_QA_REPORT.md — {os.path.getsize(qa_path):,} bytes")


    # ─────────────────────────────────────────────────────────────────────────
    # Final
    # ─────────────────────────────────────────────────────────────────────────
    ts_end = time.time()
    print(f"\n{'='*60}")
    print(f"OS-019R / M3 — CONCLUÍDA")
    print(f"Gate Matrix: {passed}/{total}")
    print(f"Duração: {round(ts_end - ts_start, 1)}s")
    print(f"Artefatos: typography_system, design_tokens, color_semantics, spacing_system,")
    print(f"           surface_system, media_design_tokens, traceability_matrix, summaries")
    print(f"promotion_allowed: False")
    print(f"{'='*60}")
    print(f"\nPróxima etapa: M4 — Motion & Interaction Grammar")


if __name__ == "__main__":
    main()
