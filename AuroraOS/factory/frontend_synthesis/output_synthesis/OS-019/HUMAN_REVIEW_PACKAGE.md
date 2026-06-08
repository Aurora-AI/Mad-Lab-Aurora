# Human Review Package — OS-019
## Mad Lab Theme — Z-Axis Tunnel Candidate

**Status:** `REVIEWABLE_CANDIDATE`  
**Data de geração:** 2026-06-08  
**Branch:** `feature/purga-debt-001`  
**Commits:** `dac1015` (M2) → `7bff08c` (M3) → `54a0fe0` (M3.1)  

---

## ⚠️ Instrução de Promoção

```
promotion_allowed: false
promotion_authorized: false
requires_promotion_approval_record: true
promotion_eligibility: HUMAN_REVIEW_REQUIRED
```

**Nenhuma promoção ocorreu. Nenhuma escrita em produção.  
Este documento é o pacote para revisão humana formal.**

Para promover, criar `PromotionApprovalRecord` em:
```
C:/Projetos/Aurora/.aurora/approvals/promotion_approval.json
```

---

## Candidato: O que está sendo revisado

O candidato é a primeira materialização física da **Mad Lab Theme** com **física de túnel Z-axis**.

Conceito: o usuário não rola uma página — ele atravessa um organismo. O scroll é convertido em progressão de profundidade Z (3000 unidades). Três LayerPortals ancoram o conteúdo em planos distintos do espaço tridimensional.

**Não há texto, assets ou marca Exo Ape.** Exo Ape fornece a gramática. Mad Lab cria a física.

---

## Screenshot

**Arquivo:** `8_rendered_screenshot.png`  
**SHA256:** `07900d7f47c2ab00aa37128f2b5af693b17ba148537ee236ca0e60dba7965074`  
**Viewport:** 1440×900 — Playwright offline  
**Gerado por:** Playwright headless, `context.offline=True`, sem rede  

---

## Estrutura do Candidato

| Componente | Z-Position | Scale | Opacity | Conteúdo |
|---|---|---|---|---|
| `ZAxisScrollContainer` | root | — | — | Tunnel engine — converte scroll em profundidade |
| `LayerPortal` (hero) | z=0 | 1.0 | 1.0 | "Mad Lab Aurora" + CTA "Explorar o Sistema" |
| `LayerPortal` (mid) | z=-800 | 0.85 | 0.8 | "A fábrica cognitiva que materializa produto..." |
| `LayerPortal` (horizon) | z=-2000 | 0.6 | 0.5 | "Depth Horizon — Aurora Factory" |

**Física:** scroll input → `translate3d(0,0,z)` via rAF lerp (0.08). GPU-only transforms.

---

## Contratos de Acessibilidade

### prefers-reduced-motion
| Contrato | Status |
|---|---|
| Mecanismo | `useReducedMotion()` hook — lê `prefers-reduced-motion` do sistema |
| Fail-closed | `true` quando SSR ou `window` indisponível (sem motion) |
| Reatividade | Responde a mudanças do sistema em runtime |
| Passthrough | `reducedMotion={systemReducedMotion}` em `ZAxisScrollContainer` e `LayerPortal` (×3) |
| Compilação | Sentinel `__RUNTIME_EXPR__:systemReducedMotion` → expressão JSX `{systemReducedMotion}` |
| Fallback | `fallback="static_depth_sections"` — sem transforms em caso de reduced-motion |

### Contraste de Cores (WCAG AA)
| Token | Valor | Sobre | Contraste | Status |
|---|---|---|---|---|
| `text-primary` | `#0A0A0A` | `base-surface #FAFAF8` | ~19:1 | ✓ |
| `text-secondary` | `#555555` | `base-surface #FAFAF8` | ~7.2:1 | ✓ |
| `editorial-warm` | `#7A6A52` *(corrigido M3.1)* | `base-surface #FAFAF8` | 5.01:1 | ✓ |

---

## Perceptual QA

| Métrica | Valor |
|---|---|
| Score final | **89.4%** |
| Decisão | **approved** |
| Blocked reasons | 0 |
| Structural similarity | 100% |
| Contrast score | 100% |
| Layout integrity | 100% |
| Viewport fit | 100% |

### Findings

| Severidade | Código | Mensagem | Interpretação |
|---|---|---|---|
| P2 | `LOW_VISUAL_DENSITY` | Densidade visual baixa (0.005 < 0.015) | **Intencional.** Layout Z-axis de profundidade editorial usa espaço negativo como gramática. Não é um erro — é a física. |

