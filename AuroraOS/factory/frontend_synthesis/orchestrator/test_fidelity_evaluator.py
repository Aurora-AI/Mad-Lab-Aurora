import pytest
import os
import sys
from datetime import datetime

sys.path.extend([
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../contracts')),
])

from fidelity_contracts import VisualFidelityReport
from fidelity_evaluator import VisualFidelityEvaluator
from models import HybridTruthArtifact, ColorSample
from alvaro_contracts import FrontendCodeSpec, TailwindThemeSpec, ScaffoldingResolution, ComponentMissingAlert
from transmutation_contracts import ProprietaryPatternCandidate, OriginalityScoreBreakdown, CandidateFingerprint

@pytest.fixture
def base_truth():
    return HybridTruthArtifact(
        resolved_at=datetime.now(),
        resolved_fields={},
        colors=[
            ColorSample(hex_value="#1A73E8", usage_frequency=30.0),
            ColorSample(hex_value="#FFFFFF", usage_frequency=60.0),
            ColorSample(hex_value="#202124", usage_frequency=10.0)
        ],
        typography=[],
        spatial_system=[],
        motion=[],
        a11y_tree=[],
        css_variables={},
        breakpoints={},
        asset_paths={}
    )

@pytest.fixture
def base_candidate():
    return ProprietaryPatternCandidate(
        candidate_id="CAND-001",
        source_pattern_ids=[],
        generated_name="Aurora UI",
        design_intent="Test",
        transformed_description="Test",
        implementation_guidance="Test",
        originality_score=90.0,
        score_breakdown=OriginalityScoreBreakdown(
            brand_score=100.0,
            text_score=100.0,
            asset_score=100.0,
            layout_score=90.0,
            motion_score=90.0,
            color_score=90.0,
            component_score=90.0,
            final_score=90.0
        ),
        transformation_axes=["semantic", "visual"],
        risk_level="low",
        blocked_reasons=[],
        color_findings=[],
        candidate_fingerprint=CandidateFingerprint()
    )

@pytest.fixture
def base_spec():
    return FrontendCodeSpec(
        spec_id="SPEC-001",
        derived_from_draft_id="DRAFT-001",
        theme_config=TailwindThemeSpec(
            colors={"primary": "#2B84F9", "background": "#F5F5F5", "text": "#111111"},
            fontFamily={"sans": ["Inter", "sans-serif"]},
            fontSize={"base": "1rem"}
        ),
        component_registry=[],
        component_alerts=[],
        debt_tracking=ScaffoldingResolution(pending_injectors=[], resolution_status="OK"),
        ready_for_factory=True
    )

def test_happy_path_proprietary_spec(base_truth, base_candidate, base_spec):
    evaluator = VisualFidelityEvaluator()
    report = evaluator.evaluate("REP-01", base_truth, base_candidate, base_spec)
    
    assert report.decision == "approved"
    assert report.fidelity.intent_fidelity_score >= 75.0
    assert report.clone_risk.final_clone_risk <= 80.0
    assert not any(f.severity == "P0" for f in report.findings)

def test_poor_hierarchy_blocked(base_truth, base_candidate, base_spec):
    evaluator = VisualFidelityEvaluator()
    # Simulate broken hierarchy via 3 missing alerts
    base_spec.component_alerts = [
        ComponentMissingAlert(original_role="hero", degraded_to="div", reason="missing"),
        ComponentMissingAlert(original_role="cta", degraded_to="span", reason="missing"),
        ComponentMissingAlert(original_role="nav", degraded_to="ul", reason="missing")
    ]
    
    report = evaluator.evaluate("REP-02", base_truth, base_candidate, base_spec)
    
    assert report.decision == "rejected"
    assert report.fidelity.visual_hierarchy_score < 75.0
    assert any(f.code == "POOR_HIERARCHY" for f in report.findings)
    assert any(f.severity == "P1" for f in report.findings)

def test_insufficient_contrast_blocked(base_truth, base_candidate, base_spec):
    evaluator = VisualFidelityEvaluator()
    # Simulate bad contrast (only light colors)
    base_spec.theme_config.colors = {"bg": "#FFFFFF", "text": "#F8F9FA"}
    
    report = evaluator.evaluate("REP-03", base_truth, base_candidate, base_spec)
    
    assert report.decision == "rejected"
    assert report.fidelity.contrast_score < 50.0
    assert any(f.code == "INSUFFICIENT_CONTRAST" for f in report.findings)

def test_clone_like_spec_blocked(base_truth, base_candidate, base_spec):
    evaluator = VisualFidelityEvaluator()
    # Simulate clone by using exact same color hex as the original (excluding neutral ones)
    base_spec.theme_config.colors = {"primary": "#1A73E8"} 
    
    report = evaluator.evaluate("REP-04", base_truth, base_candidate, base_spec)
    
    assert report.decision == "rejected"
    assert report.clone_risk.color_similarity_risk >= 90.0
    assert report.clone_risk.final_clone_risk > 40.0 # Enough to be noticeable or trigger
    
    # Force max risk
    base_spec.theme_config.colors = {"primary": "#1A73E8", "accent": "#202124"} 
    report2 = evaluator.evaluate("REP-04-2", base_truth, base_candidate, base_spec)
    assert report2.decision == "rejected"
    assert any("Clone risk" in r for r in report2.blocked_reasons)
