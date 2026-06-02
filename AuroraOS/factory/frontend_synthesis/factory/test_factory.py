from factory_contracts import UINode, ComponentTree
from tsx_compiler import compile_tsx, generate_tailwind_config

def test_tsx_compiler_basic_tag():
    node = UINode(node_id="1", component_type="div", tailwind_classes=["flex"])
    tree = ComponentTree(spec_id="TEST", root_node=node)
    
    output = compile_tsx(tree)
    assert 'className="flex"' in output
    assert "<div" in output
    # Como não tem filhos nem texto, deve auto-fechar no padrão XML/JSX
    assert "/>" in output 

def test_tsx_compiler_auto_imports():
    node = UINode(node_id="1", component_type="AuroraButton", props={"variant": "ghost"})
    tree = ComponentTree(spec_id="TEST", root_node=node)
    
    output = compile_tsx(tree)
    assert "import { AuroraButton } from '@/components/core';" in output
    assert 'variant="ghost"' in output

def test_tsx_compiler_nested_elements():
    child1 = UINode(node_id="child1", component_type="span", text_content="Hello")
    child2 = UINode(node_id="child2", component_type="AuroraButton", text_content="Click me")
    parent = UINode(node_id="parent", component_type="div", children=[child1, child2])
    tree = ComponentTree(spec_id="TEST-NESTED", root_node=parent)
    
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
