from enum import Enum
from typing import List, Literal, Optional
from pydantic import BaseModel, Field

class MadLabThemeIntent(str, Enum):
    TUNNEL_PROGRESSION = "tunnel_progression"
    DEPTH_TRAVERSE = "depth_traverse"
    FLUID_EDITORIAL = "fluid_editorial"

class ZAxisScrollModel(str, Enum):
    VERTICAL_INPUT_TO_Z = "vertical_input_to_z"
    HORIZONTAL_INPUT_TO_Z = "horizontal_input_to_z"

class DepthLayerSpec(BaseModel):
    layer_id: str = Field(..., description="Unique ID for this depth layer")
    z_position: float = Field(..., description="Absolute depth position in Z axis (e.g., -1000px)")
    scale_factor: float = Field(..., description="Visual scale factor at this depth layer (e.g., 0.5)")
    opacity_limit: float = Field(1.0, description="Maximum opacity allowed for elements in this layer")

class NullSpaceProfile(BaseModel):
    null_space_ratio: float = Field(..., description="Ratio of empty space to content (e.g., 0.6 means 60% of viewport is empty)")
    min_padding_rem: float = Field(..., description="Minimum padding in rem units (e.g., 8.0)")

class TunnelProgressionStrategy(str, Enum):
    FORWARD_ONLY = "forward_only"
    BIDIRECTIONAL = "bidirectional"

class MotionBudget(BaseModel):
    desktop_fps: int = Field(60, description="Target frame rate on desktop devices")
    mobile_fps: int = Field(30, description="Target frame rate on mobile devices")
    max_layers: int = Field(5, description="Maximum depth layers allowed to preserve performance")

class ReducedMotionFallback(str, Enum):
    STATIC_DEPTH_SECTIONS = "static_depth_sections"
    FADE_SECTIONS = "fade_sections"
    STATIC_SECTIONS = "static_sections"

class MadLabThemeContract(BaseModel):
    intent: MadLabThemeIntent = Field(default=MadLabThemeIntent.TUNNEL_PROGRESSION)
    scroll_model: ZAxisScrollModel = Field(default=ZAxisScrollModel.VERTICAL_INPUT_TO_Z)
    layers: List[DepthLayerSpec] = Field(default_factory=list)
    null_space: NullSpaceProfile = Field(
        default_factory=lambda: NullSpaceProfile(null_space_ratio=0.5, min_padding_rem=6.0)
    )
    progression: TunnelProgressionStrategy = Field(default=TunnelProgressionStrategy.FORWARD_ONLY)
    budget: MotionBudget = Field(default_factory=MotionBudget)
    fallback: ReducedMotionFallback = Field(default=ReducedMotionFallback.STATIC_DEPTH_SECTIONS)
