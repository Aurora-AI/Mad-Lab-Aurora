import sys
import os

sys.path.append(os.path.dirname(__file__))

from src.pipeline import run_pipeline
from storage.vault import persist

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

skill_path = r"C:\Projetos\MadLabAurora\integrations\open-design\skills\elysian-sequence-rig\SKILL.md"
benchmark_path = r"C:\Projetos\MadLabAurora\integrations\open-design\skills\elysian-chamber-prototype\SKILL.md"

skill_content = read_file(skill_path)
benchmark_content = read_file(benchmark_path)

test_cases = [
    {
        "input": "Generate full SequenceRig scaffold for 5 chambers with snap",
        "expected_properties": ["lenis_init", "scrolltrigger_pin", "camera_context", "reduced_motion"]
    },
    {
        "input": "Generate only useCameraProgress.ts",
        "expected_properties": ["world_map", "progress_to_chamber", "context_export"]
    },
    {
        "input": "Generate HudTelemetry with dark/light world switching",
        "expected_properties": ["chamber_labels", "world_tone_colors", "fixed_position"]
    }
]

print("--- SES EXECUTION: elysian-sequence-rig ---")
result = run_pipeline(skill_content, [benchmark_content], test_cases)

evolved_preview = "\n".join(result["evolved_skill"].split("\n")[:20])
print(f"Evolved Skill Preview:\n{evolved_preview}\n...")
print(f"\nScore: {result['score']}")
print(f"Pass Rate: {result['validation']['pass_rate']}")
print(f"Certification: {result['certification']}")

persist(result)
print("\nEvidence persisted to vault_log.json")
