from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Literal, Optional

class DiagnosticFinding(BaseModel):
    code: str
    severity: Literal["P0", "P1", "P2", "P3"]
    file_path: Optional[str]
    redacted_message: str
    raw_value_hash: Optional[str] = None
    recommended_action: str

class PipelinePausedException(Exception):
    def __init__(self, message: str, findings: List[DiagnosticFinding]):
        super().__init__(message)
        self.findings = findings

class PatchCandidate(BaseModel):
    sandbox_run_id: str
    base_commit: str
    files_changed: List[str]
    diff_sha256: str
    unified_diff: str
    validator_status: Literal["pending", "passed", "failed"]
    repair_attempt: int
    created_at: datetime = Field(default_factory=datetime.now)

class TelemetryHeartbeat(BaseModel):
    sandbox_run_id: str
    os_id: str
    stage: str
    progress_percent: int
    status: Literal["IN_PROGRESS", "SUCCESS", "FAILED", "PAUSED"]
    elapsed_seconds: int
    error_class: str
    correlation_id: str

class PromotionApprovalRecord(BaseModel):
    promotion_candidate_id: str
    sandbox_run_id: str
    patch_candidate_sha256: str
    qa_report_sha256: str
    approved_by: str
    approved_at: datetime
    approval_nonce: str
    approval_source: Literal["manual_cli", "signed_file", "approval_record"]
    approval_record_sha256: Optional[str] = None
