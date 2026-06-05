import sys
import os
import pytest
import uuid
import json
from pathlib import Path
from pydantic import ValidationError

# Ensure correct path discovery for contracts and sibling files
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.extend([
    os.path.abspath(os.path.join(current_dir, "../frontend_synthesis/contracts")),
    os.path.abspath(os.path.join(current_dir, "../frontend_synthesis/factory")),
    os.path.abspath(os.path.join(current_dir, "../frontend_synthesis/orchestrator")),
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
from stories_builder_contracts import StoriesBuildPlan, BuilderConstraint, BuilderCapability
from factory_agent import generate_ui_tree, SafeDegradedNode
from alvaro_contracts import FrontendCodeSpec, TailwindThemeSpec, ComponentRequirement, ScaffoldingResolution
from sandbox_contracts import PipelinePausedException, DiagnosticFinding
from promote import promote_candidate

def create_blueprint(
    surface=ExperienceSurface.LANDING,
    nav=NavigationStrategy.STANDARD,
    spatial=SpatialStrategy.CLEAN_BENTO,
    motion=MotionStrategy.SUBTLE_TRANSITIONS
) -> ExperienceBlueprint:
    return ExperienceBlueprint(
        surface_type=surface,
        navigation_strategy=nav,
        motion_strategy=motion,
        spatial_strategy=spatial,
        attention_strategy=AttentionStrategy.FOCAL_HIERARCHY,
        narrative_strategy=NarrativeStrategy.STANDARD,
        interaction_density="medium",
        visual_energy="low",
        immersion_level="high",
        rationale="Blueprint for testing alignment."
    )

def create_code_spec(components, blueprint=None) -> FrontendCodeSpec:
    return FrontendCodeSpec(
        spec_id=f"SPEC-{uuid.uuid4().hex[:4].upper()}",
        derived_from_draft_id="DRAFT-123",
        theme_config=TailwindThemeSpec(
            colors={"base-surface": "#FFFFFF", "text-primary": "#000000", "action-primary": "#4A3FF4", "accent": "#4F46E5"},
            fontFamily={"sans": ["Inter", "sans-serif"]},
            fontSize={"body": "1rem"}
        ),
        component_registry=[
            ComponentRequirement(
                component_name=c, 
                required_variants=["default"], 
                is_core_library=True,
                transformed_text="Test Component Description"
            ) for c in components
        ],
        component_alerts=[],
        debt_tracking=ScaffoldingResolution(target_os="OS-003", pending_injectors=[], resolution_status="RESOLVED"),
        ready_for_factory=True,
        blueprint=blueprint
    )

def test_generate_ui_tree_accepts_valid_stories_plan():
    blueprint = create_blueprint()
    resolver = BuildPlanResolver()
    proposed = ["AuroraLandingShell", "AuroraTopNavigation", "AuroraHeroStatement", "AuroraButton"]
    plan = resolver.resolve_build_plan(blueprint, proposed_components=proposed)
    spec = create_code_spec(proposed, blueprint=blueprint)

    tree = generate_ui_tree(spec, stories_plan=plan, compatibility_mode=False)
    assert tree is not None
    assert tree.layout_selection.profile == "bento_grid" # clean_bento maps to bento_grid
    assert tree.layout_selection.source_signals == ["stories_plan"]

def test_generate_ui_tree_missing_plan_raises_stories_plan_missing():
    blueprint = create_blueprint()
    proposed = ["AuroraLandingShell"]
    spec = create_code_spec(proposed, blueprint=blueprint)

    with pytest.raises(PipelinePausedException) as exc:
        generate_ui_tree(spec, stories_plan=None, compatibility_mode=False)
    
    assert "STORIES_PLAN_MISSING" in str(exc.value)
    assert exc.value.findings[0].code == "STORIES_PLAN_MISSING"

def test_generate_ui_tree_blueprint_hash_mismatch():
    blueprint_a = create_blueprint(spatial=SpatialStrategy.CLEAN_BENTO)
    blueprint_b = create_blueprint(spatial=SpatialStrategy.STANDARD)
    
    resolver = BuildPlanResolver()
    plan = resolver.resolve_build_plan(blueprint_a, proposed_components=["AuroraLandingShell"])
    
    # spec holds blueprint_b while plan was resolved from blueprint_a
    spec = create_code_spec(["AuroraLandingShell"], blueprint=blueprint_b)

    with pytest.raises(PipelinePausedException) as exc:
        generate_ui_tree(spec, stories_plan=plan, compatibility_mode=False)

    assert exc.value.findings[0].code == "SOURCE_BLUEPRINT_HASH_MISSING"

def test_generate_ui_tree_untraced_component_raises_untraced_implementation():
    blueprint = create_blueprint()
    resolver = BuildPlanResolver()
    plan = resolver.resolve_build_plan(blueprint, proposed_components=["AuroraLandingShell"])
    
    # AuroraButton is in spec but not in plan (untraced implementation component)
    spec = create_code_spec(["AuroraLandingShell", "AuroraButton"], blueprint=blueprint)

    with pytest.raises(PipelinePausedException) as exc:
        generate_ui_tree(spec, stories_plan=plan, compatibility_mode=False)

    assert exc.value.findings[0].code == "STORIES_UNTRACED_IMPLEMENTATION"
    assert exc.value.findings[0].severity == "P1"

def test_generate_ui_tree_untraced_layout_raises_builder_architecture_leak():
    blueprint = create_blueprint()
    resolver = BuildPlanResolver()
    plan = resolver.resolve_build_plan(blueprint, proposed_components=["AuroraLandingShell"])
    
    # AuroraCard is a layout component, untraced in the plan
    spec = create_code_spec(["AuroraLandingShell", "AuroraCard"], blueprint=blueprint)

    with pytest.raises(PipelinePausedException) as exc:
        generate_ui_tree(spec, stories_plan=plan, compatibility_mode=False)

    assert exc.value.findings[0].code == "BUILDER_ARCHITECTURE_LEAK"
    assert exc.value.findings[0].severity == "P0"

def test_generate_ui_tree_architectural_fallback_blocked():
    # Blueprint navigation_strategy is none / no navigation allowed
    blueprint = create_blueprint(nav=NavigationStrategy.MINIMAL_CHROME) # using standard/minimal
    # Force navigation strategy value to none to simulate architectural restriction
    blueprint.navigation_strategy = "none"

    resolver = BuildPlanResolver()
    plan = resolver.resolve_build_plan(blueprint, proposed_components=["AuroraLandingShell"])
    
    # Spec attempts to generate AuroraTopNavigation when strategy is none
    spec = create_code_spec(["AuroraLandingShell", "AuroraTopNavigation"], blueprint=blueprint)

    with pytest.raises(PipelinePausedException) as exc:
        generate_ui_tree(spec, stories_plan=plan, compatibility_mode=False)

    assert "BUILDER_ARCHITECTURE_LEAK" in str(exc.value)
    assert exc.value.findings[0].code == "BUILDER_ARCHITECTURE_LEAK"

def test_generate_ui_tree_implementation_fallback_allowed_with_trace():
    blueprint = create_blueprint()
    resolver = BuildPlanResolver()
    # AuroraTable is in SUPPORTED_COMPONENTS but unimplemented (falls back to SafeDegradedNode)
    plan = resolver.resolve_build_plan(blueprint, proposed_components=["AuroraLandingShell", "AuroraTable"])
    spec = create_code_spec(["AuroraLandingShell", "AuroraTable"], blueprint=blueprint)

    tree = generate_ui_tree(spec, stories_plan=plan, compatibility_mode=False)
    assert tree is not None
    
    # Find degraded node in children
    degraded = None
    # Traverse to find SafeDegradedNode
    def find_degraded(node):
        nonlocal degraded
        if isinstance(node, SafeDegradedNode) or node.fallback_used:
            degraded = node
            return
        for child in node.children:
            find_degraded(child)
            
    find_degraded(tree.root_node)
    assert degraded is not None
    assert degraded.fallback_used is True
    assert degraded.blueprint_source == "surface_type"
    assert degraded.decision_owner == "stories_builder"
    assert degraded.authority_level == "implementation"

def test_generate_ui_tree_degraded_architectural_component_raises_leak():
    blueprint = create_blueprint()
    resolver = BuildPlanResolver()
    # Let's say we have an architectural component not implemented or degraded
    # To simulate this, we can force a layout component to degrade
    # We will instantiate a UINode that is a layout type and force fallback_used = True
    spec = create_code_spec(["AuroraLandingShell"], blueprint=blueprint)
    plan = resolver.resolve_build_plan(blueprint, proposed_components=["AuroraLandingShell"])
    
    # Since we can't easily force degradation of implemented layout components in normal loop,
    # we can intercept and inject a degraded layout node in the tree manually inside a custom test block
    # or test that the validate_and_trace_node raises P0 if fallback_used is set on layout
    from factory_contracts import UINode
    root_node = UINode(
        node_id="test",
        component_name="AuroraLandingShell",
        semantic_role="presentation",
        fallback_used=True,
        fallback_reason="Degraded layout test",
        blueprint_source="surface_type"
    )
    
    # We can invoke the validation traversal function directly to prove the rule holds!
    # In factory_agent, the validate_and_trace_node checks is_degraded and original_is_arch
    # Let's construct a SafeDegradedNode directly
    degraded_layout = SafeDegradedNode(
        node_id="degraded-layout",
        component_name="div",
        semantic_role="presentation",
        props={"originalComponent": "AuroraLandingShell"},
        fallback_used=True,
        fallback_reason="Degraded layout test",
        blueprint_source="surface_type",
        decision_owner="stories_builder",
        authority_level="implementation"
    )
    
    from factory_agent import generate_ui_tree
    # Let's run a test where the code spec has a layout component that falls back.
    # To simulate layout component fallback, let's pass an unimplemented layout component that starts with Aurora, e.g. AuroraSidebar (which is in SUPPORTED_COMPONENTS but unimplemented in loop)
    plan = resolver.resolve_build_plan(blueprint, proposed_components=["AuroraLandingShell", "AuroraSidebar"])
    spec = create_code_spec(["AuroraLandingShell", "AuroraSidebar"], blueprint=blueprint)
    
    with pytest.raises(PipelinePausedException) as exc:
        generate_ui_tree(spec, stories_plan=plan, compatibility_mode=False)
        
    assert exc.value.findings[0].code == "BUILDER_ARCHITECTURE_LEAK"
    assert "SafeDegradedNode cannot be used for architectural component" in exc.value.findings[0].redacted_message

def test_promote_py_blocks_synthetic(tmp_path):
    candidate_dir = tmp_path / "candidate"
    candidate_dir.mkdir()
    
    # Write synthetic promotion metadata
    meta = {
        "promotion_allowed": False,
        "human_promotion_allowed": False,
        "candidate_status": "NON_PROMOTABLE_FIXTURE"
    }
    with open(candidate_dir / "promotion_metadata.json", "w") as f:
        json.dump(meta, f)
        
    # Attempting to promote this candidate must exit with 1
    with pytest.raises(SystemExit) as exc:
        promote_candidate(str(tmp_path))
    assert exc.value.code == 1
