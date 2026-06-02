import pytest
from alvaro_agent import infer_components, orchestrate_code_spec
from synthesizer_models import DesignSystemDraft, SemanticToken
from models import A11yNodeSummary
from datetime import datetime

class MockA11yNode:
    def __init__(self, role):
        self.role = role

def test_semantic_mapping_matches_core_components():
    """Garante que roles padrão invocam os componentes Aurora corretos."""
    tree = [MockA11yNode("button"), MockA11yNode("navigation"), MockA11yNode("textbox")]
    
    registry, alerts = infer_components(tree)
    
    component_names = [comp.component_name for comp in registry]
    assert "AuroraButton" in component_names
    assert "AuroraNavbar" in component_names
    assert "AuroraInput" in component_names
    assert len(alerts) == 0

def test_fallback_degradation_for_unknown_roles():
    """Garante que roles bizarros não alucinam componentes e disparam alertas."""
    tree = [MockA11yNode("button"), MockA11yNode("marquee"), MockA11yNode("timer")]
    
    registry, alerts = infer_components(tree)
    
    # O botão deve ter passado normal
    component_names = [comp.component_name for comp in registry]
    assert "AuroraButton" in component_names
    
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
            A11yNodeSummary(role="button", aria_label_present=True, contrast_ratio=7.0),
            A11yNodeSummary(role="custom-marquee", aria_label_present=False, contrast_ratio=2.1)
        ],
        is_safe_for_production=True
    )
    
    spec = orchestrate_code_spec(mock_draft)
    assert spec.derived_from_draft_id == "DS-INTEGRATION"
    assert len(spec.component_registry) == 1
    assert spec.component_registry[0].component_name == "AuroraButton"
    assert len(spec.component_alerts) == 1
    assert spec.component_alerts[0].original_role == "custom-marquee"
    assert spec.component_alerts[0].degraded_to == "div"
