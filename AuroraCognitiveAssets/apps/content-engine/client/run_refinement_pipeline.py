from __future__ import annotations

import argparse
import json
from pathlib import Path

from infoproduct_factory_client import InfoproductFactoryClient
from refinement_pipeline import (
    build_refinement_summary,
    execute_refinement_pipeline,
    load_stage_payloads,
    write_refinement_outputs,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the in-app refinement pipe against the Infoproduct Factory.")
    parser.add_argument("--payload-dir", required=True, help="Directory containing brief.json and optional stage payload files.")
    parser.add_argument("--output-dir", help="Optional directory for generated outputs.")
    parser.add_argument("--print-json", action="store_true", help="Print the raw result JSON to stdout.")
    parser.add_argument("--print-summary", action="store_true", help="Print the human-readable summary to stdout.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    payload_dir = Path(args.payload_dir).resolve()

    payloads = load_stage_payloads(payload_dir)
    client = InfoproductFactoryClient()
    result = execute_refinement_pipeline(client, payloads)

    if args.output_dir:
        written_paths = write_refinement_outputs(Path(args.output_dir), result)
        print(
            json.dumps(
                {key: str(value) for key, value in written_paths.items()},
                ensure_ascii=False,
                indent=2,
            )
        )

    if args.print_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))

    if args.print_summary or not args.print_json:
        print(build_refinement_summary(result))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
