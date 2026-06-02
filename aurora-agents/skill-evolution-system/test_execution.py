import sys
import os
import json

# Add root to path
sys.path.append(os.path.dirname(__file__))

from src.pipeline import run_pipeline
from storage.vault import persist

payload = {
  "skill": "texto genérico",
  "benchmarks": ["skill altamente estruturada"],
  "test_cases": [
    {"input": "A", "expected_properties": ["structure"]},
    {"input": "B", "expected_properties": ["structure"]},
    {"input": "C", "expected_properties": ["structure"]}
  ]
}

print("--- SES EXECUTION TEST ---")
result = run_pipeline(payload["skill"], payload["benchmarks"], payload["test_cases"])

print(json.dumps(result, indent=2))

# Persist evidence
print("\n--- PERSISTING EVIDENCE ---")
persist(result)
print("Evidence persisted to vault_log.json")
