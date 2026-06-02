import pytest
from pydantic import ValidationError
import sys
import os

# Ajuste de path para importações
sys.path.extend([
    os.path.abspath(os.path.dirname(__file__)),
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../contracts'))
])

from motion_primitive_injector import MotionConfig, MotionPrimitiveInjector
from factory_contracts import UINode, ComponentTree

def test_motion_config_validation():
    # Valid config
    config = MotionConfig(
        primitive="fade_in",
        durationMs=400,
        easing="ease-out",
        reducedMotionFallback="opacity"
    )
    assert config.primitive == "fade_in"
    assert config.duration_ms == 400
    assert config.easing == "ease-out"
    assert config.reduced_motion_fallback == "opacity"

    # Invalid config - invalid primitive
    with pytest.raises(ValidationError):
        MotionConfig(primitive="gsap_timeline")

    # Invalid config - invalid easing
    with pytest.raises(ValidationError):
        MotionConfig(primitive="fade_in", easing="linear")

def test_motion_injection_in_node():
    injector = MotionPrimitiveInjector()
    node = UINode(
        node_id="btn-1",
        component_type="button",
        tailwind_classes=["bg-blue-500"]
    )
    config = MotionConfig(
        primitive="press_scale",
        durationMs=150,
        reducedMotionFallback="static"
    )
    
    updated_node = injector.inject_node_motion(node, config)
    assert "transition-transform" in updated_node.tailwind_classes
    assert "active:motion-safe:scale-95" in updated_node.tailwind_classes
    assert "motion-safe:duration-150" in updated_node.tailwind_classes
    assert updated_node.props["motionConfig"]["primitive"] == "press_scale"

def test_reduced_motion_fallbacks():
    injector = MotionPrimitiveInjector()
    node = UINode(
        node_id="btn-1",
        component_type="button",
        tailwind_classes=[]
    )
    config = MotionConfig(
        primitive="fade_in",
        durationMs=300,
        reducedMotionFallback="opacity"
    )
    
    updated_node = injector.inject_node_motion(node, config)
    assert "motion-reduce:transition-opacity" in updated_node.tailwind_classes
    assert "motion-reduce:duration-100" in updated_node.tailwind_classes

    node2 = UINode(
        node_id="btn-2",
        component_type="button",
        tailwind_classes=[]
    )
    config2 = MotionConfig(
        primitive="subtle_lift",
        reducedMotionFallback="none"
    )
    updated_node2 = injector.inject_node_motion(node2, config2)
    assert "motion-reduce:transition-none" in updated_node2.tailwind_classes
