from __future__ import annotations

import json
import os
import subprocess
import time
import urllib.request
from pathlib import Path
from urllib.error import HTTPError


BASE = Path(__file__).resolve().parent
OUTPUT_PATH = BASE / "auth-only-summary.json"
SERVICE_LOG_PATH = BASE / "auth-only-service.log"
NODE = r"C:\PythonShim\node.cmd"
TSX = r"C:\Aurora\Ozzmosis\apps\aurora-omnichannel-ingestor\node_modules\.pnpm\tsx@4.21.0\node_modules\tsx\dist\cli.mjs"
SERVICE_ENTRY = r"C:\Aurora\Ozzmosis\apps\infoproduct-factory-service\src\server.ts"
PORT = "4311"


def wait_for_health(url: str) -> dict:
    last_error = None
    for _ in range(80):
        try:
            with urllib.request.urlopen(url, timeout=1.5) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception as exc:
            last_error = repr(exc)
            time.sleep(0.25)
    raise RuntimeError(f"service_not_ready: {last_error}")


def main() -> int:
    env = os.environ.copy()
    env["INFOPRODUCT_FACTORY_PORT"] = PORT
    env["INFOPRODUCT_FACTORY_TOKEN"] = "aurora-local-e2e-token"
    env["INFOPRODUCT_FACTORY_ARTIFACT_DIR"] = str(BASE / "service-artifacts-auth-only")

    with SERVICE_LOG_PATH.open("w", encoding="utf-8") as service_log:
        process = subprocess.Popen(
            [NODE, TSX, SERVICE_ENTRY],
            cwd=r"C:\Aurora\Ozzmosis\apps\infoproduct-factory-service",
            env=env,
            stdout=service_log,
            stderr=subprocess.STDOUT,
        )
        try:
            health = wait_for_health(f"http://localhost:{PORT}/health")
            unauthorized = {"status": None, "code": None}
            try:
                request = urllib.request.Request(
                    f"http://localhost:{PORT}/pipeline/intake",
                    data=(BASE / "brief.json").read_bytes(),
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                urllib.request.urlopen(request, timeout=2)
            except HTTPError as exc:
                unauthorized["status"] = exc.code
                unauthorized["code"] = json.loads(exc.read().decode("utf-8")).get("code")

            OUTPUT_PATH.write_text(
                json.dumps(
                    {
                        "health_ok": health.get("ok"),
                        "unauthorized_status": unauthorized["status"],
                        "unauthorized_code": unauthorized["code"],
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
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
