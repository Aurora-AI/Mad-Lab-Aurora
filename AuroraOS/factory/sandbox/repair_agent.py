import os
import sys
import hashlib
from datetime import datetime
from pathlib import Path
from typing import List, Literal

# Ajuste de path para importação
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from sandbox_contracts import PatchCandidate, DiagnosticFinding, PipelinePausedException
from orchestrator import SandboxOrchestrator
from validator import SandboxValidator

class LimitedRepairAgent:
    def __init__(self, orchestrator: SandboxOrchestrator):
        self.orchestrator = orchestrator
        self.max_attempts = 3
        
    def generate_diff(self, original_content: str, modified_content: str, file_name: str) -> str:
        """Generates a standard unified diff between original and modified content."""
        import difflib
        diff = difflib.unified_diff(
            original_content.splitlines(keepends=True),
            modified_content.splitlines(keepends=True),
            fromfile=f"a/{file_name}",
            tofile=f"b/{file_name}"
        )
        return "".join(diff)

    def attempt_repair(self, file_path_relative: str, original_content: str, repair_hypotheses: List[str]) -> PatchCandidate:
        """
        Runs the repair loop up to 3 times.
        Validates findings on each attempt, outputting a PatchCandidate.
        """
        sandbox_file = self.orchestrator.sandbox_dir / file_path_relative
        self.orchestrator.validate_path(sandbox_file)
        
        validator = SandboxValidator(str(self.orchestrator.sandbox_dir))
        
        last_diff = ""
        last_diff_hash = ""
        status: Literal["pending", "passed", "failed"] = "failed"
        
        # Limita o número de tentativas a max_attempts
        run_attempts = min(len(repair_hypotheses), self.max_attempts)
        attempts_made = 0
        
        for attempt in range(1, run_attempts + 1):
            attempts_made = attempt
            modified_content = repair_hypotheses[attempt - 1]
            
            # Grava no arquivo temporário do sandbox
            with open(sandbox_file, "w", encoding="utf-8") as f:
                f.write(modified_content)
                
            try:
                # Valida o workspace
                validator.validate_workspace()
                status = "passed"
                last_diff = self.generate_diff(original_content, modified_content, file_path_relative)
                last_diff_hash = hashlib.sha256(last_diff.encode()).hexdigest()
                break
            except PipelinePausedException:
                last_diff = self.generate_diff(original_content, modified_content, file_path_relative)
                last_diff_hash = hashlib.sha256(last_diff.encode()).hexdigest()
                status = "failed"
                
        return PatchCandidate(
            sandbox_run_id=self.orchestrator.run_id,
            base_commit=self.get_head_commit(),
            files_changed=[file_path_relative],
            diff_sha256=last_diff_hash,
            unified_diff=last_diff,
            validator_status=status,
            repair_attempt=attempts_made
        )
        
    def get_head_commit(self) -> str:
        """Retrieves current HEAD commit sha safely."""
        try:
            import subprocess
            res = subprocess.run(
                ["git", "-c", "core.hooksPath=/dev/null", "rev-parse", "HEAD"], 
                capture_output=True, text=True, env={"GIT_CONFIG_NOSYSTEM": "1"}
            )
            return res.stdout.strip()
        except Exception:
            return "unknown-commit-sha"
