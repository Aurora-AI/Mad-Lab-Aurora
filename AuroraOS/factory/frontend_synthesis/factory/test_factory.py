import pytest
from factory_contracts import UINode, ComponentTree, LayoutProfileSelection, ComponentMappingFinding
from tsx_compiler import compile_tsx, generate_tailwind_config
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
    
    tree = generate_ui_tree(spec)
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
        generate_ui_tree(spec)
        
    assert "Component Transpilation Paused" in str(exc.value)
    findings = exc.value.findings
    assert any(f.code == "CONTAINER_EMPTY" and f.severity == "P1" for f in findings)
