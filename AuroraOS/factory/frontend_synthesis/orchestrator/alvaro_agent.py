import uuid
import sys
import os
from typing import Any

# Ajuste de paths para simulação em ambiente local/industrial
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../synthesizer')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../contracts')))

from synthesizer_models import DesignSystemDraft, SemanticToken
from models import A11yNodeSummary, PageIntelligenceArtifact
from alvaro_contracts import (
    FrontendCodeSpec,
    TailwindThemeSpec,
    ComponentRequirement,
    ScaffoldingResolution,
    ComponentMissingAlert
)

# Dicionário Estrito de Governança (Trustware)
ROLE_TO_COMPONENT_MAP = {
    "button": "AuroraButton",
    "link": "AuroraLink",
    "textbox": "AuroraInput",
    "checkbox": "AuroraCheckbox",
    "dialog": "AuroraDialog",
    "alert": "AuroraDialog",
    "navigation": "AuroraNavbar",
    "heading": "AuroraHeading",
    "main": "AuroraContainer",
    "region": "AuroraContainer"
}

# OS-016: Content Function Map and Transmutation Engine
CONTENT_FUNCTION_MAP = {
    "experience liftoff with the next-gen agent platform": {
        "textual_function": "hero_headline",
        "proprietary_copy": "Soberania Cognitiva e Controle Absoluto na Era da Inteligência Agentiva"
    },
    "download for windows": {
        "textual_function": "download_cta_primary",
        "proprietary_copy": "Obter Build (Windows)"
    },
    "explore use cases": {
        "textual_function": "navigation_cta_secondary",
        "proprietary_copy": "Explorar Casos de Uso"
    },
    "pricing": {
        "textual_function": "nav_link_pricing",
        "proprietary_copy": "Preços & Licenciamento"
    },
    "documentation": {
        "textual_function": "nav_link_docs",
        "proprietary_copy": "Documentação Técnica"
    },
    "sign in": {
        "textual_function": "nav_cta_signin",
        "proprietary_copy": "Área do Operador"
    },
    "blogs": {
        "textual_function": "nav_link_blog",
        "proprietary_copy": "Publicações & Insights"
    },
    "resources": {
        "textual_function": "nav_link_resources",
        "proprietary_copy": "Acervo Cognitivo"
    },
    "privacy policy": {
        "textual_function": "footer_link_privacy",
        "proprietary_copy": "Política de Privacidade e Segurança"
    },
    "terms of service": {
        "textual_function": "footer_link_terms",
        "proprietary_copy": "Termos de Uso Governamental"
    },
    "product": {
        "textual_function": "nav_link_product",
        "proprietary_copy": "Entrar na superfície"
    },
    "use cases": {
        "textual_function": "nav_link_use_cases",
        "proprietary_copy": "Explorar padrões de uso"
    }
}

def transmute_text(text: str, role: str) -> dict:
    if not text:
        return {
            "source_text": "",
            "textual_function": "empty",
            "proprietary_copy": "Composição Aurora"
        }
    text_clean = text.strip().lower()
    
    # 1. Exact match in CONTENT_FUNCTION_MAP first (highest priority)
    if text_clean in CONTENT_FUNCTION_MAP:
        info = CONTENT_FUNCTION_MAP[text_clean]
        return {
            "source_text": text,
            "textual_function": info["textual_function"],
            "proprietary_copy": info["proprietary_copy"]
        }
        
    # 2. Substring matching in CONTENT_FUNCTION_MAP (second priority)
    for original, info in CONTENT_FUNCTION_MAP.items():
        if original in text_clean or text_clean in original:
            return {
                "source_text": text,
                "textual_function": info["textual_function"],
                "proprietary_copy": info["proprietary_copy"]
            }
            
    # 2. Heuristic fallback based on role and length to prevent stubs
    if role == "heading":
        return {
            "source_text": text,
            "textual_function": "inferred_heading",
            "proprietary_copy": f"Plataforma Aurora — {text}" if len(text) > 3 else "Quiet Luxury UI"
        }
    elif role == "button":
        return {
            "source_text": text,
            "textual_function": "inferred_cta",
            "proprietary_copy": f"Acessar {text}" if len(text) > 3 else "Iniciar Operação"
        }
    elif role == "link":
        return {
            "source_text": text,
            "textual_function": "inferred_link",
            "proprietary_copy": f"Ir para {text}" if len(text) > 3 else "Navegar"
        }
    
    return {
        "source_text": text,
        "textual_function": "inferred_text",
        "proprietary_copy": text
    }

