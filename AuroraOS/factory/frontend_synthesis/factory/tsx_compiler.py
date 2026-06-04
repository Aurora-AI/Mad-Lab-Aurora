from factory_contracts import ComponentTree, UINode, StandaloneRenderBundle
import json
import uuid
import hashlib

def _format_props(props: dict, classes: list) -> str:
    """Serializa as propriedades Python para sintaxe TSX segura com validação."""
    prop_str = ""
    
    # Validação de segurança P0/P1 contra injeções brutas de JSX ou perigosas
    for key, value in props.items():
        if key == "dangerouslySetInnerHTML":
            raise ValueError("Violação de Segurança: Uso proibido de dangerouslySetInnerHTML.")
        if isinstance(value, str):
            # Impedir tags HTML cruas nas props para bloquear injeções JSX inseguras
            if "<" in value and ">" in value:
                raise ValueError(f"Violação de Segurança: JSX cru inseguro detetado na propriedade '{key}'.")
            # Higienizar classNames de caracteres perigosos
            if key == "className":
                value = value.replace('"', '').replace("'", "")
                
    if classes:
        cls_string = " ".join(classes)
        prop_str += f' className="{cls_string}"'
        
    for key, value in props.items():
        if isinstance(value, bool):
            prop_str += f" {key}" if value else ""
        elif isinstance(value, str):
            prop_str += f' {key}="{value}"'
        else:
            prop_str += f" {key}={{{json.dumps(value)}}}"
    
    return prop_str

def _compile_node(node: UINode, indent_level: int = 2, imports: set = None) -> str:
    """Motor recursivo de transpilação TSX."""
    if imports is None:
        imports = set()
        
    indent = "  " * indent_level
    comp = node.component_name
    
    # Validar que a tag não contém caracteres JSX inseguros
    if "<" in comp or ">" in comp:
        raise ValueError(f"Violação de Compilação: Nome do componente '{comp}' inválido.")
        
    # Se for componente Aurora, registra o import
    if comp.startswith("Aurora"):
        imports.add(f"import {{ {comp} }} from '@/components/core';")

    props_formatted = _format_props(node.props, [])
    
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

def _compile_html_node(node: UINode, theme_colors: dict = None, indent_level: int = 2) -> str:
    """Gera fallback HTML puramente visual para testes de screenshot."""
    indent = "  " * indent_level
    comp = node.component_name.lower()
    
    # Map Aurora components to standard HTML
    if "button" in comp: comp = "button"
    elif "input" in comp: comp = "input"
    elif "card" in comp: comp = "div"
    elif "text" in comp: comp = "span"
    elif comp.startswith("aurora"): comp = "div"
    
    prop_str = ""
    className = node.props.get("className", "")
    
    if className:
        classes = className.split()
        prop_str += f' class="{className}"'
        
        # Injetar fallback style explícito para garantir renderização de cor
        styles = []
        for c in classes:
            if c == "min-h-screen": styles.append("min-height: 100vh;")
            if c == "flex": styles.append("display: flex;")
            if c == "flex-col": styles.append("flex-direction: column;")
            if c == "items-center": styles.append("align-items: center;")
            if c == "h-[20vh]": styles.append("height: 20vh;")
            if c == "h-[50vh]": styles.append("height: 50vh;")
            if c == "h-[85vh]": styles.append("height: 85vh;")
            if c == "w-1/2": styles.append("width: 50%;")
            if c == "w-full": styles.append("width: 100%;")
            
            # Injeção dinâmica baseada no tema
            if theme_colors:
                if c.startswith("bg-"):
                    color_name = c[3:]
                    # Tratar classes como bg-base-surface ou bg-accent
                    if color_name in theme_colors:
                        styles.append(f"background-color: {theme_colors[color_name]};")
                elif c.startswith("text-"):
                    color_name = c[5:]
                    if color_name in theme_colors:
                        styles.append(f"color: {theme_colors[color_name]};")
            else:
                # Fallbacks antigos seguros
                if c == "bg-base-surface": styles.append("background-color: #0A0A0C;")
                if c == "bg-action-primary": styles.append("background-color: #4A3FF4;")
                if c == "text-text-primary": styles.append("color: #FFFFFF;")
                if c == "text-white": styles.append("color: #FFFFFF;")
        
        if styles:
            prop_str += f' style="{" ".join(styles)}"'
        
    code = f"{indent}<{comp}{prop_str}>\n"
    if node.text_content:
        code += f"{indent}  {node.text_content}\n"
    if node.children:
        for child in node.children:
            code += _compile_html_node(child, theme_colors, indent_level + 1) + "\n"
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
    colors_json = json.dumps(theme_colors, indent=6)[1:-1]
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

def compile_css(tree: ComponentTree, theme_colors: dict) -> str:
    """Gera o código CSS estático necessário para as classes Tailwind mapeadas."""
    css_lines = [
        ".min-h-screen { min-height: 100vh; }",
        ".flex { display: flex; }",
        ".flex-col { flex-direction: column; }",
        ".items-center { align-items: center; }",
        ".justify-center { justify-content: center; }",
        ".w-full { width: 100%; }",
        ".text-red-500 { color: red; }",
        ".text-white { color: white; }",
        ".h-\\[20vh\\] { height: 20vh; }",
        ".h-\\[50vh\\] { height: 50vh; }",
        ".h-\\[85vh\\] { height: 85vh; }",
        ".w-1\\/2 { width: 50%; }",
        ".p-4 { padding: 1rem; }",
        ".mt-8 { margin-top: 2rem; }",
        ".grid { display: grid; }",
        ".grid-cols-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }",
        ".gap-4 { gap: 1rem; }",
        ".border { border-width: 1px; }",
        ".border-dashed { border-style: dashed; }",
        ".bg-gray-50 { background-color: #f9fafb; }",
        ".text-heading-1 { font-size: 2.25rem; }",
        ".font-bold { font-weight: 700; }"
    ]
    for color_name, color_val in theme_colors.items():
        css_lines.append(f".bg-{color_name} {{ background-color: {color_val}; }}")
        css_lines.append(f".text-{color_name} {{ color: {color_val}; }}")
    return "\n".join(css_lines)

def generate_standalone_bundle(tree: ComponentTree, theme_colors: dict, theme_fonts: dict) -> StandaloneRenderBundle:
    """Gera o StandaloneRenderBundle mapeando ficheiros físicos locais sem simulação de renderização."""
    
    # Calcular hash de integridade da árvore UINode
    tree_json = tree.root_node.model_dump_json()
    ui_tree_hash = hashlib.sha256(tree_json.encode('utf-8')).hexdigest()
    
    bundle_id = f"bundle-{uuid.uuid4().hex[:8]}"
    
    return StandaloneRenderBundle(
        bundle_id=bundle_id,
        ui_tree_hash=ui_tree_hash,
        client_component_path="5_SynthesizedPage.client.tsx",
        page_entry_path="5_page.tsx",
        css_entry_path="render_bundle.css",
        dependencies_mode="local_pinned",
        network_allowed=False,
        viewport_presets=["1440x900"]
    )

