"""
OS-019 — Micro Etapa M2
FrontendCodeSpec + ComponentTree Z-axis + TSX Candidate

Objetivo:
  Transformar os artefatos aprovados da M1 em ComponentTree com ZAxisScrollContainer
  e LayerPortal, compilar para TSX candidate com useReducedMotion real.

Gate de Aceite:
  - TSX contém 'use client';
  - TSX contém useReducedMotion hook
  - TSX contém systemReducedMotion (derivado de prefers-reduced-motion)
  - TSX contém ZAxisScrollContainer com reducedMotion={systemReducedMotion}
  - TSX contém LayerPortal com reducedMotion={systemReducedMotion}
  - TSX contém import @/components/fx
  - TSX NÃO contém import orfao de @/components/fx
  - TSX NÃO contém texto/marca Exo Ape
  - source_blueprint_hash integro

Evidencias geradas:
  output_synthesis/OS-019/4_code_spec.json
  output_synthesis/OS-019/5_component_tree.json
  output_synthesis/OS-019/6_SynthesizedPage.client.tsx
  output_synthesis/OS-019/7_render_bundle_manifest.json

Aurora v9.0 — OS-019 M2 / Contrato Antes de Codigo.
"""

import sys
import os
import json

this_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.extend([
    os.path.join(this_dir, "contracts"),
    os.path.join(this_dir, "factory"),
    os.path.join(this_dir, "orchestrator"),
    os.path.join(this_dir, "..", "stories_builder"),
    os.path.join(this_dir, "..", "contracts"),
    os.path.join(this_dir, "..", "sandbox"),
])

from experience_architecture_contracts import (
    ExperienceBlueprint, ExperienceSurface, NavigationStrategy,
    MotionStrategy, SpatialStrategy, AttentionStrategy, NarrativeStrategy,
)
from build_plan_resolver import BuildPlanResolver, compute_blueprint_hash
from stories_builder_gate import StoriesBuilderGate
from factory_contracts import UINode, ComponentTree, LayoutProfileSelection
from tsx_compiler import compile_tsx, generate_standalone_bundle, RUNTIME_EXPRESSION_PREFIX
from alvaro_contracts import (
    FrontendCodeSpec, TailwindThemeSpec, ComponentRequirement, ScaffoldingResolution
)

OUT_DIR = os.path.join(this_dir, "output_synthesis", "OS-019")
os.makedirs(OUT_DIR, exist_ok=True)

print("=" * 64)
print("OS-019 M2 — ComponentTree Z-axis + TSX Candidate")
print(f"Output: {OUT_DIR}")
print("=" * 64)

# ─── M2.1: Ler artefatos M1 e verificar integridade do hash ──────────────────
print("\n[M2.1] Lendo artefatos M1 e verificando integridade...")

blueprint_path = os.path.join(OUT_DIR, "1_blueprint.json")
build_plan_path = os.path.join(OUT_DIR, "2_build_plan.json")
gate_path = os.path.join(OUT_DIR, "3_gate_report.json")

for path in [blueprint_path, build_plan_path, gate_path]:
    if not os.path.exists(path):
        print(f"  FALHA: Artefato M1 ausente: {path}")
        sys.exit(1)

with open(gate_path, "r", encoding="utf-8") as f:
    gate_data = json.load(f)

if gate_data.get("status") != "passed":
    print(f"  FALHA: gate_report M1 nao esta com status=passed. Status: {gate_data.get('status')}")
    sys.exit(1)

print("  OK: Todos os artefatos M1 existem")
print(f"  OK: gate_report.status = {gate_data['status']}")

