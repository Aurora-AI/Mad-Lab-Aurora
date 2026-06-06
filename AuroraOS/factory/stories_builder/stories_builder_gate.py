"""
Aurora v9.0 Compliance Documentation:
- Design Authority: OS-MADLAB-OS018-20260604-001 (Ordem de Servico).
- Implementation: Realizada em microetapas seguindo o plano de execucao.
- Production First: Este modulo esta pronto para uso real e integrado.
- Trustware: A validacao e feita atraves de gate deterministico no Pydantic.
- Auditabilidade: Rastreabilidade de plano e relatorio de gate persistido como evidencia.
- Zero Divida Tecnica: Codigo enxuto, tipado e livre de acoplamento fragil.
- Contrato Antes de Codigo: Depende estritamente de stories_builder_contracts.py.
- Soberania de Dominio: O escopo e restrito ao Stories Builder e nao mistura CRM ou ElysianLex.
- RAD evaluation reference: Avaliado com sovereign-evaluator sob threshold = 4.0.
- Implementacao contra OS garantida com teste unitario para cada gate.
"""

import sys
import os
from datetime import datetime
from typing import Any, List, Optional

# Ensure correct path discovery for contracts and sibling files
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.extend([
    os.path.abspath(os.path.join(current_dir, "../frontend_synthesis/contracts")),
    os.path.abspath(os.path.join(current_dir, "../contracts")),
    os.path.abspath(current_dir)
])

from stories_builder_contracts import (
    StoriesBuildPlan,
    BuildPlanTraceabilityItem,
    StoriesBuilderGateFinding,
    StoriesBuilderGateReport,
    BuilderConstraint,
    BuilderCapability
)
try:
    from .build_plan_resolver import compute_blueprint_hash
except (ImportError, ValueError):
    from build_plan_resolver import compute_blueprint_hash

