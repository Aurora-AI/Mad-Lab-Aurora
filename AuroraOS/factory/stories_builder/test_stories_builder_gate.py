import sys
import os
import pytest
from datetime import datetime
from pydantic import ValidationError

# Ensure correct path discovery for contracts
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.extend([
    os.path.abspath(os.path.join(current_dir, "../frontend_synthesis/contracts")),
    os.path.abspath(os.path.join(current_dir, "../contracts")),
    os.path.abspath(current_dir)
])

from build_plan_resolver import BuildPlanResolver, compute_blueprint_hash
from stories_builder_gate import StoriesBuilderGate
from experience_architecture_contracts import (
    ExperienceBlueprint,
    ExperienceSurface,
    NavigationStrategy,
    MotionStrategy,
    SpatialStrategy,
    AttentionStrategy,
    NarrativeStrategy
)
from stories_builder_contracts import (
    StoriesBuildPlan,
    BuildPlanTraceabilityItem,
    BuilderConstraint,
    BuilderCapability
)

def create_mock_blueprint() -> ExperienceBlueprint:
    return ExperienceBlueprint(
        surface_type=ExperienceSurface.LANDING,
        navigation_strategy=NavigationStrategy.STANDARD,
        motion_strategy=MotionStrategy.SUBTLE_TRANSITIONS,
        spatial_strategy=SpatialStrategy.CLEAN_BENTO,
        attention_strategy=AttentionStrategy.FOCAL_HIERARCHY,
        narrative_strategy=NarrativeStrategy.STANDARD,
        interaction_density="medium",
        visual_energy="low",
        immersion_level="high",
        rationale="Mock blueprint for testing."
    )

def test_gate_approves_valid_plan():
    resolver = BuildPlanResolver()
    gate = StoriesBuilderGate()
    blueprint = create_mock_blueprint()
    
    plan = resolver.resolve_build_plan(blueprint, proposed_components=["AuroraHero", "AuroraButton"])
    report = gate.validate_build_plan(plan, blueprint)
    
    assert report.status == "passed"
    # Verify serializability
    assert report.model_dump_json() is not None
    
    # Must have info trace complete and valid info findings
    finding_codes = [f.code for f in report.findings]
    assert "INFO_TRACE_COMPLETE" in finding_codes
    assert "INFO_BUILD_PLAN_VALID" in finding_codes

def test_gate_blocks_hash_mismatch():
    resolver = BuildPlanResolver()
    gate = StoriesBuilderGate()
    blueprint = create_mock_blueprint()
    
    plan = resolver.resolve_build_plan(blueprint)
    
    # Modify blueprint to simulate mismatch after plan resolution
    another_blueprint = create_mock_blueprint()
    another_blueprint.immersion_level = "low" # different hash
    
    report = gate.validate_build_plan(plan, another_blueprint)
    
    assert report.status == "failed"
    finding_codes = [f.code for f in report.findings]
    assert "SOURCE_BLUEPRINT_HASH_MISSING" in finding_codes

def test_gate_blocks_builder_architecture_leak():
    gate = StoriesBuilderGate()
    blueprint = create_mock_blueprint()
    bp_hash = compute_blueprint_hash(blueprint)
    
    # Manually build a plan containing a leaked item (Pydantic model validation bypassed or manually instantiated if possible, or validated by gate)
    # Wait, the contracts file blocks authority_level == "architectural" and decision_owner == "stories_builder" at Pydantic level!
    # So we verify that Pydantic blocks it first, or that the gate catches it.
    with pytest.raises(ValidationError) as exc_info:
        BuildPlanTraceabilityItem(
            element_id="AuroraShell",
            element_type="layout",
            blueprint_source="spatial_strategy",
            decision_owner="stories_builder", # Leak!
            authority_level="architectural"
        )
    assert "BUILDER_ARCHITECTURE_LEAK" in str(exc_info.value)

def test_gate_blocks_raw_reference_authority_leak():
    gate = StoriesBuilderGate()
    blueprint = create_mock_blueprint()
    bp_hash = compute_blueprint_hash(blueprint)
    
    # Item with raw URL as blueprint_source
    item = BuildPlanTraceabilityItem(
        element_id="AuroraLandingShell",
        element_type="layout",
        blueprint_source="https://raw.githubusercontent.com/benchmark", # Raw leak!
        decision_owner="experience_architect",
        authority_level="architectural"
    )
    
    plan = StoriesBuildPlan(
        plan_id="PLAN-LEAK",
        source_blueprint_id="BP-001",
        source_blueprint_hash=bp_hash,
        target_surface="landing",
        capabilities=[BuilderCapability.RENDER_LAYOUT],
        forbidden_decisions=[
            BuilderConstraint.NO_SPATIAL_GENERATION,
            BuilderConstraint.NO_MOTION_DERIVATION,
            BuilderConstraint.NO_NAVIGATION_ORIGIN,
            BuilderConstraint.NO_THEME_DEFINITION
        ],
        traceability_items=[item]
    )
    
    report = gate.validate_build_plan(plan, blueprint)
    
    assert report.status == "failed"
    finding_codes = [f.code for f in report.findings]
    assert "RAW_REFERENCE_AUTHORITY_LEAK" in finding_codes