# Reconstruir blueprint identico (para verificar hash)
blueprint = ExperienceBlueprint(
    surface_type=ExperienceSurface.LANDING,
    navigation_strategy=NavigationStrategy.CANVAS_NAVIGATION,
    motion_strategy=MotionStrategy.KINETIC_FIELD,
    spatial_strategy=SpatialStrategy.FREEFORM_DEPTH,
    attention_strategy=AttentionStrategy.FOCAL_HIERARCHY,
    narrative_strategy=NarrativeStrategy.PROGRESSIVE_DISCOVERY,
    interaction_density="medium",
    visual_energy="high",
    immersion_level="high",
    rationale=(
        "Mad Lab Theme — Z-axis tunnel progression inspirada na gramatica editorial do exoape. "
        "Nao eh um clone do exoape. Eh uma fisica propria: o usuario nao rola uma pagina, "
        "ele atravessa um organismo digital. Fundo editorial radical, nao dark generico. "
        "Tension earned through depth, not decoration. "
        "canvas_navigation ativa Z-axis. freeform_depth ativa depth layers. "
        "exoape referencia de gramatica — constraint NO_EXOAPE_SURFACE_CLONE obrigatorio."
    )
)

with open(build_plan_path, "r", encoding="utf-8") as f:
    build_plan_data = json.load(f)

stored_hash = build_plan_data.get("source_blueprint_hash", "")
current_hash = compute_blueprint_hash(blueprint)
if stored_hash != current_hash:
    print(f"  FALHA: Hash integrity mismatch")
    print(f"    stored:  {stored_hash[:16]}...")
    print(f"    current: {current_hash[:16]}...")
    sys.exit(1)

print(f"  OK: source_blueprint_hash integro ({current_hash[:12]}...)")

# ─── M2.2: FrontendCodeSpec Mad Lab Theme ────────────────────────────────────
print("\n[M2.2] Construindo FrontendCodeSpec Mad Lab Theme...")

# Mad Lab Theme — editorial light surface, not dark generic
MAD_LAB_COLORS = {
    "base-surface":    "#FAFAF8",   # editorial cream
    "text-primary":    "#0A0A0A",   # near-black editorial
    "text-secondary":  "#555555",   # editorial secondary
    "accent":          "#0D0D1A",   # deep editorial navy
    "depth-mid":       "#2D2D3E",   # mid-depth layer
    "depth-horizon":   "#1A1A2E",   # far depth layer
    "editorial-warm":  "#D4C5A9",   # warm editorial tone
    "motion-trace":    "#4A4A6A",   # motion path indicator
}

MAD_LAB_FONTS = {
    "sans":  ["Space Grotesk", "Helvetica Neue", "sans-serif"],
    "mono":  ["Space Mono", "Courier New", "monospace"],
}

MAD_LAB_FONT_SIZES = {
    "body":     "1rem",
    "caption":  "0.875rem",
    "heading":  "3rem",
    "display":  "5rem",
}

# Z-axis component registry — FX components have is_core_library=False
component_registry = [
    ComponentRequirement(
        component_name="AuroraLandingShell",
        required_variants=["default"],
        is_core_library=True,
        label="Landing Shell",
        semantic_role="shell",
        content_function="layout_container",
        source_reference_id="mad_lab_shell",
        transformed_text="Mad Lab Aurora",
        section_group="shell",
    ),
    ComponentRequirement(
        component_name="ZAxisScrollContainer",
        required_variants=["z_axis_depth"],
        is_core_library=False,  # from @/components/fx, not core
        label="Tunnel Engine",
        semantic_role="z_axis_scroll",
        content_function="depth_progression",
        source_reference_id="mad_lab_tunnel",
        transformed_text="Z-Axis Tunnel",
        section_group="fx_layer",
    ),
    ComponentRequirement(
        component_name="LayerPortal",
        required_variants=["depth_layer"],
        is_core_library=False,  # from @/components/fx, not core
        label="Depth Layer",
        semantic_role="depth_layer",
        content_function="depth_positioning",
        source_reference_id="mad_lab_layer",
        transformed_text="Layer Portal",
        section_group="fx_layer",
    ),
    ComponentRequirement(
        component_name="AuroraHeading",
        required_variants=["display"],
        is_core_library=True,
        label="Mad Lab Aurora",
        semantic_role="heading",
        content_function="primary_headline",
        source_reference_id="mad_lab_hero_headline",
        transformed_text="Mad Lab Aurora",
        section_group="hero",
    ),
    ComponentRequirement(
        component_name="AuroraButton",
        required_variants=["primary"],
        is_core_library=True,
        label="Explorar o Sistema",
        semantic_role="button",
        content_function="primary_cta",
        source_reference_id="mad_lab_cta_primary",
        transformed_text="Explorar o Sistema",
        section_group="hero",
    ),
]

