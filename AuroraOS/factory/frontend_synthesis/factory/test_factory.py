import pytest
from factory_contracts import UINode, ComponentTree, LayoutProfileSelection, ComponentMappingFinding
from tsx_compiler import compile_tsx, compile_tsx_nodes, generate_tailwind_config
from factory_agent import generate_ui_tree
from alvaro_contracts import FrontendCodeSpec, TailwindThemeSpec, ComponentRequirement, ScaffoldingResolution
from sandbox_contracts import PipelinePausedException, DiagnosticFinding

def _get_mock_layout():
    return LayoutProfileSelection(
        profile="editorial_field",
        reason="Mock layout for tests",
        confidence=1.0,
        source_signals=["mock_signal"]
    )

def test_tsx_compiler_basic_tag():
    node = UINode(
        node_id="1", 
        component_name="div", 
        semantic_role="container",
        props={"className": "flex"}
    )
    tree = ComponentTree(spec_id="TEST", root_node=node, layout_selection=_get_mock_layout())
    
    output = compile_tsx(tree)
    assert 'className="flex"' in output
    assert "<div" in output
    # React JSX supports and prefers self-closing for empty components
    assert "/>" in output 

def test_tsx_compiler_auto_imports():
    node = UINode(
        node_id="1", 
        component_name="AuroraButton", 
        semantic_role="button",
        props={"variant": "ghost"}
    )
    tree = ComponentTree(spec_id="TEST", root_node=node, layout_selection=_get_mock_layout())
    
    output = compile_tsx(tree)
    assert "import { AuroraButton } from '@/components/core';" in output
    assert 'variant="ghost"' in output

def test_tsx_compiler_nested_elements():
    child1 = UINode(node_id="child1", component_name="span", semantic_role="text", text_content="Hello")
    child2 = UINode(node_id="child2", component_name="AuroraButton", semantic_role="button", text_content="Click me")
    parent = UINode(node_id="parent", component_name="div", semantic_role="container", children=[child1, child2])
    tree = ComponentTree(spec_id="TEST-NESTED", root_node=parent, layout_selection=_get_mock_layout())
    
    output = compile_tsx(tree)
    assert "<div>" in output
    assert "<span>" in output
    assert "Hello" in output
    assert "import { AuroraButton } from '@/components/core';" in output
    assert "<AuroraButton>" in output
    assert "Click me" in output
    assert "</div>" in output

def test_generate_tailwind_config_output():
    colors = {"surface": "#121212", "primary": "#ffffff"}
    fonts = {"sans": ["Inter", "sans-serif"]}
    
    output = generate_tailwind_config(colors, fonts)
    assert '"surface": "#121212"' in output
    assert '"primary": "#ffffff"' in output
    assert '"sans"' in output
    assert "module.exports" in output

def test_generate_ui_tree_hierarchical_success():
    spec = FrontendCodeSpec(
        spec_id="TEST-SPEC-NESTED",
        derived_from_draft_id="DRAFT-123",
        theme_config=TailwindThemeSpec(
            colors={"base-surface": "#FFFFFF", "text-primary": "#000000", "action-primary": "#4A3FF4"},
            fontFamily={"sans": ["Inter", "sans-serif"]},
            fontSize={"body": "1rem"}
        ),
        component_registry=[
            ComponentRequirement(component_name="AuroraContainer", required_variants=["default"], is_core_library=True),
            ComponentRequirement(component_name="AuroraButton", required_variants=["default"], is_core_library=True)
        ],
        component_alerts=[],
        debt_tracking=ScaffoldingResolution(target_os="OS-003", pending_injectors=[], resolution_status="RESOLVED"),
        ready_for_factory=True
    )
    
    tree = generate_ui_tree(spec, compatibility_mode=True)
    # Check nesting: AuroraButton is a child of AuroraContainer
    container_node = None
    for child in tree.root_node.children[-1].children:
        if child.component_name == "AuroraContainer":
            container_node = child
            break
            
    assert container_node is not None
    assert len(container_node.children) == 1
    assert container_node.children[0].component_name == "AuroraButton"
    
    # Check that CONTAINER_EMPTY finding is not there
    assert not any(f.code == "CONTAINER_EMPTY" for f in tree.component_findings)

