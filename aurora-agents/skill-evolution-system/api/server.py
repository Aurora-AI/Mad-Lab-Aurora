import sys
import os

# Add src to path to allow imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from fastapi import FastAPI
from pipeline import run_pipeline

app = FastAPI()

@app.post("/skill/evolve")
def evolve(payload: dict):
    skill = payload["skill"]
    test_cases = payload.get("test_cases", [])
    benchmarks = payload.get("benchmarks", [])

    result = run_pipeline(skill, benchmarks, test_cases)

    return result
