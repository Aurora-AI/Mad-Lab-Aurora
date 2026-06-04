import re
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime

class ExperienceSurface(str, Enum):
    LANDING = "landing"
    CRM = "crm"
    PORTAL = "portal"
    DASHBOARD = "dashboard"
    CANVAS = "canvas"

class NavigationStrategy(str, Enum):
    CANVAS_NAVIGATION = "canvas_navigation"
    STANDARD = "standard"
    KEYBOARD_DRIVEN = "keyboard_driven"
    MEGA_DROPDOWN = "mega_dropdown"
    MINIMAL_CHROME = "minimal_chrome"
    SMOOTH_SCROLL = "smooth_scroll"

class MotionStrategy(str, Enum):
    KINETIC_FIELD = "kinetic_field"
    PARALLAX = "parallax"
    SUBTLE_TRANSITIONS = "subtle_transitions"
    GRADIENT_FLOW = "gradient_flow"
    STREAM_RESPONSE = "stream_response"
    NONE = "none"

class SpatialStrategy(str, Enum):
    FREEFORM_DEPTH = "freeform_depth"
    CLEAN_BENTO = "clean_bento"
    LAYERED_CARDS = "layered_cards"
    SPLIT_SCREEN = "split_screen"
    STANDARD = "standard"

class AttentionStrategy(str, Enum):
    FOCAL_HIERARCHY = "focal_hierarchy"
    READING_FLOW = "reading_flow"
    MINIMAL_FOCUS = "minimal_focus"

class NarrativeStrategy(str, Enum):
    PROGRESSIVE_DISCOVERY = "progressive_discovery"
    IMMERSIVE_NARRATIVE = "immersive_narrative"
    CHAT_FLOW = "chat_flow"
    STANDARD = "standard"

class ExperienceBlueprint(BaseModel):
    surface_type: ExperienceSurface = Field(..., description="The main target surface classification")
    navigation_strategy: NavigationStrategy = Field(..., description="Navigation pattern to use")
    motion_strategy: MotionStrategy = Field(..., description="Motion pattern and animation strategy to apply")
    spatial_strategy: SpatialStrategy = Field(..., description="Spatial structure and layout design")
    attention_strategy: AttentionStrategy = Field(..., description="Attention mapping and visual focus design")
    narrative_strategy: NarrativeStrategy = Field(..., description="Content flow and user progression narrative style")
    interaction_density: str = Field(..., description="Interaction complexity: low, medium, high")
    visual_energy: str = Field(..., description="Visual aesthetic energy level: low, medium, high")
    immersion_level: str = Field(..., description="Depth of focus and engagement: low, medium, high")
    rationale: str = Field("Default experience blueprint architecture design rationale.", description="Design rationale")

class ExperienceArchitectureReport(BaseModel):
    blueprint: ExperienceBlueprint = Field(..., description="Resolved Experience Architecture Blueprint")
    rationale: str = Field(..., description="Detailed design rationale for the choices made")
    architected_at: datetime = Field(default_factory=datetime.now, description="Timestamp of generation")