code_spec = FrontendCodeSpec(
    spec_id="SPEC-OS019-MAD-LAB-001",
    derived_from_draft_id=f"DRAFT-{build_plan_data['source_blueprint_id']}",
    theme_config=TailwindThemeSpec(
        colors=MAD_LAB_COLORS,
        fontFamily=MAD_LAB_FONTS,
        fontSize=MAD_LAB_FONT_SIZES,
    ),
    component_registry=component_registry,
    component_alerts=[],
    debt_tracking=ScaffoldingResolution(
        target_os="OS-019",
        pending_injectors=[],
        resolution_status="RESOLVED",
    ),
    ready_for_factory=True,
    blueprint=blueprint,
)

code_spec_dict = code_spec.model_dump(exclude={"blueprint"})
code_spec_path = os.path.join(OUT_DIR, "4_code_spec.json")
with open(code_spec_path, "w", encoding="utf-8") as f:
    json.dump(code_spec_dict, f, indent=2, default=str)

print(f"  spec_id:             {code_spec.spec_id}")
print(f"  derived_from_draft:  {code_spec.derived_from_draft_id}")
print(f"  theme colors:        {len(MAD_LAB_COLORS)} tokens")
print(f"  component_registry:  {len(component_registry)} entries")
print(f"  Code spec salvo em:  {code_spec_path}")

# ─── M2.3: ComponentTree Z-axis ──────────────────────────────────────────────
print("\n[M2.3] Construindo ComponentTree com Z-axis...")

# Mad Lab Theme tunnel structure:
#   ZAxisScrollContainer (tunnel engine)
#     LayerPortal z=0   (hero — at viewer plane)
#       AuroraHeading   (editorial headline)
#       AuroraButton    (primary CTA)
#     LayerPortal z=-800 (mid-depth narrative layer)
#       section         (editorial copy)
#     LayerPortal z=-2000 (far-depth immersion layer)
#       section         (depth horizon content)
#
# reducedMotion uses RUNTIME_EXPRESSION_PREFIX sentinel:
# The compiler translates "__RUNTIME_EXPR__:systemReducedMotion" to {systemReducedMotion}
# systemReducedMotion is declared via useReducedMotion() hook in the generated file.
# Fail-closed: returns true (no motion) when window is unavailable (SSR).

REDUCED_MOTION = f"{RUNTIME_EXPRESSION_PREFIX}systemReducedMotion"
PERFORMANCE_BUDGET_DESKTOP = {"targetFps": 60, "maxLayers": 8}

# Hero layer — at viewer plane (z=0)
hero_heading = UINode(
    node_id="hero-heading",
    component_name="AuroraHeading",
    semantic_role="heading",
    text_content="Mad Lab Aurora",
    props={"className": "text-5xl font-bold text-text-primary tracking-tight"},
    blueprint_source="narrative_strategy",
    decision_owner="experience_architect",
    authority_level="architectural",
)

hero_cta = UINode(
    node_id="hero-cta",
    component_name="AuroraButton",
    semantic_role="button",
    text_content="Explorar o Sistema",
    props={"variant": "primary", "className": "mt-8 px-10 py-4"},
    blueprint_source="interaction_density",
    decision_owner="experience_architect",
    authority_level="architectural",
)

layer_hero = UINode(
    node_id="layer-0-hero",
    component_name="LayerPortal",
    semantic_role="presentation",
    children=[hero_heading, hero_cta],
    props={
        "zPosition": 0,
        "scaleFactor": 1.0,
        "opacityLimit": 1.0,
        "visible": True,
        "reducedMotion": REDUCED_MOTION,
    },
    blueprint_source="spatial_strategy",
    decision_owner="experience_architect",
    authority_level="architectural",
)

