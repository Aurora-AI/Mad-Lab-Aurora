import pytest
import tempfile
import shutil
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
from orchestrator import SandboxOrchestrator, CommandBlockedException

@pytest.fixture
def temp_workspace():
    d = tempfile.mkdtemp()
    yield d
    shutil.rmtree(d)

def test_sandbox_path_boundary_check(temp_workspace):
    orchestrator = SandboxOrchestrator(temp_workspace)
    
    # Valid relative path inside workspace
    valid_path = Path(temp_workspace) / "sandbox_run_test"
    assert orchestrator.validate_path(valid_path) == valid_path.resolve()
    
    # Escaping target path
    invalid_path = Path(temp_workspace).parent / "escaped_dir"
    with pytest.raises(CommandBlockedException) as exc:
        orchestrator.validate_path(invalid_path)
    assert "escapes workspace boundary" in str(exc.value)

def test_sandbox_symlink_blocking(temp_workspace):
    orchestrator = SandboxOrchestrator(temp_workspace)
    test_path = Path(temp_workspace) / "symlinked_dir"
    
    # Mock Path.is_symlink to return True to simulate a junction/symlink escape
    with patch.object(Path, "is_symlink", return_value=True):
        with pytest.raises(CommandBlockedException) as exc:
            orchestrator.validate_path(test_path)
        assert "contains symlink or junction escapes" in str(exc.value)

def test_sandbox_execution_allowlist(temp_workspace):
    orchestrator = SandboxOrchestrator(temp_workspace)
    orchestrator.setup_worktree()
    
    # Allowed command (using prefix check)
    # mock subprocess.run inside
    with patch("subprocess.run") as mock_sub:
        mock_sub.return_value = MagicMock(returncode=0)
        orchestrator.run_command(["python", "-m", "pytest", "tests/"], cwd=orchestrator.sandbox_dir)
        mock_sub.assert_called_once()
        
    # Blocked command (not in allowlist)
    with pytest.raises(CommandBlockedException) as exc:
        orchestrator.run_command(["python", "run_server.py"], cwd=orchestrator.sandbox_dir)
    assert "blocked by allowlist policy" in str(exc.value)
    
    # Blocked shell usage
    with pytest.raises(CommandBlockedException) as exc:
        orchestrator.run_command(["python", "-m", "pytest"], cwd=orchestrator.sandbox_dir, shell=True)
    assert "shell=True is strictly prohibited" in str(exc.value)

def test_sandbox_blocked_keywords(temp_workspace):
    orchestrator = SandboxOrchestrator(temp_workspace)
    orchestrator.setup_worktree()
    
    # Blocked keywords like npm install
    with pytest.raises(CommandBlockedException) as exc:
        orchestrator.run_command(["npm", "install", "lodash"], cwd=orchestrator.sandbox_dir)
    assert "Blocked command keyword 'install'" in str(exc.value)

    # Blocked git push
    with pytest.raises(CommandBlockedException) as exc:
        orchestrator.run_command(["git", "push", "origin", "main"], cwd=orchestrator.sandbox_dir)
    assert "Blocked command keyword 'push'" in str(exc.value)
    
    orchestrator.cleanup_worktree()
