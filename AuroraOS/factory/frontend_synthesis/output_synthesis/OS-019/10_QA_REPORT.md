# QA Report — OS-019 M3.1
## Contrast Token Remediation & Re-render

**Data:** 2026-06-08  
**Remediação:** `editorial-warm` `#D4C5A9` → `#7A6A52`  
**Contraste:** `5.01:1` (WCAG AA >= 4.5:1 ✓)  

---

## Correção Aplicada

| Token | Antes | Depois | Motivo |
|---|---|---|---|
| `editorial-warm` | `#D4C5A9` | `#7A6A52` | Contraste insuficiente 1.63:1 → 5.01:1 sobre `base-surface #FAFAF8` |

---

## Gate M3.1 — Checks

| Check | Status |
|---|---|
| editorial-warm corrected to #7A6A52 | OK |
| Contrast ratio 5.01:1 >= 4.5:1 WCAG AA | OK |
| CSS has corrected editorial-warm | OK |
| CSS has no old editorial-warm | OK |
| No P0/P1 LOW_CONTRAST_RATIO findings | OK |
| TSX: 'use client'; | OK |
| TSX: reducedMotion={systemReducedMotion} | OK |
| TSX: useReducedMotion fail-closed | OK |
| TSX: no __RUNTIME_EXPR__ sentinel | OK |
| TSX: ZAxisScrollContainer present | OK |
| TSX: 3 LayerPortal layers | OK |
| Screenshot valid PNG | OK |
| Perceptual report generated | OK |
| No Exo Ape text | OK |
| promotion_allowed = false (invariant) | OK |
| HumanPromotionGate will be raised | OK |

---

## Render Evidence

| Artifact | Valor |
|---|---|
| Screenshot SHA256 | `07900d7f47c2ab00aa37128f2b5af693…` |
| Perceptual score | `89.4%` |
| Perceptual decision | `approved` |
| Perceptual findings | `1` |
| P0/P1 LOW_CONTRAST_RATIO findings | `0` (expected 0) |

---

## HumanPromotionGate Status

```
[M3.1] HumanPromotionGate — PAUSED
promotion_allowed: false
promotion_authorized: false
requires_promotion_approval_record: true
promotion_eligibility: HUMAN_REVIEW_REQUIRED
```

---

## Veredicto

```
GATE M3.1: PASSOU — 16/16 checks
CONTRASTE: 5.01:1 (WCAG AA ✓)
PERCEPTUAL SCORE: 89.4%
P1 LOW_CONTRAST_RATIO: REMEDIADO
HUMANPROMOTIONGATES: PAUSED — exit 0 (nominal)
STATUS: M3.1 CONCLUÍDA — CANDIDATO VISUALMENTE APROVÁVEL
```