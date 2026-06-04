import pytest
from alvaro_agent import infer_components, orchestrate_code_spec
from synthesizer_models import DesignSystemDraft, SemanticToken
from models import A11yNodeSummary
from datetime import datetime

class MockA11yNode:
    def __init__(self, role, text_content=None):
        self.role = role
        self.text_content = text_content

def test_semantic_mapping_matches_core_components():
    """Garante que a composição semântica mapeia para componentes estruturais do Aurora (OS-016)."""
    tree = [
        MockA11yNode("button", "Download for Windows"), 
        MockA11yNode("navigation", "pricing"), 
        MockA11yNode("heading", "experience liftoff with the next-gen agent platform")
    ]
    
    registry, alerts = infer_components(tree)
    
    component_names = [comp.component_name for comp in registry]
    assert "AuroraLandingShell" in component_names
    assert "AuroraHeroStatement" in component_names
    assert "AuroraTopNavigation" in component_names
    assert "AuroraPrimaryCTA" in component_names

def test_fallback_degradation_for_unknown_roles():
    """Garante que roles bizarros não alucinam componentes e disparam alertas."""
    tree = [MockA11yNode("marquee"), MockA11yNode("timer")]
    
    registry, alerts = infer_components(tree)
    
    # As anomalias devem ter gerado alertas e degradações específicas
    assert len(alerts) == 2
    assert alerts[0].original_role == "marquee"
    assert alerts[0].degraded_to == "div"
    assert alerts[1].original_role == "timer"
    assert alerts[1].degraded_to == "div"

def test_full_orchestration_pipeline():
    """Garante que o orquestrador gera uma especificação completa e válida sob validação estrita."""
    mock_draft = DesignSystemDraft(
        synthesis_id="DS-INTEGRATION",
        synthesized_at=datetime.now(),
        semantic_tokens=[
            SemanticToken(name="color-base-surface", value="#0A0A0C", rationale="Ok")
        ],
        typography_scale={"body": "1.0rem"},
        do_not_copy_rules=[],
        a11y_tree=[
            A11yNodeSummary(role="button", aria_label_present=True, contrast_ratio=7.0, text_content="Download for Windows", depth=4),
            A11yNodeSummary(role="custom-marquee", aria_label_present=False, contrast_ratio=2.1, text_content="Promo", depth=3)
        ],
        is_safe_for_production=True
    )
    
    spec = orchestrate_code_spec(mock_draft)
    assert spec.derived_from_draft_id == "DS-INTEGRATION"
    component_names = [comp.component_name for comp in spec.component_registry]
    assert "AuroraLandingShell" in component_names
    assert "AuroraPrimaryCTA" in component_names
    assert len(spec.component_alerts) == 1
    assert spec.component_alerts[0].original_role == "custom-marquee"
    assert spec.component_alerts[0].degraded_to == "div"
