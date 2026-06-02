import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

def conductor_hook(event):
    if event["type"] == "skill.created" or event["type"] == "skill.updated":
        from pipeline import run_pipeline

        result = run_pipeline(
            event["skill"],
            event["benchmarks"],
            event["test_cases"]
        )

        if result["certification"] != "certified":
            raise Exception("Skill não certificada - bloqueada pelo Conductor")

        return result
