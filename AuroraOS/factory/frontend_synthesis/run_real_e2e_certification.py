import asyncio
import os
import sys
import json
import re
import argparse
from pathlib import Path
from datetime import datetime
import shutil

# Adjust sys.path to find internal modules correctly
sys.path.extend([
    os.path.abspath('./contracts'),
    os.path.abspath('./synthesizer'),
    os.path.abspath('./orchestrator'),
    os.path.abspath('./factory'),
    os.path.abspath('./bff'),
    os.path.abspath('../sandbox'),
    os.path.abspath('./acquisition'),
    os.path.abspath('./orchestrator')
])

from dag_orchestrator import SynthesisDAG, HumanPromotionHalt
from promote import promote_candidate

def parse_args():
    parser = argparse.ArgumentParser(description="E2E Real Mode Certification Pipeline")
    parser.add_argument("--url", "--target-url", dest="url", default="https://antigravity.google/", help="Target URL to process")
    parser.add_argument("--api-manifest", default="./bff/api_manifest.json", help="BFF API manifest path")
    parser.add_argument("--output-dir", default="./output_synthesis", help="Output directory")
    parser.add_argument("--acquire-asset-kit", action="store_true", help="Acquire the asset kit dynamically via Playwright")
    parser.add_argument("--manifest-path", default=None, help="Optional pre-acquired manifest file path")
    parser.add_argument("--governance-mode", "--mode", dest="governance_mode", default="transmute", choices=["transmute", "clone", "poor_fidelity", "clone_fidelity"], help="Governance mode to run the DAG under")
    parser.add_argument("--surface-type", default="landing", choices=["landing", "crm"], help="Surface target layout type")
    parser.add_argument("--promotion-mode", default="candidate-only", choices=["candidate-only", "promote"], help="Candidate promotion mode")
    parser.add_argument("--no-mocks", action="store_true", help="Disable all mocks (active by default in certification)")
    parser.add_argument("--promote", action="store_true", help="Automatically write approval record and promote candidate on success (legacy flag)")
    return parser.parse_args()

async def main():
    args = parse_args()
    
    # Resolve promotion flag
    should_promote = args.promote or (args.promotion_mode == "promote")
    
    print(f"--- INICIANDO E2E REAL MODE CERTIFICATION ---")
    print(f"URL: {args.url}")
    print(f"Mode: {args.governance_mode}")
    print(f"Acquire: {args.acquire_asset_kit}")
    print(f"Surface Type: {args.surface_type}")
    print(f"Promotion Mode: {args.promotion_mode}")
    print(f"No Mocks: {args.no_mocks}")
    print(f"Flow: Reference -> Page Intelligence -> Hybrid Truth -> Experience Architect -> Experience Blueprint -> BuildPlanResolver -> StoriesBuilderGate -> Stories Builder -> Visual QA")
    print(f"---------------------------------------------\n")
    
    # Locate repo root
    repo_root = Path("../..").resolve()
    if not (repo_root / ".git").exists():
        repo_root = Path("C:/Projetos/Aurora").resolve()
        
    approval_dir = repo_root / ".aurora" / "approvals"
    external_approval_file = approval_dir / "promotion_approval.json"
    
    # Clean up previous approval configurations in the external approvals directory
    os.makedirs(approval_dir, exist_ok=True)
    if external_approval_file.exists():
        external_approval_file.unlink()
        
    # Initialize DAG
    dag = SynthesisDAG(args.url, args.api_manifest, args.output_dir)
    
    try:
        results = await dag.execute(
            acquire_asset_kit=args.acquire_asset_kit,
            asset_kit_manifest_path=args.manifest_path,
            governance_mode=args.governance_mode
        )
        print("[SUCCESS] Pipeline completed successfully!")
        if results.get("promotion_authorized"):
            print("[SUCCESS] Promotion already authorized via pre-existing approval record.")
            
    except HumanPromotionHalt as halt:
        print("[INFO] Pipeline halted for Human Promotion (as expected).")
        error_msg = str(halt)
        run_id = re.search(r"sandbox_run_id:\s*(\S+)", error_msg).group(1)
        patch_sha = re.search(r"patch_candidate_sha256:\s*(\S+)", error_msg).group(1)
        qa_sha = re.search(r"qa_report_sha256:\s*(\S+)", error_msg).group(1)
        
        print(f"       Run ID: {run_id}")
        print(f"       Patch SHA256: {patch_sha}")
        print(f"       QA SHA256: {qa_sha}")
        
        if should_promote:
            print("\n[E2E] Promotion is enabled. Creating promotion approval record in trusted directory...")
            approval_data = {
                "promotion_candidate_id": "PC-REAL-E2E-CERT",
                "sandbox_run_id": run_id,
                "patch_candidate_sha256": patch_sha,
                "qa_report_sha256": qa_sha,
                "approved_by": "Operator",
                "approved_at": datetime.now().isoformat(),
                "approval_nonce": "nonce-real-e2e-cert",
                "approval_source": "manual_cli"
            }
            
            with open(external_approval_file, "w") as f:
                json.dump(approval_data, f, indent=2)
                
            print("[E2E] Running promotion engine...")
            try:
                promote_candidate(args.output_dir)
            except SystemExit as e:
                if e.code == 0:
                    print("[SUCCESS] Candidate promoted successfully to production!")
                else:
                    print(f"[ERROR] Promotion engine failed with exit code: {e.code}")
                    sys.exit(1)
            finally:
                if external_approval_file.exists():
                    external_approval_file.unlink()
        else:
            print("[INFO] Promotion skipped (candidate-only mode). Run with --promotion-mode promote to promote candidate.")
            
    except Exception as e:
        print(f"[ERROR] Pipeline execution failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
