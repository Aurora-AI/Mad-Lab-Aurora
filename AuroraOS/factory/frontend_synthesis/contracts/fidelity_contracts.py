from pydantic import BaseModel
from typing import Literal, List

class FidelityScoreBreakdown(BaseModel):
    proportion_score: float
    visual_hierarchy_score: float
    density_score: float
    contrast_score: float
    spacing_score: float
    compositional_rhythm_score: float
    intent_fidelity_score: float

class CloneRiskBreakdown(BaseModel):
    layout_similarity_risk: float
    spacing_similarity_risk: float
    typography_similarity_risk: float
    color_similarity_risk: float
    motion_similarity_risk: float
    final_clone_risk: float

class FidelityFinding(BaseModel):
    code: str
    severity: Literal["P0", "P1", "P2", "P3"]
    axis: Literal[
        "proportion",
        "visual_hierarchy",
        "density",
        "contrast",
        "spacing",
        "compositional_rhythm",
        "clone_risk"
    ]
    message: str
    recommended_action: str

class VisualFidelityReport(BaseModel):
    report_id: str
    code_spec_id: str
    hybrid_truth_id: str
    proprietary_candidate_id: str
    fidelity: FidelityScoreBreakdown
    clone_risk: CloneRiskBreakdown
    findings: List[FidelityFinding]
    decision: Literal["approved", "rejected", "manual_review_required"]
    blocked_reasons: List[str]