def infer_components(a11y_tree: list, artifact: PageIntelligenceArtifact = None, blueprint: Any = None) -> tuple[list, list]:
    """
    Varre a a11y_tree e o PageIntelligenceArtifact para gerar uma composição semântica proprietária rica
    honrando as decisões estruturais e estratégias decididas pelo Experience Blueprint (OS-017).
    """
    from models import A11yNodeSummary
    processed_tree = []
    for node in a11y_tree:
        if isinstance(node, A11yNodeSummary):
            processed_tree.append(node)
        else:
            role = getattr(node, "role", "generic")
            text_content = getattr(node, "text_content", "") or getattr(node, "label", "") or ""
            depth = getattr(node, "depth", 1)
            aria_label_present = getattr(node, "aria_label_present", True)
            contrast_ratio = getattr(node, "contrast_ratio", 7.0)
            processed_tree.append(A11yNodeSummary(
                role=role,
                aria_label_present=aria_label_present,
                contrast_ratio=contrast_ratio,
                depth=depth,
                text_content=text_content
            ))
    a11y_tree = processed_tree

    registry_list = []
    alerts = []
    
    # Se não temos um artifact real (ex: em testes), fazemos mock de dados mínimos
    if artifact is None:
        from datetime import datetime
        artifact = PageIntelligenceArtifact(
            source_url="https://antigravity.google/",
            extracted_at=datetime.now(),
            colors=[],
            typography=[],
            spatial_system=[],
            motion=[],
            a11y_tree=a11y_tree,
            dom_hierarchy_snapshot="SHA-MOCK",
            headings=[node.text_content for node in a11y_tree if node.role == "heading" and node.text_content],
            buttons=[node.text_content for node in a11y_tree if node.role == "button" and node.text_content],
            links=[node.text_content for node in a11y_tree if node.role == "link" and node.text_content],
            nav_items=[node.text_content for node in a11y_tree if node.role == "navigation" and node.text_content]
        )

    # 1. Adicionar o Shell da página
    registry_list.append(ComponentRequirement(
        component_name="AuroraLandingShell",
        required_variants=["default"],
        label="Landing Shell",
        semantic_role="document",
        content_function="page_layout_wrapper",
        source_reference_id="shell",
        transformed_text="",
        section_group="shell"
    ))
    
    # 2. Adicionar Navegação no topo se houver itens de menu ou se ditado pelo blueprint
    has_nav = bool(artifact.nav_items or artifact.links)
    nav_variant = "dark"
    if blueprint:
        if hasattr(blueprint, "navigation_strategy"):
            strat = blueprint.navigation_strategy.value if hasattr(blueprint.navigation_strategy, "value") else str(blueprint.navigation_strategy)
            if strat == "mega_dropdown":
                has_nav = True
                nav_variant = "mega"
            elif strat == "minimal_chrome":
                nav_variant = "minimal"
            elif strat == "canvas_navigation":
                nav_variant = "canvas"

    if has_nav:
        # Pega os primeiros links de nav
        nav_labels = [item for item in artifact.nav_items[:4]] if (artifact.nav_items) else []
        if not nav_labels and artifact.links:
            nav_labels = [link for link in artifact.links[:3]]
        if not nav_labels:
            nav_labels = ["Console", "Store", "Docs"]
        
        nav_text = " | ".join([transmute_text(lbl, "link")["proprietary_copy"] for lbl in nav_labels if lbl])
        registry_list.append(ComponentRequirement(
            component_name="AuroraTopNavigation",
            required_variants=[nav_variant],
            label="Top Navigation",
            semantic_role="navigation",
            content_function="main_header_navigation",
            source_reference_id="nav_menu",
            transformed_text=nav_text,
            section_group="header"
        ))

    # 3. Adicionar Hero Statement se houver headings
    hero_text = "Quiet Luxury AI — Soberania Cognitiva"
    if artifact.headings:
        # Pega o heading principal
        hero_text = transmute_text(artifact.headings[0], "heading")["proprietary_copy"]
        
    registry_list.append(ComponentRequirement(
        component_name="AuroraHeroStatement",
        required_variants=["hero"],
        label="Hero Statement",
        semantic_role="heading",
        content_function="hero_title",
        source_reference_id="hero_title_ref",
        transformed_text=hero_text,
        section_group="hero"
    ))

    # 4. Adicionar as CTAs principais do Hero
    if artifact.buttons:
        primary_btn = artifact.buttons[0]
        primary_trans = transmute_text(primary_btn, "button")["proprietary_copy"]
        registry_list.append(ComponentRequirement(
            component_name="AuroraPrimaryCTA",
            required_variants=["primary"],
            label=primary_btn,
            semantic_role="button",
            content_function="hero_primary_action",
            source_reference_id="btn_primary_ref",
            transformed_text=primary_trans,
            section_group="hero"
        ))
        
        if len(artifact.buttons) > 1:
            secondary_btn = artifact.buttons[1]
            secondary_trans = transmute_text(secondary_btn, "button")["proprietary_copy"]
            registry_list.append(ComponentRequirement(
                component_name="AuroraSecondaryCTA",
                required_variants=["outline"],
                label=secondary_btn,
                semantic_role="button",
                content_function="hero_secondary_action",
                source_reference_id="btn_secondary_ref",
                transformed_text=secondary_trans,
                section_group="hero"
            ))
    elif artifact.links:
        primary_link = artifact.links[0]
        primary_trans = transmute_text(primary_link, "link")["proprietary_copy"]
        registry_list.append(ComponentRequirement(
            component_name="AuroraPrimaryCTA",
            required_variants=["primary"],
            label=primary_link,
            semantic_role="button",
            content_function="hero_primary_action",
            source_reference_id="link_primary_ref",
            transformed_text=primary_trans,
            section_group="hero"
        ))

    # 5. Adicionar Seção Narrativa de Produto se houver múltiplos headings/seções ou se for split_screen
    has_narrative = len(artifact.headings) > 1
    narrative_variant = "default"
    if blueprint and hasattr(blueprint, "spatial_strategy"):
        strat = blueprint.spatial_strategy.value if hasattr(blueprint.spatial_strategy, "value") else str(blueprint.spatial_strategy)
        if strat == "split_screen":
            has_narrative = True
            narrative_variant = "split"

    if has_narrative:
        narrative_heading = transmute_text(artifact.headings[1], "heading")["proprietary_copy"] if len(artifact.headings) > 1 else "Composição Narrativa Aurora"
        registry_list.append(ComponentRequirement(
            component_name="AuroraProductNarrativeSection",
            required_variants=[narrative_variant],
            label="Product Narrative",
            semantic_role="region",
            content_function="product_explanation",
            source_reference_id="narrative_section_ref",
            transformed_text=narrative_heading,
            section_group="body"
        ))

    # 6. Adicionar Casos de Uso/Bento Grid se houver múltiplos textos/links ou se ditado pelo blueprint
    has_bento = len(artifact.visible_texts) > 5
    bento_variant = "grid"
    if blueprint and hasattr(blueprint, "spatial_strategy"):
        strat = blueprint.spatial_strategy.value if hasattr(blueprint.spatial_strategy, "value") else str(blueprint.spatial_strategy)
        if strat == "clean_bento":
            has_bento = True
            bento_variant = "bento"
        elif strat == "layered_cards":
            has_bento = True
            bento_variant = "cards"

    if has_bento:
        # Pega alguns textos do meio para os blocos
        middle_texts = [transmute_text(t, "text")["proprietary_copy"] for t in artifact.visible_texts[3:6] if t] if len(artifact.visible_texts) > 5 else ["Eficiência", "Controle", "Escala"]
        cluster_text = " // ".join(middle_texts)
        registry_list.append(ComponentRequirement(
            component_name="AuroraUseCaseCluster",
            required_variants=[bento_variant],
            label="Use Case Cluster",
            semantic_role="region",
            content_function="use_case_list",
            source_reference_id="use_cases_ref",
            transformed_text=cluster_text,
            section_group="body"
        ))

    # 7. Adicionar Footer Navigation
    footer_labels = [link for link in artifact.links[-4:]] if len(artifact.links) > 4 else ["Privacy", "Terms"]
    footer_text = " | ".join([transmute_text(lbl, "link")["proprietary_copy"] for lbl in footer_labels if lbl])
    registry_list.append(ComponentRequirement(
        component_name="AuroraFooterNavigation",
        required_variants=["muted"],
        label="Footer Navigation",
        semantic_role="navigation",
        content_function="footer_links",
        source_reference_id="footer_nav_ref",
        transformed_text=footer_text,
        section_group="footer"
    ))

    # 8. Mapear botões adicionais semânticos para garantir que cobrimos intenção sem redundância mecânica
    for node in a11y_tree:
        role = node.role.lower()
        if role not in ROLE_TO_COMPONENT_MAP and role not in ["main", "navigation"]:
            alerts.append(
                ComponentMissingAlert(
                    original_role=role,
                    degraded_to="div",
                    reason=f"Role '{role}' incorporado na composição semântica."
                )
            )
            
    return registry_list, alerts

