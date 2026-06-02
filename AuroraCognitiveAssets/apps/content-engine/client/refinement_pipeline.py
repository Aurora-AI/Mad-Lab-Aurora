from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from infoproduct_factory_client import InfoproductFactoryClient


STAGE_FILES = {
    "brief": "brief.json",
    "research": "research.json",
    "architecture": "architecture.json",
    "review": "review.json",
    "distribution": "distribution.json",
}


def load_stage_payloads(payload_dir: Path) -> Dict[str, Dict[str, Any]]:
    resolved_dir = Path(payload_dir).resolve()
    payloads: Dict[str, Dict[str, Any]] = {}

    for stage, filename in STAGE_FILES.items():
        file_path = resolved_dir / filename
        if stage == "brief" and not file_path.exists():
            raise FileNotFoundError(f"Missing required payload file: {file_path}")
        if not file_path.exists():
            continue
        payloads[stage] = json.loads(file_path.read_text(encoding="utf-8"))

    return payloads


def execute_refinement_pipeline(
    client: InfoproductFactoryClient,
    payloads: Dict[str, Dict[str, Any]],
) -> Dict[str, Any]:
    if "brief" not in payloads:
        raise ValueError("brief payload is required")

    health = client.health()
    intake = client.intake(payloads["brief"])
    run = intake.get("run")
    if run is None:
        raise RuntimeError("Factory intake did not return a pipeline run.")
    run_id = run["runId"]

    steps: Dict[str, Any] = {"intake": intake}

    if "research" in payloads:
        steps["research"] = client.research(run_id, payloads["research"])
    if "architecture" in payloads:
        steps["architecture"] = client.architecture(run_id, payloads["architecture"])
    if "review" in payloads:
        steps["review"] = client.review(run_id, payloads["review"])
    if "distribution" in payloads:
        steps["distribution"] = client.distribution(run_id, payloads["distribution"])

    final_state = client.get_run(run_id)
    return {
        "health": health,
        "run_id": run_id,
        "steps": steps,
        "final_state": final_state,
    }


def build_refinement_summary(result: Dict[str, Any]) -> str:
    final_record = result["final_state"]["record"]
    artifacts = final_record.get("artifacts", {})
    brief = artifacts.get("brief", {}).get("payload", {})
    architecture = artifacts.get("architecture", {}).get("payload", {})
    review = artifacts.get("review", {}).get("payload", {})
    distribution = artifacts.get("distribution", {}).get("payload", {})
    run = final_record.get("run", {})

    lines = [
        "# Refinement Summary",
        "",
        f"Run ID: {run.get('runId', 'unknown')}",
        f"Final Stage: {run.get('currentStage', 'unknown')}",
        f"Completed Stages: {', '.join(run.get('completedStages', []))}",
        "",
        "## Brief",
        "",
        f"Tema: {brief.get('tema', '')}",
        f"ICP: {brief.get('icp', '')}",
        f"Dor central: {brief.get('dorCentral', '')}",
        f"Promessa central: {brief.get('promessaCentral', '')}",
        f"Objetivo de negocio: {brief.get('objetivoDeNegocio', '')}",
        "",
        "## Strategy",
        "",
        f"Tese: {architecture.get('tese', '')}",
        f"Transformacao prometida: {architecture.get('transformacaoPrometida', '')}",
        f"CTA principal: {architecture.get('ctaPrincipal', '')}",
        "",
        "## Trustware",
        "",
        f"Decisao: {review.get('decision', '')}",
        f"Global score: {review.get('globalScore', '')}",
        f"Reviewer: {review.get('reviewer', '')}",
        "",
        "## Distribution",
        "",
        f"Title: {distribution.get('title', '')}",
        f"Subtitle: {distribution.get('subtitle', '')}",
        f"Promise: {distribution.get('promise', '')}",
        f"CTA: {distribution.get('cta', '')}",
        f"Landing copy: {distribution.get('landingCopy', '')}",
    ]

    email_sequence = distribution.get("emailSequence", [])
    if email_sequence:
        lines.extend(["", "Email sequence:"] + [f"- {item}" for item in email_sequence])

    social_derivatives = distribution.get("socialDerivatives", [])
    if social_derivatives:
        lines.extend(["", "Social derivatives:"] + [f"- {item}" for item in social_derivatives])

    return "\n".join(lines) + "\n"


def write_refinement_outputs(output_dir: Path, result: Dict[str, Any]) -> Dict[str, Path]:
    resolved_dir = Path(output_dir).resolve()
    resolved_dir.mkdir(parents=True, exist_ok=True)

    result_path = resolved_dir / "refinement-result.json"
    final_record_path = resolved_dir / "final-run-record.json"
    summary_path = resolved_dir / "refinement-summary.md"

    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    final_record_path.write_text(
        json.dumps(result["final_state"]["record"], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    summary_path.write_text(build_refinement_summary(result), encoding="utf-8")

    return {
        "result": result_path,
        "final_record": final_record_path,
        "summary": summary_path,
    }
