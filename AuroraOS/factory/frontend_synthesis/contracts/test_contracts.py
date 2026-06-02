import pytest
from pydantic import ValidationError
from models import PageIntelligenceArtifact, ColorSample, TypographyNode
from fixtures import SYNTHETIC_PROBE_OUTPUT

def test_page_intelligence_artifact_valid_data():
    """Valida se a nossa fixture sintética passa perfeitamente pelo crivo do contrato central."""
    artifact = PageIntelligenceArtifact(**SYNTHETIC_PROBE_OUTPUT)
    
    # Validações estruturais confirmando o Trustware
    assert str(artifact.source_url) == "https://competitor-quiet-luxury.example.com/"
    assert len(artifact.colors) == 3
    assert artifact.spatial_system[0].value_px == 16.0
    assert artifact.motion[0].duration_ms == 250

def test_color_validation_rejects_rgba():
    """Garante que a fábrica aniquila extrações de CSS com RGBA ou nomenclaturas sujas."""
    with pytest.raises(ValidationError) as exc_info:
        ColorSample(hex_value="rgba(15, 15, 19, 1)", usage_frequency=10.0, semantic_guess="test")
    
    assert "HEX válido" in str(exc_info.value)
    assert "RGBA" in str(exc_info.value)

def test_typography_validation_rejects_no_fallback():
    """Impede que a Probe injete tipografia frágil (sem fallback nativo)."""
    with pytest.raises(ValidationError) as exc_info:
        TypographyNode(font_family="Geist", weight=400, size_px=16.0, line_height=24.0)
    
    assert "fonte de fallback" in str(exc_info.value)

def test_weight_validation_out_of_bounds():
    """Garante que pesos de fontes bizarros ou ilegais no CSS sejam barrados."""
    with pytest.raises(ValidationError) as exc_info:
        TypographyNode(font_family="Inter, sans-serif", weight=950, size_px=16.0, line_height=24.0)
    
    assert "Input should be less than or equal to 900" in str(exc_info.value)
