from pydantic import BaseModel, Field
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

class MicroTask(BaseModel):
    """Uma micro-tarefa decomposta de uma OS."""
    task_id: str  # ex: "MT-001"
    description: str
    input_expected: str  # estado do código antes
    output_expected: str  # estado do código depois
    test_cmd: List[str]  # comando determinístico (shell=False)
    test_exit_code: int = 0  # exit code esperado
    depends_on: List[str] = Field(default_factory=list)  # IDs das micro-tarefas predecessoras
    max_lines_delta: int = 50
    max_duration_seconds: int = 120

class DecomposedOS(BaseModel):
    """Output da decomposição de uma OS."""
    os_id: str
    original_os_path: Path
    tasks: List[MicroTask]
    dependency_graph: Dict[str, List[str]]  # task_id → [predecessors]
    estimated_total_duration_seconds: int
    decomposed_at: datetime = Field(default_factory=datetime.now)
