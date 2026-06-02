import uuid
import sys
import os

# Ajuste de paths para simulação em ambiente local/industrial
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../synthesizer')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../contracts')))

from synthesizer_models import DesignSystemDraft, SemanticToken
from models import A11yNodeSummary
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

def infer_components(a11y_tree: list) -> tuple[list, list]:
    """
    Varre a árvore semântica (a11y_tree), mapeia para componentes Aurora governados 
    e degrada elementos desconhecidos para primitivos HTML estilizados.
    """
    registry_map = {}
    alerts = []

    for node in a11y_tree:
        role = node.role.lower()
        
        if role in ROLE_TO_COMPONENT_MAP:
            comp_name = ROLE_TO_COMPONENT_MAP[role]
            # Evita duplicações redundantes no spec do frontend
            if comp_name not in registry_map:
                registry_map[comp_name] = ComponentRequirement(
                    component_name=comp_name,
                    required_variants=["default"], # Mapeamento futuro de estados
                    is_core_library=True
                )
        else:
            # Protocolo de Degradação Controlada para Primitivos (Fallback)
            degraded_tag = "span" if role in ["text", "statictext", "status"] else "div"
            alerts.append(
                ComponentMissingAlert(
                    original_role=role,
                    degraded_to=degraded_tag,
                    reason=f"Role '{role}' não é suportado nativamente no Aurora Core. Degradado para <{degraded_tag}>."
                )
            )
            
    return list(registry_map.values()), alerts

def orchestrate_code_spec(draft: DesignSystemDraft) -> FrontendCodeSpec:
    """
    Orquestrador Central (Álvaro).
    Consome o Design System Draft e gera a especificação de frontend definitiva.
    """
    print(f"[ÁLVARO] A processar especificação a partir do Draft: {draft.synthesis_id}")
    
    # 1. Tradução de Cores Semânticas para Tailwind Theme
    tailwind_colors = {}
    for token in draft.semantic_tokens:
        clean_key = token.name.replace("color-", "")
        tailwind_colors[clean_key] = token.value

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
    print("[ÁLVARO] A executar Inferência de Componentes via A11y Tree...")
    components, alerts = infer_components(draft.a11y_tree)
    
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
        ready_for_factory=True
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