---

## Gate Matrix Consolidado

| Micro-etapa | Gates | Status |
|---|---|---|
| M0 — FX Components | Rules of Hooks, ZAxisScrollContainer, LayerPortal | APROVADA APÓS CORREÇÃO |
| M1 — Blueprint + BuildPlan | StoriesBuilderGate (0 P0/P1), Z-axis capabilities, NO_EXOAPE_SURFACE_CLONE | APROVADA |
| M2 — ComponentTree + TSX | 16/16 checks, 114/114 tests, reducedMotion contract | APROVADA |
| M3 — Render + Perceptual | 24/24 checks, screenshot PNG válido, HumanPromotionGate paused | CONCLUÍDA TECNICAMENTE |
| M3.1 — Contrast Remediation | 16/16 checks, editorial-warm 5.01:1, perceptual: approved | CONCLUÍDA / P1 REMEDIADO |

---

## Testes

```
126/126 passing — zero regressão
Suíte: AuroraOS/factory (excluindo sandbox)
```

---

## Artefatos Físicos

| Arquivo | Micro-etapa | Conteúdo |
|---|---|---|
| `1_blueprint.json` | M1 | ExperienceBlueprint — canvas_navigation, freeform_depth, exoape in rationale |
| `2_build_plan.json` | M1 | StoriesBuildPlan — 11 capabilities, 12 constraints |
| `3_gate_report.json` | M1 | StoriesBuilderGateReport — status: passed, 0 P0/P1 |
| `4_code_spec.json` | M2/M3.1 | FrontendCodeSpec — 8 color tokens, Space Grotesk, editorial-warm corrigido |
| `5_component_tree.json` | M2 | ComponentTree — ZAxisScrollContainer + 3 LayerPortals |
| `6_SynthesizedPage.client.tsx` | M2 | TSX candidate — 61 linhas, useReducedMotion fail-closed |
| `7_render_bundle_manifest.json` | M2 | StandaloneRenderBundle manifest |
| `8_rendered_screenshot.png` | M3.1 | **Screenshot final** — Playwright offline 1440×900 |
| `9_perceptual_report.json` | M3.1 | Perceptual report — approved, score 89.4% |
| `10_QA_REPORT.md` | M3.1 | QA evidence consolidado |
| `11_promotion_metadata.json` | M3.1 | promotion_allowed=false, promotion_authorized=false |
| `12_candidate_manifest.json` | M3 | Candidate manifest — física Z-axis + acessibilidade |
| `M2_QA_REPORT.md` | M2 | Gate M2 — 16/16 checks |
| `M3_QA_REVIEW.md` | M3 | Gate M3 — 24/24 checks |
| `M3.1_QA_REVIEW.md` | M3.1 | Gate M3.1 — 16/16 checks, P1 remediado |

---

## Decisão Pendente

O revisor humano deve:

1. **Verificar `8_rendered_screenshot.png`** — o túnel Z-axis renderizou corretamente? As 3 camadas estão presentes? A tipografia está legível?

2. **Aceitar P2 `LOW_VISUAL_DENSITY` como intencional?** O espaço negativo é a física do layout. Se não for intencional para o contexto final, o conteúdo das camadas pode ser expandido.

3. **Aceitar a física de fallback?** Quando `prefers-reduced-motion` está ativo, o layout cai para `static_depth_sections` — sem transforms, sem Z-axis. O layout estático também precisa de validação visual.

4. **Se aprovado:** criar `PromotionApprovalRecord` com os hashes abaixo.

### Hashes para PromotionApprovalRecord

```json
{
  "screenshot_sha256": "07900d7f47c2ab00aa37128f2b5af693b17ba148537ee236ca0e60dba7965074",
  "qa_report_sha256":  "6c509506a5193ea4280a9469050b16dbe0406c493fd263d7ffb8de15cc70969e",
  "approved_by": "<nome do revisor>",
  "approval_source": "signed_file"
}
```

---

## Status Canônico Final

```
OS-019 — CANDIDATO REVISÁVEL GERADO
Física: Z-axis tunnel, 3 layers, fail-closed reduced-motion
Contraste: WCAG AA compliant (editorial-warm 5.01:1)
Perceptual: approved, 89.4%
Promoção: BLOQUEADA — aguardando PromotionApprovalRecord
HumanPromotionGate: PAUSED
promotion_allowed: false
promotion_authorized: false
```
