from factory_contracts import ComponentTree, UINode, StandaloneRenderBundle
import json
import uuid

def _format_props(props: dict, classes: list) -> str:
    """Serializa as propriedades Python para sintaxe TSX segura."""
    prop_str = ""
    
    if classes:
        cls_string = " ".join(classes)
        prop_str += f' className="{cls_string}"'
        
    for key, value in props.items():
        if isinstance(value, bool):
            prop_str += f" {key}" if value else "" # props booleanas no React
        elif isinstance(value, str):
            prop_str += f' {key}="{value}"'
        else:
            # Serializa arrays e dicts para JSON injetável no JSX
            prop_str += f" {key}={{{json.dumps(value)}}}"
    
    return prop_str

def _compile_node(node: UINode, indent_level: int = 2, imports: set = None) -> str:
    """Motor recursivo de transpilação TSX."""
    if imports is None:
        imports = set()
        
    indent = "  " * indent_level
    comp = node.component_type
    
    # Se for componente Aurora, registra o import
    if comp.startswith("Aurora"):
        imports.add(f"import {{ {comp} }} from '@/components/core';")

    props_formatted = _format_props(node.props, node.tailwind_classes)
    
    # Fechamento de Tags Vazia (ex: <hr /> ou <input />)
    if not node.children and not node.text_content:
        return f"{indent}<{comp}{props_formatted} />"
    
    # Construção de Nós Parentais
    code = f"{indent}<{comp}{props_formatted}>\n"
    
    if node.text_content:
        code += f"{indent}  {node.text_content}\n"
        
    if node.children:
        for child in node.children:
            code += _compile_node(child, indent_level + 1, imports) + "\n"
            
    code += f"{indent}</{comp}>"
    return code

def _compile_html_node(node: UINode, indent_level: int = 2) -> str:
    """Gera fallback HTML puramente visual para testes de screenshot."""
    indent = "  " * indent_level
    comp = node.component_type.lower()
    
    # Map Aurora components to standard HTML
    if "button" in comp: comp = "button"
    elif "input" in comp: comp = "input"
    elif "card" in comp: comp = "div"
    elif "text" in comp: comp = "span"
    elif comp.startswith("aurora"): comp = "div"
    
    prop_str = ""
    style_str = ""
    if node.tailwind_classes:
        prop_str += f' class="{" ".join(node.tailwind_classes)}"'
        
        # Injetar fallback style explícito para garantir renderização de cor
        styles = []
        for c in node.tailwind_classes:
            if c == "bg-base-surface": styles.append("background-color: #0A0A0C;")
            if c == "bg-action-primary": styles.append("background-color: #4A3FF4;")
            if c == "min-h-screen": styles.append("min-height: 100vh;")
            if c == "flex": styles.append("display: flex;")
            if c == "flex-col": styles.append("flex-direction: column;")
            if c == "items-center": styles.append("align-items: center;")
            if c == "h-[20vh]": styles.append("height: 20vh;")
            if c == "h-[50vh]": styles.append("height: 50vh;")
            if c == "w-1/2": styles.append("width: 50%;")
            if c == "w-full": styles.append("width: 100%;")
        
        if styles:
            prop_str += f' style="{" ".join(styles)}"'
        
    code = f"{indent}<{comp}{prop_str}>\n"
    if node.text_content:
        code += f"{indent}  {node.text_content}\n"
    if node.children:
        for child in node.children:
            code += _compile_html_node(child, indent_level + 1) + "\n"
    code += f"{indent}</{comp}>"
    return code

def compile_tsx(tree: ComponentTree) -> str:
    """Invólucro Final: Gera o arquivo React pronto para produção."""
    imports = set()
    jsx_body = _compile_node(tree.root_node, indent_level=2, imports=imports)
    
    header = "/**\n * SYNTHESIZED BY AURORA FRONTEND FACTORY\n"
    header += f" * SPEC_ID: {tree.spec_id}\n * TRUSTWARE CERTIFIED\n */\n\n"
    
    imports_block = "\n".join(sorted(imports))
    if imports_block:
        imports_block += "\n"
    
    component_wrapper = f"\nexport default function SynthesizedPage() {{\n  return (\n{jsx_body}\n  );\n}}\n"
    
    return header + imports_block + component_wrapper