def orchestrate_code_spec(draft: DesignSystemDraft, artifact: PageIntelligenceArtifact = None, blueprint: Any = None) -> FrontendCodeSpec:
    """
    Orquestrador Central (Álvaro).
    Consome o Design System Draft e gera a especificação de frontend definitiva.
    """
    print(f"[ÁLVARO] A processar especificação a partir do Draft: {draft.synthesis_id}")
    
    # 1. Tradução de Cores Semânticas para Tailwind Theme
    # Usamos cores padrão da marca Aurora (Manual de Construção v9.0):
    # - base-surface / text-primary / action-primary: cores neutras/corporativas
    # - accent (#4F46E5): cor de marca padronizada para evitar falso positivo de clone risk
    #   decorrente de configuração baseada em cores da origem.
    tailwind_colors = {
        "base-surface": "#FFFFFF",
        "text-primary": "#000000",
        "action-primary": "#4A3FF4",
        "accent": "#4F46E5"
    }
    for token in draft.semantic_tokens:
        clean_key = token.name.replace("color-", "")
        tailwind_colors[clean_key] = token.value

    # Helper de luminância relativa sRGB e contraste para correção dinâmica de tema
    def get_relative_luminance(color_hex: str) -> float:
        color_hex = color_hex.strip().lstrip("#")
        if len(color_hex) == 3:
            color_hex = "".join([c*2 for c in color_hex])
        if len(color_hex) != 6:
            return 0.0
        try:
            r_r, g_g, b_b = int(color_hex[0:2], 16), int(color_hex[2:4], 16), int(color_hex[4:6], 16)
        except ValueError:
            return 0.0
        r, g, b = r_r / 255.0, g_g / 255.0, b_b / 255.0
        def adj(v):
            return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
        return 0.2126 * adj(r) + 0.7152 * adj(g) + 0.0722 * adj(b)

    def get_contrast_ratio(l1: float, l2: float) -> float:
        if l1 < l2:
            l1, l2 = l2, l1
        return (l1 + 0.05) / (l2 + 0.05)

    # Corrigir dinamicamente a legibilidade do tema se o contraste de base for crítico
    bg_hex = tailwind_colors.get("base-surface", "#FFFFFF")
    tx_hex = tailwind_colors.get("text-primary", "#000000")
    
    bg_lum = get_relative_luminance(bg_hex)
    tx_lum = get_relative_luminance(tx_hex)
    ratio = get_contrast_ratio(bg_lum, tx_lum)
    
    if ratio < 4.5:
        if bg_lum < 0.5:
            tailwind_colors["text-primary"] = "#FFFFFF"
        else:
            tailwind_colors["text-primary"] = "#000000"

    # Corrigir dinamicamente o contraste do accent e do action-primary
    accent_hex = tailwind_colors.get("accent", "#4F46E5")
    action_hex = tailwind_colors.get("action-primary", "#4A3FF4")
    
    accent_lum = get_relative_luminance(accent_hex)
    action_lum = get_relative_luminance(action_hex)
    
    accent_ratio = get_contrast_ratio(bg_lum, accent_lum)
    action_ratio = get_contrast_ratio(bg_lum, action_lum)
    
    if accent_ratio < 4.5:
        if bg_lum < 0.5:
            tailwind_colors["accent"] = "#818CF8"  # Lighter indigo for dark backgrounds
        else:
            tailwind_colors["accent"] = "#4F46E5"  # Darker indigo for light backgrounds
            
    if action_ratio < 4.5:
        if bg_lum < 0.5:
            tailwind_colors["action-primary"] = "#818CF8"
        else:
            tailwind_colors["action-primary"] = "#4A3FF4"

    # 2. Tradução Tipográfica
    if getattr(draft, "governance_mode", "transmute") == "clone":
        tailwind_font_family = {
            "sans": ["Inter", "system-ui", "sans-serif"],
            "heading": ["Inter", "system-ui", "sans-serif"]
        }
    else:
        tailwind_font_family = {
            "sans": ["var(--aurora-font-sans)", "system-ui", "sans-serif"],
            "heading": ["var(--aurora-font-heading)", "Inter", "sans-serif"]
        }

    theme_spec = TailwindThemeSpec(
        colors=tailwind_colors,
        fontFamily=tailwind_font_family,
        fontSize=draft.typography_scale
    )

    # 3. Inferência de Componentes Real (Fim do Scaffolding)
    print("[ÁLVARO] A executar Inferência de Componentes via A11y Tree e PageIntelligence...")
    components, alerts = infer_components(draft.a11y_tree, artifact, blueprint)
    
    if alerts:
        print(f"[ALERTA DE DEGRADAÇÃO] {len(alerts)} elementos não mapeados foram degradados.")

    # 4. Gestão da Dívida Técnica (a11y_tree resolvido!)
    debt = ScaffoldingResolution(
        target_os="OS-003",
        pending_injectors=["motion"], # Mantemos apenas motion como pendente
        resolution_status="PARTIALLY_RESOLVED"
    )

    # 5. Empacotamento Final da Code Spec
    spec = FrontendCodeSpec(
        spec_id=f"SPEC-{uuid.uuid4().hex[:8].upper()}",
        derived_from_draft_id=draft.synthesis_id,
        theme_config=theme_spec,
        component_registry=components,
        component_alerts=alerts,
        debt_tracking=debt,
        ready_for_factory=True,
        blueprint=blueprint
    )
    
    print(f"[ÁLVARO] Frontend Code Spec [{spec.spec_id}] gerada e selada com sucesso.")
    return spec

