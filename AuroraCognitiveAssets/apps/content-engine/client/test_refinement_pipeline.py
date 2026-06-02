from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from refinement_pipeline import (
    build_refinement_summary,
    execute_refinement_pipeline,
    load_stage_payloads,
)


class _FakeClient:
    def health(self):
        return {"ok": True}

    def intake(self, payload):
        return {"ok": True, "run": {"runId": f"run_{payload['id']}"}, "payload": payload}

    def research(self, run_id, payload):
        return {"ok": True, "runId": run_id, "payload": payload}

    def architecture(self, run_id, payload):
        return {"ok": True, "runId": run_id, "payload": payload}

    def review(self, run_id, payload):
        return {"ok": True, "runId": run_id, "payload": payload}

    def distribution(self, run_id, payload):
        return {"ok": True, "runId": run_id, "payload": payload}

    def get_run(self, run_id):
        return {
            "ok": True,
            "record": {
                "run": {
                    "runId": run_id,
                    "currentStage": "distribution",
                    "completedStages": [
                        "brief",
                        "research",
                        "architecture",
                        "review",
                        "distribution",
                    ],
                },
                "artifacts": {
                    "brief": {"payload": {"tema": "APO", "icp": "gestores", "dorCentral": "ruido", "promessaCentral": "clareza", "objetivoDeNegocio": "demanda"}},
                    "architecture": {"payload": {"tese": "gestor como infraestrutura", "transformacaoPrometida": "criterio", "ctaPrincipal": "Solicitar diagnostico APO"}},
                    "review": {"payload": {"decision": "approved", "globalScore": 9.1, "reviewer": "trustware-reviewer"}},
                    "distribution": {
                        "payload": {
                            "title": "APO",
                            "subtitle": "Gestor como infraestrutura",
                            "promise": "criterio sistemico",
                            "cta": "Solicitar diagnostico APO",
                            "landingCopy": "copy",
                            "emailSequence": ["email_1", "email_2"],
                            "socialDerivatives": ["post_1"],
                        }
                    },
                },
            },
        }


class RefinementPipelineTests(unittest.TestCase):
    def test_load_stage_payloads_reads_required_and_optional_files(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            payload_dir = Path(tmp_dir)
            (payload_dir / "brief.json").write_text(json.dumps({"id": "brief_001"}), encoding="utf-8")
            (payload_dir / "review.json").write_text(json.dumps({"id": "review_001"}), encoding="utf-8")

            payloads = load_stage_payloads(payload_dir)

        self.assertEqual(payloads["brief"]["id"], "brief_001")
        self.assertEqual(payloads["review"]["id"], "review_001")
        self.assertNotIn("research", payloads)

    def test_execute_refinement_pipeline_returns_final_state(self):
        client = _FakeClient()
        payloads = {
            "brief": {"id": "brief_apo_001"},
            "research": {"id": "research_apo_001"},
            "architecture": {"id": "architecture_apo_001"},
            "review": {"id": "review_apo_001"},
            "distribution": {"id": "distribution_apo_001"},
        }

        result = execute_refinement_pipeline(client, payloads)

        self.assertEqual(result["run_id"], "run_brief_apo_001")
        self.assertEqual(result["final_state"]["record"]["run"]["currentStage"], "distribution")
        self.assertIn("distribution", result["steps"])

    def test_build_refinement_summary_formats_key_sections(self):
        summary = build_refinement_summary(
            execute_refinement_pipeline(
                _FakeClient(),
                {
                    "brief": {"id": "brief_apo_001"},
                    "research": {"id": "research_apo_001"},
                    "architecture": {"id": "architecture_apo_001"},
                    "review": {"id": "review_apo_001"},
                    "distribution": {"id": "distribution_apo_001"},
                },
            )
        )

        self.assertIn("Refinement Summary", summary)
        self.assertIn("Final Stage: distribution", summary)
        self.assertIn("Tese: gestor como infraestrutura", summary)
        self.assertIn("Decisao: approved", summary)
        self.assertIn("Solicitar diagnostico APO", summary)
