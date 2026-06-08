"""
OS-019 — Micro Etapa M1
ExperienceBlueprint + BuildPlanResolver + StoriesBuilderGate

Objetivo:
  Construir o ExperienceBlueprint com parâmetros Mad Lab Theme canônicos,
  resolver o BuildPlan e validar no StoriesBuilderGate determinístico.

Gate de Aceite:
  StoriesBuilderGateReport.status == "passed" sem P0/P1 findings.

Evidências geradas:
  output_synthesis/OS-019/1_blueprint.json
  output_synthesis/OS-019/2_build_plan.json
  output_synthesis/OS-019/3_gate_report.json

Aurora v9.0 — OS-019 / Anti-Alucinação: todos contratos verificados fisicamente.
"""

import sys
import os
import json

# ─── Path Resolution ────────────────────────────────────────────────────────
this_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.extend([
    os.path.join(this_dir, "contracts"),
    os.path.join(this_dir, "factory"),
    os.path.join(this_dir, "..", "stories_builder"),
    os.path.join(this_dir, "..", "contracts"),
])

from experience_architecture_contracts import (
    ExperienceBlueprint,
    ExperienceSurface,
    NavigationStrategy,
    MotionStrategy,
    SpatialStrategy,
    AttentionStrategy,
    NarrativeStrategy,
)
from build_plan_resolver import BuildPlanResolver
from stories_builder_gate import StoriesBuilderGate

# ─── Output directory ────────────────────────────────────────────────────────
OUT_DIR = os.path.join(this_dir, "output_synthesis", "OS-019")
os.makedirs(OUT_DIR, exist_ok=True)

print("=" * 60)
print("OS-019 M1 — ExperienceBlueprint + Gate")
print(f"Output: {OUT_DIR}")
print("=" * 60)

# ─── M1.1: ExperienceBlueprint Mad Lab Theme ─────────────────────────────────
print("\n[M1.1] Construindo ExperienceBlueprint...")

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

blueprint_dict = blueprint.model_dump()
blueprint_path = os.path.join(OUT_DIR, "1_blueprint.json")
with open(blueprint_path, "w", encoding="utf-8") as f:
    json.dump(blueprint_dict, f, indent=2, default=str)

print(f"  surface_type:         {blueprint.surface_type.value}")
print(f"  navigation_strategy:  {blueprint.navigation_strategy.value}")
print(f"  motion_strategy:      {blueprint.motion_strategy.value}")
print(f"  spatial_strategy:     {blueprint.spatial_strategy.value}")
print(f"  visual_energy:        {blueprint.visual_energy}")
print(f"  immersion_level:      {blueprint.immersion_level}")
print(f"  Blueprint salvo em:   {blueprint_path}")

# ─── M1.2: BuildPlanResolver ─────────────────────────────────────────────────
print("\n[M1.2] Resolvendo StoriesBuildPlan...")

resolver = BuildPlanResolver()
build_plan = resolver.resolve_build_plan(
    blueprint=blueprint,
    plan_id="PLAN-OS019-MAD-LAB-001"
)

build_plan_dict = build_plan.model_dump()
build_plan_path = os.path.join(OUT_DIR, "2_build_plan.json")
with open(build_plan_path, "w", encoding="utf-8") as f:
    json.dump(build_plan_dict, f, indent=2, default=str)

print(f"  plan_id:              {build_plan.plan_id}")
print(f"  source_blueprint_id:  {build_plan.source_blueprint_id}")
print(f"  capabilities ({len(build_plan.capabilities)}):")
for cap in build_plan.capabilities:
    print(f"    - {cap.value}")
print(f"  forbidden_decisions ({len(build_plan.forbidden_decisions)}):")
for constraint in build_plan.forbidden_decisions:
    print(f"    - {constraint.value}")
print(f"  traceability_items:   {len(build_plan.traceability_items)}")
print(f"  Build plan salvo em:  {build_plan_path}")

# ─── M1.3: Verificação de Z-axis capabilities ────────────────────────────────
print("\n[M1.3] Verificando Z-axis capabilities no BuildPlan...")

z_required = {"render_z_axis_scroll", "render_depth_layers", "bind_scroll_to_depth"}
z_present = {cap.value for cap in build_plan.capabilities}
z_missing = z_required - z_present
if z_missing:
    print(f"  FALHA: Capabilities Z-axis ausentes: {z_missing}")
    sys.exit(1)
else:
    print(f"  OK: RENDER_Z_AXIS_SCROLL presente")
    print(f"  OK: RENDER_DEPTH_LAYERS presente")
    print(f"  OK: BIND_SCROLL_TO_DEPTH presente")

exoape_constraint = "no_exoape_surface_clone"
if exoape_constraint not in {c.value for c in build_plan.forbidden_decisions}:
    print(f"  FALHA: NO_EXOAPE_SURFACE_CLONE ausente")
    sys.exit(1)
else:
    print(f"  OK: NO_EXOAPE_SURFACE_CLONE presente")

# ─── M1.4: StoriesBuilderGate ────────────────────────────────────────────────
print("\n[M1.4] Executando StoriesBuilderGate...")

gate = StoriesBuilderGate()
gate_report = gate.validate_build_plan(build_plan, blueprint)

gate_dict = gate_report.model_dump()
gate_path = os.path.join(OUT_DIR, "3_gate_report.json")
with open(gate_path, "w", encoding="utf-8") as f:
    json.dump(gate_dict, f, indent=2, default=str)

print(f"  Gate status:  {gate_report.status.upper()}")
print(f"  Findings ({len(gate_report.findings)}):")
for finding in gate_report.findings:
    severity_marker = "  [P0/P1] " if finding.severity in ["P0", "P1"] else "  [INFO]  "
    print(f"{severity_marker}{finding.code}: {finding.message[:80]}")
print(f"  Gate report salvo em: {gate_path}")

# ─── M1 Gate Final ────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
critical = [f for f in gate_report.findings if f.severity in ["P0", "P1"]]
if gate_report.status != "passed" or critical:
    print("GATE M1: FALHOU")
    print(f"  {len(critical)} finding(s) P0/P1 detectados")
    for f in critical:
        print(f"  [{f.severity}] {f.code}: {f.message}")
    sys.exit(1)
else:
    print("GATE M1: PASSOU")
    print(f"  StoriesBuilderGateReport.status = passed")
    print(f"  Sem P0/P1 findings")
    print(f"  Z-axis capabilities verificadas")
    print(f"  NO_EXOAPE_SURFACE_CLONE verificada")
    print()
    print("Micro Etapa M1 concluida.")
    print("Proxima: M2 — FrontendCodeSpec + ComponentTree + TSX Synthesis")
print("=" * 60)