# Mid-depth layer — narrative (z=-800)
mid_copy = UINode(
    node_id="mid-narrative-copy",
    component_name="div",
    semantic_role="region",
    text_content="A fabrica cognitiva que materializa produto a partir de fisica de profundidade.",
    props={"className": "text-2xl text-text-secondary font-sans max-w-2xl text-center"},
)

layer_mid = UINode(
    node_id="layer-1-mid",
    component_name="LayerPortal",
    semantic_role="presentation",
    children=[mid_copy],
    props={
        "zPosition": -800,
        "scaleFactor": 0.85,
        "opacityLimit": 0.8,
        "visible": True,
        "reducedMotion": REDUCED_MOTION,
    },
    blueprint_source="spatial_strategy",
    decision_owner="experience_architect",
    authority_level="architectural",
)

# Far-depth layer — horizon (z=-2000)
horizon_text = UINode(
    node_id="horizon-text",
    component_name="div",
    semantic_role="region",
    text_content="Depth Horizon — Aurora Factory",
    props={"className": "text-lg text-editorial-warm tracking-widest uppercase"},
)

layer_far = UINode(
    node_id="layer-2-far",
    component_name="LayerPortal",
    semantic_role="presentation",
    children=[horizon_text],
    props={
        "zPosition": -2000,
        "scaleFactor": 0.6,
        "opacityLimit": 0.5,
        "visible": True,
        "reducedMotion": REDUCED_MOTION,
    },
    blueprint_source="spatial_strategy",
    decision_owner="experience_architect",
    authority_level="architectural",
)

# Tunnel root — ZAxisScrollContainer
tunnel_root = UINode(
    node_id="tunnel-root",
    component_name="ZAxisScrollContainer",
    semantic_role="container",
    children=[layer_hero, layer_mid, layer_far],
    props={
        "enabled": True,
        "quality": "high",
        "depth": 3000,
        "scrollAxis": "vertical_input_to_z",
        "performanceBudget": PERFORMANCE_BUDGET_DESKTOP,
        "fallback": "static_depth_sections",
        "reducedMotion": REDUCED_MOTION,
        "className": "w-full min-h-screen bg-base-surface",
    },
    blueprint_source="navigation_strategy",
    decision_owner="experience_architect",
    authority_level="architectural",
)

component_tree = ComponentTree(
    spec_id=code_spec.spec_id,
    root_node=tunnel_root,
    layout_selection=LayoutProfileSelection(
        profile="z_axis_depth",
        reason="Mad Lab Theme — Z-axis tunnel progression",
        confidence=1.0,
        source_signals=["canvas_navigation", "freeform_depth", "mad_lab_theme"],
    ),
    component_findings=[],
)

tree_dict = component_tree.model_dump()
tree_path = os.path.join(OUT_DIR, "5_component_tree.json")
with open(tree_path, "w", encoding="utf-8") as f:
    json.dump(tree_dict, f, indent=2, default=str)

print(f"  root component:    {component_tree.root_node.component_name}")
print(f"  Z-axis layers:     {len(tunnel_root.children)} LayerPortals")
print(f"  layout_profile:    {component_tree.layout_selection.profile}")
print(f"  Component tree salvo em: {tree_path}")

# ─── M2.4: TSX Compilation ────────────────────────────────────────────────────
print("\n[M2.4] Compilando TSX candidate...")

tsx_output = compile_tsx(component_tree)

tsx_path = os.path.join(OUT_DIR, "6_SynthesizedPage.client.tsx")
with open(tsx_path, "w", encoding="utf-8") as f:
    f.write(tsx_output)

print(f"  TSX salvo em: {tsx_path}")
print(f"  Tamanho: {len(tsx_output)} chars / {tsx_output.count(chr(10))} linhas")

