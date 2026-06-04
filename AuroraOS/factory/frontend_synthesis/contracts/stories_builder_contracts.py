import re
from datetime import datetime
from enum import Enum
from typing import List, Optional, Literal, Any
from pydantic import BaseModel, Field, field_validator, model_validator

class BuilderCapability(str, Enum):
    RENDER_LAYOUT = "render_layout"
    BIND_STYLES = "bind_styles"
    INJECT_MOTION_PRIMITIVES = "inject_motion_primitives"
    HYDRATE_TEXTS = "hydrate_texts"
    COMPILE_TSX = "compile_tsx"
    ASSEMBLE_COMPONENT_TREE = "assemble_component_tree"
    PREPARE_RENDER_BUNDLE = "prepare_render_bundle"
    BIND_ACCESSIBILITY_ATTRIBUTES = "bind_accessibility_attributes"

class BuilderConstraint(str, Enum):
    NO_SPATIAL_GENERATION = "no_spatial_generation"
    NO_MOTION_DERIVATION = "no_motion_derivation"
    NO_NAVIGATION_ORIGIN = "no_navigation_origin"
    NO_THEME_DEFINITION = "no_theme_definition"
    NO_NARRATIVE_STRATEGY_DEFINITION = "no_narrative_strategy_definition"
    NO_ATTENTION_STRATEGY_DEFINITION = "no_attention_strategy_definition"
    NO_REFERENCE_RAW_CONSUMPTION = "no_reference_raw_consumption"
    NO_UNTRACED_COMPONENT_CREATION = "no_untraced_component_creation"
    NO_UNAPPROVED_ASSET_REUSE = "no_unapproved_asset_reuse"

class BuildPlanTraceabilityItem(BaseModel):
    element_id: str = Field(..., description="Unique ID of the generated element (e.g., node, component, container)")
    element_type: Literal["component", "layout", "motion", "navigation", "copy"] = Field(..., description="Element type category")
    blueprint_source: Optional[str] = Field(None, description="The specific field source in the blueprint (e.g., spatial_strategy, motion_strategy)")
    decision_owner: Literal["experience_architect", "stories_builder", "qa_gate"] = Field(..., description="The owner responsible for this decision")
    authority_level: Literal["architectural", "implementation", "validation"] = Field(..., description="Level of decision authority")

    @model_validator(mode='after')
    def validate_architectural_authority(self) -> 'BuildPlanTraceabilityItem':
        if self.authority_level == "architectural" and self.decision_owner != "experience_architect":
            raise ValueError("BUILDER_ARCHITECTURE_LEAK: Architectural decisions must be owned by the experience_architect.")
        return self

class StoriesBuildPlan(BaseModel):
    plan_id: str = Field(..., description="Unique ID for this build plan")
    source_blueprint_id: str = Field(..., description="The ID of the source ExperienceBlueprint")
    source_blueprint_hash: str = Field(..., description="SHA256 signature linking this plan to the physical blueprint")
    target_surface: str = Field(..., description="Target layout surface (e.g., landing, crm, dashboard)")
    capabilities: List[BuilderCapability] = Field(..., description="Set of allowed builder execution capabilities")
    forbidden_decisions: List[BuilderConstraint] = Field(..., description="Architectural restrictions applied to this builder")
    traceability_items: List[BuildPlanTraceabilityItem] = Field(..., description="Traceability map linking implementation back to blueprint decisions")
    generated_at: datetime = Field(default_factory=datetime.now)

    @field_validator('forbidden_decisions')
    @classmethod
    def validate_core_constraints(cls, v: List[BuilderConstraint]) -> List[BuilderConstraint]:
        required = {
            BuilderConstraint.NO_SPATIAL_GENERATION,
            BuilderConstraint.NO_MOTION_DERIVATION,
            BuilderConstraint.NO_NAVIGATION_ORIGIN,
            BuilderConstraint.NO_THEME_DEFINITION
        }
        missing = required - set(v)
        if missing or not v:
            raise ValueError(f"BUILDER_CONSTRAINTS_MISSING: The build plan must enforce the core architectural constraints. Missing: {[m.value for m in missing]}")
        return v

class StoriesBuilderGateFinding(BaseModel):
    code: Literal["BUILDER_ARCHITECTURE_LEAK", "STORIES_UNTRACED_IMPLEMENTATION", "BUILDER_CONSTRAINTS_MISSING", "INFO_TRACE_COMPLETE", "MISSING_OPTIONAL_TRACE"]
    severity: Literal["P0", "P1", "P2", "P3"]
    message: str
    element_id: Optional[str] = None

class StoriesBuilderGateReport(BaseModel):
    verified_at: datetime = Field(default_factory=datetime.now)
    findings: List[StoriesBuilderGateFinding] = Field(default_factory=list)
    status: Literal["passed", "failed"]
