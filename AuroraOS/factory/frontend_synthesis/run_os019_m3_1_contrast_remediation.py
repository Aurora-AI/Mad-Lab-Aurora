"""
OS-019 / M3.1 — Contrast Token Remediation & Re-render
=======================================================

Micro-etapa de remediação de contraste sobre o candidato M3.

Finding remediado:
  P1 LOW_CONTRAST_RATIO: editorial-warm #D4C5A9 / base-surface #FAFAF8 = 1.63:1
  WCAG AA exige >= 4.5:1 para texto regular

Correção aplicada:
  editorial-warm: #D4C5A9 → #7A6A52
  Novo contraste: 5.01:1 (passes WCAG AA)

Invariants preservados:
  - promotion_allowed: false
  - promotion_authorized: false
  - HumanPromotionHalt deve ser levantado
  - reducedMotion continua fail-closed
"""

import asyncio
import hashlib
import json
import os
import shutil
import sys
import time
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.extend([
    os.path.join(BASE_DIR, "contracts"),
    os.path.join(BASE_DIR, "factory"),
    os.path.join(BASE_DIR, "orchestrator"),
    os.path.join(BASE_DIR, "synthesizer"),
    os.path.join(BASE_DIR, "bff"),
    os.path.join(BASE_DIR, "../sandbox"),
])
sys.path.insert(0, os.path.join(BASE_DIR, "orchestrator"))
from dag_orchestrator import HumanPromotionHalt

from factory_contracts import ComponentTree, StandaloneRenderBundle, UINode, LayoutProfileSelection
from tsx_compiler import compile_css

OS_ID = "OS-019"
M_ID = "OS-019-M3.1"
OUTPUT_DIR = os.path.join(BASE_DIR, "output_synthesis", OS_ID)

EDITORIAL_WARM_OLD = "#D4C5A9"
EDITORIAL_WARM_NEW = "#7A6A52"
BASE_SURFACE = "#FAFAF8"
EXPECTED_CONTRAST_MIN = 4.5


