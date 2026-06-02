from pydantic import BaseModel
from typing import Literal, List

class PerceptualScoreBreakdown(BaseModel):
    structural_similarity_score: float
    contrast_score: float
    visual_density_score: float
    layout_integrity_score: float
    overlap_score: float
    viewport_fit_score: float
    final_score: float

class PerceptualFinding(BaseModel):
    code: str
    severity: Literal["P0", "P1", "P2", "P3"]
    axis: Literal[
        "blank_screen",
        "contrast",
        "density",
        "overlap",
        "layout_shift",
        "viewport_fit",
        "render_error",
        "visual_similarity"
    ]
    message: str
    recommended_action: str

class VisualRegressionReport(BaseModel):
    report_id: str
    render_bundle_id: str
    screenshot_path: str
    perceptual_score: PerceptualScoreBreakdown
    findings: List[PerceptualFinding]
    decision: Literal["approved", "rejected", "manual_review_required"]
    blocked_reasons: List[str]
