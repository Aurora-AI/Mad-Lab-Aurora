# QA Report — OS-019 M2
## FrontendCodeSpec + ComponentTree Z-axis + TSX Candidate

**Data:** 2026-06-08  
**Commit:** `dac1015` (feature/purga-debt-001)  
**Testes:** 114/114 passing (108 anteriores + 6 novos M2)

---

## Gate M2 — 16/16 Checks

| Check | Status |
|---|---|
| TSX tem `'use client';` | OK |
| TSX tem `function useReducedMotion` | OK |
| TSX tem `prefers-reduced-motion` no hook | OK |
| TSX declara `systemReducedMotion = useReducedMotion()` | OK |
| TSX passa `reducedMotion={systemReducedMotion}` | OK |
| TSX importa React | OK |
| TSX importa ZAxisScrollContainer de `@/components/fx` | OK |
| TSX importa LayerPortal de `@/components/fx` | OK |
| TSX sem import orfao de ZAxisScrollContainer em core | OK |
| TSX sem import orfao de LayerPortal em core | OK |
| TSX sem texto/marca Exo Ape | OK |
| TSX renderiza `<ZAxisScrollContainer` | OK |
| TSX renderiza `<LayerPortal` | OK |
| TSX passa `fallback="static_depth_sections"` | OK |
| TSX passa `performanceBudget` | OK |
| TSX sem sentinel bruto `__RUNTIME_EXPR__` | OK |

---

## Criterios de Aceite da OS

| Criterio | Status |
|---|---|
| M1 artifacts lidos como fonte (nao recriados) | OK — hash verificado |
| source_blueprint_hash integro | OK — `ba6fd079a911...` |
| FrontendCodeSpec com Mad Lab Theme | OK — 8 color tokens, Space Grotesk |
| ComponentTree com ZAxisScrollContainer | OK — root node |
| ComponentTree com LayerPortal | OK — 3 layers (z=0, -800, -2000) |
| Z-axis capabilities presentes e rastreadas | OK — herdadas do BuildPlan M1 |
| reducedMotion de prefers-reduced-motion | OK — via useReducedMotion hook, fail-closed |
| performanceBudget presente | OK — `{targetFps: 60, maxLayers: 8}` |
| mobile fallback presente | OK — `fallback="static_depth_sections"` |
| reduced-motion fallback presente | OK — retorna true em SSR, desabilita transforms |
| TSX sem import orfao | OK |
| TSX sem violacao Rules of Hooks | OK — hook antes de qualquer return |
| Sem texto/asset/marca Exo Ape | OK |
| 114/114 testes passando | OK |
| QA M2 rodado | OK — este documento |

---

## Novos Testes Adicionados (M2)

| Teste | Verifica |
|---|---|
| `test_tsx_compiler_fx_emits_use_client_directive` | `'use client';` ao topo |
| `test_tsx_compiler_fx_emits_use_reduced_motion_hook` | hook + prefers-reduced-motion |
| `test_tsx_compiler_fx_emits_react_import` | import React presente |
| `test_tsx_compiler_no_use_client_without_fx` | sem FX = sem 'use client' |
| `test_tsx_compiler_runtime_expression_sentinel_emits_jsx_expression` | `{systemReducedMotion}` emitido |
| `test_tsx_compiler_runtime_expression_does_not_affect_non_sentinel_props` | props normais nao afetados |

---

## Evidencias Fisicas

| Arquivo | Conteudo |
|---|---|
| `1_blueprint.json` | ExperienceBlueprint Mad Lab Theme |
| `2_build_plan.json` | StoriesBuildPlan — 11 caps, 12 constraints |
| `3_gate_report.json` | StoriesBuilderGateReport — status passed |
| `4_code_spec.json` | FrontendCodeSpec — 8 tokens, 5 components |
| `5_component_tree.json` | ComponentTree — ZAxisScrollContainer + 3 LayerPortals |
| `6_SynthesizedPage.client.tsx` | TSX candidate — 61 linhas |
| `7_render_bundle_manifest.json` | StandaloneRenderBundle manifest |

---

## Veredicto

```
GATE M2: PASSOU — 16/16 checks
TESTES: 114/114 passing
COMMIT: dac1015 pushed
STATUS: M2 CONCLUIDA / APROVADA
```

---

## Fora de Escopo (para M3 / HumanPromotionGate)

- Render final / screenshot perceptual
- HumanPromotionGate / PromotionCandidate
- promotion_metadata
- Push de OS-019 final
