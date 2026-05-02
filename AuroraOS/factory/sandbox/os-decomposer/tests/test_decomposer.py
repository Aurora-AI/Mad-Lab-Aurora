import unittest
from pathlib import Path
import sys
import os

# Ajusta path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.os_parser import OSParser
from scripts.decomposer import Decomposer

class TestOSDecomposer(unittest.TestCase):
    
    def test_parser_basic(self):
        content = """
## Passos de Execução
### Passo 1 — Setup
Conteúdo do passo 1.
### Passo 2 — Build
Conteúdo do passo 2.
"""
        parser = OSParser(content)
        steps = parser.extract_steps()
        self.assertEqual(len(steps), 2)
        self.assertEqual(steps[0]["title"], "Passo 1 — Setup")
        
    def test_parser_fallback(self):
        content = """
## Plano de Reparo
- [ ] Tarefa A
- [ ] Tarefa B
"""
        parser = OSParser(content)
        steps = parser.extract_steps()
        self.assertEqual(len(steps), 2)
        self.assertEqual(steps[0]["title"], "Passo 1")
        
    def test_decomposer_dag(self):
        # Usa um path no diretório scratch (que deve ser gravável)
        scratch_dir = r"C:\Users\rodri\.gemini\antigravity\brain\7dcf52cf-2974-49bc-83a0-84114a371980\scratch"
        if not os.path.exists(scratch_dir):
            os.makedirs(scratch_dir)
        os_path = Path(scratch_dir) / "test_os_temp.md"
        try:
            with open(os_path, "w", encoding="utf-8") as f:
                f.write("## Passos de Execução\n### Passo 1 — A\nTest\n### Passo 2 — B\nTest")
                
            decomposer = Decomposer("OS-TEST", os_path)
            decomposed = decomposer.decompose()
            
            self.assertEqual(len(decomposed.tasks), 2)
            self.assertEqual(decomposed.tasks[1].depends_on, ["MT-001"])
        finally:
            # Cleanup
            if os_path.exists():
                os_path.unlink()

if __name__ == "__main__":
    unittest.main()
