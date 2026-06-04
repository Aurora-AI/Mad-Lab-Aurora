import sys
import os
import pytest
from pydantic import HttpUrl

# Ensure correct path discovery
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.extend([
    os.path.abspath(os.path.join(current_dir, "../frontend_synthesis/contracts")),
    os.path.abspath(os.path.join(current_dir, "../contracts")),
    os.path.abspath(current_dir)
])

from blueprint_resolver import BlueprintResolver
from models import PageIntelligenceArtifact
from experience_architecture_contracts import (
    ExperienceBlueprint,
    ExperienceSurface,
    NavigationStrategy,
    MotionStrategy,
    SpatialStrategy,
    AttentionStrategy,
    NarrativeStrategy
)
from datetime import datetime

def create_mock_artifact(url: str) -> PageIntelligenceArtifact:
    return PageIntelligenceArtifact(
        source_url=HttpUrl(url),
        extracted_at=datetime.now(),
        colors=[],
        typography=[],
        spatial_system=[],
        motion=[],
        a11y_tree=[],
        dom_hierarchy_snapshot="MOCK-HASH"
    )

def test_resolve_antigravity():
    resolver = BlueprintResolver()
    artifact = create_mock_artifact("https://antigravity.google/")
    blueprint = resolver.resolve_blueprint(page_intelligence=artifact)
    
    assert blueprint.surface_type == ExperienceSurface.LANDING
    assert blueprint.navigation_strategy == NavigationStrategy.CANVAS_NAVIGATION
    assert blueprint.motion_strategy == MotionStrategy.KINETIC_FIELD
    assert blueprint.spatial_strategy == SpatialStrategy.FREEFORM_DEPTH

def test_resolve_exo_ape():
    resolver = BlueprintResolver()
    artifact = create_mock_artifact("https://exoape.com/")
    blueprint = resolver.resolve_blueprint(page_intelligence=artifact)
    
    assert blueprint.surface_type == ExperienceSurface.LANDING
    assert blueprint.navigation_strategy == NavigationStrategy.SMOOTH_SCROLL
    assert blueprint.motion_strategy == MotionStrategy.PARALLAX
    assert blueprint.spatial_strategy == SpatialStrategy.STANDARD

def test_resolve_linear():
    resolver = BlueprintResolver()
    artifact = create_mock_artifact("https://linear.app/")
    blueprint = resolver.resolve_blueprint(page_intelligence=artifact)
    
    assert blueprint.surface_type == ExperienceSurface.LANDING
    assert blueprint.navigation_strategy == NavigationStrategy.KEYBOARD_DRIVEN
    assert blueprint.motion_strategy == MotionStrategy.SUBTLE_TRANSITIONS
    assert blueprint.spatial_strategy == SpatialStrategy.CLEAN_BENTO

def test_resolve_stripe():
    resolver = BlueprintResolver()
    artifact = create_mock_artifact("https://stripe.com/")
    blueprint = resolver.resolve_blueprint(page_intelligence=artifact)
    
    assert blueprint.surface_type == ExperienceSurface.LANDING
    assert blueprint.navigation_strategy == NavigationStrategy.MEGA_DROPDOWN
    assert blueprint.motion_strategy == MotionStrategy.GRADIENT_FLOW
    assert blueprint.spatial_strategy == SpatialStrategy.LAYERED_CARDS

def test_resolve_chatgpt():
    resolver = BlueprintResolver()
    artifact = create_mock_artifact("https://chatgpt.com/")
    blueprint = resolver.resolve_blueprint(page_intelligence=artifact)
    
    assert blueprint.surface_type == ExperienceSurface.CANVAS
    assert blueprint.navigation_strategy == NavigationStrategy.MINIMAL_CHROME
    assert blueprint.motion_strategy == MotionStrategy.STREAM_RESPONSE
    assert blueprint.spatial_strategy == SpatialStrategy.SPLIT_SCREEN

def test_blueprints_are_distinct():
    resolver = BlueprintResolver()
    urls = [
        "https://antigravity.google/",
        "https://exoape.com/",
        "https://linear.app/",
        "https://stripe.com/",
        "https://chatgpt.com/"
    ]
    blueprints = [
        resolver.resolve_blueprint(page_intelligence=create_mock_artifact(url))
        for url in urls
    ]
    
    # Assert they are distinct
    serialized_bps = [bp.model_dump_json() for bp in blueprints]
    assert len(set(serialized_bps)) == 5

