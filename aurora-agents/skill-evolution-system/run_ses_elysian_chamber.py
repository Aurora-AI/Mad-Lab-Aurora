import sys
import os

sys.path.append(os.path.dirname(__file__))

from src.pipeline import run_pipeline
from storage.vault import persist

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

skill_path = r"C:\Projetos\MadLabAurora\integrations\open-design\skills\elysian-chamber-prototype\SKILL.md"
benchmark_path = r"C:\Projetos\MadLabAurora\integrations\open-design\skills\web-prototype-taste-editorial\SKILL.md"

skill_content = read_file(skill_path)
benchmark_content = read_file(benchmark_path)

test_cases = [
    {
        "input": "Chamber C02 dark world fail-closed gate",
        "expected_properties": ["dark_canvas", "fail_closed_gate", "locked_copy", "hud_pillars"]
    },
    {
        "input": "Chamber C01 light world spring fragments",
        "expected_properties": ["light_canvas", "asymmetric_layout", "fibonacci_spacing", "hud_label"]
    },
    {
        "input": "Chamber C05 dark world category declaration",
        "expected_properties": ["dark_canvas", "monumental_wordmark", "cta_button", "anti_patterns_absent"]
    }
]

print("--- SES EXECUTION: elysian-chamber-prototype ---")
result = run_pipeline(skill_content, [benchmark_content], test_cases)

evolved_preview = "\n".join(result["evolved_skill"].split("\n")[:20])
print(f"Evolved Skill Preview:\n{evolved_preview}\n...")
print(f"\nScore: {result['score']}")
print(f"Pass Rate: {result['validation']['pass_rate']}")
print(f"Certification: {result['certification']}")

persist(result)
print("\nEvidence persisted to vault_log.json")
