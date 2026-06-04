import sys
import os
import pytest
from pydantic import ValidationError

# Ensure correct path discovery for contracts
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.extend([
    os.path.abspath(os.path.join(current_dir, "../frontend_synthesis/contracts")),
    os.path.abspath(os.path.join(current_dir, "../contracts")),
    os.path.abspath(current_dir)
])

from build_plan_resolver import BuildPlanResolver, compute_blueprint_hash
from experience_architecture_contracts import (
    ExperienceBlueprint,
    ExperienceSurface,
    NavigationStrategy,
    MotionStrategy,
    SpatialStrategy,
    AttentionStrategy,
    NarrativeStrategy
)
from stories_builder_contracts import BuilderConstraint, BuilderCapability

def create_mock_blueprint(surface: ExperienceSurface) -> ExperienceBlueprint:
    return ExperienceBlueprint(
        surface_type=surface,
        navigation_strategy=NavigationStrategy.STANDARD,
        motion_strategy=MotionStrategy.SUBTLE_TRANSITIONS,
        spatial_strategy=SpatialStrategy.CLEAN_BENTO,
        attention_strategy=AttentionStrategy.FOCAL_HIERARCHY,
        narrative_strategy=NarrativeStrategy.STANDARD,
        interaction_density="medium",
        visual_energy="low",
        immersion_level="high",
        rationale="Mock blueprint for testing build plan resolver."
    )

def test_resolve_build_plan_landing():
    resolver = BuildPlanResolver()
    blueprint = create_mock_blueprint(ExperienceSurface.LANDING)
    
    plan = resolver.resolve_build_plan(blueprint, proposed_components=["AuroraHeroStatement", "AuroraPrimaryCTA"])
    
    assert plan.target_surface == "landing"
    assert plan.source_blueprint_hash == compute_blueprint_hash(blueprint)
    
    # Assert core constraints exist in forbidden_decisions
    assert BuilderConstraint.NO_SPATIAL_GENERATION in plan.forbidden_decisions
    assert BuilderConstraint.NO_MOTION_DERIVATION in plan.forbidden_decisions
    
    # Assert capabilities are mapped correctly
    assert BuilderCapability.RENDER_LAYOUT in plan.capabilities
    assert BuilderCapability.INJECT_MOTION_PRIMITIVES in plan.capabilities
    
    # Assert traceability items
    elem_ids = [item.element_id for item in plan.traceability_items]
    assert "AuroraLandingShell" in elem_ids
    assert "AuroraTopNavigation" in elem_ids
    assert "AuroraUseCaseCluster" in elem_ids
    assert "AuroraHeroStatement" in elem_ids
    assert "AuroraPrimaryCTA" in elem_ids
    assert "AuroraLandingShell-styling" in elem_ids

def test_resolve_build_plan_canvas_without_motion():
    resolver = BuildPlanResolver()
    blueprint = create_mock_blueprint(ExperienceSurface.CANVAS)
    blueprint.motion_strategy = MotionStrategy.NONE # Disable motion
    
    plan = resolver.resolve_build_plan(blueprint, proposed_components=["AuroraSidebar"])
    
    assert plan.target_surface == "canvas"
    
    # Assert motion capability is disabled
    assert BuilderCapability.INJECT_MOTION_PRIMITIVES not in plan.capabilities
    
    # Assert element IDs
    elem_ids = [item.element_id for item in plan.traceability_items]
    assert "AuroraLandingShell" in elem_ids
    assert "motion_primitives" not in elem_ids
    assert "AuroraSidebar" in elem_ids

def test_resolve_build_plan_dashboard():
    resolver = BuildPlanResolver()
    blueprint = create_mock_blueprint(ExperienceSurface.DASHBOARD)
    
    plan = resolver.resolve_build_plan(blueprint)
    
    assert plan.target_surface == "dashboard"
    assert len(plan.traceability_items) >= 3

def test_resolve_build_plan_portal():
    resolver = BuildPlanResolver()
    blueprint = create_mock_blueprint(ExperienceSurface.PORTAL)
    
    plan = resolver.resolve_build_plan(blueprint)
    
    assert plan.target_surface == "portal"
    assert len(plan.traceability_items) >= 3

def test_invalid_blueprint_fails():
    resolver = BuildPlanResolver()
    
    with pytest.raises(ValueError) as exc_info:
        resolver.resolve_build_plan(None)
    assert "Blueprint cannot be None" in str(exc_info.value)
    
    # Blueprint missing surface_type
    class BadBlueprint:
        pass
    bad_bp = BadBlueprint()
    with pytest.raises(ValueError) as exc_info:
        resolver.resolve_build_plan(bad_bp)
    assert "ExperienceBlueprint has no surface_type" in str(exc_info.value)

def test_traceability_authority_level_preserved():
    resolver = BuildPlanResolver()
    blueprint = create_mock_blueprint(ExperienceSurface.LANDING)
    
    plan = resolver.resolve_build_plan(blueprint)
    
    # Assert that all architectural traceability items belong to experience_architect
    for item in plan.traceability_items:
        if item.authority_level == "architectural":
            assert item.decision_owner == "experience_architect"
            assert item.blueprint_source is not None
        elif item.authority_level == "implementation":
            assert item.decision_owner == "stories_builder"
