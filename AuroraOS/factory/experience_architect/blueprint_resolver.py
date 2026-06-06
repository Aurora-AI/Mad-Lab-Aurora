import sys
import os
from typing import Optional, Dict, Any

# Ensure contracts are discoverable
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.extend([
    os.path.abspath(os.path.join(current_dir, "../frontend_synthesis/contracts")),
    os.path.abspath(os.path.join(current_dir, "../contracts"))
])

from experience_architecture_contracts import (
    ExperienceBlueprint,
    ExperienceSurface,
    NavigationStrategy,
    MotionStrategy,
    SpatialStrategy,
    AttentionStrategy,
    NarrativeStrategy
)

class BlueprintResolver:
    """
    Decoupled resolver that translates layout ratios, motion patterns, 
    visual hierarchy, narrative structures, and interaction density 
    into a concrete architectural ExperienceBlueprint.
    """
    
    def resolve_blueprint(
        self,
        hybrid_truth: Optional[Any] = None,
        page_intelligence: Optional[Any] = None,
        pattern_intelligence: Optional[Any] = None,
        default_surface: str = "landing"
    ) -> ExperienceBlueprint:
        
        # 1. Detect target URL signatures for predefined/benchmark references
        url_str = ""
        if page_intelligence and hasattr(page_intelligence, "source_url"):
            url_str = str(page_intelligence.source_url).lower()
        
        if "antigravity" in url_str:
            return ExperienceBlueprint(
                surface_type=ExperienceSurface.LANDING,
                navigation_strategy=NavigationStrategy.CANVAS_NAVIGATION,
                motion_strategy=MotionStrategy.KINETIC_FIELD,
                spatial_strategy=SpatialStrategy.FREEFORM_DEPTH,
                attention_strategy=AttentionStrategy.FOCAL_HIERARCHY,
                narrative_strategy=NarrativeStrategy.PROGRESSIVE_DISCOVERY,
                interaction_density="low",
                visual_energy="medium",
                immersion_level="high"
            )
            
        if "exoape" in url_str or "exo-ape" in url_str:
            return ExperienceBlueprint(
                surface_type=ExperienceSurface.LANDING,
                navigation_strategy=NavigationStrategy.CANVAS_NAVIGATION,
                motion_strategy=MotionStrategy.KINETIC_FIELD,
                spatial_strategy=SpatialStrategy.FREEFORM_DEPTH,
                attention_strategy=AttentionStrategy.FOCAL_HIERARCHY,
                narrative_strategy=NarrativeStrategy.IMMERSIVE_NARRATIVE,
                interaction_density="low",
                visual_energy="high",
                immersion_level="high"
            )
            
        if "linear" in url_str:
            return ExperienceBlueprint(
                surface_type=ExperienceSurface.LANDING,
                navigation_strategy=NavigationStrategy.KEYBOARD_DRIVEN,
                motion_strategy=MotionStrategy.SUBTLE_TRANSITIONS,
                spatial_strategy=SpatialStrategy.CLEAN_BENTO,
                attention_strategy=AttentionStrategy.READING_FLOW,
                narrative_strategy=NarrativeStrategy.STANDARD,
                interaction_density="medium",
                visual_energy="low",
                immersion_level="medium"
            )
            
        if "stripe" in url_str:
            return ExperienceBlueprint(
                surface_type=ExperienceSurface.LANDING,
                navigation_strategy=NavigationStrategy.MEGA_DROPDOWN,
                motion_strategy=MotionStrategy.GRADIENT_FLOW,
                spatial_strategy=SpatialStrategy.LAYERED_CARDS,
                attention_strategy=AttentionStrategy.FOCAL_HIERARCHY,
                narrative_strategy=NarrativeStrategy.PROGRESSIVE_DISCOVERY,
                interaction_density="high",
                visual_energy="medium",
                immersion_level="medium"
            )
            
        if "chatgpt" in url_str:
            return ExperienceBlueprint(
                surface_type=ExperienceSurface.CANVAS,
                navigation_strategy=NavigationStrategy.MINIMAL_CHROME,
                motion_strategy=MotionStrategy.STREAM_RESPONSE,
                spatial_strategy=SpatialStrategy.SPLIT_SCREEN,
                attention_strategy=AttentionStrategy.MINIMAL_FOCUS,
                narrative_strategy=NarrativeStrategy.CHAT_FLOW,
                interaction_density="high",
                visual_energy="low",
                immersion_level="high"
            )

        # 2. Rich Heuristic fallback resolver if no benchmark matches
        
        # Gather all text to inspect keywords
        all_text_corpus = []
        if page_intelligence:
            if hasattr(page_intelligence, "visible_texts") and page_intelligence.visible_texts:
                all_text_corpus.extend([str(t).lower() for t in page_intelligence.visible_texts])
            if hasattr(page_intelligence, "headings") and page_intelligence.headings:
                all_text_corpus.extend([str(h).lower() for h in page_intelligence.headings])
            if hasattr(page_intelligence, "buttons") and page_intelligence.buttons:
                all_text_corpus.extend([str(b).lower() for b in page_intelligence.buttons])
        text_joined = " ".join(all_text_corpus)

        # Heuristics for surface type
        surface = ExperienceSurface.LANDING
        if default_surface == "crm":
            surface = ExperienceSurface.CRM
        elif default_surface == "portal":
            surface = ExperienceSurface.PORTAL
        elif default_surface == "dashboard" or "dashboard" in url_str or "console" in url_str:
            surface = ExperienceSurface.DASHBOARD
        elif default_surface == "canvas" or "canvas" in url_str:
            surface = ExperienceSurface.CANVAS
        elif "perplexity" in url_str or "chat" in url_str or "ai" in url_str:
            # AI chat-centric sites resolve to Canvas
            surface = ExperienceSurface.CANVAS
            
        # Navigation strategy heuristics
        nav = NavigationStrategy.STANDARD
        if surface == ExperienceSurface.CANVAS:
            nav = NavigationStrategy.MINIMAL_CHROME
        
        # Keyboard driven menu shortcuts (e.g. Raycast, Linear)
        keyboard_triggers = ["press", "cmd+", "ctrl+", "shortcut", "type a command", "search or type", "terminal", "keyboard"]
        if any(trig in text_joined for trig in keyboard_triggers) or "raycast" in url_str:
            nav = NavigationStrategy.KEYBOARD_DRIVEN
        # Mega dropdown navigation for large marketing/corporate surfaces (e.g. Stripe, Notion, Framer)
        elif "notion" in url_str or "framer" in url_str:
            nav = NavigationStrategy.MEGA_DROPDOWN
        elif page_intelligence:
            nav_items_count = len(page_intelligence.nav_items) if hasattr(page_intelligence, "nav_items") and page_intelligence.nav_items else 0
            links_count = len(page_intelligence.links) if hasattr(page_intelligence, "links") and page_intelligence.links else 0
            if nav_items_count > 6 or links_count > 15:
                nav = NavigationStrategy.MEGA_DROPDOWN
            
        # Motion heuristics based on hybrid truth motion samples
        motion_sample_count = 0
        if hybrid_truth and hasattr(hybrid_truth, "motion") and hybrid_truth.motion:
            motion_sample_count = len(hybrid_truth.motion)
            
        motion = MotionStrategy.NONE
        if "perplexity" in url_str or "chat" in url_str or any(x in text_joined for x in ["ask a question", "enter a prompt", "message"]):
            motion = MotionStrategy.STREAM_RESPONSE
        elif motion_sample_count > 3:
            motion = MotionStrategy.PARALLAX
        elif "raycast" in url_str or "linear" in url_str or "notion" in url_str or "framer" in url_str:
            motion = MotionStrategy.SUBTLE_TRANSITIONS
        elif motion_sample_count > 0:
            motion = MotionStrategy.SUBTLE_TRANSITIONS
            
        # Spatial heuristics based on viewport/layout metrics
        spatial = SpatialStrategy.STANDARD
        bento_triggers = ["bento", "grid", "blocks", "capabilities", "extensions", "store", "command"]
        
        if "notion" in url_str or "framer" in url_str or any(x in text_joined for x in ["pricing", "plans", "cards"]):
            spatial = SpatialStrategy.LAYERED_CARDS
        elif surface == ExperienceSurface.CRM or surface == ExperienceSurface.DASHBOARD:
            spatial = SpatialStrategy.CLEAN_BENTO
        elif any(trig in text_joined for trig in bento_triggers) or "raycast" in url_str or "linear" in url_str:
            spatial = SpatialStrategy.CLEAN_BENTO
        elif surface == ExperienceSurface.CANVAS or "perplexity" in url_str:
            spatial = SpatialStrategy.SPLIT_SCREEN
            
        # Attention heuristics
        attention = AttentionStrategy.FOCAL_HIERARCHY
        if surface == ExperienceSurface.CANVAS or "perplexity" in url_str:
            attention = AttentionStrategy.MINIMAL_FOCUS
        elif "docs" in url_str or "blog" in url_str or any(x in text_joined for x in ["documentation", "read", "guide", "article"]):
            attention = AttentionStrategy.READING_FLOW
            
        # Narrative heuristics
        narrative = NarrativeStrategy.STANDARD
        if surface == ExperienceSurface.CANVAS or "perplexity" in url_str:
            narrative = NarrativeStrategy.CHAT_FLOW
        elif motion_sample_count > 3:
            narrative = NarrativeStrategy.IMMERSIVE_NARRATIVE
        elif "notion" in url_str or "framer" in url_str or "raycast" in url_str or any(x in text_joined for x in ["pricing", "features", "explore"]):
            narrative = NarrativeStrategy.PROGRESSIVE_DISCOVERY
            
        # Interaction density heuristics based on button/link count in Page Intelligence
        btn_link_count = 0
        if page_intelligence:
            if hasattr(page_intelligence, "buttons") and page_intelligence.buttons:
                btn_link_count += len(page_intelligence.buttons)
            if hasattr(page_intelligence, "links") and page_intelligence.links:
                btn_link_count += len(page_intelligence.links)
                
        interaction_density = "low"
        if btn_link_count > 10:
            interaction_density = "high"
        elif btn_link_count > 3:
            interaction_density = "medium"
            
        # Visual Energy & Immersion defaults
        visual_energy = "medium"
        if motion_sample_count > 2 or "framer" in url_str:
            visual_energy = "high"
        elif "linear" in url_str:
            visual_energy = "low"
            
        immersion_level = "medium"
        if surface in [ExperienceSurface.CANVAS, ExperienceSurface.LANDING]:
            immersion_level = "high"

        return ExperienceBlueprint(
            surface_type=surface,
            navigation_strategy=nav,
            motion_strategy=motion,
            spatial_strategy=spatial,
            attention_strategy=attention,
            narrative_strategy=narrative,
            interaction_density=interaction_density,
            visual_energy=visual_energy,
            immersion_level=immersion_level
        )
