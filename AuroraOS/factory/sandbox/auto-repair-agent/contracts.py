"""Contratos Pydantic para o auto-repair-agent."""
from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Literal, Any

from pydantic import BaseModel, Field


class SandboxMode(str, Enum):
    MEMORY = "memory"
    WORKTREE = "worktree"
    CONTAINER = "container"


class RepairRequest(BaseModel):
    """Input para uma tentativa de reparo."""
    task_id: str = Field(..., description="ID único da tarefa falha")
    evidence_path: Path = Field(..., description="Caminho para o artefato de evidência")
    test_cmd: list[str] = Field(
        ...,
        description="Comando de teste como lista de tokens (shell=False)",
        min_length=1,
    )
    source_files: list[Path] = Field(
        default_factory=list,
        description="Arquivos-fonte envolvidos na falha",
    )
    original_requirement: str = Field(
        default="",
        description="Requisito original extraído da micro-tarefa"
    )
    max_attempts: int = Field(default=3, ge=1, le=5)
    timeout_seconds: int = Field(default=120, ge=10, le=600)
    qa_timeout_seconds: int = Field(default=300, ge=10, le=1800)


class AttemptResult(BaseModel):
    """Resultado de uma tentativa individual de reparo."""
    attempt_number: int
    status: Literal["success", "failure", "timeout"]
    duration_seconds: float
    stdout: str = ""
    stderr: str = ""
    patch_diff: str | None = None
    hypothesis: str = ""
    metrics: dict[str, Any] = Field(default_factory=dict)


class RepairResult(BaseModel):
    """Resultado final do ciclo de reparo."""
    task_id: str
    status: Literal["fixed", "escalated", "timeout"]
    sandbox_mode: SandboxMode
    total_attempts: int
    attempts: list[AttemptResult]
    patch_diff: str | None = None
    anti_pattern_id: str | None = None
    escalation_reason: str | None = None


class RepairState(BaseModel):
    """Checkpoint de estado para idempotência (M1)."""
    task_id: str
    sandbox_mode: SandboxMode
    completed_attempts: list[AttemptResult] = Field(default_factory=list)
    current_attempt: int = 0
    is_terminal: bool = False
    final_result: RepairResult | None = None


class ActivityEvent(BaseModel):
    """Evento estruturado para activity.jsonl (M2)."""
    timestamp: str
    event_type: Literal[
        "REPAIR_STARTED",
        "REPAIR_ATTEMPT",
        "REPAIR_COMPLETED",
        "REPAIR_ESCALATED",
    ]
    os_id: str
    task_id: str
    metadata: dict


class AntiPatternCandidate(BaseModel):
    """Candidato a anti-pattern para delegação ao agent-reflexion-code."""
    pattern_id: str  # ex: "KI-20260501-schema-missing-field"
    category: Literal["CI", "IR", "CA", "DT", "IA", "CC", "PE"]
    product: str  # ex: "ElysianLex", "CRM", "Ozzmosis"
    symptom: str  # o que aconteceu
    fix_applied: str  # o que corrigiu
    domains: list[str]  # ex: ["Schema", "API"]


class QAHeadlessRequest(BaseModel):
    """Input para QA headless — gerado pelo repair_loop."""
    task_id: str
    os_id: str
    repair_result: RepairResult
    original_requirement: str
    test_cmd: str | list[str]
    test_output: str
    patch_diff: str


class QAHeadlessVerdict(BaseModel):
    """Output do QA headless."""
    task_id: str
    verdict: Literal["APPROVED", "REJECTED", "NEEDS_REVIEW"]
    findings: list[str]
    suggested_corrections: list[str]
    anti_pattern_candidate: bool
    confidence: float


class DispatchEvent(BaseModel):
    """Evento detectado pelo dispatcher."""
    event_type: Literal[
        "MICRO_TASK_COMPLETED",
        "REPAIR_COMPLETED",
        "QA_REJECTED",
        "QA_APPROVED",
    ]
    source_file: Path  # arquivo que disparou o evento
    task_id: str
    os_id: str
    detected_at: str  # ISO timestamp
    dispatched_to: str  # ex: "repair_loop", "qa_headless"


class DispatcherConfig(BaseModel):
    """Configuração do dispatcher."""
    watch_dirs: list[Path]
    poll_interval_seconds: int = 5
    max_concurrent_dispatches: int = 1  # v0 é serial
    activity_log_path: Path
