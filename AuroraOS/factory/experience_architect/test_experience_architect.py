import sys
import os
import pytest
from pydantic import HttpUrl

# Ensure correct path discovery
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.extend([
    os.path.abspath(os.path.join(current_dir, "../frontend_synthesis/contracts")),
    os.path.abspath(os.path.join(current_dir, "../contracts")),
    os.path.abspath(current_dir)
])

from experience_architect import ExperienceArchitect
from models import PageIntelligenceArtifact
from experience_architecture_contracts import (
    ExperienceBlueprint,
    ExperienceSurface,
    NavigationStrategy,
    MotionStrategy,
    SpatialStrategy,
    AttentionStrategy,
    NarrativeStrategy
)
from datetime import datetime

def create_mock_artifact(url: str) -> PageIntelligenceArtifact:
    return PageIntelligenceArtifact(
        source_url=HttpUrl(url),
        extracted_at=datetime.now(),
        colors=[],
        typography=[],
        spatial_system=[],
        motion=[],
        a11y_tree=[],
        dom_hierarchy_snapshot="MOCK-HASH"
    )

def test_architect_default_surfaces():
    architect = ExperienceArchitect()
    artifact = create_mock_artifact("https://generic-site.com/")
    
    # Test Landing
    bp_landing = architect.architect(
        url="https://generic-site.com/",
        page_intel=artifact,
        default_surface="landing"
    )
    assert bp_landing.surface_type == ExperienceSurface.LANDING
    
    # Test CRM
    bp_crm = architect.architect(
        url="https://generic-site.com/",
        page_intel=artifact,
        default_surface="crm"
    )
    assert bp_crm.surface_type == ExperienceSurface.CRM
    
    # Test Portal
    bp_portal = architect.architect(
        url="https://generic-site.com/",
        page_intel=artifact,
        default_surface="portal"
    )
    assert bp_portal.surface_type == ExperienceSurface.PORTAL
    
    # Test Dashboard
    bp_dashboard = architect.architect(
        url="https://generic-site.com/",
        page_intel=artifact,
        default_surface="dashboard"
    )
    assert bp_dashboard.surface_type == ExperienceSurface.DASHBOARD
    
    # Test Canvas
    bp_canvas = architect.architect(
        url="https://generic-site.com/",
        page_intel=artifact,
        default_surface="canvas"
    )
    assert bp_canvas.surface_type == ExperienceSurface.CANVAS

def test_architect_rationale_populated():
    architect = ExperienceArchitect()
    artifact = create_mock_artifact("https://generic-site.com/")
    blueprint = architect.architect(
        url="https://generic-site.com/",
        page_intel=artifact,
        default_surface="landing"
    )
    
    assert blueprint.rationale is not None
    assert len(blueprint.rationale) >= 10