def test_gate_blocks_auto_promotion_attempt():
    gate = StoriesBuilderGate()
    blueprint = create_mock_blueprint()
    bp_hash = compute_blueprint_hash(blueprint)
    
    item = BuildPlanTraceabilityItem(
        element_id="Auto-Promote-Core-Fidelity", # Auto promotion attempt!
        element_type="component",
        blueprint_source="surface_type",
        decision_owner="qa_gate",
        authority_level="validation"
    )
    
    plan = StoriesBuildPlan(
        plan_id="PLAN-AUTO",
        source_blueprint_id="BP-001",
        source_blueprint_hash=bp_hash,
        target_surface="landing",
        capabilities=[BuilderCapability.RENDER_LAYOUT],
        forbidden_decisions=[
            BuilderConstraint.NO_SPATIAL_GENERATION,
            BuilderConstraint.NO_MOTION_DERIVATION,
            BuilderConstraint.NO_NAVIGATION_ORIGIN,
            BuilderConstraint.NO_THEME_DEFINITION
        ],
        traceability_items=[item]
    )
    
    report = gate.validate_build_plan(plan, blueprint)
    
    assert report.status == "failed"
    finding_codes = [f.code for f in report.findings]
    assert "AUTO_PROMOTION_ATTEMPT" in finding_codes

def test_gate_blocks_missing_constraints():
    gate = StoriesBuilderGate()
    blueprint = create_mock_blueprint()
    bp_hash = compute_blueprint_hash(blueprint)
    
    # Bypass Pydantic validator of StoriesBuildPlan by catching validation error when creating it with missing constraints
    with pytest.raises(ValidationError) as exc_info:
        StoriesBuildPlan(
            plan_id="PLAN-BAD",
            source_blueprint_id="BP-001",
            source_blueprint_hash=bp_hash,
            target_surface="landing",
            capabilities=[BuilderCapability.RENDER_LAYOUT],
            forbidden_decisions=[BuilderConstraint.NO_SPATIAL_GENERATION], # missing other core constraints!
            traceability_items=[]
        )
    assert "BUILDER_CONSTRAINTS_MISSING" in str(exc_info.value)

def test_gate_reports_missing_responsive_or_performance_budgets():
    gate = StoriesBuilderGate()
    blueprint = create_mock_blueprint()
    bp_hash = compute_blueprint_hash(blueprint)
    
    # Motion element without performance budget (missing immersion_level or visual_energy source)
    motion_item = BuildPlanTraceabilityItem(
        element_id="AuroraSphereMotion",
        element_type="motion",
        blueprint_source="surface_type", # Not immersion_level!
        decision_owner="experience_architect",
        authority_level="architectural"
    )
    
    # Layout element without responsive strategy (missing spatial_strategy or surface_type source)
    layout_item = BuildPlanTraceabilityItem(
        element_id="AuroraGrid",
        element_type="layout",
        blueprint_source="narrative_strategy", # Not spatial_strategy!
        decision_owner="experience_architect",
        authority_level="architectural"
    )
    
    plan = StoriesBuildPlan(
        plan_id="PLAN-P1",
        source_blueprint_id="BP-001",
        source_blueprint_hash=bp_hash,
        target_surface="landing",
        capabilities=[BuilderCapability.RENDER_LAYOUT],
        forbidden_decisions=[
            BuilderConstraint.NO_SPATIAL_GENERATION,
            BuilderConstraint.NO_MOTION_DERIVATION,
            BuilderConstraint.NO_NAVIGATION_ORIGIN,
            BuilderConstraint.NO_THEME_DEFINITION
        ],
        traceability_items=[motion_item, layout_item]
    )
    
    report = gate.validate_build_plan(plan, blueprint)
    
    assert report.status == "failed"
    finding_codes = [f.code for f in report.findings]
    assert "MOTION_WITHOUT_PERFORMANCE_BUDGET" in finding_codes
    assert "LAYOUT_WITHOUT_RESPONSIVE_STRATEGY" in finding_codes

def test_gate_warns_weak_description():
    gate = StoriesBuilderGate()
    blueprint = create_mock_blueprint()
    bp_hash = compute_blueprint_hash(blueprint)
    
    item = BuildPlanTraceabilityItem(
        element_id="x", # Weak description!
        element_type="component",
        blueprint_source="surface_type",
        decision_owner="experience_architect",
        authority_level="architectural"
    )
    
    plan = StoriesBuildPlan(
        plan_id="PLAN-P2",
        source_blueprint_id="BP-001",
        source_blueprint_hash=bp_hash,
        target_surface="landing",
        capabilities=[BuilderCapability.RENDER_LAYOUT],
        forbidden_decisions=[
            BuilderConstraint.NO_SPATIAL_GENERATION,
            BuilderConstraint.NO_MOTION_DERIVATION,
            BuilderConstraint.NO_NAVIGATION_ORIGIN,
            BuilderConstraint.NO_THEME_DEFINITION
        ],
        traceability_items=[item]
    )
    
    report = gate.validate_build_plan(plan, blueprint)
    # Status should be passed since P2 is warning not blocker
    assert report.status == "passed"
    finding_codes = [f.code for f in report.findings]
    assert "WEAK_TRACEABILITY_DESCRIPTION" in finding_codes
