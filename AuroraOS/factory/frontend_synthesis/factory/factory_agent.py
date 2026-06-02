import uuid
from factory_contracts import UINode, ComponentTree
from tsx_compiler import compile_tsx, generate_tailwind_config
import sys
import os

# Ajuste temporal para importar o spec mockado (sys.path.append seria via PYTHONPATH industrial)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../orchestrator')))
from alvaro_contracts import (
    FrontendCodeSpec,
    TailwindThemeSpec,
    ComponentRequirement,
    ComponentMissingAlert,
    ScaffoldingResolution
)

def generate_ui_tree(spec: FrontendCodeSpec) -> ComponentTree:
    """Mapeia o Spec Orquestrado para a Árvore AST."""
    print(f"[FACTORY] Instanciando ComponentTree a partir da Spec: {spec.spec_id}")
    
    # 1. Estrutura Base (Identifica paradigma Luz Monumental)
    is_luz_monumental = (spec.theme_config.colors.get("base-surface") == "#FFFFFF")
    
    if is_luz_monumental:
        root = UINode(
            node_id="root-001",
            component_type="main",
            tailwind_classes=["min-h-screen", "bg-base-surface", "text-text-primary", "flex", "flex-col", "items-center", "w-full", "font-sans"],
            children=[]
        )
        
        # Header / Navigation
        nav_node = UINode(
            node_id="nav-container",
            component_type="header",
            tailwind_classes=["w-full", "max-w-6xl", "px-6", "py-8", "flex", "justify-between", "items-center"],
            children=[
                UINode(
                    node_id="logo",
                    component_type="div",
                    text_content="ANTIGRAVITY",
                    tailwind_classes=["font-heading", "text-xl", "font-bold", "tracking-widest"]
                ),
                UINode(
                    node_id="nav-links",
                    component_type="nav",
                    tailwind_classes=["flex", "gap-8", "text-sm", "font-medium", "text-text-secondary"],
                    children=[
                        UINode(node_id="link-1", component_type="span", text_content="Overview", tailwind_classes=["cursor-pointer", "hover:text-text-primary"]),
                        UINode(node_id="link-2", component_type="span", text_content="Technology", tailwind_classes=["cursor-pointer", "hover:text-text-primary"]),
                        UINode(node_id="link-3", component_type="span", text_content="Status", tailwind_classes=["cursor-pointer", "hover:text-text-primary"])
                    ]
                )
            ]
        )
        root.children.append(nav_node)
        
        # Hero Section (Ocupa 85vh conforme QA)
        hero_node = UINode(
            node_id="hero-section",
            component_type="section",
            tailwind_classes=["h-[85vh]", "w-full", "max-w-4xl", "px-6", "flex", "flex-col", "justify-center", "items-center", "text-center", "relative"],
            children=[
                # Particles Canvas Container (Isolado com ID para injeção de motion primitives)
                UINode(
                    node_id="particles-canvas-container",
                    component_type="div",
                    tailwind_classes=["absolute", "inset-0", "pointer-events-none", "z-0", "opacity-40"],
                    props={"id": "particles-canvas-container"}
                ),
                UINode(
                    node_id="hero-title",
                    component_type="h1",
                    text_content="Antigravity",
                    tailwind_classes=["text-heading-1", "font-heading", "font-bold", "tracking-tighter", "z-10", "mb-6"]
                ),
                UINode(
                    node_id="hero-subtitle",
                    component_type="p",
                    text_content="Experience the precision of architectural whitespace and premium editorial typography.",
                    tailwind_classes=["text-heading-2", "text-text-secondary", "max-w-2xl", "mb-8", "z-10", "leading-relaxed"]
                ),
                UINode(
                    node_id="hero-cta",
                    component_type="AuroraButton",
                    props={"variant": "default"},
                    text_content="Explore Workspace Status",
                    tailwind_classes=["z-10", "px-8", "py-4", "bg-action-primary", "text-white", "rounded-none", "font-medium", "hover:opacity-90", "transition-opacity"]
                )
            ]
        )
        root.children.append(hero_node)
        
    else:
        root = UINode(
            node_id="root-001",
            component_type="main",
            tailwind_classes=["min-h-screen", "w-full", "bg-base-surface", "flex", "flex-col", "items-center"],
            children=[]
        )
        
        container = UINode(node_id="container-001", component_type="div", tailwind_classes=["flex", "flex-col", "w-full"], children=[])

        btn = UINode(
            node_id="btn-001",
            component_type="AuroraButton",
            tailwind_classes=["mt-8", "w-1/2", "h-[50vh]", "bg-action-primary"],
            children=[]
        )
        
        container.children.append(btn)
        root.children.append(container)
        
        # 2. Injetando Componentes Inferidos
        for req in spec.component_registry:
            if req.component_name == "AuroraNavbar":
                root.children.append(UINode(
                    node_id=f"nav-{uuid.uuid4().hex[:4]}",
                    component_type="AuroraNavbar",
                    tailwind_classes=["w-full", "shadow-sm", "bg-action-primary", "h-[20vh]"]
                ))
            elif req.component_name == "AuroraButton":
                root.children.append(UINode(
                    node_id=f"btn-{uuid.uuid4().hex[:4]}",
                    component_type="AuroraButton",
                    props={"variant": req.required_variants[0]},
                    text_content="Ação Primária",
                    tailwind_classes=["mt-8", "w-1/2", "h-[50vh]", "bg-action-primary"]
                ))

    # 3. Injetando a Degradação (O Tratamento do Fallback da OS-004)
    for alert in spec.component_alerts:
        root.children.append(UINode(
            node_id=f"fallback-{uuid.uuid4().hex[:4]}",
            component_type=alert.degraded_to,
            text_content=f"[Degraded: {alert.original_role}]",
            tailwind_classes=["text-red-500", "p-4", "border", "border-dashed"]
        ))

    return ComponentTree(spec_id=spec.spec_id, root_node=root)

if __name__ == "__main__":
    # Teste de Ponta a Ponta usando os modelos de contrato reais
    mock_spec = FrontendCodeSpec(
        spec_id="SPEC-TEST-999",
        derived_from_draft_id="DS-001",
        theme_config=TailwindThemeSpec(
            colors={"base-surface": "#0A0A0C", "action-primary": "#4A3FF4"},
            fontFamily={"sans": ["var(--aurora-font-sans)", "system-ui"]},
            fontSize={"body": "1rem"}
        ),
        component_registry=[
            ComponentRequirement(component_name="AuroraNavbar", required_variants=["default"], is_core_library=True),
            ComponentRequirement(component_name="AuroraButton", required_variants=["primary"], is_core_library=True)
        ],
        component_alerts=[
            ComponentMissingAlert(original_role="marquee", degraded_to="div", reason="Not supported")
        ],
        debt_tracking=ScaffoldingResolution(
            target_os="OS-003", 
            pending_injectors=["motion"], 
            resolution_status="PARTIALLY_RESOLVED"
        )
    )

    tree = generate_ui_tree(mock_spec)
    tsx_output = compile_tsx(tree)
    tw_output = generate_tailwind_config(mock_spec.theme_config.colors, mock_spec.theme_config.fontFamily)
    
    print("\n=== PAGE.TSX (COMPILADO) ===\n")
    print(tsx_output)
    print("\n=== TAILWIND.CONFIG.JS ===\n")
    print(tw_output)
