import asyncio
import os
import sys
import json
import re
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
    os.path.abspath('../sandbox')
])

from probe import extract_page_intelligence
from dag_orchestrator import SynthesisDAG, HumanPromotionHalt
# Import promotion engine function directly to test in-process
sys.path.append(os.path.abspath('./orchestrator'))
from promote import promote_candidate

TARGET_URL = "https://antigravity.google/"
MANIFEST_PATH = "./bff/api_manifest.json"
OUTPUT_DIR = "./output_synthesis"

async def execute_pipeline():
    print(f"--- INICIANDO OS-008 PIPELINE E2E EXECUTION ---")
    print(f"Alvo: {TARGET_URL}\n")
    
    # Locate repo root
    repo_root = Path("../..").resolve()
    if not (repo_root / ".git").exists():
        repo_root = Path("C:/Projetos/Aurora").resolve()
        
    approval_dir = repo_root / ".aurora" / "approvals"
    external_approval_file = approval_dir / "promotion_approval.json"
    untrusted_approval_file = Path(OUTPUT_DIR) / "promotion_approval.json"
    
    # 0. Clean up previous approval configurations and output directories
    os.makedirs(approval_dir, exist_ok=True)
    if external_approval_file.exists():
        external_approval_file.unlink()
    if untrusted_approval_file.exists():
        untrusted_approval_file.unlink()
        
    # Clean up output directory completely to ensure no old files exist
    if os.path.exists(OUTPUT_DIR):
        # We delete everything except the candidate folder if we want to test staging,
        # but since we are running Probe from scratch, we delete all files in output_dir.
        for item in os.listdir(OUTPUT_DIR):
            item_path = os.path.join(OUTPUT_DIR, item)
            if os.path.isfile(item_path):
                os.unlink(item_path)
            elif os.path.isdir(item_path) and item != "candidate":
                shutil.rmtree(item_path, ignore_errors=True)
        
    # Extract target page metadata
    print("[E2E] Iniciando Probe...")
    artifact = await extract_page_intelligence(TARGET_URL)
    
    # Initialize DAG
    dag = SynthesisDAG(TARGET_URL, MANIFEST_PATH, OUTPUT_DIR)
    
    asset_kit_mock = "C:/Users/rodri/OneDrive/Pessoal/Desktop"
    
    # 1. Negative Case: Originality Gate Blocks Clone
    print("[E2E] Teste 1: Executando em modo clone (Originality Gate deve Pausar)...")
    from sandbox_contracts import PipelinePausedException
    try:
        await dag.execute(
            probe_artifact_mock=artifact,
            asset_kit_mock=asset_kit_mock,
            governance_mode="clone"
        )
        print("[ERRO] Pipeline executou clone sem lançar exceção do Originality Gate!")
        sys.exit(1)
    except PipelinePausedException as p:
        if "OriginalityGate blocked" in str(p):
            print(f"[SUCESSO] Pipeline pausou corretamente no Originality Gate por plágio. Achados: {len(p.findings)}")
            for finding in p.findings:
                print(f"       - {finding.code}: {finding.redacted_message}")
        else:
            print(f"[ERRO] Exceção incorreta lançada: {p}")
            sys.exit(1)
            
    # 1.5. Negative Case: Poor Fidelity (OS-011)
    print("\n[E2E] Teste 1.5: Executando CodeSpec com baixa fidelidade (Visual Fidelity Evaluator deve Pausar)...")
    try:
        await dag.execute(
            probe_artifact_mock=artifact,
            asset_kit_mock=asset_kit_mock,
            governance_mode="poor_fidelity"
        )
        print("[ERRO] Pipeline executou spec pobre sem lançar exceção do Visual Fidelity Evaluator!")
        sys.exit(1)
    except PipelinePausedException as p:
        if "VisualFidelityEvaluator blocked" in str(p):
            print(f"[SUCESSO] Pipeline pausou corretamente no Visual Fidelity Evaluator por baixa fidelidade. Achados: {len(p.findings)}")
            for finding in p.findings:
                print(f"       - {finding.code}: {finding.redacted_message}")
        else:
            print(f"[ERRO] Exceção incorreta lançada: {p}")
            sys.exit(1)

    # 1.6. Negative Case: Clone Risk High (OS-011)
    print("\n[E2E] Teste 1.6: Executando CodeSpec clone-like (Visual Fidelity Evaluator deve Pausar)...")
    try:
        await dag.execute(
            probe_artifact_mock=artifact,
            asset_kit_mock=asset_kit_mock,
            governance_mode="clone_fidelity"
        )
        print("[ERRO] Pipeline executou spec clone-like sem lançar exceção do Visual Fidelity Evaluator!")
        sys.exit(1)
    except PipelinePausedException as p:
        if "VisualFidelityEvaluator blocked" in str(p):
            print(f"[SUCESSO] Pipeline pausou corretamente no Visual Fidelity Evaluator por clone risk. Achados: {len(p.findings)}")
            for finding in p.findings:
                print(f"       - {finding.code}: {finding.redacted_message}")
        else:
            print(f"[ERRO] Exceção incorreta lançada: {p}")
            sys.exit(1)

    # 2. Negative Case: Expect HumanPromotionHalt when no approval record is present
    print("\n[E2E] Teste 2: Executando transmutação sem registro de aprovação (Sandbox Gate deve Pausar)...")
    run_id, patch_sha, qa_sha = None, None, None
    try:
        await dag.execute(
            probe_artifact_mock=artifact,
            asset_kit_mock=asset_kit_mock,
            governance_mode="transmute"
        )
        print("[ERRO] Pipeline executou sem lançar HumanPromotionHalt!")
        sys.exit(1)
    except HumanPromotionHalt as halt:
        print("[SUCESSO] Pipeline pausou corretamente no Promotion Sandbox Gate.")
        # Extract run_id and hashes from exception info
        error_msg = str(halt)
        run_id = re.search(r"sandbox_run_id:\s*(\S+)", error_msg).group(1)
        patch_sha = re.search(r"patch_candidate_sha256:\s*(\S+)", error_msg).group(1)
        qa_sha = re.search(r"qa_report_sha256:\s*(\S+)", error_msg).group(1)
        print(f"       Run ID: {run_id}")
        print(f"       Patch SHA256: {patch_sha}")
        print(f"       QA SHA256: {qa_sha}\n")
        
    # 3. Negative Case 2: Reject approval record placed in untrusted paths (e.g. inside output folder)
    print("[E2E] Teste 3: Gravando aprovação em pasta NÃO confiável (Deve ser rejeitada)...")
    approval_data = {
        "promotion_candidate_id": "PC-E2E-TEST",
        "sandbox_run_id": run_id,
        "patch_candidate_sha256": patch_sha,
        "qa_report_sha256": qa_sha,
        "approved_by": "Operator",
        "approved_at": datetime.now().isoformat(),
        "approval_nonce": "nonce-e2e-123",
        "approval_source": "manual_cli"
    }
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(untrusted_approval_file, "w") as f:
        json.dump(approval_data, f)
        
    try:
        promote_candidate(OUTPUT_DIR)
        print("[ERRO] Engine de promoção aceitou aprovação de pasta não confiável!")
        sys.exit(1)
    except SystemExit as e:
        if e.code == 1:
            print("[SUCESSO] Aprovação não confiável foi rejeitada corretamente.")
        else:
            print(f"[ERRO] Engine saiu com código inesperado: {e.code}")
            sys.exit(1)
    finally:
        if untrusted_approval_file.exists():
            untrusted_approval_file.unlink()
    print("")
        
    # 4. Positive Case: Write approval record to the trusted approvals directory and run promotion
    print("[E2E] Teste 4: Gravando aprovação no diretório externo confiável...")
    with open(external_approval_file, "w") as f:
        json.dump(approval_data, f)
        
    print("[E2E] Executando comando de promoção separado...")
    try:
        promote_candidate(OUTPUT_DIR)
    except SystemExit as e:
        if e.code == 0:
            print("[SUCESSO] Promoção autorizada e executada com sucesso!")
        else:
            print(f"[ERRO] Engine de promoção falhou com código: {e.code}")
            sys.exit(1)
            
    # Verify that files are now present in the production output folder
    assert os.path.exists(os.path.join(OUTPUT_DIR, "5_SynthesizedPage.client.tsx")), "Staged files should be promoted to output"
    assert os.path.exists(os.path.join(OUTPUT_DIR, "QA_REPORT.md")), "QA Report should be promoted to output"
    
    print("\n[SUCESSO] OS-008 E2E concluído com sucesso. Candidato de promoção PROMOVIDO!")
    
    # Clean up approvals file
    if external_approval_file.exists():
        external_approval_file.unlink()

if __name__ == "__main__":
    asyncio.run(execute_pipeline())