def test_generate_ui_tree_empty_container_fails():
    spec = FrontendCodeSpec(
        spec_id="TEST-SPEC-EMPTY",
        derived_from_draft_id="DRAFT-123",
        theme_config=TailwindThemeSpec(
            colors={"base-surface": "#FFFFFF", "text-primary": "#000000", "action-primary": "#4A3FF4"},
            fontFamily={"sans": ["Inter", "sans-serif"]},
            fontSize={"body": "1rem"}
        ),
        component_registry=[
            ComponentRequirement(component_name="AuroraContainer", required_variants=["default"], is_core_library=True)
        ],
        component_alerts=[],
        debt_tracking=ScaffoldingResolution(target_os="OS-003", pending_injectors=[], resolution_status="RESOLVED"),
        ready_for_factory=True
    )
    
    with pytest.raises(PipelinePausedException) as exc:
        generate_ui_tree(spec, compatibility_mode=True)
        
    assert "Component Transpilation Paused" in str(exc.value)
    findings = exc.value.findings
    assert any(f.code == "CONTAINER_EMPTY" and f.severity == "P1" for f in findings)


# ─────────────────────────────────────────────────────────────────────────────
# OS-019-M0: FX Component Compiler Tests
# Verifies tsx_compiler conditionally imports @/components/fx only when
# ZAxisScrollContainer or LayerPortal appear in the UI tree.
# An orphan import (imported but unused) is a P1 violation.
# ─────────────────────────────────────────────────────────────────────────────

def _get_fx_layout():
    return LayoutProfileSelection(
        profile="z_axis_depth",
        reason="Mad Lab Theme Z-axis layout",
        confidence=1.0,
        source_signals=["stories_plan"]
    )


def test_tsx_compiler_imports_z_axis_scroll_container():
    """ZAxisScrollContainer triggers conditional import from @/components/fx."""
    node = UINode(
        node_id="tunnel-root",
        component_name="ZAxisScrollContainer",
        semantic_role="container",
        props={"enabled": True, "quality": "high", "depth": 3000}
    )
    tree = ComponentTree(spec_id="TEST-FX-001", root_node=node, layout_selection=_get_fx_layout())
    output = compile_tsx(tree)

    assert "import { ZAxisScrollContainer } from '@/components/fx';" in output
    assert "<ZAxisScrollContainer" in output
    # Must NOT import from @/components/core — wrong package
    assert "import { ZAxisScrollContainer } from '@/components/core';" not in output


def test_tsx_compiler_imports_layer_portal():
    """LayerPortal triggers conditional import from @/components/fx."""
    node = UINode(
        node_id="depth-layer-0",
        component_name="LayerPortal",
        semantic_role="presentation",
        props={"zPosition": -1000, "scaleFactor": 0.7}
    )
    tree = ComponentTree(spec_id="TEST-FX-002", root_node=node, layout_selection=_get_fx_layout())
    output = compile_tsx(tree)

    assert "import { LayerPortal } from '@/components/fx';" in output
    assert "<LayerPortal" in output
    assert "import { LayerPortal } from '@/components/core';" not in output


def test_tsx_compiler_no_orphan_fx_import_when_no_fx_component():
    """When no FX components are in the tree, @/components/fx is NOT imported."""
    node = UINode(
        node_id="hero",
        component_name="AuroraHeroStatement",
        semantic_role="hero",
        props={"className": "text-center"}
    )
    tree = ComponentTree(spec_id="TEST-FX-003", root_node=node, layout_selection=_get_fx_layout())
    output = compile_tsx(tree)

    assert "@/components/fx" not in output
    assert "import { AuroraHeroStatement } from '@/components/core';" in output


def test_tsx_compiler_both_fx_components_in_same_tree():
    """Both ZAxisScrollContainer and LayerPortal can coexist in one tree with separate imports."""
    layer_node = UINode(
        node_id="layer-0",
        component_name="LayerPortal",
        semantic_role="presentation",
        props={"zPosition": -2000, "scaleFactor": 0.5}
    )
    root_node = UINode(
        node_id="tunnel",
        component_name="ZAxisScrollContainer",
        semantic_role="container",
        props={"enabled": True, "depth": 4000},
        children=[layer_node]
    )
    tree = ComponentTree(spec_id="TEST-FX-004", root_node=root_node, layout_selection=_get_fx_layout())
    output = compile_tsx(tree)

    assert "import { ZAxisScrollContainer } from '@/components/fx';" in output
    assert "import { LayerPortal } from '@/components/fx';" in output
    assert "<ZAxisScrollContainer" in output
    assert "<LayerPortal" in output


