import pytest
import tempfile
import shutil
import os
from pathlib import Path
from unittest.mock import MagicMock, patch
from orchestrator import SandboxOrchestrator
from repair_agent import LimitedRepairAgent
from sandbox_contracts import PatchCandidate

@pytest.fixture
def temp_workspace():
    d = tempfile.mkdtemp()
    yield d
    shutil.rmtree(d)

def test_repair_agent_attempts_limit(temp_workspace):
    orchestrator = SandboxOrchestrator(temp_workspace)
    orchestrator.setup_worktree()
    
    # Prepara o arquivo original
    target_file_rel = "app.py"
    original_file = orchestrator.sandbox_dir / target_file_rel
    original_file.write_text("print('hello')", encoding="utf-8")
    
    agent = LimitedRepairAgent(orchestrator)
    
    # 4 hypotheses that fail validation because they contain P0 code 'eval()'
    hypotheses = [
        "eval('1')\n",
        "eval('2')\n",
        "eval('3')\n",
        "eval('4')\n"
    ]
    
    candidate = agent.attempt_repair(target_file_rel, "print('hello')", hypotheses)
    
    # Deve executar exatamente 3 tentativas (limite de max_attempts)
    assert candidate.repair_attempt == 3
    assert candidate.validator_status == "failed"
    assert "eval('3')" in candidate.unified_diff
    assert "eval('4')" not in candidate.unified_diff
    
    orchestrator.cleanup_worktree()

def test_repair_agent_success_stop(temp_workspace):
    orchestrator = SandboxOrchestrator(temp_workspace)
    orchestrator.setup_worktree()
    
    target_file_rel = "app.py"
    original_file = orchestrator.sandbox_dir / target_file_rel
    original_file.write_text("print('hello')", encoding="utf-8")
    
    agent = LimitedRepairAgent(orchestrator)
    
    # First hypothesis fails (eval), second succeeds (clean code), third (exec) is not run
    hypotheses = [
        "eval('1')\n",
        "print('clean code')\n",
        "exec('print(2)')\n"
    ]
    
    candidate = agent.attempt_repair(target_file_rel, "print('hello')", hypotheses)
    
    # Deve rodar 2 tentativas e parar na segunda (sucesso)
    assert candidate.repair_attempt == 2
    assert candidate.validator_status == "passed"
    assert "print('clean code')" in candidate.unified_diff
    assert "exec('print(2)')" not in candidate.unified_diff
    
    orchestrator.cleanup_worktree()
