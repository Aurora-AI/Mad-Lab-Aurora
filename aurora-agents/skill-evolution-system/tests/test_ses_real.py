import unittest
import sys
import os
from pathlib import Path

# Add src to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from src.analyzer import analyze
from src.scorer import score
from src.compiler import compile_skill
from src.validator import validate
from src.pipeline import run_pipeline

class TestSESReal(unittest.TestCase):

    def setUp(self):
        # Use an existing file in the project as reference so it exists
        self.mock_skill = """---
name: test-skill
version: 1.0.0
domain: test
trigger: "test trigger user input"
---

# Test Skill

Você é um agente de testes.

## Gatilhos de Ativação
- Quando o usuário disser "teste este fluxo" ou solicitar um diagnóstico express.

## Referenciais Cognitivos
- Raciocínio de teste de conformidade.

## Modos de Operação
### Modo 1 — Execução Expressa
Indicado para tarefas rápidas.

### Modo 2 — Auditoria Completa
Indicado para análises profundas.

## Formato de Saída
format: markdown
A saída deve conter o diagnóstico completo. Não usar placeholders.

## Regras Invariantes (Anti-Alucinação)
- NÃO assuma APIs ou comandos sem antes fazer uma varredura física ativa de contratos.

## Referências
- docs/Vault/Raw/critique_theater_spec.md
"""

    def test_analyzer(self):
        analysis = analyze(self.mock_skill)
        self.assertEqual(analysis["name"], "test-skill")
        self.assertIn("Modos de Operação", analysis["headings"])
        self.assertTrue(analysis["has_templates"])
        self.assertIn("docs/Vault/Raw/critique_theater_spec.md", analysis["references"])

    def test_scorer(self):
        scoring = score(self.mock_skill)
        self.assertIn("score", scoring)
        self.assertIn("rubrics", scoring)
        # It should have a score >= 70 since it's a complete mock skill
        self.assertGreaterEqual(scoring["score"], 70)
        self.assertIn("trigger-clarity", scoring["rubrics"])

    def test_compiler(self):
        patterns = {
            "required_frontmatter_keys": ["name", "version", "domain", "classification"],
            "expected_headings": ["Referenciais Cognitivos", "Modos de Operação", "Referências", "Regras Invariantes (Anti-Alucinação)"]
        }
        # In this mock skill, references and modes are already present, so compiler will merge keys and keep content
        evolved = compile_skill(self.mock_skill, patterns)
        self.assertIn("classification: local-agents", evolved)
        self.assertIn("Regras Invariantes (Anti-Alucinação)", evolved)

    def test_pipeline(self):
        test_cases = [
            {"input": "Standard task", "expected_properties": ["determinism", "structure"]}
        ]
        result = run_pipeline(self.mock_skill, [self.mock_skill], test_cases)
        self.assertIn("score", result)
        self.assertIn("certification", result)
        self.assertTrue(len(result["evolved_skill"]) > len(self.mock_skill))

if __name__ == "__main__":
    unittest.main()