# ─── M2.5: Render Bundle Manifest ────────────────────────────────────────────
print("\n[M2.5] Gerando render bundle manifest...")

from factory_contracts import StandaloneRenderBundle
import hashlib
tree_hash = hashlib.sha256(component_tree.root_node.model_dump_json().encode()).hexdigest()

bundle = StandaloneRenderBundle(
    bundle_id="bundle-os019-mad-lab-001",
    ui_tree_hash=tree_hash,
    client_component_path="6_SynthesizedPage.client.tsx",
    page_entry_path="page.tsx",
    css_entry_path=None,
    dependencies_mode="local_pinned",
    network_allowed=False,
    viewport_presets=["1440x900", "375x812"],
)

bundle_path = os.path.join(OUT_DIR, "7_render_bundle_manifest.json")
with open(bundle_path, "w", encoding="utf-8") as f:
    json.dump(bundle.model_dump(), f, indent=2, default=str)

print(f"  bundle_id:   {bundle.bundle_id}")
print(f"  ui_tree_hash: {tree_hash[:12]}...")
print(f"  Bundle salvo em: {bundle_path}")

# ─── M2 Gate Final ────────────────────────────────────────────────────────────
print("\n" + "=" * 64)
print("EXECUTANDO GATE M2...")

failures = []

def check(condition: bool, label: str):
    if condition:
        print(f"  OK: {label}")
    else:
        print(f"  FALHA: {label}")
        failures.append(label)

check("'use client';" in tsx_output,
      "TSX tem 'use client';")
check("function useReducedMotion" in tsx_output,
      "TSX tem useReducedMotion hook")
check("prefers-reduced-motion" in tsx_output,
      "TSX tem prefers-reduced-motion no hook")
check("systemReducedMotion = useReducedMotion()" in tsx_output,
      "TSX declara systemReducedMotion no body")
check("reducedMotion={systemReducedMotion}" in tsx_output,
      "TSX passa reducedMotion={systemReducedMotion} (derivado de sistema)")
check("import React from 'react';" in tsx_output,
      "TSX importa React")
check("import { ZAxisScrollContainer } from '@/components/fx';" in tsx_output,
      "TSX importa ZAxisScrollContainer de @/components/fx")
check("import { LayerPortal } from '@/components/fx';" in tsx_output,
      "TSX importa LayerPortal de @/components/fx")
check("import { ZAxisScrollContainer } from '@/components/core';" not in tsx_output,
      "TSX nao tem import orfao de ZAxisScrollContainer em core")
check("import { LayerPortal } from '@/components/core';" not in tsx_output,
      "TSX nao tem import orfao de LayerPortal em core")
check("exoape" not in tsx_output.lower(),
      "TSX nao contem texto/marca Exo Ape")
check("<ZAxisScrollContainer" in tsx_output,
      "TSX renderiza ZAxisScrollContainer")
check("<LayerPortal" in tsx_output,
      "TSX renderiza LayerPortal")
check('"fallback"' not in tsx_output and 'fallback="static_depth_sections"' in tsx_output,
      "TSX passa fallback=static_depth_sections")
check("performanceBudget=" in tsx_output,
      "TSX passa performanceBudget")
check("__RUNTIME_EXPR__" not in tsx_output,
      "TSX nao contem sentinel bruto (foi compilado corretamente)")

print()
if failures:
    print(f"GATE M2: FALHOU ({len(failures)} falha(s))")
    for f in failures:
        print(f"  - {f}")
    sys.exit(1)
else:
    print("GATE M2: PASSOU")
    print()
    print("  Todos os criterios de aceite satisfeitos.")
    print("  reducedMotion derivado de prefers-reduced-motion (fail-closed).")
    print("  Nenhum texto/marca Exo Ape no candidato.")
    print("  Import @/components/fx condicional e sem orfao.")
    print()
    print("Micro Etapa M2 concluida.")
    print("Proxima: QA M2 → M3 HumanPromotionGate")

print("=" * 64)
