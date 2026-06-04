import json
import os
import sys
from pathlib import Path
from typing import List, Optional, Any

# Ensure sandbox and contracts are in Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.extend([
    os.path.abspath(os.path.join(current_dir, "../../sandbox")),
    os.path.abspath(os.path.join(current_dir, "../contracts"))
])

from sandbox_contracts import PipelinePausedException, DiagnosticFinding
from experience_architecture_contracts import ExperienceBlueprint, ExperienceArchitectureReport

class ExperienceArchitectureGate:
    """
    Validates that the Experience Blueprint exists, is complete, valid, 
    and has audit metadata.
    """
    def evaluate(self, blueprint: Any) -> None:
        findings = []
        if not blueprint:
            findings.append(DiagnosticFinding(
                severity="P0",
                code="BLUEPRINT_MISSING",
                redacted_message="Experience Blueprint is null or missing.",
                file_path="experience_blueprint.json",
                line_number=0,
                recommended_action="Ensure the Experience Architect agent runs."
            ))
            raise PipelinePausedException("ExperienceArchitectureGate: Blueprint missing.", findings)
            
        required_fields = [
            "surface_type", "navigation_strategy", "motion_strategy", 
            "spatial_strategy", "attention_strategy", "narrative_strategy",
            "interaction_density", "visual_energy", "immersion_level"
        ]
        for field in required_fields:
            if not getattr(blueprint, field, None):
                findings.append(DiagnosticFinding(
                    severity="P0",
                    code="BLUEPRINT_INCOMPLETE",
                    redacted_message=f"Experience Blueprint field '{field}' is missing or empty.",
                    file_path="experience_blueprint.json",
                    line_number=0,
                    recommended_action="Ensure all enum values match experience_architecture_contracts specifications."
                ))
                
        if findings:
            raise PipelinePausedException("ExperienceArchitectureGate: Blueprint validation failed.", findings)

    def evaluate_sandbox_files(self, sandbox_dir_path: str) -> None:
        sandbox_dir = Path(sandbox_dir_path)
        blueprint_file = sandbox_dir / "experience_blueprint.json"
        
        findings = []
        
        # Check if the blueprint file exists
        if not blueprint_file.exists():
            findings.append(DiagnosticFinding(
                severity="P0",
                code="BLUEPRINT_MISSING",
                redacted_message="Experience Blueprint is missing in sandbox.",
                file_path="experience_blueprint.json",
                line_number=0,
                recommended_action="Ensure the Experience Architect task runs and generates experience_blueprint.json."
            ))
            raise PipelinePausedException("ExperienceArchitectureGate: Blueprint missing.", findings)
            
        try:
            with open(blueprint_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            findings.append(DiagnosticFinding(
                severity="P0",
                code="BLUEPRINT_INVALID_JSON",
                redacted_message=f"Experience Blueprint has invalid JSON structure: {e}",
                file_path="experience_blueprint.json",
                line_number=0,
                recommended_action="Fix syntax issues in generated experience_blueprint.json."
            ))
            raise PipelinePausedException("ExperienceArchitectureGate: Invalid JSON.", findings)
            
        # Validate using Pydantic
        try:
            if "blueprint" in data:
                report = ExperienceArchitectureReport(**data)
                blueprint = report.blueprint
                rationale = report.rationale
            else:
                blueprint = ExperienceBlueprint(**data)
                rationale = "Direct blueprint validation."
                
            # Auditability check
            if not rationale or len(rationale.strip()) < 10:
                findings.append(DiagnosticFinding(
                    severity="P1",
                    code="BLUEPRINT_NOT_AUDITABLE",
                    redacted_message="Experience Blueprint has missing or insufficient design rationale for audit.",
                    file_path="experience_blueprint.json",
                    line_number=0,
                    recommended_action="Provide a detailed rationale in the Experience Architecture report."
                ))
        except Exception as e:
            findings.append(DiagnosticFinding(
                severity="P0",
                code="BLUEPRINT_SCHEMA_VIOLATION",
                redacted_message=f"Experience Blueprint schema validation failed: {e}",
                file_path="experience_blueprint.json",
                line_number=0,
                recommended_action="Ensure all enum values match experience_architecture_contracts specifications."
            ))
            
        if findings:
            raise PipelinePausedException("ExperienceArchitectureGate: Blueprint validation failed.", findings)

class ArchitectureCoverageGate:
    """
    Validates that essential strategies (Navigation, Motion, Spatial, Narrative) 
    are fully defined in the blueprint.
    """
    def evaluate(self, blueprint: Any) -> None:
        findings = []
        
        if not getattr(blueprint, "navigation_strategy", None):
            findings.append(DiagnosticFinding(
                severity="P1",
                code="MISSING_NAVIGATION_STRATEGY",
                redacted_message="Navigation Strategy is not defined in the Experience Blueprint.",
                file_path="experience_blueprint.json",
                line_number=0,
                recommended_action="Ensure the Experience Architect assigns a valid NavigationStrategy."
            ))
            
        if not getattr(blueprint, "motion_strategy", None):
            findings.append(DiagnosticFinding(
                severity="P1",
                code="MISSING_MOTION_STRATEGY",
                redacted_message="Motion Strategy is not defined in the Experience Blueprint.",
                file_path="experience_blueprint.json",
                line_number=0,
                recommended_action="Ensure the Experience Architect assigns a valid MotionStrategy."
            ))
            
        if not getattr(blueprint, "spatial_strategy", None):
            findings.append(DiagnosticFinding(
                severity="P1",
                code="MISSING_SPATIAL_STRATEGY",
                redacted_message="Spatial Strategy is not defined in the Experience Blueprint.",
                file_path="experience_blueprint.json",
                line_number=0,
                recommended_action="Ensure the Experience Architect assigns a valid SpatialStrategy."
            ))
            
        if not getattr(blueprint, "narrative_strategy", None):
            findings.append(DiagnosticFinding(
                severity="P1",
                code="MISSING_NARRATIVE_STRATEGY",
                redacted_message="Narrative Strategy is not defined in the Experience Blueprint.",
                file_path="experience_blueprint.json",
                line_number=0,
                recommended_action="Ensure the Experience Architect assigns a valid NarrativeStrategy."
            ))
            
        if findings:
            raise PipelinePausedException("ArchitectureCoverageGate: Coverage validation failed.", findings)