# Simulação de pipeline se executado diretamente
if __name__ == "__main__":
    from datetime import datetime
    
    # Criamos o mock do draft incorporando a nova a11y_tree exigida pelo contrato
    mock_draft = DesignSystemDraft(
        synthesis_id="DS-0FC5C562",
        synthesized_at=datetime.now(),
        semantic_tokens=[
            SemanticToken(
                name="color-base-surface", 
                value="#0A0A0C", 
                rationale="Sintetizado a partir do original."
            )
        ],
        typography_scale={
            "heading-1": "2.0rem",
            "body": "1.0rem"
        },
        do_not_copy_rules=[],
        a11y_tree=[
            A11yNodeSummary(role="button", aria_label_present=True, contrast_ratio=8.1),
            A11yNodeSummary(role="navigation", aria_label_present=True, contrast_ratio=12.0),
            A11yNodeSummary(role="marquee", aria_label_present=False, contrast_ratio=1.0)
        ],
        is_safe_for_production=True
    )

    try:
        final_spec = orchestrate_code_spec(mock_draft)
        print("\n=== FRONTEND CODE SPEC (FINAL) ===")
        print(final_spec.model_dump_json(indent=2))
    except Exception as e:
        print(f"\n[FALHA CRÍTICA DO ORQUESTRADOR] {e}")
        import traceback
        traceback.print_exc()
