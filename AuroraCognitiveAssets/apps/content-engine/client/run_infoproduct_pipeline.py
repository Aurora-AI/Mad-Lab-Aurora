from __future__ import annotations

import argparse
import json
from pathlib import Path

from infoproduct_factory_client import InfoproductFactoryClient


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    parser = argparse.ArgumentParser(description="Consume the Infoproduct Factory typed API.")
    parser.add_argument("--brief", required=True, help="Path to a ProductBrief-compatible JSON file.")
    parser.add_argument("--research", help="Optional path to a ResearchPack-compatible JSON file.")
    parser.add_argument("--architecture", help="Optional path to a ProductArchitecture-compatible JSON file.")
    parser.add_argument("--review", help="Optional path to a ReviewScorecard-compatible JSON file.")
    parser.add_argument("--distribution", help="Optional path to a DistributionPack-compatible JSON file.")
    args = parser.parse_args()

    brief = load_json(Path(args.brief))
    client = InfoproductFactoryClient()
    intake_result = client.intake(brief)
    print(json.dumps({"intake": intake_result}, ensure_ascii=False, indent=2))

    run = intake_result.get("run")
    if run is None:
        raise RuntimeError("Factory intake did not return a pipeline run.")
    run_id = run["runId"]

    if args.research:
        research_result = client.research(run_id, load_json(Path(args.research)))
        print(json.dumps({"research": research_result}, ensure_ascii=False, indent=2))

    if args.architecture:
        architecture_result = client.architecture(run_id, load_json(Path(args.architecture)))
        print(json.dumps({"architecture": architecture_result}, ensure_ascii=False, indent=2))

    if args.review:
        review_result = client.review(run_id, load_json(Path(args.review)))
        print(json.dumps({"review": review_result}, ensure_ascii=False, indent=2))

    if args.distribution:
        distribution_result = client.distribution(run_id, load_json(Path(args.distribution)))
        print(json.dumps({"distribution": distribution_result}, ensure_ascii=False, indent=2))

    final_state = client.get_run(run_id)
    print(json.dumps({"run_state": final_state}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
