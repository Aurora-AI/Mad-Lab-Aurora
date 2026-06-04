from __future__ import annotations

import json
from pathlib import Path

from infoproduct_factory_client import InfoproductFactoryClient


base = Path(__file__).resolve().parents[3] / "docs" / "Vault" / "OS-Evidence" / "ifactory-e2e"
brief = json.loads((base / "brief.json").read_text(encoding="utf-8"))
stage_payload = json.loads((base / "brief-stage-payload.json").read_text(encoding="utf-8"))

client = InfoproductFactoryClient(base_url="http://localhost:4310")
health = client.health()
intake = client.intake(brief)
advance = client.advance(intake["run"], stage_payload)

print(
    json.dumps(
        {
            "health": health,
            "intake": intake,
            "advance": advance,
        },
        ensure_ascii=False,
        indent=2,
    )
)
