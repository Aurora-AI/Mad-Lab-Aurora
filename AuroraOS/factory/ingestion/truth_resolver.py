import sys
import os
from datetime import datetime, timezone
from typing import Dict, Any, List

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../contracts')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../sandbox')))

from truth_resolver_port import TruthResolverPort, TruthResolutionResult, ConflictReport
from models import HybridTruthArtifact, ResolvedField, ProvenanceWinner
from sandbox_contracts import PipelinePausedException, DiagnosticFinding

class HybridTruthResolver(TruthResolverPort):
    """
    Motor de Resolução de Conflitos Híbridos (OS-009).
    Prioridade Kit: css_variables, font_declarations, breakpoints, asset_paths
    Prioridade Probe: computed_styles, layout_viewport, runtime_animations, interactive_states
    """
    
    def resolve(self, probe_data: Dict[str, Any], kit_data: Dict[str, Any]) -> TruthResolutionResult:
        resolved_data = {}
        conflicts = {}
        has_critical_conflicts = False
        findings: List[DiagnosticFinding] = []
        resolved_fields = {}

        kit_priority_keys = {"css_variables", "font_declarations", "breakpoints", "asset_paths"}
        probe_priority_keys = {"computed_styles", "layout_viewport", "runtime_animations", "interactive_states", "visible_text"}

        all_keys = set(probe_data.keys()).union(set(kit_data.keys()))

        for key in all_keys:
            val_probe = probe_data.get(key)
            val_kit = kit_data.get(key)

            if val_probe is not None and val_kit is not None and val_probe != val_kit:
                # Conflito detectado
                if key in kit_priority_keys:
                    resolved_data[key] = val_kit
                    conflicts[key] = ConflictReport(
                        key=key, kit_value=val_kit, probe_value=val_probe,
                        resolved_value=val_kit, resolution_source="kit", needs_escalation=False
                    )
                    resolved_fields[key] = ResolvedField(
                        winner=ProvenanceWinner.KIT, loser_value=val_probe,
                        reason=f"Verdade Canônica (Kit) domina {key}", confidence=1.0
                    )
                elif key in probe_priority_keys:
                    resolved_data[key] = val_probe
                    conflicts[key] = ConflictReport(
                        key=key, kit_value=val_kit, probe_value=val_probe,
                        resolved_value=val_probe, resolution_source="probe", needs_escalation=False
                    )
                    resolved_fields[key] = ResolvedField(
                        winner=ProvenanceWinner.PROBE, loser_value=val_kit,
                        reason=f"Verdade Renderizada (Probe) domina {key}", confidence=1.0
                    )
                else:
                    has_critical_conflicts = True
                    resolved_data[key] = val_probe
                    conflicts[key] = ConflictReport(
                        key=key, kit_value=val_kit, probe_value=val_probe,
                        resolved_value=val_probe, resolution_source="manual", needs_escalation=True
                    )
                    resolved_fields[key] = ResolvedField(
                        winner=ProvenanceWinner.PROBE, loser_value=val_kit,
                        reason=f"Conflito crítico não mapeado em {key}, fallback para Probe.", confidence=0.0
                    )
                    findings.append(
                        DiagnosticFinding(
                            severity="P1",
                            code="TRUTH_RESOLVER_CONFLICT",
                            redacted_message=f"Conflito estrutural crítico na chave {key}. Exige revisão humana (Fail-Closed).",
                            recommended_action="Rever HybridTruth e aplicar override manual na matriz de resolução.",
                            file_path="truth_resolver.py"
                        )
                    )
            else:
                resolved_value = val_probe if val_probe is not None else val_kit
                resolved_data[key] = resolved_value
                resolved_fields[key] = ResolvedField(
                    winner=ProvenanceWinner.PROBE if val_probe is not None else ProvenanceWinner.KIT,
                    loser_value=None,
                    reason="Sem conflito empírico",
                    confidence=1.0
                )

        if has_critical_conflicts:
            raise PipelinePausedException(
                "ResolveTruth pausado: Conflito Crítico identificado. Aguardando escalação manual.",
                findings
            )

        return TruthResolutionResult(
            resolved_data=resolved_data,
            conflicts=conflicts,
            has_critical_conflicts=has_critical_conflicts
        )
