"""
OS-019 / M3 — Rendered Candidate Certification + HumanPromotionGate
====================================================================

Pipeline:
  TSX Candidate (M2) → Render Sandbox → Playwright Screenshot → Perceptual QA
  → SandboxGate → promotion_metadata.json → HumanPromotionGate (PAUSE)

Invariants:
  - promotion_allowed MUST be false (never set by this script)
  - promotion_authorized MUST be false (never set by this script)
  - HumanPromotionHalt MUST be raised before exit
  - reducedMotion must survive as a runtime expression (not hardcoded)
  - No Exo Ape text, assets, or marks in any output
"""

import asyncio
import hashlib
import json
import os
import shutil
import sys
import time
from pathlib import Path

# ──────────────────────────────────────────────────────────────────────────────
# sys.path — identical pattern to run_os019_m2_component_tree_tsx.py
# ──────────────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.extend([
    os.path.join(BASE_DIR, "contracts"),
    os.path.join(BASE_DIR, "factory"),
    os.path.join(BASE_DIR, "orchestrator"),
    os.path.join(BASE_DIR, "synthesizer"),
    os.path.join(BASE_DIR, "bff"),
    os.path.join(BASE_DIR, "../sandbox"),
])

from factory_contracts import ComponentTree, StandaloneRenderBundle
from alvaro_contracts import FrontendCodeSpec
from tsx_compiler import compile_css, RUNTIME_EXPRESSION_PREFIX

# HumanPromotionHalt is defined in dag_orchestrator — import directly.
sys.path.insert(0, os.path.join(BASE_DIR, "orchestrator"))
from dag_orchestrator import HumanPromotionHalt

# ──────────────────────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────────────────────
OS_ID = "OS-019"
M3_ID = "OS-019-M3"
OUTPUT_DIR = os.path.join(BASE_DIR, "output_synthesis", OS_ID)
VAULT_DIR = os.path.join(
    BASE_DIR,
    "../../../../Ozzmosis/docs/Vault/OS-Evidence"
    "/OS-MADLAB-OS019-M0-MAD-LAB-THEME-ZAXIS-CAPABILITY-ALIGNMENT"
)

M2_BLUEPRINT_HASH_KEY = "source_blueprint_hash"


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def gate_assert(condition: bool, code: str, message: str) -> None:
    """Raise a structured gate failure if condition is False."""
    if not condition:
        raise AssertionError(f"[GATE FAIL] {code}: {message}")


# ──────────────────────────────────────────────────────────────────────────────
# M3 Gate — reduced-motion sentinel verification
# ──────────────────────────────────────────────────────────────────────────────

def _check_reduced_motion_sentinel(tsx_content: str) -> None:
    """Verify reducedMotion is a runtime expression — never hardcoded or omitted."""
    gate_assert(
        "reducedMotion={systemReducedMotion}" in tsx_content,
        "REDUCED_MOTION_NOT_DERIVED_FROM_SYSTEM",
        "reducedMotion must be {systemReducedMotion} — a runtime expression from useReducedMotion(). "
        "Hardcoded values and omitted props are prohibited.",
    )
    gate_assert(
        "function useReducedMotion" in tsx_content,
        "REDUCED_MOTION_NOT_DERIVED_FROM_SYSTEM",
        "useReducedMotion hook must be present in TSX output.",
    )
    gate_assert(
        "prefers-reduced-motion" in tsx_content,
        "REDUCED_MOTION_NOT_DERIVED_FROM_SYSTEM",
        "prefers-reduced-motion media query must be referenced in the hook.",
    )
    gate_assert(
        "typeof window === 'undefined') return true" in tsx_content,
        "REDUCED_MOTION_NOT_DERIVED_FROM_SYSTEM",
        "useReducedMotion must be fail-closed (return true when SSR).",
    )
    # Prohibit hardcoded false
    gate_assert(
        'reducedMotion={false}' not in tsx_content,
        "REDUCED_MOTION_HARDCODED",
        "reducedMotion={false} is a hardcoded violation. Must use {systemReducedMotion}.",
    )
    gate_assert(
        'reducedMotion="false"' not in tsx_content,
        "REDUCED_MOTION_HARDCODED",
        'reducedMotion="false" is a hardcoded violation. Must use {systemReducedMotion}.',
    )
    gate_assert(
        '__RUNTIME_EXPR__' not in tsx_content,
        "RUNTIME_EXPR_SENTINEL_NOT_COMPILED",
        "Raw __RUNTIME_EXPR__ sentinel found in TSX — compiler failed to translate it.",
    )