# ─────────────────────────────────────────────────────────────────────────────
# OS-019 M2: useReducedMotion + RUNTIME_EXPRESSION_PREFIX tests
# Verifies tsx_compiler emits 'use client', useReducedMotion hook, and
# systemReducedMotion variable when FX components are present.
# Verifies RUNTIME_EXPRESSION_PREFIX sentinel emits JSX expression (not string literal).
# ─────────────────────────────────────────────────────────────────────────────

def test_tsx_compiler_fx_emits_use_client_directive():
    """FX component in tree causes 'use client'; directive at top of output."""
    node = UINode(
        node_id="tunnel",
        component_name="ZAxisScrollContainer",
        semantic_role="container",
        props={"enabled": True, "depth": 3000}
    )
    tree = ComponentTree(spec_id="TEST-FX-UC", root_node=node, layout_selection=_get_fx_layout())
    output = compile_tsx(tree)
    assert output.startswith("'use client';"), "Generated file must start with 'use client';"


def test_tsx_compiler_fx_emits_use_reduced_motion_hook():
    """FX component in tree causes useReducedMotion hook to be emitted."""
    node = UINode(
        node_id="tunnel",
        component_name="ZAxisScrollContainer",
        semantic_role="container",
        props={"enabled": True, "depth": 3000}
    )
    tree = ComponentTree(spec_id="TEST-FX-RMH", root_node=node, layout_selection=_get_fx_layout())
    output = compile_tsx(tree)
    assert "function useReducedMotion" in output
    assert "prefers-reduced-motion" in output
    assert "systemReducedMotion = useReducedMotion()" in output


def test_tsx_compiler_fx_emits_react_import():
    """FX component in tree causes React import to be emitted."""
    node = UINode(
        node_id="layer",
        component_name="LayerPortal",
        semantic_role="presentation",
        props={"zPosition": -500, "scaleFactor": 0.8}
    )
    tree = ComponentTree(spec_id="TEST-FX-REACT", root_node=node, layout_selection=_get_fx_layout())
    output = compile_tsx(tree)
    assert "import React from 'react';" in output


def test_tsx_compiler_no_use_client_without_fx():
    """Non-FX tree must NOT emit 'use client'; — only FX triggers it."""
    node = UINode(
        node_id="hero",
        component_name="AuroraHeroStatement",
        semantic_role="hero",
        props={"className": "text-center"}
    )
    tree = ComponentTree(spec_id="TEST-NOFX-UC", root_node=node, layout_selection=_get_fx_layout())
    output = compile_tsx(tree)
    assert "'use client';" not in output
    assert "useReducedMotion" not in output


def test_tsx_compiler_runtime_expression_sentinel_emits_jsx_expression():
    """RUNTIME_EXPRESSION_PREFIX sentinel emits {expr} instead of string literal."""
    from tsx_compiler import RUNTIME_EXPRESSION_PREFIX
    node = UINode(
        node_id="tunnel",
        component_name="ZAxisScrollContainer",
        semantic_role="container",
        props={
            "enabled": True,
            "depth": 3000,
            "reducedMotion": f"{RUNTIME_EXPRESSION_PREFIX}systemReducedMotion",
        }
    )
    tree = ComponentTree(spec_id="TEST-FX-SENTINEL", root_node=node, layout_selection=_get_fx_layout())
    output = compile_tsx(tree)
    # Must emit JSX expression, not string literal
    assert "reducedMotion={systemReducedMotion}" in output
    assert 'reducedMotion="__RUNTIME_EXPR__' not in output


def test_tsx_compiler_runtime_expression_does_not_affect_non_sentinel_props():
    """Regular string props must NOT be emitted as JSX expressions."""
    node = UINode(
        node_id="layer",
        component_name="LayerPortal",
        semantic_role="presentation",
        props={"quality": "high", "scaleFactor": 0.9}
    )
    tree = ComponentTree(spec_id="TEST-FX-REGULAR", root_node=node, layout_selection=_get_fx_layout())
    output = compile_tsx(tree)
    assert 'quality="high"' in output
