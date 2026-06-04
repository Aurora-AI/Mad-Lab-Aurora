import pytest
from datetime import datetime
from pydantic import ValidationError
from stories_builder_contracts import (
    BuilderCapability,
    BuilderConstraint,
    BuildPlanTraceabilityItem,
    StoriesBuildPlan,
    StoriesBuilderGateFinding,
    StoriesBuilderGateReport
)

def create_valid_build_plan_dict() -> dict:
    return {
        "plan_id": "PLAN-001",
        "source_blueprint_id": "BP-001",
        "source_blueprint_hash": "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b",
        "target_surface": "landing",
        "capabilities": [
            "render_layout",
            "bind_styles",
            "hydrate_texts",
            "compile_tsx"
        ],
        "forbidden_decisions": [
            "no_spatial_generation",
            "no_motion_derivation",
            "no_navigation_origin",
            "no_theme_definition",
            "no_untraced_component_creation"
        ],
        "traceability_items": [
            {
                "element_id": "AuroraNavbar-1",
                "element_type": "navigation",
                "blueprint_source": "navigation_strategy",
                "decision_owner": "experience_architect",
                "authority_level": "architectural"
            },
            {
                "element_id": "AuroraUseCaseCluster-bento",
                "element_type": "layout",
                "blueprint_source": "spatial_strategy",
                "decision_owner": "experience_architect",
                "authority_level": "architectural"
            },
            {
                "element_id": "AuroraButton-submit",
                "element_type": "component",
                "blueprint_source": "interaction_density",
                "decision_owner": "stories_builder",
                "authority_level": "implementation"
            }
        ],
        "generated_at": datetime.now().isoformat()
    }

def test_stories_build_plan_serialization():
    valid_data = create_valid_build_plan_dict()
    plan = StoriesBuildPlan(**valid_data)
    
    assert plan.plan_id == "PLAN-001"
    assert plan.source_blueprint_id == "BP-001"
    assert plan.source_blueprint_hash.startswith("6b86b2")
    assert len(plan.traceability_items) == 3
    
    # Assert JSON roundtrip
    json_data = plan.model_dump_json()
    parsed_plan = StoriesBuildPlan.model_validate_json(json_data)
    assert parsed_plan.plan_id == plan.plan_id
    assert parsed_plan.source_blueprint_hash == plan.source_blueprint_hash

def test_required_fields():
    data = create_valid_build_plan_dict()
    
    # Missing source_blueprint_id
    bad_data_1 = data.copy()
    del bad_data_1["source_blueprint_id"]
    with pytest.raises(ValidationError) as exc_info:
        StoriesBuildPlan(**bad_data_1)
    assert "Field required" in str(exc_info.value)
    
    # Missing source_blueprint_hash
    bad_data_2 = data.copy()
    del bad_data_2["source_blueprint_hash"]
    with pytest.raises(ValidationError) as exc_info:
        StoriesBuildPlan(**bad_data_2)
    assert "Field required" in str(exc_info.value)

def test_forbidden_decisions_required_and_minimum_constraints():
    data = create_valid_build_plan_dict()
    
    # Empty forbidden decisions
    bad_data_1 = data.copy()
    bad_data_1["forbidden_decisions"] = []
    with pytest.raises(ValidationError) as exc_info:
        StoriesBuildPlan(**bad_data_1)
    assert "BUILDER_CONSTRAINTS_MISSING" in str(exc_info.value)

    # Missing core constraint (no_theme_definition missing)
    bad_data_2 = data.copy()
    bad_data_2["forbidden_decisions"] = [
        "no_spatial_generation",
        "no_motion_derivation",
        "no_navigation_origin"
    ]
    with pytest.raises(ValidationError) as exc_info:
        StoriesBuildPlan(**bad_data_2)
    assert "BUILDER_CONSTRAINTS_MISSING" in str(exc_info.value)
    assert "no_theme_definition" in str(exc_info.value)

def test_traceability_architectural_leak():
    # If authority_level == architectural and decision_owner is stories_builder, validation fails (P0)
    with pytest.raises(ValidationError) as exc_info:
        BuildPlanTraceabilityItem(
            element_id="AuroraLandingShell-1",
            element_type="layout",
            blueprint_source="spatial_strategy",
            decision_owner="stories_builder", # Leak!
            authority_level="architectural"
        )
    assert "BUILDER_ARCHITECTURE_LEAK" in str(exc_info.value)

def test_traceability_implementation_allowed():
    # Implementation decisions owned by stories_builder are allowed
    item = BuildPlanTraceabilityItem(
        element_id="AuroraCard-1",
        element_type="component",
        blueprint_source="interaction_density",
        decision_owner="stories_builder",
        authority_level="implementation"
    )
    assert item.decision_owner == "stories_builder"
    assert item.authority_level == "implementation"

def test_traceability_untraced_item():
    # Blueprint source is optional in contract validation (so builder can output untraced items which are flagged in gate as P1)
    item = BuildPlanTraceabilityItem(
        element_id="CustomUINode-1",
        element_type="copy",
        blueprint_source=None, # Untraced!
        decision_owner="stories_builder",
        authority_level="implementation"
    )
    assert item.blueprint_source is None

def test_prohibited_capabilities_do_not_exist():
    # Assert prohibited capabilities are not members of the BuilderCapability enum
    prohibited = [
        "choose_layout",
        "derive_motion",
        "define_navigation",
        "define_theme",
        "write_copy_strategy"
    ]
    for cap in prohibited:
        with pytest.raises(ValueError):
            BuilderCapability(cap)

def test_gate_report_structure():
    finding_1 = StoriesBuilderGateFinding(
        code="BUILDER_ARCHITECTURE_LEAK",
        severity="P0",
        message="Builder generated spatial layout independently.",
        element_id="root-1"
    )
    finding_2 = StoriesBuilderGateFinding(
        code="STORIES_UNTRACED_IMPLEMENTATION",
        severity="P1",
        message="Component has no matching blueprint decision.",
        element_id="div-3"
    )
    finding_3 = StoriesBuilderGateFinding(
        code="MISSING_OPTIONAL_TRACE",
        severity="P2",
        message="Optional styling details were not traced.",
        element_id="button-1"
    )
    finding_4 = StoriesBuilderGateFinding(
        code="INFO_TRACE_COMPLETE",
        severity="P3",
        message="Traceability complete."
    )
    
    report = StoriesBuilderGateReport(
        findings=[finding_1, finding_2, finding_3, finding_4],
        status="failed"
    )
    
    assert len(report.findings) == 4
    assert report.status == "failed"
    assert report.findings[0].severity == "P0"
    assert report.findings[1].severity == "P1"
    assert report.findings[2].severity == "P2"
    assert report.findings[3].severity == "P3"