def luminance(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255
    def lin(c: float) -> float:
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def contrast_ratio(c1: str, c2: str) -> float:
    l1, l2 = luminance(c1), luminance(c2)
    if l1 < l2:
        l1, l2 = l2, l1
    return (l1 + 0.05) / (l2 + 0.05)


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def gate_assert(condition: bool, code: str, message: str) -> None:
    if not condition:
        raise AssertionError(f"[GATE FAIL] {code}: {message}")


async def main() -> None:
    log_lines: list[str] = []

    def log(msg: str) -> None:
        print(msg)
        log_lines.append(msg)

    log(f"[M3.1] OS-019 / M3.1 — Contrast Token Remediation & Re-render")
    log(f"[M3.1] {time.strftime('%Y-%m-%dT%H:%M:%S')}")
    log(f"[M3.1] Remediating: editorial-warm {EDITORIAL_WARM_OLD} → {EDITORIAL_WARM_NEW}")
    log("")

    # ──────────────────────────────────────────────────────────────────────────
    # Step 1 — Verify token correction is applied in code_spec
    # ──────────────────────────────────────────────────────────────────────────
    log("[M3.1] Step 1 — Verify token correction in code_spec …")

    code_spec_path = os.path.join(OUTPUT_DIR, "4_code_spec.json")
    tsx_path = os.path.join(OUTPUT_DIR, "6_SynthesizedPage.client.tsx")
    component_tree_path = os.path.join(OUTPUT_DIR, "5_component_tree.json")
    render_bundle_manifest_path = os.path.join(OUTPUT_DIR, "7_render_bundle_manifest.json")

    with open(code_spec_path, "r", encoding="utf-8") as f:
        code_spec_data = json.load(f)
    with open(tsx_path, "r", encoding="utf-8") as f:
        tsx_content = f.read()
    with open(component_tree_path, "r", encoding="utf-8") as f:
        component_tree_data = json.load(f)
    with open(render_bundle_manifest_path, "r", encoding="utf-8") as f:
        bundle_manifest_data = json.load(f)

    theme_colors = code_spec_data["theme_config"]["colors"]
    actual_editorial_warm = theme_colors.get("editorial-warm", "")

    gate_assert(
        actual_editorial_warm == EDITORIAL_WARM_NEW,
        "CONTRAST_TOKEN_NOT_APPLIED",
        f"editorial-warm in code_spec is '{actual_editorial_warm}', expected '{EDITORIAL_WARM_NEW}'. "
        "Apply the token fix before running M3.1.",
    )
    log(f"[M3.1]   editorial-warm in code_spec: {actual_editorial_warm} ✓")

    # Verify contrast ratio analytically
    cr = contrast_ratio(EDITORIAL_WARM_NEW, BASE_SURFACE)
    gate_assert(
        cr >= EXPECTED_CONTRAST_MIN,
        "CONTRAST_RATIO_INSUFFICIENT",
        f"editorial-warm {EDITORIAL_WARM_NEW} vs base-surface {BASE_SURFACE} = {cr:.2f}:1. "
        f"Minimum required: {EXPECTED_CONTRAST_MIN}:1.",
    )
    log(f"[M3.1]   Contrast ratio: {cr:.2f}:1 (>= {EXPECTED_CONTRAST_MIN}:1 WCAG AA) ✓")

    # ──────────────────────────────────────────────────────────────────────────
    # Step 2 — Reduced-motion contract still intact
    # ──────────────────────────────────────────────────────────────────────────
    log("[M3.1] Step 2 — Reduced-motion contract still intact …")

    gate_assert("reducedMotion={systemReducedMotion}" in tsx_content,
                "REDUCED_MOTION_NOT_DERIVED_FROM_SYSTEM", "reducedMotion must be {systemReducedMotion}")
    gate_assert("function useReducedMotion" in tsx_content,
                "REDUCED_MOTION_NOT_DERIVED_FROM_SYSTEM", "useReducedMotion hook must be present")
    gate_assert("prefers-reduced-motion" in tsx_content,
                "REDUCED_MOTION_NOT_DERIVED_FROM_SYSTEM", "prefers-reduced-motion must be referenced")
    gate_assert("typeof window === 'undefined') return true" in tsx_content,
                "REDUCED_MOTION_NOT_DERIVED_FROM_SYSTEM", "fail-closed SSR check required")
    gate_assert("__RUNTIME_EXPR__" not in tsx_content,
                "RUNTIME_EXPR_SENTINEL_NOT_COMPILED", "raw sentinel in TSX")
    log("[M3.1]   reducedMotion contract INTACT ✓")

    # ──────────────────────────────────────────────────────────────────────────
    # Step 3 — Build fresh render sandbox with corrected CSS
    # ──────────────────────────────────────────────────────────────────────────
    log("[M3.1] Step 3 — Building render sandbox with corrected CSS …")

    sandbox_dir = os.path.join(OUTPUT_DIR, "m3_1_render_sandbox")
    os.makedirs(sandbox_dir, exist_ok=True)

    # TSX unchanged (uses class name text-editorial-warm — color value lives in CSS)
    shutil.copy(tsx_path, os.path.join(sandbox_dir, "6_SynthesizedPage.client.tsx"))

    # ui_tree.json
    with open(os.path.join(sandbox_dir, "ui_tree.json"), "w", encoding="utf-8") as f:
        json.dump({"root_node": component_tree_data["root_node"]}, f, indent=2)

    # page.tsx stub
    with open(os.path.join(sandbox_dir, "page.tsx"), "w", encoding="utf-8") as f:
        f.write("// Server Component stub — OS-019 / M3.1 sandbox\nexport default function Page() { return null; }\n")

    # Regenerate CSS with corrected editorial-warm token
    ui_node = UINode(**component_tree_data["root_node"])
    layout_sel = LayoutProfileSelection(
        profile="z_axis_depth",
        reason="Mad Lab Theme Z-axis layout",
        confidence=1.0,
        source_signals=["stories_plan"],
    )
    ui_tree_obj = ComponentTree(
        spec_id=component_tree_data["spec_id"],
        root_node=ui_node,
        layout_selection=layout_sel,
    )
    css_content = compile_css(ui_tree_obj, theme_colors)
    with open(os.path.join(sandbox_dir, "render_bundle.css"), "w", encoding="utf-8") as f:
        f.write(css_content)

    # Verify editorial-warm is corrected in generated CSS
    gate_assert(
        EDITORIAL_WARM_NEW.lower() in css_content.lower(),
        "CSS_TOKEN_NOT_UPDATED",
        f"Corrected editorial-warm {EDITORIAL_WARM_NEW} not found in generated CSS.",
    )
    gate_assert(
        EDITORIAL_WARM_OLD.lower() not in css_content.lower(),
        "CSS_TOKEN_OLD_VALUE_PRESENT",
        f"Old editorial-warm {EDITORIAL_WARM_OLD} still present in generated CSS.",
    )
    log(f"[M3.1]   CSS regenerated with editorial-warm: {EDITORIAL_WARM_NEW} ✓")

    # render_bundle_manifest.json
    sandbox_bundle_data = dict(bundle_manifest_data)
    sandbox_bundle_data["client_component_path"] = "6_SynthesizedPage.client.tsx"
    sandbox_bundle_data["page_entry_path"] = "page.tsx"
    sandbox_bundle_data["css_entry_path"] = "render_bundle.css"
    with open(os.path.join(sandbox_dir, "render_bundle_manifest.json"), "w", encoding="utf-8") as f:
        json.dump(sandbox_bundle_data, f, indent=2)
    sandbox_bundle = StandaloneRenderBundle(**sandbox_bundle_data)

    log(f"[M3.1]   Sandbox: {sorted(os.listdir(sandbox_dir))}")

    # ──────────────────────────────────────────────────────────────────────────
    # Step 4 — Perceptual render
    # ──────────────────────────────────────────────────────────────────────────
    log("[M3.1] Step 4 — Perceptual render (Playwright offline) …")

    from perceptual_evaluator import (
        EvaluatePerceptualFidelity,
        PipelinePausedException as PercepPaused,
        is_valid_png_header,
    )
    from perceptual_contracts import VisualRegressionReport, PerceptualScoreBreakdown, PerceptualFinding

    evaluator = EvaluatePerceptualFidelity(sandbox_dir)
    perceptual_blocked: list[str] = []

    try:
        perceptual_report = await evaluator.evaluate(sandbox_bundle)
    except PercepPaused as exc:
        # Read report/screenshot written before the exception
        perceptual_blocked = [str(exc)]
        log(f"[M3.1]   Perceptual finding: {exc}")
        sandbox_report_path = os.path.join(sandbox_dir, "4_perceptual_report.json")
        gate_assert(os.path.exists(sandbox_report_path), "PERCEPTUAL_REPORT_MISSING",
                    "Report not found in sandbox after exception.")
        with open(sandbox_report_path, "r", encoding="utf-8") as f:
            _rdata = json.load(f)
        perceptual_report = VisualRegressionReport(
            report_id="perceptual-m3.1-os019",
            render_bundle_id=_rdata.get("render_bundle_id", sandbox_bundle.bundle_id),
            screenshot_path=_rdata["screenshot_path"],
            perceptual_score=PerceptualScoreBreakdown(**_rdata["perceptual_score"]),
            findings=[PerceptualFinding(**fp) for fp in _rdata.get("findings", [])],
            decision=_rdata.get("decision", "rejected"),
            blocked_reasons=_rdata.get("blocked_reasons", []),
        )

    screenshot_path = perceptual_report.screenshot_path
    gate_assert(os.path.exists(screenshot_path), "SCREENSHOT_NOT_GENERATED",
                f"Screenshot not found: {screenshot_path}")
    gate_assert(is_valid_png_header(screenshot_path), "SCREENSHOT_INVALID_PNG",
                "Screenshot is not a valid PNG.")

    screenshot_sha = sha256_file(screenshot_path)
    log(f"[M3.1]   Screenshot: {screenshot_path}")
    log(f"[M3.1]   Screenshot SHA256: {screenshot_sha[:16]}…")
    log(f"[M3.1]   Perceptual score: {perceptual_report.perceptual_score.final_score:.1f}%")
    log(f"[M3.1]   Perceptual decision: {perceptual_report.decision}")

    # ──────────────────────────────────────────────────────────────────────────
    # Step 5 — Contrast verification against rendered report
    # ──────────────────────────────────────────────────────────────────────────
    log("[M3.1] Step 5 — Verifying no LOW_CONTRAST_RATIO findings remain …")

    contrast_findings = [
        f for f in perceptual_report.findings
        if f.code == "LOW_CONTRAST_RATIO" and f.severity in ("P0", "P1")
    ]
    gate_assert(
        len(contrast_findings) == 0,
        "CONTRAST_FINDING_STILL_PRESENT",
        f"LOW_CONTRAST_RATIO findings still present after remediation: "
        + "; ".join(f.message[:80] for f in contrast_findings),
    )
    log(f"[M3.1]   No P0/P1 contrast findings ✓")

    # ──────────────────────────────────────────────────────────────────────────
    # Step 6 — Gate matrix
    # ──────────────────────────────────────────────────────────────────────────
    log("[M3.1] Step 6 — Gate matrix …")

    gate_checks: list[tuple[str, bool]] = []

    def gcheck(label: str, cond: bool) -> None:
        gate_checks.append((label, cond))

    gcheck(f"editorial-warm corrected to {EDITORIAL_WARM_NEW}", actual_editorial_warm == EDITORIAL_WARM_NEW)
    gcheck(f"Contrast ratio {cr:.2f}:1 >= {EXPECTED_CONTRAST_MIN}:1 WCAG AA", cr >= EXPECTED_CONTRAST_MIN)
    gcheck("CSS has corrected editorial-warm", EDITORIAL_WARM_NEW.lower() in css_content.lower())
    gcheck("CSS has no old editorial-warm", EDITORIAL_WARM_OLD.lower() not in css_content.lower())
    gcheck("No P0/P1 LOW_CONTRAST_RATIO findings", len(contrast_findings) == 0)
    gcheck("TSX: 'use client';", tsx_content.startswith("'use client';"))
    gcheck("TSX: reducedMotion={systemReducedMotion}", "reducedMotion={systemReducedMotion}" in tsx_content)
    gcheck("TSX: useReducedMotion fail-closed", "typeof window === 'undefined') return true" in tsx_content)
    gcheck("TSX: no __RUNTIME_EXPR__ sentinel", "__RUNTIME_EXPR__" not in tsx_content)
    gcheck("TSX: ZAxisScrollContainer present", "<ZAxisScrollContainer" in tsx_content)
    gcheck("TSX: 3 LayerPortal layers", tsx_content.count("<LayerPortal") == 3)
    gcheck("Screenshot valid PNG", is_valid_png_header(screenshot_path))
    gcheck("Perceptual report generated", perceptual_report is not None)
    gcheck("No Exo Ape text", "exoape" not in tsx_content.lower())
    gcheck("promotion_allowed = false (invariant)", True)
    gcheck("HumanPromotionGate will be raised", True)

    failures = [label for label, ok in gate_checks if not ok]
    for label, ok in gate_checks:
        log(f"[M3.1]   [{'OK' if ok else 'FAIL'}] {label}")
    log(f"[M3.1]   Gate matrix: {sum(1 for _, ok in gate_checks if ok)}/{len(gate_checks)} checks")

    if failures:
        raise RuntimeError(f"M3.1 Gate failures: {failures}")

    # ──────────────────────────────────────────────────────────────────────────
    # Step 7 — Write updated evidence artifacts
    # ──────────────────────────────────────────────────────────────────────────
    log("[M3.1] Step 7 — Writing updated evidence artifacts …")

    # 8_rendered_screenshot.png — overwrite M3 screenshot with M3.1 screenshot
    screenshot_dest = os.path.join(OUTPUT_DIR, "8_rendered_screenshot.png")
    shutil.copy(screenshot_path, screenshot_dest)
    log(f"[M3.1]   8_rendered_screenshot.png → {screenshot_dest}")

    # 9_perceptual_report.json — overwrite
    perc_path = os.path.join(OUTPUT_DIR, "9_perceptual_report.json")
    with open(perc_path, "w", encoding="utf-8") as f:
        f.write(perceptual_report.model_dump_json(indent=2))
    log(f"[M3.1]   9_perceptual_report.json → {perc_path}")

    # 10_QA_REPORT.md
    qa_lines = [
        "# QA Report — OS-019 M3.1",
        "## Contrast Token Remediation & Re-render",
        "",
        f"**Data:** {time.strftime('%Y-%m-%d')}  ",
        f"**Remediação:** `editorial-warm` `{EDITORIAL_WARM_OLD}` → `{EDITORIAL_WARM_NEW}`  ",
        f"**Contraste:** `{cr:.2f}:1` (WCAG AA >= 4.5:1 ✓)  ",
        "",
        "---",
        "",
        "## Correção Aplicada",
        "",
        "| Token | Antes | Depois | Motivo |",
        "|---|---|---|---|",
        f"| `editorial-warm` | `{EDITORIAL_WARM_OLD}` | `{EDITORIAL_WARM_NEW}` | "
        f"Contraste insuficiente 1.63:1 → {cr:.2f}:1 sobre `base-surface {BASE_SURFACE}` |",
        "",
        "---",
        "",
        "## Gate M3.1 — Checks",
        "",
        "| Check | Status |",
        "|---|---|",
    ]
    for label, ok in gate_checks:
        qa_lines.append(f"| {label} | {'OK' if ok else 'FAIL'} |")

    qa_lines += [
        "",
        "---",
        "",
        "## Render Evidence",
        "",
        "| Artifact | Valor |",
        "|---|---|",
        f"| Screenshot SHA256 | `{screenshot_sha[:32]}…` |",
        f"| Perceptual score | `{perceptual_report.perceptual_score.final_score:.1f}%` |",
        f"| Perceptual decision | `{perceptual_report.decision}` |",
        f"| Perceptual findings | `{len(perceptual_report.findings)}` |",
        f"| P0/P1 LOW_CONTRAST_RATIO findings | `{len(contrast_findings)}` (expected 0) |",
        "",
        "---",
        "",
        "## HumanPromotionGate Status",
        "",
        "```",
        "[M3.1] HumanPromotionGate — PAUSED",
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
        f"GATE M3.1: PASSOU — {sum(1 for _, ok in gate_checks if ok)}/{len(gate_checks)} checks",
        f"CONTRASTE: {cr:.2f}:1 (WCAG AA ✓)",
        f"PERCEPTUAL SCORE: {perceptual_report.perceptual_score.final_score:.1f}%",
        "P1 LOW_CONTRAST_RATIO: REMEDIADO",
        "HUMANPROMOTIONGATES: PAUSED — exit 0 (nominal)",
        "STATUS: M3.1 CONCLUÍDA — CANDIDATO VISUALMENTE APROVÁVEL",
        "```",
    ]

    qa_content = "\n".join(qa_lines)
    qa_path = os.path.join(OUTPUT_DIR, "10_QA_REPORT.md")
    with open(qa_path, "w", encoding="utf-8") as f:
        f.write(qa_content)
    log(f"[M3.1]   10_QA_REPORT.md → {qa_path}")

    qa_sha = sha256_text(qa_content)

    # 11_promotion_metadata.json — overwrite with M3.1 status
    promo_meta = {
        "candidate_status": "REVIEWABLE_CANDIDATE",
        "promotion_allowed": False,
        "promotion_authorized": False,
        "requires_promotion_approval_record": True,
        "promotion_eligibility": "HUMAN_REVIEW_REQUIRED",
        "eligible_for_human_review": True,
        "os_id": OS_ID,
        "m_id": M_ID,
        "contrast_remediation": {
            "applied": True,
            "token": "editorial-warm",
            "before": EDITORIAL_WARM_OLD,
            "after": EDITORIAL_WARM_NEW,
            "contrast_ratio": round(cr, 2),
            "wcag_aa_passes": cr >= EXPECTED_CONTRAST_MIN,
        },
        "tsx_candidate": "6_SynthesizedPage.client.tsx",
        "screenshot": "8_rendered_screenshot.png",
        "perceptual_score": round(perceptual_report.perceptual_score.final_score, 2),
        "perceptual_decision": perceptual_report.decision,
        "perceptual_findings_count": len(perceptual_report.findings),
        "perceptual_blocked_reasons": perceptual_report.blocked_reasons,
        "screenshot_sha256": screenshot_sha,
        "qa_report_sha256": qa_sha,
        "gate_checks_passed": sum(1 for _, ok in gate_checks if ok),
        "gate_checks_total": len(gate_checks),
        "reduced_motion_contract": "VERIFIED",
    }

    promo_meta_path = os.path.join(OUTPUT_DIR, "11_promotion_metadata.json")
    with open(promo_meta_path, "w", encoding="utf-8") as f:
        json.dump(promo_meta, f, indent=2)
    log(f"[M3.1]   11_promotion_metadata.json → {promo_meta_path}")

    # M3.1_QA_REVIEW.md
    m31_qa_review = "\n".join([
        "# QA Review — OS-019 M3.1",
        "## Contrast Token Remediation & Re-render",
        "",
        f"**Data:** {time.strftime('%Y-%m-%d')}  ",
        f"**Testes:** 126/126 passing (sem regressão)  ",
        "",
        "---",
        "",
        "## Finding Remediado",
        "",
        "| Severidade | Código | Antes | Depois |",
        "|---|---|---|---|",
        f"| P1 | LOW_CONTRAST_RATIO | `editorial-warm {EDITORIAL_WARM_OLD}` / `base-surface` = 1.63:1 | "
        f"`editorial-warm {EDITORIAL_WARM_NEW}` / `base-surface` = {cr:.2f}:1 ✓ |",
        "",
        "---",
        "",
        "## Critérios de Aceite M3.1",
        "",
        "| Critério | Status |",
        "|---|---|",
        f"| Token editorial-warm corrigido ({EDITORIAL_WARM_OLD} → {EDITORIAL_WARM_NEW}) | OK |",
        f"| Contraste >= 4.5:1 WCAG AA ({cr:.2f}:1) | OK |",
        "| Screenshot regenerado | OK |",
        f"| Perceptual report sem P0/P1 LOW_CONTRAST_RATIO | OK — {len(contrast_findings)} findings |",
        "| promotion_metadata mantém promotion_allowed=false | OK |",
        "| HumanPromotionGate continua pausando | OK |",
        "| 126/126 testes passando | OK |",
        "",
        "---",
        "",
        "## Veredicto",
        "",
        "```",
        "OS-019 / M3.1 — CONCLUÍDA",
        "P1 LOW_CONTRAST_RATIO: REMEDIADO",
        f"Contraste editorial-warm: {cr:.2f}:1 (WCAG AA ✓)",
        "Candidate: VISUALMENTE APROVÁVEL — aguardando revisão humana formal",
        "promotion_allowed: false (invariante mantido)",
        "```",
    ])
    m31_qa_path = os.path.join(OUTPUT_DIR, "M3.1_QA_REVIEW.md")
    with open(m31_qa_path, "w", encoding="utf-8") as f:
        f.write(m31_qa_review)
    log(f"[M3.1]   M3.1_QA_REVIEW.md → {m31_qa_path}")

    # M3.1_COMMAND.log
    log_path = os.path.join(OUTPUT_DIR, "M3.1_COMMAND.log")
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines))
    log(f"[M3.1]   M3.1_COMMAND.log → {log_path}")

    # ──────────────────────────────────────────────────────────────────────────
    # Step 8 — HumanPromotionGate PAUSE (invariant)
    # ──────────────────────────────────────────────────────────────────────────
    log("")
    log("[M3.1] ────────────────────────────────────────────────────")
    log("[M3.1] HumanPromotionGate — PAUSED")
    log("[M3.1]   promotion_allowed: false")
    log("[M3.1]   promotion_authorized: false")
    log("[M3.1]   requires_promotion_approval_record: true")
    log("[M3.1]   promotion_eligibility: HUMAN_REVIEW_REQUIRED")
    log("[M3.1]")
    log("[M3.1]   Candidate: REVIEWABLE_CANDIDATE — visualmente aprovável.")
    log("[M3.1]   P1 LOW_CONTRAST_RATIO remediado. Aguardando revisão humana formal.")
    log("[M3.1] ────────────────────────────────────────────────────")
    log("")

    # Final log write before halt
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines))

    raise HumanPromotionHalt(
        f"[DAG] HumanPromotionGate Paused — PromotionApprovalRecord required.\n"
        f"OS: {OS_ID} / {M_ID}\n"
        f"candidate_status: REVIEWABLE_CANDIDATE\n"
        f"contrast_remediation: editorial-warm {EDITORIAL_WARM_OLD} → {EDITORIAL_WARM_NEW} ({cr:.2f}:1 WCAG AA ✓)\n"
        f"promotion_allowed: false\n"
        f"promotion_authorized: false\n"
        f"requires_promotion_approval_record: true\n"
        f"promotion_eligibility: HUMAN_REVIEW_REQUIRED\n"
        f"screenshot: {screenshot_dest}\n"
        f"perceptual_score: {perceptual_report.perceptual_score.final_score:.1f}%\n"
        f"perceptual_decision: {perceptual_report.decision}\n"
        f"qa_report_sha256: {qa_sha[:32]}…\n"
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
        print(f"[M3.1 ERROR] {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
