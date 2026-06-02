import sys
import os
from typing import Dict, Any

# Ajuste de path para importação dos contratos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../contracts')))
from truth_resolver_port import TruthResolverPort, TruthResolutionResult, ConflictReport

class MockTruthResolver(TruthResolverPort):
    def resolve(self, probe_data: Dict[str, Any], asset_kit_data: Dict[str, Any]) -> TruthResolutionResult:
        resolved_data = {}
        conflicts = {}
        has_critical_conflicts = False

        # Matriz de pesos
        kit_priority_keys = {"css_variables", "font_declarations", "breakpoints", "assets_paths"}
        probe_priority_keys = {"computed_styles", "layout_viewport", "runtime_animations", "interactive_states", "visible_text"}

        # Coletar todas as chaves únicas
        all_keys = set(probe_data.keys()).union(set(asset_kit_data.keys()))

        for key in all_keys:
            val_probe = probe_data.get(key)
            val_kit = asset_kit_data.get(key)

            if val_probe is not None and val_kit is not None and val_probe != val_kit:
                # Conflito detectado!
                if key in kit_priority_keys:
                    resolved_data[key] = val_kit
                    conflicts[key] = ConflictReport(
                        key=key,
                        kit_value=val_kit,
                        probe_value=val_probe,
                        resolved_value=val_kit,
                        resolution_source="kit",
                        needs_escalation=False
                    )
                elif key in probe_priority_keys:
                    resolved_data[key] = val_probe
                    conflicts[key] = ConflictReport(
                        key=key,
                        kit_value=val_kit,
                        probe_value=val_probe,
                        resolved_value=val_probe,
                        resolution_source="probe",
                        needs_escalation=False
                    )
                else:
                    # Conflito crítico que exige escalação manual
                    has_critical_conflicts = True
                    conflicts[key] = ConflictReport(
                        key=key,
                        kit_value=val_kit,
                        probe_value=val_probe,
                        resolved_value=val_probe,  # Fallback seguro
                        resolution_source="manual",
                        needs_escalation=True
                    )
                    resolved_data[key] = val_probe
            else:
                # Sem conflito
                resolved_data[key] = val_probe if val_probe is not None else val_kit

        return TruthResolutionResult(
            resolved_data=resolved_data,
            conflicts=conflicts,
            has_critical_conflicts=has_critical_conflicts
        )
