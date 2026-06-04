from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request
from urllib.error import HTTPError
from pathlib import Path


BASE = Path(__file__).resolve().parent
NODE = r"C:\PythonShim\node.cmd"
TSX = r"C:\Aurora\Ozzmosis\apps\aurora-omnichannel-ingestor\node_modules\.pnpm\tsx@4.21.0\node_modules\tsx\dist\cli.mjs"
SERVICE_ENTRY = r"C:\Aurora\Ozzmosis\apps\infoproduct-factory-service\src\server.ts"
RUNNER = r"C:\Aurora\AuroraCognitiveAssets\apps\content-engine\client\run_infoproduct_pipeline.py"
DEFAULT_PORT = "4311"


def remove_if_exists(path: Path) -> None:
    if path.exists():
        path.unlink()


def resolve_factory_token() -> str:
    token = os.getenv("INFOPRODUCT_FACTORY_TOKEN")
    if token:
        return token

    token_file = os.getenv("INFOPRODUCT_FACTORY_TOKEN_FILE")
    if token_file:
        return Path(token_file.strip()).read_text(encoding="utf-8").strip()

    raise RuntimeError("INFOPRODUCT_FACTORY_TOKEN or INFOPRODUCT_FACTORY_TOKEN_FILE is required")


def wait_for_health(url: str) -> dict:
    last_error = None
    for _ in range(80):
        try:
            with urllib.request.urlopen(url, timeout=1.5) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception as exc:  # pragma: no cover - operational script
            last_error = repr(exc)
            time.sleep(0.25)
    raise RuntimeError(f"service_not_ready: {last_error}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a secure end-to-end Infoproduct Factory flow.")
    parser.add_argument("--payload-dir", default=str(BASE), help="Directory containing brief.json and optional stage payloads.")
    parser.add_argument("--output-dir", default=str(BASE), help="Directory for summary, logs and runner output.")
    parser.add_argument("--port", default=DEFAULT_PORT, help="Service port used during the test run.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    payload_dir = Path(args.payload_dir).resolve()
    output_dir = Path(args.output_dir).resolve()
    brief_payload = json.loads((payload_dir / "brief.json").read_text(encoding="utf-8"))
    run_id = f"run_{brief_payload['id']}"
    artifact_dir = output_dir / "service-artifacts"
    output_path = output_dir / "full-pipeline-runner-output.json"
    summary_path = output_dir / "full-pipeline-summary.json"
    service_log_path = output_dir / "full-pipeline-service.log"
    port = str(args.port)

    artifact_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    remove_if_exists(output_path)
    remove_if_exists(summary_path)
    run_artifact_path = artifact_dir / f"{run_id}.json"
    remove_if_exists(run_artifact_path)
    resolved_token = resolve_factory_token()
    env = os.environ.copy()
    env["INFOPRODUCT_FACTORY_PORT"] = port
    env["INFOPRODUCT_FACTORY_BASE_URL"] = f"http://localhost:{port}"
    env["INFOPRODUCT_FACTORY_TOKEN"] = resolved_token
    env["INFOPRODUCT_FACTORY_ARTIFACT_DIR"] = str(artifact_dir)

    with service_log_path.open("w", encoding="utf-8") as service_log:
        process = subprocess.Popen(
            [NODE, TSX, SERVICE_ENTRY],
            cwd=r"C:\Aurora\Ozzmosis\apps\infoproduct-factory-service",
            env=env,
            stdout=service_log,
            stderr=subprocess.STDOUT,
        )
        try:
            health = wait_for_health(f"http://localhost:{port}/health")
            unauthorized_probe = {"status": None, "body": None}
            try:
                request = urllib.request.Request(
                    f"http://localhost:{port}/pipeline/intake",
                    data=json.dumps(brief_payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                urllib.request.urlopen(request, timeout=2)
            except HTTPError as exc:
                unauthorized_probe["status"] = exc.code
                unauthorized_probe["body"] = json.loads(exc.read().decode("utf-8"))

            command = [
                sys.executable,
                RUNNER,
                "--brief",
                str(payload_dir / "brief.json"),
                "--research",
                str(payload_dir / "research.json"),
                "--architecture",
                str(payload_dir / "architecture.json"),
                "--review",
                str(payload_dir / "review.json"),
                "--distribution",
                str(payload_dir / "distribution.json"),
            ]
            completed = subprocess.run(
                command,
                cwd=r"C:\Aurora\AuroraCognitiveAssets\apps\content-engine\client",
                env=env,
                capture_output=True,
                text=True,
            )
            output_path.write_text(
                json.dumps(
                    {
                        "health": health,
                        "unauthorized_probe": unauthorized_probe,
                        "runner_stdout": completed.stdout,
                        "runner_stderr": completed.stderr,
                        "returncode": completed.returncode,
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )
            summary = {
                "health_ok": health.get("ok"),
                "unauthorized_status": unauthorized_probe["status"],
                "unauthorized_code": (unauthorized_probe["body"] or {}).get("code"),
                "returncode": completed.returncode,
                "run_id": run_id,
            }

            if run_artifact_path.exists():
                run_record = json.loads(run_artifact_path.read_text(encoding="utf-8"))
                summary.update(
                    {
                        "run_id": run_record["run"]["runId"],
                        "final_stage": run_record["run"]["currentStage"],
                        "completed_stages": run_record["run"]["completedStages"],
                    }
                )

            if completed.returncode != 0:
                summary["status"] = "failed"
                summary_path.write_text(
                    json.dumps(summary, ensure_ascii=False, indent=2),
                    encoding="utf-8",
                )
                raise RuntimeError("full_pipeline_runner_failed")

            summary["status"] = "ok"
            summary_path.write_text(
                json.dumps(summary, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        finally:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=10)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
