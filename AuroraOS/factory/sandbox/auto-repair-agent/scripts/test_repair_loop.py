"""Testes unitários para o loop de reparo."""
import unittest
import sys
from pathlib import Path
from unittest.mock import patch

# Adicionar caminhos para imports
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.append(str(current_dir))
sys.path.append(str(parent_dir))

# Importar diretamente o módulo no diretório atual
import repair_loop
from contracts import RepairRequest, SandboxMode, AttemptResult, RepairState

class TestRepairLoop(unittest.TestCase):
    def setUp(self):
        self.sandbox_dir = Path(__file__).parent.parent
        self.activity_path = self.sandbox_dir / "activity.jsonl"
        self.state_path = self.sandbox_dir / "repair_state.json"
        self.escalation_path = self.sandbox_dir / "ESCALATION.md"
        self.artifacts_dir = self.sandbox_dir / "artifacts"
        
        # Limpar arquivos de teste
        for p in [self.activity_path, self.state_path, self.escalation_path]:
            if p.exists(): p.unlink()
            
        if self.artifacts_dir.exists():
            for f in self.artifacts_dir.glob("*.json"):
                f.unlink()

    def test_loop_success_first_attempt(self):
        """Cenário 1: Loop com 1 hipótese que passa na 1ª tentativa -> status fixed."""
        request = RepairRequest(
            task_id="TEST-001",
            evidence_path=Path("evidence.log"),
            test_cmd=["echo", "success"],
            max_attempts=3
        )
        patches = ["patch1"]
        
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)
        qa_verdict_path = self.artifacts_dir / "qa_verdict_TEST-001_1.json"
        with open(qa_verdict_path, "w", encoding="utf-8") as f:
            f.write('{"task_id": "TEST-001", "verdict": "APPROVED", "findings": [], "suggested_corrections": [], "anti_pattern_candidate": false, "confidence": 0.99}')
        
        # Patching the reference in repair_loop module
        with patch("repair_loop.execute_in_sandbox") as mock_exec:
            mock_exec.return_value = (0, "all good", "", 1.0, {})
            
            result = repair_loop.repair_loop(
                request, patches, "OS-003", 
                self.activity_path, self.state_path
            )
            
            self.assertEqual(result.status, "fixed")
            self.assertEqual(result.total_attempts, 1)
            self.assertTrue(self.state_path.exists())
            
            # Verificação de persistência de anti-pattern (Requisito QA)
            ap_file = self.artifacts_dir / f"{result.anti_pattern_id}.json"
            self.assertTrue(ap_file.exists(), f"Artefato {ap_file} deveria existir")
            
            self.assertEqual(mock_exec.call_count, 1)
            
    def test_loop_escalation_after_all_fail(self):
        """Cenário 2: Loop com 3 hipóteses, todas falham -> status escalated."""
        request = RepairRequest(
            task_id="TEST-002",
            evidence_path=Path("evidence.log"),
            test_cmd=["echo", "fail"],
            max_attempts=2
        )
        patches = ["patch1", "patch2"]
        
        with patch("repair_loop.execute_in_sandbox") as mock_exec:
            mock_exec.return_value = (1, "", "error", 1.0, {})
            
            result = repair_loop.repair_loop(
                request, patches, "OS-003", 
                self.activity_path, self.state_path
            )
            
            self.assertEqual(result.status, "escalated")
            self.assertEqual(result.total_attempts, 2)
            self.assertTrue(self.escalation_path.exists())

    def test_idempotency_resumes_from_checkpoint(self):
        """Cenário 4: Loop retomado de checkpoint existente -> não re-executa tentativas anteriores."""
        request = RepairRequest(
            task_id="TEST-003",
            evidence_path=Path("evidence.log"),
            test_cmd=["echo", "retry"],
            max_attempts=3
        )
        patches = ["patch1", "patch2", "patch3"]
        
        # Simular que a primeira tentativa já foi feita e falhou
        initial_state = RepairState(
            task_id="TEST-003",
            sandbox_mode=SandboxMode.MEMORY,
            current_attempt=1,
            completed_attempts=[
                AttemptResult(attempt_number=1, status="failure", duration_seconds=1.0, hypothesis="Hipótese 1")
            ]
        )
        repair_loop.save_checkpoint(self.state_path, initial_state.model_dump())
        
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)
        qa_verdict_path = self.artifacts_dir / "qa_verdict_TEST-003_2.json"
        with open(qa_verdict_path, "w", encoding="utf-8") as f:
            f.write('{"task_id": "TEST-003", "verdict": "APPROVED", "findings": [], "suggested_corrections": [], "anti_pattern_candidate": false, "confidence": 0.99}')
        
        with patch("repair_loop.execute_in_sandbox") as mock_exec:
            mock_exec.return_value = (0, "success on second", "", 1.0, {})
            
            result = repair_loop.repair_loop(
                request, patches, "OS-003", 
                self.activity_path, self.state_path
            )
            
            self.assertEqual(result.status, "fixed")
            self.assertEqual(result.total_attempts, 2)
            self.assertEqual(mock_exec.call_count, 1)

    def test_timeout_registration(self):
        """Cenário 3: Loop com hipótese que causa timeout -> status registrado como timeout."""
        request = RepairRequest(
            task_id="TEST-004",
            evidence_path=Path("evidence.log"),
            test_cmd=["sleep", "10"],
            max_attempts=1,
            timeout_seconds=10
        )
        patches = ["patch1"]
        
        with patch("repair_loop.execute_in_sandbox") as mock_exec:
            mock_exec.return_value = (124, "", "timeout occurred", 15.0, {})
            
            result = repair_loop.repair_loop(
                request, patches, "OS-003", 
                self.activity_path, self.state_path
            )
            self.assertEqual(result.attempts[0].status, "timeout")

    def test_qa_headless_rejection(self):
        """Cenário 5: QA rejeita a primeira tentativa, segunda tentativa passa."""
        request = RepairRequest(
            task_id="TEST-005",
            evidence_path=Path("evidence.log"),
            test_cmd=["echo", "success"],
            max_attempts=3
        )
        patches = ["patch1", "patch2"]
        
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)
        qa_verdict_1 = self.artifacts_dir / "qa_verdict_TEST-005_1.json"
        with open(qa_verdict_1, "w", encoding="utf-8") as f:
            f.write('{"task_id": "TEST-005", "verdict": "REJECTED", "findings": ["Code is messy"], "suggested_corrections": ["Clean it up"], "anti_pattern_candidate": true, "confidence": 0.8}')
            
        qa_verdict_2 = self.artifacts_dir / "qa_verdict_TEST-005_2.json"
        with open(qa_verdict_2, "w", encoding="utf-8") as f:
            f.write('{"task_id": "TEST-005", "verdict": "APPROVED", "findings": [], "suggested_corrections": [], "anti_pattern_candidate": false, "confidence": 0.99}')
            
        with patch("repair_loop.execute_in_sandbox") as mock_exec:
            mock_exec.return_value = (0, "success", "", 1.0, {})
            
            result = repair_loop.repair_loop(
                request, patches, "OS-003", 
                self.activity_path, self.state_path
            )
            
            self.assertEqual(result.status, "fixed")
            self.assertEqual(result.total_attempts, 2)
            self.assertEqual(mock_exec.call_count, 2)
            self.assertEqual(result.attempts[0].status, "failure") # Because QA rejected it!
            self.assertTrue("QA REJECTED" in result.attempts[0].stderr)

if __name__ == "__main__":
    unittest.main()
