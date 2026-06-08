"""
Tests for Mad Lab Theme contracts.

OS-019-M0: Mad Lab Theme Canonization & Z-Axis Capability Alignment

Verifies:
- MadLabThemeContract instantiates correctly with all required fields
- MotionBudget enforces desktop/mobile fps and layer limits
- ReducedMotionFallback values are correctly defined
- ZAxisScrollModel enum covers required scroll strategies
- Default values reflect the canonical Mad Lab Theme spec
"""

import sys
import os
import pytest
from pydantic import ValidationError

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from mad_lab_theme_contracts import (
    MadLabThemeContract,
    MadLabThemeIntent,
    ZAxisScrollModel,
    DepthLayerSpec,
    NullSpaceProfile,
    TunnelProgressionStrategy,
    MotionBudget,
    ReducedMotionFallback,
)


def test_mad_lab_theme_contract_defaults():
    """MadLabThemeContract instantiates with canonical Mad Lab defaults."""
    contract = MadLabThemeContract()
    assert contract.intent == MadLabThemeIntent.TUNNEL_PROGRESSION
    assert contract.scroll_model == ZAxisScrollModel.VERTICAL_INPUT_TO_Z
    assert contract.progression == TunnelProgressionStrategy.FORWARD_ONLY
    assert contract.fallback == ReducedMotionFallback.STATIC_DEPTH_SECTIONS
    assert contract.budget.desktop_fps == 60
    assert contract.budget.mobile_fps == 30
    assert contract.budget.max_layers == 5
    assert contract.null_space.null_space_ratio == 0.5
    assert contract.null_space.min_padding_rem == 6.0


def test_mad_lab_theme_null_space_ratio_minimum():
    """NullSpaceProfile accepts the canonical 0.55 ratio for Mad Lab Theme."""
    profile = NullSpaceProfile(null_space_ratio=0.55, min_padding_rem=8.0)
    assert profile.null_space_ratio == 0.55
    assert profile.min_padding_rem == 8.0


def test_depth_layer_spec_valid():
    """DepthLayerSpec accepts valid Z positions and scale factors."""
    layer = DepthLayerSpec(
        layer_id="layer-hero",
        z_position=-1000.0,
        scale_factor=0.7,
        opacity_limit=0.95
    )
    assert layer.layer_id == "layer-hero"
    assert layer.z_position == -1000.0
    assert layer.scale_factor == 0.7
    assert layer.opacity_limit == 0.95


def test_depth_layer_spec_default_opacity():
    """DepthLayerSpec defaults opacity_limit to 1.0."""
    layer = DepthLayerSpec(
        layer_id="layer-bg",
        z_position=-3000.0,
        scale_factor=0.4
    )
    assert layer.opacity_limit == 1.0


def test_motion_budget_custom_values():
    """MotionBudget accepts custom fps and layer limits."""
    budget = MotionBudget(desktop_fps=60, mobile_fps=30, max_layers=12)
    assert budget.desktop_fps == 60
    assert budget.mobile_fps == 30
    assert budget.max_layers == 12


def test_reduced_motion_fallback_enum_values():
    """ReducedMotionFallback has all required fallback strategies."""
    assert ReducedMotionFallback.STATIC_DEPTH_SECTIONS == "static_depth_sections"
    assert ReducedMotionFallback.FADE_SECTIONS == "fade_sections"
    assert ReducedMotionFallback.STATIC_SECTIONS == "static_sections"


def test_z_axis_scroll_model_enum_values():
    """ZAxisScrollModel covers both scroll axes."""
    assert ZAxisScrollModel.VERTICAL_INPUT_TO_Z == "vertical_input_to_z"
    assert ZAxisScrollModel.HORIZONTAL_INPUT_TO_Z == "horizontal_input_to_z"


def test_tunnel_progression_bidirectional():
    """TunnelProgressionStrategy supports bidirectional traversal."""
    contract = MadLabThemeContract(
        progression=TunnelProgressionStrategy.BIDIRECTIONAL
    )
    assert contract.progression == TunnelProgressionStrategy.BIDIRECTIONAL


def test_mad_lab_theme_contract_with_layers():
    """MadLabThemeContract accepts a list of depth layer specs."""
    layers = [
        DepthLayerSpec(layer_id="bg", z_position=-3000.0, scale_factor=0.4),
        DepthLayerSpec(layer_id="mid", z_position=-1500.0, scale_factor=0.7),
        DepthLayerSpec(layer_id="fore", z_position=0.0, scale_factor=1.0),
    ]
    contract = MadLabThemeContract(layers=layers)
    assert len(contract.layers) == 3
    assert contract.layers[0].layer_id == "bg"
    assert contract.layers[2].z_position == 0.0


def test_mad_lab_theme_intent_enum_values():
    """MadLabThemeIntent covers all canonical intent strategies."""
    assert MadLabThemeIntent.TUNNEL_PROGRESSION == "tunnel_progression"
    assert MadLabThemeIntent.DEPTH_TRAVERSE == "depth_traverse"
    assert MadLabThemeIntent.FLUID_EDITORIAL == "fluid_editorial"


def test_mad_lab_theme_contract_serializable():
    """MadLabThemeContract serializes to JSON without error."""
    contract = MadLabThemeContract(
        layers=[
            DepthLayerSpec(layer_id="layer-0", z_position=-1000.0, scale_factor=0.8)
        ]
    )
    json_output = contract.model_dump_json()
    assert "tunnel_progression" in json_output
    assert "vertical_input_to_z" in json_output
    assert "layer-0" in json_output
