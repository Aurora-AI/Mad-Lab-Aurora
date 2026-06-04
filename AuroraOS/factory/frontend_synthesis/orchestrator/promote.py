import os
import sys
import json
import hashlib
import shutil
from pathlib import Path
from datetime import datetime

# Adjust path to find contracts
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../sandbox')))
from sandbox_contracts import PromotionApprovalRecord

def promote_candidate(output_dir: str):
    print(f"--- INICIANDO PROMOTION ENGINE ---")
    
    # Locate repo root
    curr_dir = Path(output_dir).resolve()
    repo_root = None
    for _ in range(5):
        if (curr_dir / ".git").exists():
            repo_root = curr_dir
            break
        curr_dir = curr_dir.parent
    if not repo_root:
        repo_root = Path("C:/Projetos/Aurora").resolve()
        
    approval_dir = repo_root / ".aurora" / "approvals"
    approval_file = approval_dir / "promotion_approval.json"
    
    if not approval_file.exists():
        print(f"[ERRO] Registro de aprovação humana não encontrado em {approval_file}")
        sys.exit(1)
        
    # Check untrusted paths
    untrusted_paths = [
        Path(output_dir).resolve(),
        Path(".").resolve()
    ]
    
    try:
        resolved_approval = approval_file.resolve()
        is_untrusted = False
        for upath in untrusted_paths:
            if resolved_approval.is_relative_to(upath) or resolved_approval == upath:
                is_untrusted = True
                break
                
        if is_untrusted or not resolved_approval.is_relative_to(approval_dir):
            print("[ERRO] Segurança: Registro de aprovação localizado em diretório não confiável!")
            sys.exit(1)
            
        with open(resolved_approval, "r") as f:
            data = json.load(f)
            approval_record = PromotionApprovalRecord(**data)
    except Exception as e:
        print(f"[ERRO] Falha ao analisar PromotionApprovalRecord: {e}")
        sys.exit(1)
        
    staging_dir = Path(output_dir) / "candidate"
    if not staging_dir.exists():
        print(f"[ERRO] Diretório de staging '{staging_dir}' não encontrado.")
        sys.exit(1)
        
    # Recalculate hashes from staged files
    client_file = staging_dir / "5_SynthesizedPage.client.tsx"
    patch_sha = hashlib.sha256(client_file.read_bytes()).hexdigest() if client_file.exists() else hashlib.sha256(b"").hexdigest()
    
    qa_report_file = staging_dir / "QA_REPORT.md"
    qa_sha = hashlib.sha256(qa_report_file.read_bytes()).hexdigest() if qa_report_file.exists() else hashlib.sha256(b"").hexdigest()
    
    import re
    expected_run_id = ""
    if qa_report_file.exists():
        qa_content = qa_report_file.read_text(encoding="utf-8")
        run_match = re.search(r"\*\*[Ss]andbox Run ID:\*\* (\S+)", qa_content)
        if run_match:
            expected_run_id = run_match.group(1)
            
    # Match double hashes and run id
    if (approval_record.sandbox_run_id != expected_run_id or
        approval_record.patch_candidate_sha256 != patch_sha or
        approval_record.qa_report_sha256 != qa_sha):
        print("[ERRO] Assinatura/Hashes do candidato de aprovação divergem do staging!")
        print(f"       Record Run ID: {approval_record.sandbox_run_id}")
        print(f"       Expected Patch SHA: {patch_sha}, Got: {approval_record.patch_candidate_sha256}")
        print(f"       Expected QA SHA: {qa_sha}, Got: {approval_record.qa_report_sha256}")
        sys.exit(1)
        
    print(f"[PROMOTION] Aprovação verificada! Copiando arquivos finais para: {output_dir}...")
    
    # copy staged files to the output dir
    files_to_copy = [
        "1_artifact.json",
        "2_draft.json",
        "3_code_spec.json",
        "4_tailwind.config.js",
        "5_SynthesizedPage.types.ts",
        "5_SynthesizedPage.client.tsx",
        "5_page.tsx",
        "QA_REPORT.md"
    ]
    
    for f in files_to_copy:
        src = staging_dir / f
        dst = Path(output_dir) / f
        if src.exists():
            shutil.copy(src, dst)
            
    print(f"[PROMOTION SUCESSO] Candidato promovido com sucesso!")
    sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python promote.py <output_dir>")
        sys.exit(1)
    promote_candidate(sys.argv[1])
