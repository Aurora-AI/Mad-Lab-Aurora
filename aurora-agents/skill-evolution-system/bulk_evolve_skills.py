import sys
import os
import json
from pathlib import Path

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from pipeline import run_pipeline
from storage.vault import persist

def read_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return None

skills_root = Path(r"c:\Users\rodri\.gemini\antigravity\skills")
benchmark_path = skills_root / "agente-awwwards" / "SKILL.md"
benchmark_content = read_file(str(benchmark_path))

test_cases = [
    {"input": "Standard processing task", "expected_properties": ["determinism", "structure"]},
    {"input": "High-impact visual request", "expected_properties": ["pacing", "hierarchy"]}
]

results = []

print("--- BULK SES EVOLUTION START ---")

# Iterate through all directories in skills_root
for skill_dir in skills_root.iterdir():
    if skill_dir.is_dir():
        skill_file = skill_dir / "SKILL.md"
        if skill_file.exists():
            print(f"Evolving: {skill_dir.name}...")
            skill_content = read_file(str(skill_file))
            if not skill_content:
                continue
                
            # Use the skill itself as a partial benchmark if needed, 
            # but here we use the global benchmark
            result = run_pipeline(skill_content, [benchmark_content], test_cases)
            
            # Record summary
            results.append({
                "skill": skill_dir.name,
                "score": result["score"],
                "certification": result["certification"],
                "pass_rate": result["validation"]["pass_rate"]
            })
            
            # Persist full evidence
            persist(result)

# Save summary to a specific file for the report
summary_path = Path(__file__).parent / "bulk_evolution_summary.json"
with open(summary_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)

print(f"\n--- BULK EVOLUTION COMPLETE ---")
print(f"Processed {len(results)} skills.")
print(f"Summary saved to {summary_path}")