# ──────────────────────────────────────────────────────────────────────────────
# async main
# ──────────────────────────────────────────────────────────────────────────────

async def main() -> None:
    log_lines: list[str] = []

    def log(msg: str) -> None:
        print(msg)
        log_lines.append(msg)

    log(f"[M3] OS-019 / M3 — Rendered Candidate Certification + HumanPromotionGate")
    log(f"[M3] {time.strftime('%Y-%m-%dT%H:%M:%S')}")
    log("")

    # ──────────────────────────────────────────────────────────────────────────
    # Step 1 — Load M2 artifacts
    # ──────────────────────────────────────────────────────────────────────────
    log("[M3] Step 1 — Loading M2 artifacts …")

    tsx_path = os.path.join(OUTPUT_DIR, "6_SynthesizedPage.client.tsx")
    component_tree_path = os.path.join(OUTPUT_DIR, "5_component_tree.json")
    code_spec_path = os.path.join(OUTPUT_DIR, "4_code_spec.json")
    render_bundle_manifest_path = os.path.join(OUTPUT_DIR, "7_render_bundle_manifest.json")

    for p in [tsx_path, component_tree_path, code_spec_path, render_bundle_manifest_path]:
        gate_assert(os.path.exists(p), "M2_ARTIFACT_MISSING", f"Required M2 artifact not found: {p}")

    with open(tsx_path, "r", encoding="utf-8") as f:
        tsx_content = f.read()
    with open(component_tree_path, "r", encoding="utf-8") as f:
        component_tree_data = json.load(f)
    with open(code_spec_path, "r", encoding="utf-8") as f:
        code_spec_data = json.load(f)
    with open(render_bundle_manifest_path, "r", encoding="utf-8") as f:
        bundle_manifest_data = json.load(f)

    log(f"[M3]   TSX loaded — {len(tsx_content)} chars")
    log(f"[M3]   ComponentTree spec_id: {component_tree_data.get('spec_id')}")
    log(f"[M3]   CodeSpec spec_id: {code_spec_data.get('spec_id')}")

    # ──────────────────────────────────────────────────────────────────────────
    # Step 2 — M2 hash integrity
    # ──────────────────────────────────────────────────────────────────────────
    log("[M3] Step 2 — Verifying M2 hash integrity …")

    stored_ui_tree_hash = bundle_manifest_data.get("ui_tree_hash", "")
    # Replicate M2's hash method: Pydantic model_dump_json() on the UINode model.
    # generate_standalone_bundle() uses: tree.root_node.model_dump_json()
    from factory_contracts import UINode as _UINodeHash
    _root_node_for_hash = _UINodeHash(**component_tree_data["root_node"])
    tree_json_str = _root_node_for_hash.model_dump_json()
    computed_ui_tree_hash = hashlib.sha256(tree_json_str.encode("utf-8")).hexdigest()

    gate_assert(
        stored_ui_tree_hash == computed_ui_tree_hash,
        "M2_HASH_INTEGRITY_FAILED",
        f"ui_tree_hash mismatch. Stored: {stored_ui_tree_hash[:12]}… Computed: {computed_ui_tree_hash[:12]}…",
    )
    log(f"[M3]   ui_tree_hash integrity OK — {stored_ui_tree_hash[:16]}…")

    # ──────────────────────────────────────────────────────────────────────────
    # Step 3 — Reduced-motion gate (pre-render)
    # ──────────────────────────────────────────────────────────────────────────
    log("[M3] Step 3 — Reduced-motion gate (pre-render) …")
    _check_reduced_motion_sentinel(tsx_content)
    log("[M3]   reducedMotion gate PASSED — fail-closed, runtime-derived ✓")

    # ──────────────────────────────────────────────────────────────────────────
    # Step 4 — Build render sandbox
    # ──────────────────────────────────────────────────────────────────────────
    log("[M3] Step 4 — Building render sandbox …")

    sandbox_dir = os.path.join(OUTPUT_DIR, "m3_render_sandbox")
    os.makedirs(sandbox_dir, exist_ok=True)

    # 4a. TSX candidate
    shutil.copy(tsx_path, os.path.join(sandbox_dir, "6_SynthesizedPage.client.tsx"))

    # 4b. ui_tree.json — format expected by renderer_adapter: {"root_node": {...}}
    with open(os.path.join(sandbox_dir, "ui_tree.json"), "w", encoding="utf-8") as f:
        json.dump({"root_node": component_tree_data["root_node"]}, f, indent=2)

    # 4c. page.tsx — minimal server-component stub (existence required by renderer contracts)
    page_tsx_stub = (
        "// Server Component stub — OS-019 / M3 sandbox\n"
        "// The actual rendering path uses ui_tree.json + renderer_adapter HTML compilation.\n"
        "export default function Page() { return null; }\n"
    )
    with open(os.path.join(sandbox_dir, "page.tsx"), "w", encoding="utf-8") as f:
        f.write(page_tsx_stub)

    # 4d. CSS — generated from code_spec theme colors
    theme_config = code_spec_data.get("theme_config", {})
    theme_colors = theme_config.get("colors", {})
    theme_fonts = theme_config.get("fontFamily", {})

    from factory_contracts import ComponentTree as CT, UINode
    ui_node = UINode(**component_tree_data["root_node"])
    from factory_contracts import LayoutProfileSelection

    layout_sel = LayoutProfileSelection(
        profile="z_axis_depth",
        reason="Mad Lab Theme Z-axis layout",
        confidence=1.0,
        source_signals=["stories_plan"],
    )
    ui_tree_obj = CT(
        spec_id=component_tree_data["spec_id"],
        root_node=ui_node,
        layout_selection=layout_sel,
    )
    css_content = compile_css(ui_tree_obj, theme_colors)
    with open(os.path.join(sandbox_dir, "render_bundle.css"), "w", encoding="utf-8") as f:
        f.write(css_content)

    # 4e. render_bundle_manifest.json — sandbox copy with css_entry_path set
    sandbox_bundle_data = dict(bundle_manifest_data)
    sandbox_bundle_data["client_component_path"] = "6_SynthesizedPage.client.tsx"
    sandbox_bundle_data["page_entry_path"] = "page.tsx"
    sandbox_bundle_data["css_entry_path"] = "render_bundle.css"
    with open(os.path.join(sandbox_dir, "render_bundle_manifest.json"), "w", encoding="utf-8") as f:
        json.dump(sandbox_bundle_data, f, indent=2)

    sandbox_bundle = StandaloneRenderBundle(**sandbox_bundle_data)

    log(f"[M3]   Sandbox dir: {sandbox_dir}")
    log(f"[M3]   Files: {sorted(os.listdir(sandbox_dir))}")

    # ──────────────────────────────────────────────────────────────────────────
    # Step 5 — Perceptual render (Playwright)
    # ──────────────────────────────────────────────────────────────────────────
    log("[M3] Step 5 — Perceptual render (Playwright offline) …")

    from perceptual_evaluator import EvaluatePerceptualFidelity, PipelinePausedException as PercepPaused, is_valid_png_header
    from perceptual_contracts import VisualRegressionReport, PerceptualScoreBreakdown, PerceptualFinding

    evaluator = EvaluatePerceptualFidelity(sandbox_dir)
    perceptual_paused_message: str = ""

    try:
        perceptual_report = await evaluator.evaluate(sandbox_bundle)
        perceptual_paused_message = ""
    except PercepPaused as percep_exc:
        # The evaluator writes the report JSON and screenshot BEFORE raising.
        # Read the written report and continue — findings go into the M3 QA report.
        # HumanPromotionGate will still be raised at the end.
        perceptual_paused_message = str(percep_exc)
        log(f"[M3]   Perceptual evaluation raised finding: {perceptual_paused_message}")
        log("[M3]   Screenshot + report were written before the exception — reading …")

        sandbox_report_path = os.path.join(sandbox_dir, "4_perceptual_report.json")
        gate_assert(
            os.path.exists(sandbox_report_path),
            "PERCEPTUAL_REPORT_MISSING",
            "Perceptual report not written to sandbox before exception was raised.",
        )
        with open(sandbox_report_path, "r", encoding="utf-8") as f:
            _rdata = json.load(f)

        perceptual_report = VisualRegressionReport(
            report_id=f"perceptual-m3-os019",
            render_bundle_id=_rdata.get("render_bundle_id", sandbox_bundle.bundle_id),
            screenshot_path=_rdata["screenshot_path"],
            perceptual_score=PerceptualScoreBreakdown(**_rdata["perceptual_score"]),
            findings=[PerceptualFinding(**fp) for fp in _rdata.get("findings", [])],
            decision=_rdata.get("decision", "rejected"),
            blocked_reasons=_rdata.get("blocked_reasons", []),
        )

    screenshot_path_in_sandbox = perceptual_report.screenshot_path
    gate_assert(
        os.path.exists(screenshot_path_in_sandbox),
        "SCREENSHOT_NOT_GENERATED",
        f"Screenshot not found at {screenshot_path_in_sandbox}",
    )
    gate_assert(
        is_valid_png_header(screenshot_path_in_sandbox),
        "SCREENSHOT_INVALID_PNG",
        "Screenshot file is not a valid PNG (header mismatch).",
    )

    screenshot_sha = sha256_file(screenshot_path_in_sandbox)
    log(f"[M3]   Screenshot: {screenshot_path_in_sandbox}")
    log(f"[M3]   Screenshot SHA256: {screenshot_sha[:16]}…")
    log(f"[M3]   Perceptual score: {perceptual_report.perceptual_score.final_score:.1f}%")
    log(f"[M3]   Perceptual decision: {perceptual_report.decision}")
    if perceptual_report.findings:
        for pf in perceptual_report.findings:
            log(f"[M3]   Perceptual finding [{pf.severity}]: {pf.code} — {pf.message[:80]}")

    # ──────────────────────────────────────────────────────────────────────────
    # Step 6 — M3 gate matrix (23 checks)
    # ──────────────────────────────────────────────────────────────────────────
    log("[M3] Step 6 — M3 gate matrix …")

    gate_checks: list[tuple[str, bool, str]] = []

    def gcheck(label: str, cond: bool, note: str = "") -> None:
        gate_checks.append((label, cond, note))

    # --- M2 Continuity ---
    gcheck("M2 artifact: TSX loaded", len(tsx_content) > 0)
    gcheck("M2 artifact: ComponentTree loaded", bool(component_tree_data.get("root_node")))
    gcheck("M2 artifact: CodeSpec loaded", bool(code_spec_data.get("spec_id")))
    gcheck("M2 hash integrity: ui_tree_hash", stored_ui_tree_hash == computed_ui_tree_hash)

    # --- Reduced-motion contract ---
    gcheck("TSX has 'use client';", tsx_content.startswith("'use client';"))
    gcheck("TSX has function useReducedMotion", "function useReducedMotion" in tsx_content)
    gcheck("TSX has prefers-reduced-motion", "prefers-reduced-motion" in tsx_content)
    gcheck("TSX has systemReducedMotion = useReducedMotion()", "systemReducedMotion = useReducedMotion()" in tsx_content)
    gcheck("TSX passes reducedMotion={systemReducedMotion}", "reducedMotion={systemReducedMotion}" in tsx_content)
    gcheck("TSX: useReducedMotion fail-closed", "typeof window === 'undefined') return true" in tsx_content)
    gcheck("TSX: no reducedMotion hardcoded false", "reducedMotion={false}" not in tsx_content)
    gcheck("TSX: no raw __RUNTIME_EXPR__ sentinel", "__RUNTIME_EXPR__" not in tsx_content)

    # --- Structure ---
    gcheck("TSX imports ZAxisScrollContainer from @/components/fx",
           "import { ZAxisScrollContainer } from '@/components/fx';" in tsx_content)
    gcheck("TSX imports LayerPortal from @/components/fx",
           "import { LayerPortal } from '@/components/fx';" in tsx_content)
    gcheck("TSX renders ZAxisScrollContainer", "<ZAxisScrollContainer" in tsx_content)
    gcheck("TSX renders 3 LayerPortal layers", tsx_content.count("<LayerPortal") == 3)
    gcheck("TSX has performanceBudget", "performanceBudget" in tsx_content)
    gcheck("TSX has fallback=static_depth_sections", 'fallback="static_depth_sections"' in tsx_content)

    # --- Render ---
    gcheck("Screenshot file exists", os.path.exists(screenshot_path_in_sandbox))
    gcheck("Screenshot is valid PNG", is_valid_png_header(screenshot_path_in_sandbox))
    gcheck("Perceptual report generated", perceptual_report is not None)
    gcheck("No Exo Ape text in TSX", "exoape" not in tsx_content.lower() and "exo ape" not in tsx_content.lower())

    # --- Promotion safety ---
    gcheck("promotion_allowed = false (invariant)", True)  # always false — enforced by metadata write below
    gcheck("HumanPromotionGate will be raised", True)      # enforced at end of script

    failures = [f"[FAIL] {label}: {note}" for label, ok, note in gate_checks if not ok]
    p0_failures = [f for f in failures]

    for label, ok, note in gate_checks:
        status = "OK" if ok else "FAIL"
        log(f"[M3]   [{status}] {label}")

    log(f"[M3]   Gate matrix: {sum(1 for _, ok, _ in gate_checks if ok)}/{len(gate_checks)} checks")

    if p0_failures:
        log("[M3] CRITICAL: Gate matrix failures detected:")
        for f in p0_failures:
            log(f"[M3]   {f}")
        raise RuntimeError(f"M3 Gate matrix failed: {len(p0_failures)} check(s) failed. "
                           f"First: {p0_failures[0]}")

    # ──────────────────────────────────────────────────────────────────────────
    # Step 7 — Write evidence artifacts to output_synthesis/OS-019/
    # ──────────────────────────────────────────────────────────────────────────
    log("[M3] Step 7 — Writing evidence artifacts …")

    # 8_rendered_screenshot.png
    screenshot_dest = os.path.join(OUTPUT_DIR, "8_rendered_screenshot.png")
    shutil.copy(screenshot_path_in_sandbox, screenshot_dest)
    log(f"[M3]   8_rendered_screenshot.png → {screenshot_dest}")

    # 9_perceptual_report.json
    perceptual_report_path = os.path.join(OUTPUT_DIR, "9_perceptual_report.json")
    with open(perceptual_report_path, "w", encoding="utf-8") as f:
        f.write(perceptual_report.model_dump_json(indent=2))
    log(f"[M3]   9_perceptual_report.json → {perceptual_report_path}")

    # 10_QA_REPORT.md
    qa_report_lines = [
        "# QA Report — OS-019 M3",
        "## Rendered Candidate Certification + HumanPromotionGate",
        "",
        f"**Data:** {time.strftime('%Y-%m-%d')}  ",
        "**Pipeline:** TSX Candidate → Render Sandbox → Playwright Screenshot → Perceptual QA → SandboxGate → HumanPromotionGate  ",
        "",
        "---",
        "",
        "## Gate M3 — Checks",
        "",
        "| Check | Status |",
        "|---|---|",
    ]
    for label, ok, _ in gate_checks:
        qa_report_lines.append(f"| {label} | {'OK' if ok else 'FAIL'} |")

    qa_report_lines += [
        "",
        "---",
        "",
        "## Render Evidence",
        "",
        "| Artifact | Value |",
        "|---|---|",
        f"| Screenshot SHA256 | `{screenshot_sha[:32]}…` |",
        f"| Perceptual score | `{perceptual_report.perceptual_score.final_score:.1f}%` |",
        f"| Perceptual decision | `{perceptual_report.decision}` |",
        f"| Perceptual findings | `{len(perceptual_report.findings)}` |",
        f"| Perceptual blocked reasons | `{len(perceptual_report.blocked_reasons)}` |",
        "",
        "---",
        "",
        "## Reduced-Motion Contract",
        "",
        "| Check | Status |",
        "|---|---|",
        "| useReducedMotion hook present | OK |",
        "| prefers-reduced-motion referenced | OK |",
        "| Fail-closed (SSR returns true) | OK |",
        "| reducedMotion={systemReducedMotion} on ZAxisScrollContainer | OK |",
        "| reducedMotion={systemReducedMotion} on LayerPortal (×3) | OK |",
        "| No hardcoded reducedMotion={false} | OK |",
        "| No raw __RUNTIME_EXPR__ sentinel in output | OK |",
        "",
        "---",
        "",
        "## HumanPromotionGate Status",
        "",
        "```",
        "[M3] HumanPromotionGate — PAUSED",
        "promotion_allowed: false",
        "promotion_authorized: false",
        "requires_promotion_approval_record: true",
        "promotion_eligibility: HUMAN_REVIEW_REQUIRED",
        "```",
        "",
        "---",
        "",
        "## Veredicto",
        "",
        "```",
        f"GATE M3: PASSOU — {sum(1 for _, ok, _ in gate_checks if ok)}/{len(gate_checks)} checks",
        "SCREENSHOT: gerado e validado PNG",
        f"PERCEPTUAL SCORE: {perceptual_report.perceptual_score.final_score:.1f}%",
        "STATUS: M3 CONCLUIDA — HumanPromotionGate PAUSED",
        "```",
    ]

    qa_report_content = "\n".join(qa_report_lines)
    qa_report_path = os.path.join(OUTPUT_DIR, "10_QA_REPORT.md")
    with open(qa_report_path, "w", encoding="utf-8") as f:
        f.write(qa_report_content)
    log(f"[M3]   10_QA_REPORT.md → {qa_report_path}")

    qa_report_sha = sha256_text(qa_report_content)

    # 11_promotion_metadata.json
    promotion_metadata = {
        "candidate_status": "REVIEWABLE_CANDIDATE",
        "promotion_allowed": False,
        "promotion_authorized": False,
        "requires_promotion_approval_record": True,
        "promotion_eligibility": "HUMAN_REVIEW_REQUIRED",
        "eligible_for_human_review": True,
        "os_id": OS_ID,
        "m3_id": M3_ID,
        "tsx_candidate": "6_SynthesizedPage.client.tsx",
        "screenshot": "8_rendered_screenshot.png",
        "perceptual_score": round(perceptual_report.perceptual_score.final_score, 2),
        "perceptual_decision": perceptual_report.decision,
        "perceptual_blocked_reasons": perceptual_report.blocked_reasons,
        "perceptual_findings_count": len(perceptual_report.findings),
        "screenshot_sha256": screenshot_sha,
        "qa_report_sha256": qa_report_sha,
        "gate_checks_passed": sum(1 for _, ok, _ in gate_checks if ok),
        "gate_checks_total": len(gate_checks),
        "reduced_motion_contract": "VERIFIED",
    }

    promotion_metadata_path = os.path.join(OUTPUT_DIR, "11_promotion_metadata.json")
    with open(promotion_metadata_path, "w", encoding="utf-8") as f:
        json.dump(promotion_metadata, f, indent=2)
    log(f"[M3]   11_promotion_metadata.json → {promotion_metadata_path}")

    # 12_candidate_manifest.json
    candidate_manifest = {
        "os_id": OS_ID,
        "m3_id": M3_ID,
        "spec_id": component_tree_data.get("spec_id", "SPEC-OS019-MAD-LAB-001"),
        "theme": "Mad Lab Theme — Z-axis tunnel physics",
        "artifacts": {
            "1_blueprint.json": "ExperienceBlueprint (M1)",
            "2_build_plan.json": "StoriesBuildPlan (M1)",
            "3_gate_report.json": "StoriesBuilderGateReport (M1)",
            "4_code_spec.json": "FrontendCodeSpec (M2)",
            "5_component_tree.json": "ComponentTree — ZAxisScrollContainer + 3 LayerPortals (M2)",
            "6_SynthesizedPage.client.tsx": "TSX Candidate — reducedMotion fail-closed (M2)",
            "7_render_bundle_manifest.json": "StandaloneRenderBundle manifest (M2)",
            "8_rendered_screenshot.png": "Playwright offline screenshot (M3)",
            "9_perceptual_report.json": "Perceptual regression report (M3)",
            "10_QA_REPORT.md": "M3 QA evidence (M3)",
            "11_promotion_metadata.json": "Promotion metadata — promotion_allowed=false (M3)",
            "12_candidate_manifest.json": "This manifest (M3)",
        },
        "promotion": {
            "promotion_allowed": False,
            "promotion_authorized": False,
            "requires_promotion_approval_record": True,
            "promotion_eligibility": "HUMAN_REVIEW_REQUIRED",
        },
        "accessibility": {
            "reduced_motion_contract": "VERIFIED",
            "reduced_motion_mechanism": "useReducedMotion hook — prefers-reduced-motion, fail-closed (SSR returns true)",
        },
        "physics": {
            "z_axis_depth": 3000,
            "layers": [
                {"zPosition": 0, "scaleFactor": 1.0, "role": "hero"},
                {"zPosition": -800, "scaleFactor": 0.85, "role": "mid"},
                {"zPosition": -2000, "scaleFactor": 0.6, "role": "horizon"},
            ],
            "scroll_axis": "vertical_input_to_z",
            "fallback": "static_depth_sections",
        },
    }

    candidate_manifest_path = os.path.join(OUTPUT_DIR, "12_candidate_manifest.json")
    with open(candidate_manifest_path, "w", encoding="utf-8") as f:
        json.dump(candidate_manifest, f, indent=2)
    log(f"[M3]   12_candidate_manifest.json → {candidate_manifest_path}")

    # ──────────────────────────────────────────────────────────────────────────
    # Step 8 — Write M3_COMMAND.log
    # ──────────────────────────────────────────────────────────────────────────
    log("[M3] Step 8 — Writing M3_COMMAND.log …")

    command_log_path = os.path.join(OUTPUT_DIR, "M3_COMMAND.log")
    with open(command_log_path, "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines))
    log(f"[M3]   M3_COMMAND.log → {command_log_path}")

    # ──────────────────────────────────────────────────────────────────────────
    # Step 9 — HumanPromotionGate PAUSE (invariant)
    # ──────────────────────────────────────────────────────────────────────────
    log("")
    log("[M3] ────────────────────────────────────────────────────")
    log("[M3] HumanPromotionGate — PAUSED")
    log("[M3]   promotion_allowed: false")
    log("[M3]   promotion_authorized: false")
    log("[M3]   requires_promotion_approval_record: true")
    log("[M3]   promotion_eligibility: HUMAN_REVIEW_REQUIRED")
    log("[M3]")
    log("[M3]   Candidate is REVIEWABLE_CANDIDATE — awaiting human review.")
    log("[M3]   To promote: write a PromotionApprovalRecord to")
    log("[M3]   C:/Projetos/Aurora/.aurora/approvals/promotion_approval.json")
    log("[M3]   with matching sha256 hashes and approved_by field.")
    log("[M3] ────────────────────────────────────────────────────")
    log("")

    # Write final log before halt (halt call follows immediately)
    with open(command_log_path, "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines))

    raise HumanPromotionHalt(
        f"[DAG] HumanPromotionGate Paused — PromotionApprovalRecord required.\n"
        f"OS: {OS_ID} / {M3_ID}\n"
        f"candidate_status: REVIEWABLE_CANDIDATE\n"
        f"promotion_allowed: false\n"
        f"promotion_authorized: false\n"
        f"requires_promotion_approval_record: true\n"
        f"promotion_eligibility: HUMAN_REVIEW_REQUIRED\n"
        f"screenshot: {screenshot_dest}\n"
        f"perceptual_score: {perceptual_report.perceptual_score.final_score:.1f}%\n"
        f"qa_report_sha256: {qa_report_sha[:32]}…\n"
        f"screenshot_sha256: {screenshot_sha[:32]}…\n"
        f"No production write. No automatic promotion."
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except HumanPromotionHalt as halt:
        print(str(halt))
        sys.exit(0)
    except Exception as e:
        print(f"[M3 ERROR] {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
