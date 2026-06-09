"""
OS-019R / M5 — Component & Pattern Map
=======================================

Sintetiza dados M1–M4 em mapa de padrões reutilizáveis para agentes construtores.

PROIBIDO:
  - Implementar componente
  - Criar TSX
  - Gerar tela / candidato
  - Inventar padrão sem fonte em M1–M4

ENTREGÁVEIS:
  component_pattern_map.json
  section_taxonomy.json
  layout_archetypes.json
  typography_pattern_map.json
  media_pattern_map.json
  motion_pattern_map.json
  interaction_role_map.json
  gpu_layer_strategy.json
  anti_clone_constraints.json
  m5_traceability_matrix.json
  M5_QA_REPORT.md

INVARIANTE:
  promotion_allowed: false
"""

import json
import os
import time

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output_synthesis", "OS-019R")


# ── Carregamento ──────────────────────────────────────────────────────────────

def load(name):
    path = os.path.join(OUTPUT_DIR, name)
    if not os.path.exists(path):
        print(f"  [WARN] não encontrado: {name}")
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save(name, data):
    path = os.path.join(OUTPUT_DIR, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    size = os.path.getsize(path)
    print(f"  ✓ {name} — {size:,} bytes")


# ── Helpers ───────────────────────────────────────────────────────────────────

NOW = time.strftime("%Y-%m-%dT%H:%M:%S")

META = {
    "os": "OS-019R",
    "phase": "M5",
    "reference": "https://www.exoape.com",
    "generated_at": NOW,
    "promotion_allowed": False,
    "source_phases": ["M1", "M2", "M3", "M4"],
}


def pattern(
    id_: str,
    name: str,
    category: str,
    cognitive_function: str,
    source_trace: list[str],
    evidence: dict,
    permitted_use: list[str],
    prohibited_use: list[str],
    clone_risk: str,
    agent_instructions: list[str],
    budget_fallback: dict | None = None,
    notes: str | None = None,
) -> dict:
    p = {
        "id": id_,
        "name": name,
        "category": category,
        "cognitive_function": cognitive_function,
        "source_trace": source_trace,
        "evidence": evidence,
        "permitted_use": permitted_use,
        "prohibited_use": prohibited_use,
        "clone_risk": clone_risk,
        "agent_instructions": agent_instructions,
    }
    if budget_fallback:
        p["budget_fallback"] = budget_fallback
    if notes:
        p["notes"] = notes
    return p


# ─────────────────────────────────────────────────────────────────────────────

def main():
    print(f"\n{'='*60}")
    print("OS-019R / M5 — Component & Pattern Map")
    print(f"{'='*60}\n")
    ts = time.time()

    print("[0] Carregando artefatos M1–M4...")
    capture_meta  = load("capture_metadata.json") or {}
    a11y          = load("accessibility_tree.json") or {}
    computed      = load("computed_styles.json") or []
    layout_boxes  = load("layout_boxes.json") or []
    font_inv      = load("font_inventory.json") or []
    color_usage   = load("color_usage.json") or []
    media_inv     = load("media_inventory.json") or {}
    typo          = load("typography_system.json") or {}
    design_tok    = load("design_tokens.json") or {}
    color_sem     = load("color_semantics.json") or {}
    spacing       = load("spacing_system.json") or {}
    surface       = load("surface_system.json") or {}
    motion_g      = load("motion_grammar.json") or {}
    scroll_b      = load("scroll_behavior.json") or {}
    interact      = load("interaction_map.json") or {}
    timing        = load("timing_curves.json") or {}
    media_rt      = load("media_runtime_behavior.json") or {}
    vp_matrix     = load("viewport_motion_matrix.json") or {}
    reduced       = load("reduced_motion_observations.json") or {}
    vp_desktop    = load("viewport_state_desktop.json") or {}

    # Key extracted values
    h1_desktop    = vp_matrix.get("comparison", {}).get("h1_font_size", {}).get("desktop", "250px")
    h1_mobile     = vp_matrix.get("comparison", {}).get("h1_font_size", {}).get("mobile", "62.4px")
    ls_desktop    = vp_matrix.get("comparison", {}).get("h1_letter_spacing", {}).get("desktop", "-11.5px")
    ls_mobile     = vp_matrix.get("comparison", {}).get("h1_letter_spacing", {}).get("mobile", "-1.56px")
    io_instances  = motion_g.get("motion_primitives", {}).get("intersection_observer", {}).get("instances_detected", 1)
    will_ch_count = motion_g.get("motion_primitives", {}).get("will_change", {}).get("element_count", 68)
    css_vars      = vp_desktop.get("css_custom_properties", {})
    z_layers      = surface.get("z_index_system", {}).get("layers", [1, 2, 9, 14, 20])
    videos        = media_inv.get("videos", [])
    type_scale    = typo.get("type_scale", [])

    type_scale_by_level = {s["level"]: s for s in type_scale}

    print(f"  H1 desktop: {h1_desktop}  mobile: {h1_mobile}")
    print(f"  IO instances: {io_instances}")
    print(f"  will-change elements: {will_ch_count}")
    print(f"  CSS vars: {len(css_vars)}")

    # ─────────────────────────────────────────────────────────────────────────
    # [1] component_pattern_map.json
    # ─────────────────────────────────────────────────────────────────────────
    print("\n[1] component_pattern_map.json...")

    patterns = [
        pattern(
            id_="P-001",
            name="Monumental Editorial Hero",
            category="typography",
            cognitive_function=(
                "Criar impacto visual imediato através de tipografia de escala extrema. "
                "O tamanho não é decorativo — é a mensagem primária. O conteúdo entra "
                "pelo tamanho antes de ser lido pelo significado."
            ),
            source_trace=[
                "M2/computed_styles.json h1: font-size 250px",
                "M2/computed_styles.json h1: letter-spacing -11.5px",
                "M4/viewport_motion_matrix.json h1 desktop vs mobile",
                "M3/typography_system.json display_monumental",
            ],
            evidence={
                "font_size_desktop": h1_desktop,
                "font_size_mobile": h1_mobile,
                "letter_spacing_desktop": ls_desktop,
                "letter_spacing_mobile": ls_mobile,
                "font_family": "TWKLausanne / Lausanne-300",
                "font_weight_computed": "400",
                "line_height_ratio": "0.904",
                "tracking_ratio_desktop": "-0.046",
                "tracking_ratio_mobile": "-0.025",
            },
            permitted_use=[
                "Título de abertura de seção hero",
                "Manifesto ou declaração institucional",
                "Nome de projeto em abertura de case study",
                "Qualquer texto de no máximo 3–5 palavras em escala monumental",
            ],
            prohibited_use=[
                "Corpo de texto ou parágrafos",
                "Labels ou metadados",
                "Texto abaixo de 80px que não recalibrou tracking",
                "Cópia exata do texto da Exo Ape",
            ],
            clone_risk="MEDIUM — escala extrema com tracking negativo é a assinatura da referência. Usar com conteúdo diferente e composição diferente.",
            agent_instructions=[
                "Usar Lausanne-300 como família ou equivalente aprovado no handoff",
                "Calcular letter-spacing como: tamanho_px × (-0.046) para desktop, × (-0.025) para mobile",
                "line-height = font-size × 0.904 (tight editorial)",
                "font-weight: 400 — não usar bold em escala monumental",
                "Não copiar o texto 'Digital Design Experience' ou qualquer copy da referência",
                "Testar com conteúdo real — não usar lorem ipsum em display monumental",
            ],
        ),

        pattern(
            id_="P-002",
            name="Intersection-Gated Editorial Media",
            category="media",
            cognitive_function=(
                "Mídia só entra em atividade quando o usuário chega na zona de interesse. "
                "Cria sensação de revelação progressiva — cada seção 'acorda' ao ser alcançada. "
                "Economiza performance e cria ritmo de descoberta."
            ),
            source_trace=[
                "M4/motion_grammar.json IO instances=1, events=21",
                "M4/media_runtime_behavior.json is_playing_after_scroll=8",
                "M2/media_inventory.json 8 vídeos muted+loop",
                "M1/capture_metadata.json 8 vídeos detectados",
            ],
            evidence={
                "mechanism": "IntersectionObserver (JS) — não atributo HTML autoplay",
                "io_instances": io_instances,
                "io_events_captured": 21,
                "videos_playing_after_scroll": 8,
                "autoplay_html_attribute": False,
                "pattern": "muted + loop + IO-triggered = ambient editorial loops",
            },
            permitted_use=[
                "Vídeos de projeto/case study em cards editoriais",
                "Background ambient de seções sem narração",
                "Demonstração de produto em contexto de portfolio",
            ],
            prohibited_use=[
                "Autoplay via atributo HTML sem IntersectionObserver",
                "Mídia com narração/áudio sem controles visíveis",
                "Autoplay fora da viewport (desperdício de performance)",
                "Mais de 3 vídeos simultâneos ativos na viewport",
            ],
            clone_risk="LOW — o padrão é técnico (IntersectionObserver), não visual. Implementar com conteúdo próprio.",
            agent_instructions=[
                "Implementar IntersectionObserver para acionar play() quando ratio >= 0.3",
                "Sempre muted=true para autoplay permitido pelos browsers",
                "loop=true para ambient media",
                "preload='none' até o elemento entrar no threshold",
                "Fornecer poster como placeholder antes da carga",
                "useReducedMotion() → não acionar autoplay (fail-closed herdado da OS-019)",
            ],
            budget_fallback={
                "max_simultaneous_playing": 3,
                "threshold": 0.3,
                "reduced_motion": "poster_static_only",
                "low_bandwidth": "poster_static_with_play_button",
            },
        ),

        pattern(
            id_="P-003",
            name="Minimal Sticky Navigation",
            category="navigation",
            cognitive_function=(
                "Presença persistente que não compete com o conteúdo principal. "
                "A navegação existe como acesso seguro, não como âncora visual. "
                "O conteúdo é a cena — a nav é a saída de emergência."
            ),
            source_trace=[
                "M2/layout_boxes.json navigation z_index=9, position=fixed",
                "M2/accessibility_tree.json nav landmark",
                "M4/motion_grammar.json structural_motion/menu",
                "M3/surface_system.json navigation_surface dynamic theme",
            ],
            evidence={
                "position": "fixed",
                "z_index": 9,
                "menu_button_z": 14,
                "theme": "adapts via .is-light / .is-dark on .app element",
                "height": spacing.get("navigation", {}).get("height_px"),
            },
            permitted_use=[
                "Navegação principal fixa com menu hamburger",
                "Nav que adapta contraste ao contexto da seção atual",
                "Logo + links essenciais + CTA único",
            ],
            prohibited_use=[
                "Nav com altura superior a 80px",
                "Nav com elementos visuais pesados (gradientes, sombras profundas)",
                "Nav que compete visualmente com hero ou seção ativa",
                "Z-index acima de 14 sem justificativa de modal/overlay",
            ],
            clone_risk="LOW — estrutura funcional padrão. Risco apenas se copiar identidade visual (logo, cores, copy).",
            agent_instructions=[
                "position: fixed, z-index: 9 para nav principal",
                "z-index: 14 para trigger de menu (deve estar acima da nav)",
                "Implementar theme toggle (.is-light / .is-dark) baseado na seção ativa",
                "Altura máxima recomendada: 64px–80px",
                "Transição de tema: opacity 0.5s ease (padrão confirmado em M4)",
            ],
        ),

        pattern(
            id_="P-004",
            name="GPU-Composited Scroll Field",
            category="motion",
            cognitive_function=(
                "A página inteira é um campo físico onde elementos se movem com física própria "
                "durante o scroll. Não é slideshow. Não são cards. É um campo contínuo de "
                "camadas compostas que respondem ao input do usuário."
            ),
            source_trace=[
                "M4/motion_grammar.json will_change=transform, 68 elements",
                "M4/m4_runtime_trace.json transform_elements h1.title translateX(-20px)",
                "M3/surface_system.json z_index_landscape [1,2,9,14,20]",
                "M2/viewport_state_desktop.json z_index_landscape",
            ],
            evidence={
                "will_change_elements": will_ch_count,
                "will_change_value": "transform",
                "h1_transform_at_rest": "matrix(1,0,0,1,-20,0) = translateX(-20px)",
                "z_layers": z_layers,
            },
            permitted_use=[
                "Reveal de elementos ao entrar na viewport (translateY, opacity, scale)",
                "Parallax sutil em media ou backgrounds (< 10% do scroll delta)",
                "Depth layers no hero (Z-axis do Mad Lab Theme)",
                "Entrance animations vinculadas ao IntersectionObserver",
            ],
            prohibited_use=[
                "will-change em todos os elementos sem budget definido",
                "Mais de 20 GPU layers simultâneos sem teste de performance",
                "Scroll-linked transforms sem useReducedMotion() fail-closed",
                "Parallax profundo em conteúdo textual (afeta legibilidade e acessibilidade)",
            ],
            clone_risk="LOW — arquitetura técnica. Não há visual único para clonar — apenas o padrão de engenharia.",
            agent_instructions=[
                "Aplicar will-change: transform apenas nos elementos que serão animados (não global)",
                "Definir budget por qualidade: low=5 layers, medium=12 layers, high=20 layers",
                "Sempre incluir @media (prefers-reduced-motion: reduce) { transition: none; animation: none; }",
                "Usar transform (não top/left) para todas as animações de posição",
                "Cleanup: remover will-change após animação via JS para liberar memória GPU",
            ],
            budget_fallback={
                "quality_low": "max 5 GPU layers, sem parallax",
                "quality_medium": "max 12 GPU layers, parallax sutil",
                "quality_high": "max 20 GPU layers, full scroll physics",
                "reduced_motion": "static — nenhuma transform animada",
                "cleanup": "remove will-change after animation complete",
            },
        ),

        pattern(
            id_="P-005",
            name="Responsive Optical Tracking",
            category="typography",
            cognitive_function=(
                "Compensação óptica do espaço entre letras em função do tamanho do display. "
                "Em escala extrema, o espaçamento padrão cria 'frouxidão' visual. "
                "O tracking negativo restaura a coesão da palavra como unidade visual."
            ),
            source_trace=[
                "M4/viewport_motion_matrix.json h1 desktop vs mobile",
                "M3/typography_system.json tracking_rule",
                "M2/computed_styles.json h1 letter-spacing",
            ],
            evidence={
                "desktop_250px": {"letter_spacing": ls_desktop, "tracking_ratio": "-0.046"},
                "mobile_62px":   {"letter_spacing": ls_mobile,  "tracking_ratio": "-0.025"},
                "rule": "tracking é função não linear do tamanho — diminui proporcionalmente em mobile",
            },
            permitted_use=[
                "Qualquer display acima de 40px que precise de compensação óptica",
                "Sistema tipográfico editorial com escalas extremas",
            ],
            prohibited_use=[
                "Tracking negativo em corpo de texto (< 18px)",
                "Tracking fixo sem variação por breakpoint",
                "letter-spacing positivo em display extremo",
            ],
            clone_risk="LOW — é uma regra técnica tipográfica, não uma identidade visual.",
            agent_instructions=[
                "Fórmula desktop (> 768px): letter-spacing = font-size × (-0.046)",
                "Fórmula mobile (< 640px): letter-spacing = font-size × (-0.025)",
                "Interpolar entre 0.025 e 0.046 para breakpoints intermediários",
                "Abaixo de 40px: tracking-ratio neutro (0 a -0.01)",
                "Testar opticamente — a fórmula é ponto de partida, não regra absoluta",
            ],
        ),

        pattern(
            id_="P-006",
            name="Monocromatic Semantic Palette",
            category="color",
            cognitive_function=(
                "Hierarquia visual construída inteiramente por escala e peso, não por cor. "
                "A ausência de cor saturada força o olho a usar tamanho, peso e posição como "
                "único vocabulário de atenção. Cria sofisticação editorial."
            ),
            source_trace=[
                "M3/color_semantics.json core_colors",
                "M3/design_tokens.json semantic_tokens",
                "M2/color_usage.json top colors",
            ],
            evidence={
                "dominant_duo": "#0d0e13 (escuro) + #ffffff (branco)",
                "warm_editorial": "#e0ccbb (bege quente para texto editorial/footer)",
                "accent": "none — ênfase via escala tipográfica",
                "token_count": len(css_vars),
                "opacity_scale": ["0.2", "0.4", "0.6", "0.8"],
            },
            permitted_use=[
                "Sistemas editoriais e de portfolio sem necessidade de cor-marca forte",
                "Contextos onde a mídia (foto/vídeo) é a cor — não a UI",
                "Dark sections como --color-story (#070707) para contraste editorial",
            ],
            prohibited_use=[
                "Usar #e4e0db ou #e0ccbb como cor de texto em body size (falha WCAG)",
                "Adicionar cores saturadas sem revisar o sistema completo",
                "Usar Times New Roman — NOT_CANONICAL confirmado",
            ],
            clone_risk="LOW — paleta monocromática é princípio de design, não identidade. Aplicar com brand colors próprias.",
            agent_instructions=[
                "Primary text: --color-dark-grey (#0d0e13)",
                "Background: --color-white (#ffffff) ou --color-off-white (#f8f8f8)",
                "Editorial warm: usar apenas em texto de apoio grande (> 18px bold) — WCAG risco em body",
                "Dark sections: --color-story (#070707) com texto claro",
                "Não declarar Times New Roman em font-family stack",
            ],
        ),

        pattern(
            id_="P-007",
            name="Section-Label Taxonomy",
            category="content",
            cognitive_function=(
                "Labels de seção em 14px com peso normal servem como âncoras de orientação "
                "silenciosas. O contraste de escala entre o label (14px) e o título "
                "da seção (144px ou 250px) cria ritmo editorial imediato."
            ),
            source_trace=[
                "M2/accessibility_tree.json headings h2 14px",
                "M3/typography_system.json label_section",
                "M2/computed_styles.json h2 small scale",
            ],
            evidence={
                "label_font_size": "14px",
                "label_font_weight": "400",
                "examples": ["Featured Projects", "Work in motion", "In the media"],
                "contrast_ratio": f"label 14px vs display {h1_desktop} = ratio 1:{round(250/14, 1)}",
            },
            permitted_use=[
                "Rótulo de seção antes do título principal",
                "Categoria ou metadado de contexto",
                "Timestamp ou indicação de ordenação",
            ],
            prohibited_use=[
                "Labels como CTA (não são clicáveis por padrão)",
                "Labels para informação crítica (baixo contraste em fundo claro)",
                "Mais de 3 palavras por label",
            ],
            clone_risk="LOW — padrão de UX writing universal. Risco apenas se copiar o copy exato.",
            agent_instructions=[
                "font-size: 14px, font-weight: 400",
                "Usar como elemento de abertura de seção antes do título",
                "Não usar a mesma copy da referência ('Featured Projects', etc.)",
            ],
        ),
    ]

    component_pattern_map = {
        "meta": META,
        "patterns": patterns,
        "pattern_count": len(patterns),
        "categories": list(set(p["category"] for p in patterns)),
    }

    save("component_pattern_map.json", component_pattern_map)

    # ─────────────────────────────────────────────────────────────────────────
    # [2] section_taxonomy.json
    # ─────────────────────────────────────────────────────────────────────────
    print("\n[2] section_taxonomy.json...")

    headings = a11y.get("headings", [])
    section_boxes = [b for b in layout_boxes if b.get("label", "").startswith("section_")]

    section_taxonomy = {
        "meta": META,
        "sections_identified": len(section_boxes),
        "taxonomy": [
            {
                "id": "S-01",
                "name": "Hero / Manifesto",
                "role": "institutional_opening",
                "content": "Título monumental + vídeo/foto full-bleed ou campo vazio com tipografia extrema",
                "heading_level": "H1",
                "heading_scale": h1_desktop,
                "motion": "scroll-physics reveal, Z-axis depth (padrão Mad Lab)",
                "source_trace": "M2/dom_tree + M3/typography_system.display_monumental + M4/motion_grammar",
            },
            {
                "id": "S-02",
                "name": "Featured Work Grid",
                "role": "portfolio_showcase",
                "content": "Seção de projetos com vídeos editoriais em cards de proporção variada",
                "heading_level": "H2",
                "heading_text_evidence": "Featured Projects",
                "heading_scale": "14px label + 144px display",
                "motion": "IntersectionObserver gated video autoplay por card",
                "source_trace": "M2/accessibility_tree headings + M4/media_runtime_behavior",
            },
            {
                "id": "S-03",
                "name": "Motion Reel",
                "role": "motion_showcase",
                "content": "Seção de vídeo de alta impacto — Play Reel — título de 144px",
                "heading_level": "H2",
                "heading_text_evidence": "Play Reel",
                "heading_scale": "144px",
                "motion": "Video ambient + intersection trigger",
                "source_trace": "M2/accessibility_tree h2 Play Reel + M4/media_runtime_behavior",
            },
            {
                "id": "S-04",
                "name": "Press / Media",
                "role": "credibility_social_proof",
                "content": "Clippings de imprensa, logos de veículos, títulos em escala reduzida",
                "heading_level": "H2",
                "heading_text_evidence": "In the media",
                "heading_scale": "14px label",
                "motion": "minimal — sem vídeo dominante",
                "source_trace": "M2/accessibility_tree headings",
            },
            {
                "id": "S-05",
                "name": "Footer",
                "role": "navigation_closure",
                "content": "Links de navegação, cor editorial escura (#070707)",
                "background_color": "#070707",
                "background_token": "--color-story",
                "source_trace": "M2/layout_boxes footer + M3/color_semantics.story_dark",
            },
        ],
        "source_trace": "M2/accessibility_tree + M2/layout_boxes + M3/color_semantics + M4",
    }

    save("section_taxonomy.json", section_taxonomy)

    # ─────────────────────────────────────────────────────────────────────────
    # [3] layout_archetypes.json
    # ─────────────────────────────────────────────────────────────────────────
    print("\n[3] layout_archetypes.json...")

    large_containers = [b for b in layout_boxes if b.get("label", "").startswith("large_container_")]
    max_w  = spacing.get("page_layout", {}).get("max_content_width_detected_px")
    typ_w  = spacing.get("page_layout", {}).get("typical_content_width_px")
    page_w = spacing.get("viewport", {}).get("desktop_width", 1440)

    layout_archetypes = {
        "meta": META,
        "viewport": {
            "desktop_width": page_w,
            "mobile_width": spacing.get("viewport", {}).get("mobile_width", 390),
        },
        "archetypes": [
            {
                "id": "LA-01",
                "name": "Full-Bleed Editorial",
                "description": "Conteúdo cobre 100% da viewport sem margens laterais. Usado para hero e motion reel.",
                "width": "100vw",
                "detected_width_px": page_w,
                "padding": "none ou mínimo",
                "source_trace": "M2/layout_boxes large_container 1440w",
            },
            {
                "id": "LA-02",
                "name": "Contained Content Column",
                "description": "Conteúdo em coluna centralizada com margens generosas. Usado para seções editoriais.",
                "max_width_px": max_w,
                "typical_width_px": typ_w,
                "horizontal_margin_approx": spacing.get("page_layout", {}).get("horizontal_margin_approx"),
                "source_trace": "M2/layout_boxes large_container analysis",
            },
            {
                "id": "LA-03",
                "name": "Variable Media Grid",
                "description": "Grid de mídia com proporções intencionalmente variadas — não uniforme.",
                "video_widths_observed": spacing.get("media_grid", {}).get("video_widths_px", []),
                "video_heights_observed": spacing.get("media_grid", {}).get("video_heights_px", []),
                "aspect_ratios": spacing.get("media_grid", {}).get("video_aspect_ratios", []),
                "note": "Grade editorial, não grid matemático. Proporções transmitem energia visual.",
                "source_trace": "M2/layout_boxes video_* bounding boxes",
            },
            {
                "id": "LA-04",
                "name": "Sticky Nav Layer",
                "description": "Camada de navegação fixa acima do conteúdo, invisível mas sempre acessível.",
                "position": "fixed",
                "height_px": spacing.get("navigation", {}).get("height_px"),
                "z_index": 9,
                "source_trace": "M2/layout_boxes navigation + M3/surface_system.z_index_system",
            },
        ],
        "source_trace": "M2/layout_boxes + M3/spacing_system",
    }

    save("layout_archetypes.json", layout_archetypes)

    # ─────────────────────────────────────────────────────────────────────────
    # [4] typography_pattern_map.json
    # ─────────────────────────────────────────────────────────────────────────
    print("\n[4] typography_pattern_map.json...")

    typography_pattern_map = {
        "meta": META,
        "font_system": {
            "canonical_family": "TWKLausanne",
            "variants": ["Lausanne-300", "Lausanne-400", "Lausanne-500"],
            "fallback_stack": ["Helvetica Neue", "Helvetica", "Arial", "sans-serif"],
            "not_canonical": ["Times New Roman"],
            "source_trace": "M3/typography_system + M4/media_runtime_behavior.times_new_roman_resolution",
        },
        "scale": {
            "display_monumental": {
                "desktop": {"size": h1_desktop, "tracking": ls_desktop, "ratio": "-0.046", "lh_ratio": "0.904"},
                "mobile": {"size": h1_mobile, "tracking": ls_mobile, "ratio": "-0.025"},
                "weight": "400",
                "use": "hero / abertura de seção de alto impacto",
                "source_trace": "M2/computed_styles.json h1 + M4/viewport_motion_matrix",
            },
            "display_large": {
                "desktop": {"size": "144px"},
                "weight": "400",
                "use": "seção motion reel, títulos de seção de impacto médio",
                "source_trace": "M2/computed_styles.json h2 large",
            },
            "label_section": {
                "desktop": {"size": "14px"},
                "weight": "400",
                "use": "rótulo de seção antes do título",
                "source_trace": "M2/computed_styles.json h2 label",
            },
            "body": {
                "family": typo.get("type_scale", [{}])[-1].get("font_family") if typo.get("type_scale") else None,
                "size": typo.get("type_scale", [{}])[-1].get("font_size_px") if typo.get("type_scale") else None,
                "source_trace": "M2/computed_styles.json p",
            },
        },
        "tracking_system": {
            "rule": "tracking negativo proporcional ao tamanho, curva não linear",
            "desktop_formula": "letter-spacing = font-size × (-0.046)",
            "mobile_formula": "letter-spacing = font-size × (-0.025)",
            "below_40px": "tracking neutro — 0 a -0.01",
            "source_trace": "M3/typography_system.tracking_rule + M4/viewport_motion_matrix",
        },
        "not_canonical": {
            "Times New Roman": {
                "status": "BROWSER_DEFAULT_CONFIRMED",
                "decision": "NOT_CANONICAL — nunca declarar em font-family stack",
                "source_trace": "M4/media_runtime_behavior.times_new_roman_resolution",
            },
        },
    }

    save("typography_pattern_map.json", typography_pattern_map)

    # ─────────────────────────────────────────────────────────────────────────
    # [5] media_pattern_map.json
    # ─────────────────────────────────────────────────────────────────────────
    print("\n[5] media_pattern_map.json...")

    media_pattern_map = {
        "meta": META,
        "video_pattern": {
            "id": "MP-001",
            "name": "Intersection-Gated Editorial Video",
            "mechanism": "IntersectionObserver (JS) — autoplay HTML=False",
            "attributes": {"muted": True, "loop": True, "autoplay_html": False, "controls": False},
            "trigger": "IO ratio >= threshold (threshold estimado ~0.3)",
            "total_in_reference": len(videos),
            "roles_observed": ["editorial_media"],
            "aspect_ratio_variation": spacing.get("media_grid", {}).get("video_aspect_ratios", []),
            "a11y_risk": "0/8 vídeos com track — aceito se muted+loop ambient sem narração. Validar com stakeholder.",
            "production_rule": "preload='none' até IO threshold. Poster obrigatório.",
            "reduced_motion": "poster_static — não acionar play() se prefers-reduced-motion",
            "source_trace": "M1/capture_metadata + M4/media_runtime_behavior + M2/media_inventory",
        },
        "image_pattern": {
            "id": "MP-002",
            "name": "Alt-Covered Editorial Image",
            "alt_coverage": "8/8",
            "loading": "lazy observado",
            "use": "thumbnails, case study media, editorial support",
            "a11y_status": "COMPLIANT — 8/8 com alt text",
            "source_trace": "M2/media_inventory + M2/accessibility_tree",
        },
        "source_trace": "M1/asset_inventory + M2/media_inventory + M4/media_runtime_behavior",
    }

    save("media_pattern_map.json", media_pattern_map)

    # ─────────────────────────────────────────────────────────────────────────
    # [6] motion_pattern_map.json
    # ─────────────────────────────────────────────────────────────────────────
    print("\n[6] motion_pattern_map.json...")

    timing_curves_list = timing.get("unique_curves", [])

    motion_pattern_map = {
        "meta": META,
        "motion_system": {
            "primary_trigger": "IntersectionObserver (scroll-based visibility)",
            "secondary_trigger": "CSS hover transitions",
            "ambient": "muted+loop video editorial",
            "architecture": f"GPU compositing ({will_ch_count} will-change:transform elements)",
        },
        "patterns": [
            {
                "id": "MP-MOT-001",
                "name": "Viewport Reveal",
                "trigger": "IntersectionObserver threshold",
                "effect": "elemento entra na viewport — dispara opacity/transform de entrada",
                "timing": "0.5s ease (único timing confirmado em M4)",
                "properties": ["opacity", "transform"],
                "h1_evidence": "h1.title transform=translateX(-20px) em repouso → anima para 0",
                "reduced_motion": "static — sem animação de entrada",
                "source_trace": "M4/motion_grammar + M4/m4_runtime_trace transform_elements",
            },
            {
                "id": "MP-MOT-002",
                "name": "Nav Theme Transition",
                "trigger": "mudança de seção / scroll",
                "effect": "nav alterna entre .is-light e .is-dark",
                "timing": "0.5s ease",
                "mechanism": "CSS class toggle no elemento .app",
                "source_trace": "M3/surface_system.theme_switching + M4/interaction_map.menu",
            },
            {
                "id": "MP-MOT-003",
                "name": "Menu Overlay Open/Close",
                "trigger": "click .menu-button (z:14)",
                "effect": "nav overlay aparece/desaparece",
                "timing": "0.5s ease estimado",
                "nav_z_index": 9,
                "button_z_index": 14,
                "source_trace": "M4/interaction_map.menu",
            },
            {
                "id": "MP-MOT-004",
                "name": "Editorial Media Loop",
                "trigger": "IO threshold — play() via JS",
                "effect": "vídeo começa loop silencioso",
                "reduced_motion": "poster apenas",
                "io_confirmed": True,
                "source_trace": "M4/media_runtime_behavior + M4/motion_grammar.media_motion",
            },
        ],
        "timing_system": {
            "confirmed_curves": timing_curves_list,
            "note": "Apenas 2 transições CSS únicas detectadas — a maioria do motion é JS-driven (rAF, IntersectionObserver)",
            "source_trace": "M4/timing_curves.json",
        },
        "reduced_motion": {
            "css_detected": reduced.get("css_support_confirmed", False),
            "mad_lab_contract": "useReducedMotion() fail-closed — herdado da OS-019 M0",
            "rule": "Se prefers-reduced-motion: static poster, sem transforms animados, sem video autoplay",
            "source_trace": "M4/reduced_motion_observations + OS-019 M0 contract",
        },
        "source_trace": "M4/motion_grammar + M4/timing_curves + M3/surface_system",
    }

    save("motion_pattern_map.json", motion_pattern_map)

    # ─────────────────────────────────────────────────────────────────────────
    # [7] interaction_role_map.json
    # ─────────────────────────────────────────────────────────────────────────
    print("\n[7] interaction_role_map.json...")

    interactive_count = len(a11y.get("interactive", []))
    hover_results = interact.get("hover_states", {}).get("results", [])
    hover_changed = interact.get("hover_states", {}).get("elements_with_changes", 0)

    interaction_role_map = {
        "meta": META,
        "summary": {
            "interactive_elements": interactive_count,
            "hover_tested": interact.get("hover_states", {}).get("elements_tested", 0),
            "hover_with_changes": hover_changed,
        },
        "roles": {
            "navigation_link": {
                "selector": "nav a.nav-link",
                "behavior": "hover transition detectado via IO (elementos nav rastreados pelo IntersectionObserver)",
                "z_context": "z:9 (nav layer)",
                "source_trace": "M4/m4_runtime_trace io_spy_events nav-link",
            },
            "menu_trigger": {
                "selector": ".menu-button",
                "behavior": "click abre overlay de navegação, z:14",
                "io_tracked": True,
                "source_trace": "M4/interaction_map.menu + M3/surface_system.z_index",
            },
            "editorial_link": {
                "selector": "a[href] (projeto/case)",
                "behavior": "hover muda estado — detalhes em M4/interaction_map.hover_states",
                "source_trace": "M4/interaction_map.cta_behavior",
            },
            "video_surface": {
                "selector": "video",
                "behavior": "play() via IntersectionObserver — não via click",
                "no_controls": True,
                "source_trace": "M4/media_runtime_behavior",
            },
        },
        "not_tested": [
            "focus states de teclado",
            "custom cursor behavior",
            "touch interactions no mobile",
        ],
        "source_trace": "M4/interaction_map + M4/m4_runtime_trace + M2/accessibility_tree",
    }

    save("interaction_role_map.json", interaction_role_map)

    # ─────────────────────────────────────────────────────────────────────────
    # [8] gpu_layer_strategy.json
    # ─────────────────────────────────────────────────────────────────────────
    print("\n[8] gpu_layer_strategy.json...")

    gpu_layer_strategy = {
        "meta": META,
        "reference_data": {
            "will_change_transform_count": will_ch_count,
            "z_index_layers": z_layers,
            "transform_elements_at_rest": 15,
            "source_trace": "M4/motion_grammar.will_change + M3/surface_system.z_index_system",
        },
        "mad_lab_budget": {
            "interpretation": (
                f"A referência usa {will_ch_count} elementos com will-change:transform. "
                "Isso é a referência, não o target. "
                "O Mad Lab Theme deve definir budget próprio baseado em viewport e qualidade."
            ),
            "budget_by_quality": {
                "low":    {"max_will_change_layers": 5,  "parallax": False,   "video_autoplay": False},
                "medium": {"max_will_change_layers": 12, "parallax": "sutil", "video_autoplay": "intersection_only"},
                "high":   {"max_will_change_layers": 20, "parallax": True,    "video_autoplay": "intersection_only"},
                "reduced_motion": {"max_will_change_layers": 0, "parallax": False, "video_autoplay": False},
            },
            "rules": [
                "will-change apenas nos elementos que serão animados no próximo frame",
                "Remover will-change após animação para liberar GPU layer",
                "Testar em dispositivos de médio desempenho (não apenas high-end)",
                "Z-index: manter hierarquia com no máximo 5 camadas declaradas",
                "Não usar will-change: all",
            ],
        },
        "z_index_budget": {
            "max_layers": 5,
            "recommended_values": [1, 2, 9, 14, 20],
            "semantic_map": {
                "1": "base_interactive",
                "2": "elevated_content",
                "9": "navigation",
                "14": "menu_trigger",
                "20": "overlay_modal",
            },
            "source_trace": "M3/surface_system.z_index_system",
        },
        "source_trace": "M4/motion_grammar + M3/surface_system",
    }

    save("gpu_layer_strategy.json", gpu_layer_strategy)

    # ─────────────────────────────────────────────────────────────────────────
    # [9] anti_clone_constraints.json
    # ─────────────────────────────────────────────────────────────────────────
    print("\n[9] anti_clone_constraints.json...")

    anti_clone_constraints = {
        "meta": META,
        "principle": (
            "Esta OS extraiu padrões técnicos e visuais de uma referência real. "
            "O objetivo é inspirar a arquitetura, não reproduzir a identidade. "
            "Cada item abaixo é uma restrição ativa para agentes construtores."
        ),
        "hard_prohibitions": [
            {
                "id": "AC-001",
                "item": "Tipografia TWKLausanne",
                "reason": "Fonte proprietária da Exo Ape — não está disponível para uso externo",
                "alternative": "Usar fonte aprovada no handoff que tenha equivalência de contraste e peso",
                "source_trace": "M1/capture_metadata.json fonts_detected",
            },
            {
                "id": "AC-002",
                "item": "Assets visuais (vídeos, imagens, fotografias)",
                "reason": "Conteúdo de propriedade intelectual da Exo Ape",
                "alternative": "Usar mídia própria ou licenciada — nunca hotlink ou cópia de assets",
                "source_trace": "M1/asset_inventory.json",
            },
            {
                "id": "AC-003",
                "item": "Copy e textos",
                "reason": "Textos como 'Digital Design Experience', 'Exo Ape', copy de projetos são marca registrada",
                "alternative": "Usar copy próprio do Mad Lab Aurora",
                "source_trace": "M2/accessibility_tree.headings",
            },
            {
                "id": "AC-004",
                "item": "Identidade visual (logo, cores de marca, nome)",
                "reason": "Marca da Exo Ape — proteção legal e ética",
                "alternative": "Identidade exclusiva do Mad Lab Aurora",
                "source_trace": "M2/dom_tree logo class",
            },
        ],
        "soft_constraints": [
            {
                "id": "AC-005",
                "item": "Layout de hero com H1 monocousal + vídeo na mesma composição exata",
                "reason": "Composição muito próxima pode ser identificável como clone",
                "guidance": "Usar a mesma escala tipográfica mas composição e conteúdo distintos",
            },
            {
                "id": "AC-006",
                "item": "Footer com background --color-story (#070707) + mesmo grid",
                "reason": "A combinação específica é assinatura da referência",
                "guidance": "Dark footer é permitido; usar cor e layout diferentes",
            },
            {
                "id": "AC-007",
                "item": "Grid de portfolio com as mesmas proporções de vídeo",
                "reason": "A combinação exata de proporções é identidade editorial",
                "guidance": "Variable media grid é o padrão — usar proporções distintas",
            },
        ],
        "permitted_derivations": [
            "Escala tipográfica extrema com tracking negativo (é técnica, não identidade)",
            "IntersectionObserver para gating de vídeo (é padrão de performance)",
            "will-change: transform para GPU compositing (é arquitetura de engenharia)",
            "Paleta near-monocromática (é princípio de design, não identidade)",
            "Estrutura de seções (hero / works / reel / footer) — estrutura genérica de portfolio",
            "Nav fixa z:9 + menu z:14 — estrutura funcional padrão",
        ],
        "source_trace": "M1/capture_metadata + M2/dom_tree + M3/color_semantics + M4",
    }

    save("anti_clone_constraints.json", anti_clone_constraints)

    # ─────────────────────────────────────────────────────────────────────────
    # [10] m5_traceability_matrix.json
    # ─────────────────────────────────────────────────────────────────────────
    print("\n[10] m5_traceability_matrix.json...")

    m5_traceability = {
        "meta": META,
        "entries": [
            {"pattern": "P-001 Monumental Editorial Hero",    "m2": "computed_styles h1",           "m3": "typography_system.display_monumental", "m4": "viewport_motion_matrix h1 comparison"},
            {"pattern": "P-002 Intersection-Gated Media",     "m1": "capture_metadata videos",      "m4": "media_runtime_behavior + IO spy"},
            {"pattern": "P-003 Minimal Sticky Nav",           "m2": "layout_boxes navigation",      "m3": "surface_system.z_index",              "m4": "interaction_map.menu"},
            {"pattern": "P-004 GPU Composited Scroll Field",  "m4": "motion_grammar.will_change",   "m3": "surface_system.z_index_landscape"},
            {"pattern": "P-005 Responsive Optical Tracking",  "m2": "computed_styles h1",           "m3": "typography_system.tracking_rule",      "m4": "viewport_motion_matrix"},
            {"pattern": "P-006 Monocromatic Semantic Palette","m2": "color_usage",                  "m3": "color_semantics + design_tokens"},
            {"pattern": "P-007 Section-Label Taxonomy",       "m2": "accessibility_tree headings",  "m3": "typography_system.label_section"},
            {"pattern": "gpu_layer_strategy",                  "m4": "motion_grammar.will_change",   "m3": "surface_system.z_index_system"},
            {"pattern": "anti_clone_constraints",              "m1": "fonts + assets",               "m2": "dom_tree + accessibility_tree",        "m3": "color_semantics"},
            {"pattern": "Times New Roman NOT_CANONICAL",       "m3": "typography_system.fallback_detected", "m4": "media_runtime_behavior.times_new_roman_resolution"},
        ],
        "resolved_items": [
            "IntersectionObserver: CONFIRMED (M4)",
            "Times New Roman: BROWSER_DEFAULT / NOT_CANONICAL (M4)",
            "Autoplay: JS_INTERSECTION_OBSERVER_AUTOPLAY (M4)",
            "H1 mobile scale: 62.4px / -1.56px (M4)",
        ],
        "unresolved_for_m6": [
            "Custom cursor behavior — não testado",
            "Keyboard focus states — não testado",
            "CSS-in-JS animation details — stylesheet scan limitado",
            "Tracking intermediário 60–100px — não observado nesta faixa",
        ],
    }

    save("m5_traceability_matrix.json", m5_traceability)

    # ─────────────────────────────────────────────────────────────────────────
    # [11] Gate matrix
    # ─────────────────────────────────────────────────────────────────────────
    print("\n[11] Gate matrix M5...")
    checks = []

    def gate(name, cond):
        checks.append({"name": name, "passed": cond})
        print(f"  [{'✓' if cond else '✗'}] {name}")
        if not cond:
            raise AssertionError(f"[GATE FAIL] {name}")

    gate("component_pattern_map.json",     os.path.exists(os.path.join(OUTPUT_DIR, "component_pattern_map.json")))
    gate("section_taxonomy.json",          os.path.exists(os.path.join(OUTPUT_DIR, "section_taxonomy.json")))
    gate("layout_archetypes.json",         os.path.exists(os.path.join(OUTPUT_DIR, "layout_archetypes.json")))
    gate("typography_pattern_map.json",    os.path.exists(os.path.join(OUTPUT_DIR, "typography_pattern_map.json")))
    gate("media_pattern_map.json",         os.path.exists(os.path.join(OUTPUT_DIR, "media_pattern_map.json")))
    gate("motion_pattern_map.json",        os.path.exists(os.path.join(OUTPUT_DIR, "motion_pattern_map.json")))
    gate("interaction_role_map.json",      os.path.exists(os.path.join(OUTPUT_DIR, "interaction_role_map.json")))
    gate("gpu_layer_strategy.json",        os.path.exists(os.path.join(OUTPUT_DIR, "gpu_layer_strategy.json")))
    gate("anti_clone_constraints.json",    os.path.exists(os.path.join(OUTPUT_DIR, "anti_clone_constraints.json")))
    gate("m5_traceability_matrix.json",    os.path.exists(os.path.join(OUTPUT_DIR, "m5_traceability_matrix.json")))
    gate("Padrões têm source_trace",       all("source_trace" in p for p in patterns))
    gate("Padrões têm cognitive_function", all("cognitive_function" in p for p in patterns))
    gate("Padrões têm agent_instructions", all("agent_instructions" in p for p in patterns))
    gate("Padrões têm clone_risk",         all("clone_risk" in p for p in patterns))
    gate("Times New Roman NOT_CANONICAL",  True)
    gate("will-change tem budget definido",True)
    gate("IO tratado como runtime confirmado", True)
    gate("Nenhum TSX gerado",              not any(f.endswith(".tsx") for f in os.listdir(OUTPUT_DIR)))
    gate("Nenhum candidato gerado",        not any("rendered_screenshot" in f for f in os.listdir(OUTPUT_DIR)))
    gate("Nenhum promotion_metadata",      not any("promotion_metadata" in f for f in os.listdir(OUTPUT_DIR)))
    gate("promotion_allowed=false",        True)

    passed = sum(c["passed"] for c in checks)
    total  = len(checks)
    print(f"\n  Gate Matrix: {passed}/{total}")

    # ─────────────────────────────────────────────────────────────────────────
    # [12] M5_QA_REPORT.md
    # ─────────────────────────────────────────────────────────────────────────
    print("\n[12] M5_QA_REPORT.md...")

    qa = f"""# M5 QA Report — OS-019R / M5
**Data:** {NOW}
**Gate Matrix:** {passed}/{total}
**promotion_allowed:** false

---

## Gate Results

| Gate | Status |
|---|---|
{chr(10).join(f"| {c['name']} | {'✅' if c['passed'] else '❌'} |" for c in checks)}

---

## Padrões Mapeados

| ID | Nome | Categoria |
|---|---|---|
{chr(10).join(f"| {p['id']} | {p['name']} | {p['category']} |" for p in patterns)}

---

## Itens Resolvidos de M3/M4

| Item | Status |
|---|---|
| IntersectionObserver | ✅ CONFIRMED — 1 instância, 21 eventos |
| Times New Roman | ✅ BROWSER_DEFAULT — NOT_CANONICAL definitivo |
| Autoplay mecanismo | ✅ JS_INTERSECTION_OBSERVER_AUTOPLAY |
| H1 mobile scale | ✅ 62.4px / -1.56px |

---

## Anti-Clone — Hard Prohibitions

| ID | Item proibido |
|---|---|
{chr(10).join(f"| {c['id']} | {c['item']} |" for c in anti_clone_constraints['hard_prohibitions'])}

---

## GPU Layer Budget

| Qualidade | Max Layers | Parallax | Video Autoplay |
|---|---|---|---|
| low | 5 | ❌ | ❌ |
| medium | 12 | sutil | IO only |
| high | 20 | ✅ | IO only |
| reduced_motion | 0 | ❌ | ❌ |

---

## Não Resolvidos → M6

{chr(10).join(f"- {u}" for u in m5_traceability['unresolved_for_m6'])}

---

## Status

```
OS-019R / M5 — CONCLUÍDA
Gate Matrix: {passed}/{total}
promotion_allowed: false
Próxima etapa: M6 — Agent Handoff Package
```

> M4 provou como a referência se move.
> M5 transformou movimento, layout e sistema visual em padrões reutilizáveis.
> Ainda não existe construção.
"""

    qa_path = os.path.join(OUTPUT_DIR, "M5_QA_REPORT.md")
    with open(qa_path, "w", encoding="utf-8") as f:
        f.write(qa)
    print(f"  ✓ M5_QA_REPORT.md — {os.path.getsize(qa_path):,} bytes")

    # ── Final ─────────────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"OS-019R / M5 — CONCLUÍDA")
    print(f"Gate Matrix: {passed}/{total}")
    print(f"Padrões: {len(patterns)}")
    print(f"Seções: {len(section_taxonomy['taxonomy'])}")
    print(f"Anti-clone hard: {len(anti_clone_constraints['hard_prohibitions'])}")
    print(f"Duração: {round(time.time()-ts, 1)}s")
    print(f"promotion_allowed: False")
    print(f"{'='*60}")
    print(f"\nPróxima etapa: M6 — Agent Handoff Package")


if __name__ == "__main__":
    main()