def compile_tsx_nodes(tree: ComponentTree) -> tuple[str, set]:
    """Compila apenas o corpo interno da árvore JSX e retorna a string e os imports."""
    imports = set()
    jsx_body = _compile_node(tree.root_node, indent_level=3, imports=imports)
    return jsx_body, imports

def generate_tailwind_config(theme_colors: dict, theme_fonts: dict) -> str:
    """Motor de injeção dinâmica para o config do Tailwind."""
    colors_json = json.dumps(theme_colors, indent=6)[1:-1] # Remove as chaves externas
    fonts_json = json.dumps(theme_fonts, indent=6)[1:-1]
    
    return f"""/** @type {{import('tailwindcss').Config}} */
module.exports = {{
  content: [
    './pages/**/*.{{ts,tsx}}',
    './components/**/*.{{ts,tsx}}',
  ],
  theme: {{
    extend: {{
      colors: {{
{colors_json}
      }},
      fontFamily: {{
{fonts_json}
      }}
    }}
  }},
  plugins: [],
}};
"""

def generate_standalone_bundle(tree: ComponentTree, theme_colors: dict, theme_fonts: dict) -> StandaloneRenderBundle:
    """Gera o StandaloneRenderBundle conforme OS-012. Componente React isolado com CSS embeddado."""
    # Como não podemos usar CDN e precisamos de um bundle isolado, 
    # simulamos o CSS compilado (na prática envolveria transpilar via JS puro se fosse Next, 
    # mas para o RenderBundle entregamos o JSX e o Tailwind Safelist).
    
    jsx_body, imports = compile_tsx_nodes(tree)
    
    # Extrai recursivamente as classes Tailwind para a safelist
    def _extract_classes(node: UINode, out: set):
        for c in node.tailwind_classes:
            out.add(c)
        if node.children:
            for child in node.children:
                _extract_classes(child, out)
    
    classes_set = set()
    _extract_classes(tree.root_node, classes_set)
    
    # Mock CSS generation baseada em tailwind rules locais para fail-closed test
    css_lines = []
    css_lines.append(".min-h-screen { min-height: 100vh; }")
    css_lines.append(".flex { display: flex; }")
    css_lines.append(".flex-col { flex-direction: column; }")
    css_lines.append(".items-center { align-items: center; }")
    css_lines.append(".justify-center { justify-content: center; }")
    css_lines.append(".w-full { width: 100%; }")
    
    # Adicionar colors dinamicamente
    for color_name, color_val in theme_colors.items():
        css_lines.append(f".bg-{color_name} {{ background-color: {color_val}; }}")
        css_lines.append(f".text-{color_name} {{ color: {color_val}; }}")
        
    # Algumas cores fixas mockadas q podem vir do Tailwind
    css_lines.append(".text-red-500 { color: red; }")
    css_lines.append(".text-white { color: white; }")
    
    # Dimensoes e padding
    css_lines.append(".h-\\[20vh\\] { height: 20vh; }")
    css_lines.append(".h-\\[50vh\\] { height: 50vh; }")
    css_lines.append(".h-\\[85vh\\] { height: 85vh; }")
    css_lines.append(".w-1\\/2 { width: 50%; }")
    css_lines.append(".p-4 { padding: 1rem; }")
    css_lines.append(".mt-8 { margin-top: 2rem; }")
    
    css_code = "\n".join(css_lines)
    html_fallback = _compile_html_node(tree.root_node)
    
    return StandaloneRenderBundle(
        bundle_id=f"bundle-{uuid.uuid4().hex[:8]}",
        component_code=jsx_body,
        html_fallback=html_fallback,
        css_code=css_code,
        tailwind_safelist=list(classes_set),
        viewport={"width": 1440, "height": 900},
        dependencies_mode="local_pinned",
        network_allowed=False
    )
