from typing import List, Literal, Optional
from pydantic import BaseModel, Field

class ColorOriginalityFinding(BaseModel):
    hex_value: str
    is_neutral: bool
    is_distinctive: bool
    source_usage: Literal["background", "text", "cta", "brand", "accent", "unknown"]
    action: Literal["allow", "transform", "block"]
    reason: str

class OriginalityScoreBreakdown(BaseModel):
    brand_score: float
    text_score: float
    asset_score: float
    layout_score: float
    motion_score: float
    color_score: float
    component_score: float
    final_score: float

class SourceFingerprint(BaseModel):
    source_artifact_hash: str
    layout_hash: Optional[str] = None
    color_palette_hash: Optional[str] = None
    typography_hash: Optional[str] = None
    motion_hash: Optional[str] = None
    asset_hashes: List[str] = Field(default_factory=list)
    text_hashes: List[str] = Field(default_factory=list)
    component_names: List[str] = Field(default_factory=list)

class CandidateFingerprint(BaseModel):
    layout_hash: Optional[str] = None
    color_palette_hash: Optional[str] = None
    typography_hash: Optional[str] = None
    motion_hash: Optional[str] = None
    asset_hashes: List[str] = Field(default_factory=list)
    text_hashes: List[str] = Field(default_factory=list)
    component_names: List[str] = Field(default_factory=list)

class SourcePattern(BaseModel):
    pattern_id: str
    source_url: Optional[str] = None
    source_artifact_hash: str
    pattern_type: Literal[
        "layout",
        "typography",
        "color",
        "motion",
        "component",
        "interaction",
        "copy_structure"
    ]
    extracted_principle: str
    raw_reference: Optional[str] = None

class TransmutationRule(BaseModel):
    rule_id: str
    source_pattern_id: str
    transformation_axes: List[
        Literal["semantic", "visual", "structural", "motion", "brand", "interaction"]
    ]
    forbidden_similarities: List[str]
    required_differences: List[str]

class ProprietaryPatternCandidate(BaseModel):
    candidate_id: str
    source_pattern_ids: List[str]
    generated_name: str
    design_intent: str
    transformed_description: str
    implementation_guidance: str
    
    # Originality Governance
    originality_score: float
    score_breakdown: OriginalityScoreBreakdown
    transformation_axes: List[
        Literal["semantic", "visual", "structural", "motion", "brand", "interaction"]
    ]
    
    # Risk Level
    risk_level: Literal["low", "medium", "high", "blocked", "manual_review_required"]
    blocked_reasons: List[str]
    color_findings: List[ColorOriginalityFinding] = Field(default_factory=list)
    candidate_fingerprint: CandidateFingerprint