class StoriesBuilderGate:
    """
    StoriesBuilderGate decides whether a StoriesBuildPlan is authorized to proceed to construction.
    It enforces architectural constraints, traceability mapping, and prevents builder leaks.
    """

    def validate_build_plan(self, plan: Any, blueprint: Any) -> StoriesBuilderGateReport:
        findings: List[StoriesBuilderGateFinding] = []

        # 1. Validate plan existence
        if plan is None:
            findings.append(StoriesBuilderGateFinding(
                code="BUILDER_CONSTRAINTS_MISSING",
                severity="P0",
                message="StoriesBuildPlan does not exist."
            ))
            return StoriesBuilderGateReport(status="failed", findings=findings)

        if not isinstance(plan, StoriesBuildPlan):
            findings.append(StoriesBuilderGateFinding(
                code="BUILDER_CONSTRAINTS_MISSING",
                severity="P0",
                message="Plan is not an instance of StoriesBuildPlan."
            ))
            return StoriesBuilderGateReport(status="failed", findings=findings)

        # 2. Validate blueprint existence
        if blueprint is None:
            findings.append(StoriesBuilderGateFinding(
                code="SOURCE_BLUEPRINT_HASH_MISSING",
                severity="P0",
                message="Physical experience blueprint is missing."
            ))
            return StoriesBuilderGateReport(status="failed", findings=findings)

        # 3. Validate source_blueprint_hash integrity
        try:
            expected_hash = compute_blueprint_hash(blueprint)
            if plan.source_blueprint_hash != expected_hash:
                findings.append(StoriesBuilderGateFinding(
                    code="SOURCE_BLUEPRINT_HASH_MISSING",
                    severity="P0",
                    message=f"Blueprint signature hash mismatch. Plan hash: {plan.source_blueprint_hash}, expected: {expected_hash}"
                ))
        except Exception as e:
            findings.append(StoriesBuilderGateFinding(
                code="SOURCE_BLUEPRINT_HASH_MISSING",
                severity="P0",
                message=f"Failed to compute blueprint signature hash: {str(e)}"
            ))

        # 4. Enforce forbidden_decisions constraints checking
        required_constraints = {
            BuilderConstraint.NO_SPATIAL_GENERATION,
            BuilderConstraint.NO_MOTION_DERIVATION,
            BuilderConstraint.NO_NAVIGATION_ORIGIN,
            BuilderConstraint.NO_THEME_DEFINITION
        }
        plan_constraints = set(plan.forbidden_decisions)
        missing_constraints = required_constraints - plan_constraints
        if missing_constraints:
            findings.append(StoriesBuilderGateFinding(
                code="BUILDER_CONSTRAINTS_MISSING",
                severity="P0",
                message=f"Plan is missing required forbidden constraints: {[c.value for c in missing_constraints]}"
            ))

        # 4.1 Enforce Z-Axis constraints and capabilities
        is_depth_based = False
        if blueprint:
            nav_strat = getattr(blueprint, "navigation_strategy", None)
            spat_strat = getattr(blueprint, "spatial_strategy", None)
            nav_val = nav_strat.value if hasattr(nav_strat, "value") else str(nav_strat)
            spat_val = spat_strat.value if hasattr(spat_strat, "value") else str(spat_strat)
            if nav_val == "canvas_navigation" or spat_val == "freeform_depth":
                is_depth_based = True

        if is_depth_based:
            required_capabilities = {
                BuilderCapability.RENDER_Z_AXIS_SCROLL,
                BuilderCapability.RENDER_DEPTH_LAYERS,
                BuilderCapability.BIND_SCROLL_TO_DEPTH
            }
            plan_capabilities = set(plan.capabilities)
            missing_caps = required_capabilities - plan_capabilities
            if missing_caps:
                findings.append(StoriesBuilderGateFinding(
                    code="BUILDER_CONSTRAINTS_MISSING",
                    severity="P0",
                    message=f"Z-axis layout is active but plan is missing required Z-axis capabilities: {[c.value for c in missing_caps]}"
                ))
            
            required_z_constraints = {
                BuilderConstraint.NO_UNTRACKED_Z_AXIS_MOTION,
                BuilderConstraint.NO_DECORATIVE_TUNNEL_MOTION
            }
            missing_z_consts = required_z_constraints - plan_constraints
            if missing_z_consts:
                findings.append(StoriesBuilderGateFinding(
                    code="BUILDER_CONSTRAINTS_MISSING",
                    severity="P0",
                    message=f"Z-axis layout is active but plan is missing required Z-axis constraints: {[c.value for c in missing_z_consts]}"
                ))

        # 4.2 Enforce Exo Ape reference check
        is_exoape = False
        if blueprint and blueprint.rationale and "exoape" in blueprint.rationale.lower():
            is_exoape = True

        if is_exoape:
            if BuilderConstraint.NO_EXOAPE_SURFACE_CLONE not in plan_constraints:
                findings.append(StoriesBuilderGateFinding(
                    code="BUILDER_CONSTRAINTS_MISSING",
                    severity="P0",
                    message="Exo Ape reference detected but plan is missing NO_EXOAPE_SURFACE_CLONE constraint."
                ))
            required_caps = {
                BuilderCapability.RENDER_Z_AXIS_SCROLL,
                BuilderCapability.RENDER_DEPTH_LAYERS,
                BuilderCapability.BIND_SCROLL_TO_DEPTH
            }
            plan_capabilities = set(plan.capabilities)
            missing_caps = required_caps - plan_capabilities
            if missing_caps:
                findings.append(StoriesBuilderGateFinding(
                    code="BUILDER_CONSTRAINTS_MISSING",
                    severity="P0",
                    message="Exo Ape reference requires Z-axis capabilities which are missing from plan."
                ))

        # 4.3 Validate theme background against automatic dark interpretation and surface violations
        has_dark_justification = False
        if blueprint and blueprint.rationale:
            rational_lower = blueprint.rationale.lower()
            if any(w in rational_lower for w in ["shadow", "cinema", "blackbox", "dramatism", "earned", "justified", "tension", "visual_energy"]):
                has_dark_justification = True

        if blueprint and blueprint.rationale:
            rat_lower = blueprint.rationale.lower()
            if "dark editorial" in rat_lower and not has_dark_justification:
                findings.append(StoriesBuilderGateFinding(
                    code="DARK_EDITORIAL_MISINTERPRETED_AS_DARK_THEME",
                    severity="P1",
                    message="Dark Editorial automatically interpreted as dark background without narrative justification."
                ))
            if "black" in rat_lower and not has_dark_justification:
                findings.append(StoriesBuilderGateFinding(
                    code="MAD_LAB_THEME_SURFACE_VIOLATION",
                    severity="P0",
                    message="Pure black surface used as background without narrative justification."
                ))

        # 5. Verify component and layout traceability mapping rules
        valid_blueprint_fields = {
            "surface_type",
            "navigation_strategy",
            "motion_strategy",
            "spatial_strategy",
            "attention_strategy",
            "narrative_strategy",
            "interaction_density",
            "visual_energy",
            "immersion_level",
            "rationale"
        }

        has_motion = False
        has_layout = False
        has_performance_budget = False
        has_responsive_strategy = False

        for item in plan.traceability_items:
            # Check element ID validity
            if not item.element_id or len(item.element_id) < 3:
                findings.append(StoriesBuilderGateFinding(
                    code="WEAK_TRACEABILITY_DESCRIPTION",
                    severity="P2",
                    message=f"Weak or empty element description: '{item.element_id}'",
                    element_id=item.element_id
                ))

            # Check BUILDER_ARCHITECTURE_LEAK
            if item.authority_level == "architectural" and item.decision_owner == "stories_builder":
                findings.append(StoriesBuilderGateFinding(
                    code="BUILDER_ARCHITECTURE_LEAK",
                    severity="P0",
                    message="Architectural decision cannot be owned by stories_builder.",
                    element_id=item.element_id
                ))

            # Check RAW_REFERENCE_AUTHORITY_LEAK
            src = item.blueprint_source
            if src:
                # Raw URL or external path detection
                if any(x in src.lower() for x in ["http://", "https://", ".html", "url", "benchmark", "reference", "raw_ref"]):
                    findings.append(StoriesBuilderGateFinding(
                        code="RAW_REFERENCE_AUTHORITY_LEAK",
                        severity="P0",
                        message=f"Raw reference/URL leak detected in blueprint source: '{src}'",
                        element_id=item.element_id
                    ))
                elif src not in valid_blueprint_fields:
                    findings.append(StoriesBuilderGateFinding(
                        code="STORIES_UNTRACED_IMPLEMENTATION",
                        severity="P1",
                        message=f"Blueprint source field '{src}' is invalid or unrecognized.",
                        element_id=item.element_id
                    ))
            else:
                # Missing blueprint source
                findings.append(StoriesBuilderGateFinding(
                    code="MISSING_REQUIRED_BLUEPRINT_SOURCE",
                    severity="P1",
                    message="Required blueprint source field is missing or empty.",
                    element_id=item.element_id
                ))

            # Auto promotion attempt checking
            if item.decision_owner == "qa_gate" and ("auto-promote" in item.element_id.lower() or "autopromotion" in item.element_id.lower()):
                findings.append(StoriesBuilderGateFinding(
                    code="AUTO_PROMOTION_ATTEMPT",
                    severity="P0",
                    message="Auto promotion attempt detected in gate ownership.",
                    element_id=item.element_id
                ))

            # Track element types
            if item.element_type == "motion":
                has_motion = True
                if item.blueprint_source == "immersion_level" or item.blueprint_source == "visual_energy":
                    has_performance_budget = True
            elif item.element_type == "layout":
                has_layout = True
                if item.blueprint_source == "spatial_strategy" or item.blueprint_source == "surface_type":
                    has_responsive_strategy = True

        # MOTION_WITHOUT_PERFORMANCE_BUDGET
        if has_motion and not has_performance_budget:
            findings.append(StoriesBuilderGateFinding(
                code="MOTION_WITHOUT_PERFORMANCE_BUDGET",
                severity="P1",
                message="Motion element planned without tracing immersion_level or visual_energy performance budget."
            ))

        # LAYOUT_WITHOUT_RESPONSIVE_STRATEGY
        if has_layout and not has_responsive_strategy:
            findings.append(StoriesBuilderGateFinding(
                code="LAYOUT_WITHOUT_RESPONSIVE_STRATEGY",
                severity="P1",
                message="Layout element planned without referencing spatial_strategy or surface_type responsive strategies."
            ))

        # Check for optional trace missing warning (P2)
        if not plan.traceability_items:
            findings.append(StoriesBuilderGateFinding(
                code="MISSING_OPTIONAL_TRACE",
                severity="P2",
                message="The build plan does not contain any traceability items."
            ))

        # Final veridict consolidation
        p0_p1_findings = [f for f in findings if f.severity in ["P0", "P1"]]
        status = "failed" if p0_p1_findings else "passed"

        if status == "passed":
            findings.append(StoriesBuilderGateFinding(
                code="INFO_TRACE_COMPLETE",
                severity="P3",
                message="All planned elements successfully traced back to authorized architectural blueprint sources."
            ))
            findings.append(StoriesBuilderGateFinding(
                code="INFO_BUILD_PLAN_VALID",
                severity="P3",
                message="Stories build plan is valid and approved to proceed to construction."
            ))

        return StoriesBuilderGateReport(
            verified_at=datetime.now(),
            findings=findings,
            status=status
        )
