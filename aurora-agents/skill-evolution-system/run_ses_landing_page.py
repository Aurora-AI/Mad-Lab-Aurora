import sys
import os
import json

# Add root to path
sys.path.append(os.path.dirname(__file__))

from src.pipeline import run_pipeline
from storage.vault import persist

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

# Paths
skill_path = r"c:\Users\rodri\.gemini\antigravity\skills\landing-page-architect\SKILL.md"
benchmark_path = r"C:\Users\rodri\.gemini\antigravity\skills\agente-awwwards\SKILL.md"

# Read contents
skill_content = read_file(skill_path)
benchmark_content = read_file(benchmark_path)

test_cases = [
    {"input": "Landing Page for AI Startup", "expected_properties": ["structure", "design_manual"]},
    {"input": "Investor Deck Page", "expected_properties": ["pacing", "hierarchy"]},
    {"input": "Legal Tech Dashboard", "expected_properties": ["audit", "compliance"]}
]

print("--- SES EXECUTION: landing-page-architect ---")
result = run_pipeline(skill_content, [benchmark_content], test_cases)

# Formatting evolved skill for display (first 20 lines)
evolved_preview = "\n".join(result["evolved_skill"].split("\n")[:20])
print(f"Evolved Skill Preview:\n{evolved_preview}\n...")

print(f"\nScore: {result['score']}")
print(f"Pass Rate: {result['validation']['pass_rate']}")
print(f"Certification: {result['certification']}")

# Persist evidence
persist(result)
print("\nEvidence persisted to vault_log.json")
