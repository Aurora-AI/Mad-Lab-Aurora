# OS-019 — Stories Builder First Real Product Candidate
## Ordem de Serviço Aurora v9.0

**ID:** `OS-MADLAB-OS019-STORIES-BUILDER-FIRST-REAL-PRODUCT-CANDIDATE-20260608`  
**Domínio:** Mad Lab Aurora / Frontend Synthesis  
**Risco:** Alto  
**Status Alvo:** `REVIEWABLE_CANDIDATE`  
**Data de Criação:** 2026-06-08  
**Pré-requisito:** `OS-MADLAB-OS019-M0` — CONCLUÍDA / APROVADA APÓS CORREÇÃO CRÍTICA

---

## Contexto

A OS-019-M0 ensinou ao sistema a física do Mad Lab Theme.
O StoriesBuilderGate está ativo, os FX components estão corrigidos (Rules of Hooks — commit 5e562de),
os contratos canônicos existem e os 108 testes passam.

Esta OS executa pela primeira vez o pipeline completo com parâmetros reais,
usando `exoape.com` como referência de gramática — não como template de clone.
O resultado é um candidato `REVIEWABLE_CANDIDATE` pausado no `HumanPromotionGate`.

**Promoção automática é proibida.**  
**Nenhum candidato sai desta OS sem revisão humana explícita.**

---

## Parâmetros Canônicos

```
Reference:            https://www.exoape.com/
Theme:                Mad Lab Theme
Core physics:         Z-axis tunnel progression
Surface:              landing
Navigation:           canvas_navigation
Motion:               kinetic_field
Spatial:              freeform_depth
Status alvo:          REVIEWABLE_CANDIDATE
promotion_allowed:    false
promotion_authorized: false
```

---

## Contratos Físicos Verificados (Anti-Alucinação)

| Contrato | Caminho | Status |
|---|---|---|
| `ExperienceBlueprint` | `contracts/experience_architecture_contracts.py` | Verificado |
| `NavigationStrategy.CANVAS_NAVIGATION` | `experience_architecture_contracts.py:13` | Verificado |
| `SpatialStrategy.FREEFORM_DEPTH` | `experience_architecture_contracts.py:29` | Verificado |
| `MotionStrategy.KINETIC_FIELD` | `experience_architecture_contracts.py:22` | Verificado |
| `BuildPlanResolver.resolve_build_plan()` | `stories_builder/build_plan_resolver.py:55` | Verificado |
| `StoriesBuilderGate.validate_build_plan()` | `stories_builder/stories_builder_gate.py:47` | Verificado |
| `generate_ui_tree(spec, stories_plan)` | `factory/factory_agent.py:45` | Verificado |
| `compile_tsx(tree)` | `factory/tsx_compiler.py` | Verificado |
| `ZAxisScrollContainer` | `components/fx/ZAxisScrollContainer.tsx` | Rules of Hooks corrigido |
| `LayerPortal` | `components/fx/LayerPortal.tsx` | Zero Layout Shift garantido |
| `StoriesBuildPlan` | `contracts/stories_builder_contracts.py:47` | Verificado |

---

## Critério de Acessibilidade Obrigatório (Herdado de M0 QA)

`ZAxisScrollContainer` recebe `reducedMotion` como prop.
O pipeline **deve** derivá-la de `prefers-reduced-motion` — não pode ser hardcoded nem omitida.

Opções aceitas:
1. `reducedMotion` derivado de `window.matchMedia('(prefers-reduced-motion: reduce)')` via hook
2. Constante `REDUCED_MOTION_SYSTEM_PREFERENCE` lida do ambiente de build
3. Fail-closed: se o valor não for determinável, `reducedMotion=True` (mais restritivo, sempre seguro)

---

## Micro Etapas

### M1 — ExperienceBlueprint + BuildPlanResolver + StoriesBuilderGate
**Blast Radius:** 10 min  
**Gate Deterministico:** `StoriesBuilderGateReport.status == "passed"` sem P0/P1  
**Evidência:** `output_synthesis/1_blueprint.json`, `2_build_plan.json`, `3_gate_report.json`

### M2 — FrontendCodeSpec + ComponentTree + TSX Synthesis
**Blast Radius:** 15 min  
**Gate Deterministico:** TSX contém imports `@/components/fx`; sem orphan import; gate de segurança do tsx_compiler passa  
**Evidência:** `output_synthesis/4_code_spec.json`, `5_component_tree.json`, `6_candidate.tsx`

### M3 — HumanPromotionGate
**Blast Radius:** 5 min  
**Gate Deterministico:** `108/108 testes passando`; arquivos de evidência existem fisicamente  
**Evidência:** `output_synthesis/7_candidate_summary.md`, `8_test_results.log`  
**PARADA OBRIGATÓRIA:** aguardar revisão humana — não promover automaticamente

---

## Critérios de Aceite

- [ ] Blueprint com parâmetros Mad Lab Theme canônicos (canvas_navigation, freeform_depth, kinetic_field, exoape no rationale)
- [ ] BuildPlanResolver injeta Z-axis capabilities + NO_EXOAPE_SURFACE_CLONE
- [ ] StoriesBuilderGate passa sem P0/P1
- [ ] generate_ui_tree executado em strict mode (sem compatibility_mode)
- [ ] ComponentTree contém ZAxisScrollContainer e LayerPortal com traceability
- [ ] tsx_compiler gera imports `@/components/fx` condicionais
- [ ] `reducedMotion` derivado via fail-closed (não hardcoded)
- [ ] Candidato pausado no HumanPromotionGate
- [ ] 108/108 testes passando
- [ ] Nenhuma promoção automática

---

## Template ExperienceBlueprint Mad Lab Theme

```python
ExperienceBlueprint(
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
        "Tension earned through depth, not decoration."
    )
)
```