def test_resolve_perplexity():
    resolver = BlueprintResolver()
    # Test text clues for Perplexity
    artifact = create_mock_artifact("https://perplexity.ai/")
    artifact.visible_texts = ["Ask a question...", "Perplexity PRO", "Enter a query"]
    blueprint = resolver.resolve_blueprint(page_intelligence=artifact)
    
    assert blueprint.surface_type == ExperienceSurface.CANVAS
    assert blueprint.navigation_strategy == NavigationStrategy.MINIMAL_CHROME
    assert blueprint.motion_strategy == MotionStrategy.STREAM_RESPONSE
    assert blueprint.spatial_strategy == SpatialStrategy.SPLIT_SCREEN
    assert blueprint.attention_strategy == AttentionStrategy.MINIMAL_FOCUS
    assert blueprint.narrative_strategy == NarrativeStrategy.CHAT_FLOW

def test_resolve_raycast():
    resolver = BlueprintResolver()
    # Test text clues for Raycast
    artifact = create_mock_artifact("https://raycast.com/")
    artifact.visible_texts = ["Raycast Store", "Extensions", "Press Cmd+K to launch", "Shortcuts and Commands"]
    blueprint = resolver.resolve_blueprint(page_intelligence=artifact)
    
    assert blueprint.surface_type == ExperienceSurface.LANDING
    assert blueprint.navigation_strategy == NavigationStrategy.KEYBOARD_DRIVEN
    assert blueprint.motion_strategy == MotionStrategy.SUBTLE_TRANSITIONS
    assert blueprint.spatial_strategy == SpatialStrategy.CLEAN_BENTO
    assert blueprint.narrative_strategy == NarrativeStrategy.PROGRESSIVE_DISCOVERY

def test_resolve_notion_framer():
    resolver = BlueprintResolver()
    artifact_notion = create_mock_artifact("https://notion.so/")
    artifact_notion.visible_texts = ["Pricing plans", "Features and templates", "Read our guide"]
    blueprint_notion = resolver.resolve_blueprint(page_intelligence=artifact_notion)
    
    assert blueprint_notion.navigation_strategy == NavigationStrategy.MEGA_DROPDOWN
    assert blueprint_notion.spatial_strategy == SpatialStrategy.LAYERED_CARDS
    assert blueprint_notion.narrative_strategy == NarrativeStrategy.PROGRESSIVE_DISCOVERY

def test_generalization_comparison():
    resolver = BlueprintResolver()
    
    # Antigravity (Benchmark)
    bp_antigravity = resolver.resolve_blueprint(page_intelligence=create_mock_artifact("https://antigravity.google/"))
    
    # Perplexity (Generalization)
    art_perplexity = create_mock_artifact("https://perplexity.ai/")
    art_perplexity.visible_texts = ["Ask a question", "Prompt"]
    bp_perplexity = resolver.resolve_blueprint(page_intelligence=art_perplexity)
    
    # Raycast (Generalization)
    art_raycast = create_mock_artifact("https://raycast.com/")
    art_raycast.visible_texts = ["Press Cmd+K", "extensions", "store"]
    bp_raycast = resolver.resolve_blueprint(page_intelligence=art_raycast)
    
    # Assert they are substantially different in key strategies
    assert bp_antigravity.spatial_strategy != bp_perplexity.spatial_strategy
    assert bp_antigravity.spatial_strategy != bp_raycast.spatial_strategy
    assert bp_perplexity.spatial_strategy != bp_raycast.spatial_strategy
    
    assert bp_antigravity.navigation_strategy != bp_perplexity.navigation_strategy
    assert bp_antigravity.navigation_strategy != bp_raycast.navigation_strategy
    assert bp_perplexity.navigation_strategy != bp_raycast.navigation_strategy
    
    assert bp_antigravity.motion_strategy != bp_perplexity.motion_strategy
    assert bp_antigravity.motion_strategy != bp_raycast.motion_strategy
    assert bp_perplexity.motion_strategy != bp_raycast.motion_strategy

