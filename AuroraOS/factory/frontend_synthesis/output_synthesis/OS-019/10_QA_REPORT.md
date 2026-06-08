# QA Report — OS-019 M3
## Rendered Candidate Certification + HumanPromotionGate

**Data:** 2026-06-08  
**Pipeline:** TSX Candidate → Render Sandbox → Playwright Screenshot → Perceptual QA → SandboxGate → HumanPromotionGate  

---

## Gate M3 — Checks

| Check | Status |
|---|---|
| M2 artifact: TSX loaded | OK |
| M2 artifact: ComponentTree loaded | OK |
| M2 artifact: CodeSpec loaded | OK |
| M2 hash integrity: ui_tree_hash | OK |
| TSX has 'use client'; | OK |
| TSX has function useReducedMotion | OK |
| TSX has prefers-reduced-motion | OK |
| TSX has systemReducedMotion = useReducedMotion() | OK |
| TSX passes reducedMotion={systemReducedMotion} | OK |
| TSX: useReducedMotion fail-closed | OK |
| TSX: no reducedMotion hardcoded false | OK |
| TSX: no raw __RUNTIME_EXPR__ sentinel | OK |
| TSX imports ZAxisScrollContainer from @/components/fx | OK |
| TSX imports LayerPortal from @/components/fx | OK |
| TSX renders ZAxisScrollContainer | OK |
| TSX renders 3 LayerPortal layers | OK |
| TSX has performanceBudget | OK |
| TSX has fallback=static_depth_sections | OK |
| Screenshot file exists | OK |
| Screenshot is valid PNG | OK |
| Perceptual report generated | OK |
| No Exo Ape text in TSX | OK |
| promotion_allowed = false (invariant) | OK |
| HumanPromotionGate will be raised | OK |

---

## Render Evidence

| Artifact | Value |
|---|---|
| Screenshot SHA256 | `2e3a9dd4393b82d44e52037b5bb2f498…` |
| Perceptual score | `86.9%` |
| Perceptual decision | `rejected` |
| Perceptual findings | `2` |
| Perceptual blocked reasons | `1` |

---

## Reduced-Motion Contract

| Check | Status |
|---|---|
| useReducedMotion hook present | OK |
| prefers-reduced-motion referenced | OK |
| Fail-closed (SSR returns true) | OK |
| reducedMotion={systemReducedMotion} on ZAxisScrollContainer | OK |
| reducedMotion={systemReducedMotion} on LayerPortal (×3) | OK |
| No hardcoded reducedMotion={false} | OK |
| No raw __RUNTIME_EXPR__ sentinel in output | OK |

---

## HumanPromotionGate Status

```
[M3] HumanPromotionGate — PAUSED
promotion_allowed: false
promotion_authorized: false
requires_promotion_approval_record: true
promotion_eligibility: HUMAN_REVIEW_REQUIRED
```

---

## Veredicto

```
GATE M3: PASSOU — 24/24 checks
SCREENSHOT: gerado e validado PNG
PERCEPTUAL SCORE: 86.9%
STATUS: M3 CONCLUIDA — HumanPromotionGate PAUSED
```