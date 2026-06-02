import os
import sys
import pytest

sys.path.extend([
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../contracts')),
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../factory'))
])

from perceptual_contracts import PerceptualFinding
from factory_contracts import StandaloneRenderBundle
from perceptual_evaluator import EvaluatePerceptualFidelity, PipelinePausedException

@pytest.mark.asyncio
async def test_perceptual_evaluator_blank_screen(tmp_path):
    # Simulate a totally white HTML fallback
    bundle = StandaloneRenderBundle(
        bundle_id="test-blank",
        component_code="<div />",
        html_fallback="<div style='width: 100vw; height: 100vh; background: white;'></div>",
        css_code="",
        tailwind_safelist=[],
        viewport={"width": 1440, "height": 900},
        dependencies_mode="local_pinned",
        network_allowed=False
    )
    
    evaluator = EvaluatePerceptualFidelity(str(tmp_path))
    
    with pytest.raises(PipelinePausedException) as exc:
        await evaluator.evaluate(bundle)
        
    assert "Perceptual Evaluation Failed" in str(exc.value)
    assert "Tela considerada em branco/vazia" in str(exc.value)

@pytest.mark.asyncio
async def test_perceptual_evaluator_success(tmp_path):
    # Simulate a healthy UI
    html = """
    <div style='width: 100vw; height: 100vh; background: white; display: flex; align-items: center; justify-content: center;'>
        <h1 style='color: black; font-size: 48px;'>Aurora OS-012</h1>
        <div style='background: blue; width: 800px; height: 800px; margin-top: 50px;'></div>
    </div>
    """
    bundle = StandaloneRenderBundle(
        bundle_id="test-success",
        component_code="<div />",
        html_fallback=html,
        css_code="",
        tailwind_safelist=[],
        viewport={"width": 1440, "height": 900},
        dependencies_mode="local_pinned",
        network_allowed=False
    )
    
    evaluator = EvaluatePerceptualFidelity(str(tmp_path))
    
    report = await evaluator.evaluate(bundle)
    assert report.decision == "approved"
    assert report.perceptual_score.final_score >= 75.0
    assert os.path.exists(report.screenshot_path)
