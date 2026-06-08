# QA Review — OS-019 M3
## Rendered Candidate Certification + HumanPromotionGate

**Data:** 2026-06-08  
**Pipeline:** TSX Candidate → Render Sandbox → Playwright Screenshot → Perceptual QA → SandboxGate → HumanPromotionGate  
**Testes:** 126/126 passing (suíte completa da fábrica — sem regressão)

---

## Gate M3 — 24/24 Checks

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

| Artifact | Valor |
|---|---|
| Screenshot | `8_rendered_screenshot.png` (PNG real, Playwright offline 1440x900) |
| Screenshot SHA256 | `2e3a9dd4393b82d4…` |
| Perceptual score | `86.9%` |
| Perceptual decision | `rejected` |
| Perceptual findings | 2 (P2: LOW_VISUAL_DENSITY, P1: LOW_CONTRAST_RATIO) |

---

## Perceptual Findings Registrados

| Severidade | Código | Mensagem |
|---|---|---|
| P2 | LOW_VISUAL_DENSITY | Densidade visual baixa (0.0054 < 0.015) — esperado para layout Z-axis minimal |
| P1 | LOW_CONTRAST_RATIO | Contraste insuficiente no `<div>` Depth Horizon: `#D4C5A9` (`editorial-warm`) sobre `#FAFAF8` (`base-surface`) — 1.6:1. Mínimo WCAG AA: 4.5:1 |

**Interpretação:**  
- `LOW_VISUAL_DENSITY` é esperado para um layout Z-axis de profundidade editorial — a física de túnel intenciona espaço negativo.  
- `LOW_CONTRAST_RATIO` é um finding legítimo de acessibilidade: o token `editorial-warm` (`#D4C5A9`) foi projetado para uma superfície escura (tema dark). Na Mad Lab Theme light editorial (`base-surface: #FAFAF8`), o contraste é insuficiente. Este finding deve ser avaliado na revisão humana.

---

## Contrato Reduced-Motion

| Check | Status |
|---|---|
| useReducedMotion hook presente | OK |
| prefers-reduced-motion referenciado | OK |
| Fail-closed (SSR retorna true) | OK |
| reducedMotion={systemReducedMotion} em ZAxisScrollContainer | OK |
| reducedMotion={systemReducedMotion} em LayerPortal (×3) | OK |
| Sem reducedMotion={false} hardcoded | OK |
| Sem sentinel __RUNTIME_EXPR__ bruto no output | OK |

---

## HumanPromotionGate Status

```
[M3] HumanPromotionGate — PAUSED
promotion_allowed: false
promotion_authorized: false
requires_promotion_approval_record: true
promotion_eligibility: HUMAN_REVIEW_REQUIRED
candidate_status: REVIEWABLE_CANDIDATE
exit: 0 (halt is nominal, not failure)
```

---

## Critérios de Aceite da M3

| Critério | Status |
|---|---|
| Screenshot real gerado (não placeholder) | OK — Playwright offline, arquivo PNG válido |
| Perceptual QA executado | OK — score 86.9%, 2 findings registrados |
| promotion_metadata.json com promotion_allowed=false | OK |
| promotion_metadata.json com promotion_authorized=false | OK |
| promotion_metadata.json com requires_promotion_approval_record=true | OK |
| promotion_metadata.json com promotion_eligibility=HUMAN_REVIEW_REQUIRED | OK |
| HumanPromotionGate levantado (pausa nominal) | OK — exit 0 |
| reducedMotion sobrevive até o render | OK — sentinel compilado, hook emitido |
| 12 artifacts de evidência escritos | OK |
| 126 testes sem regressão | OK |

---

## Evidências Físicas

| Arquivo | Conteúdo |
|---|---|
| `1_blueprint.json` | ExperienceBlueprint Mad Lab Theme (M1) |
| `2_build_plan.json` | StoriesBuildPlan — 11 caps, 12 constraints (M1) |
| `3_gate_report.json` | StoriesBuilderGateReport — status passed (M1) |
| `4_code_spec.json` | FrontendCodeSpec — 8 color tokens, Space Grotesk (M2) |
| `5_component_tree.json` | ComponentTree — ZAxisScrollContainer + 3 LayerPortals (M2) |
| `6_SynthesizedPage.client.tsx` | TSX candidate — 61 linhas, reducedMotion fail-closed (M2) |
| `7_render_bundle_manifest.json` | StandaloneRenderBundle manifest (M2) |
| `8_rendered_screenshot.png` | Screenshot Playwright offline 1440×900 (M3) |
| `9_perceptual_report.json` | Perceptual regression report — 2 findings (M3) |
| `10_QA_REPORT.md` | QA evidence 24/24 checks (M3) |
| `11_promotion_metadata.json` | Promotion metadata — promotion_allowed=false (M3) |
| `12_candidate_manifest.json` | Candidate manifest completo (M3) |
| `M3_COMMAND.log` | Log de execução do pipeline M3 (M3) |

---

## Veredicto

```
GATE M3: PASSOU — 24/24 checks
SCREENSHOT: gerado e validado PNG (Playwright offline)
PERCEPTUAL SCORE: 86.9%
PERCEPTUAL DECISION: rejected (P1: LOW_CONTRAST_RATIO — para revisão humana)
TESTES: 126/126 passing
HUMANPROMOTIONGATES: PAUSED — exit 0 (nominal)
STATUS: M3 CONCLUÍDA — REVIEWABLE_CANDIDATE
```

---

## Observação para Revisão Humana

O candidato está **revisável** (`REVIEWABLE_CANDIDATE`). Para promoção, o revisor deve:

1. Verificar o screenshot `8_rendered_screenshot.png` — túnel Z-axis renderizado, 3 camadas de profundidade
2. Avaliar o finding P1 `LOW_CONTRAST_RATIO`: o token `editorial-warm` precisa de ajuste para a surface light editorial  
   - Sugestão: `editorial-warm: #7A6A52` (contraste ~5.2:1 sobre `#FAFAF8`) preservando o caráter quente
3. Se aprovado: criar `PromotionApprovalRecord` em `C:/Projetos/Aurora/.aurora/approvals/promotion_approval.json`

**Promoção automática: proibida. Merge automático: proibido.**
