# OS-Evidence: Stories Builder Domain Separation

**ID:** OS-MADLAB-OS018-20260604-001
**Status:** MICRO-STEP 2 CONCLUÍDO ✅ (OS EM ANDAMENTO)
**Data:** 2026-06-04
**Executor:** Antigravity (Gemini 1.5 Pro)

## Descrição do Resultado

Esta Ordem de Serviço formaliza a separação de domínio do Stories Builder para evitar que decisões arquiteturais (layout, motion, navegação e temas) vazem para o executor de código.

- **Micro-step 1 (Contracts & Authority Boundary):** Criação dos contratos formais (`StoriesBuildPlan`, `BuildPlanTraceabilityItem`, `BuilderCapability`, `BuilderConstraint`) no arquivo [stories_builder_contracts.py](file:///C:/Projetos/Aurora/AuroraOS/factory/frontend_synthesis/contracts/stories_builder_contracts.py). Foram implementadas validações estritas no Pydantic que emitem P0 `BUILDER_ARCHITECTURE_LEAK` se uma decisão arquitetural for marcada como de posse do `stories_builder`.
- **Micro-step 2 (BuildPlanResolver):** Criação do [build_plan_resolver.py](file:///C:/Projetos/Aurora/AuroraOS/factory/stories_builder/build_plan_resolver.py) que traduz um `ExperienceBlueprint` em um `StoriesBuildPlan` concreto com rastreabilidade detalhada, aplicando assinatura hash SHA256 determinística para associar fisicamente o plano de execução ao blueprint de entrada.

## Evidências de Execução

### Arquivos Criados/Modificados
1. [stories_builder_contracts.py](file:///C:/Projetos/Aurora/AuroraOS/factory/frontend_synthesis/contracts/stories_builder_contracts.py) — Contratos e modelos de validação.
2. [test_stories_builder_contracts.py](file:///C:/Projetos/Aurora/AuroraOS/factory/frontend_synthesis/contracts/test_stories_builder_contracts.py) — Testes unitários para validação de limites de autoridade.
3. [__init__.py](file:///C:/Projetos/Aurora/AuroraOS/factory/stories_builder/__init__.py) — Módulo `stories_builder`.
4. [build_plan_resolver.py](file:///C:/Projetos/Aurora/AuroraOS/factory/stories_builder/build_plan_resolver.py) — Resolvedor que traduz blueprint em plano.
5. [test_build_plan_resolver.py](file:///C:/Projetos/Aurora/AuroraOS/factory/stories_builder/test_build_plan_resolver.py) — Testes de resolução para múltiplos perfis de superfície (landing, canvas, dashboard, portal).

### Output do Terminal (pytest)
```txt
collected 84 items

factory\frontend_synthesis\acquisition\test_asset_kit_acquisition_agent.py . [  1%]
.                                                                        [  2%]
factory\frontend_synthesis\bff\test_bff_agent.py .....                   [  8%]
factory\frontend_synthesis\bff\test_bff_contracts.py ....                [ 13%]
factory\frontend_synthesis\contracts\test_contracts.py ....              [ 17%]
factory\frontend_synthesis\contracts\test_stories_builder_contracts.py . [ 19%]
.......                                                                  [ 27%]
factory\frontend_synthesis\factory\test_factory.py ......                [ 34%]
factory\frontend_synthesis\factory\test_motion_primitive_injector.py ... [ 38%]
                                                                         [ 38%]
factory\frontend_synthesis\orchestrator\test_dag_orchestrator.py ...     [ 41%]
factory\frontend_synthesis\orchestrator\test_fidelity_evaluator.py ....  [ 46%]
factory\frontend_synthesis\orchestrator\test_ingestion_resolver.py ....  [ 51%]
factory\frontend_synthesis\orchestrator\test_orchestrator.py ...         [ 54%]
factory\frontend_synthesis\orchestrator\test_originality_gate.py ....... [ 63%]
...                                                                      [ 66%]
factory\frontend_synthesis\orchestrator\test_perceptual_evaluator.py ... [ 70%]
.....                                                                    [ 76%]
factory\frontend_synthesis\orchestrator\test_truth_resolver.py ..        [ 78%]
factory\experience_architect\test_blueprint_resolver.py ..........       [ 90%]
factory\experience_architect\test_experience_architect.py ..             [ 92%]
factory\stories_builder\test_build_plan_resolver.py ......               [100%]

============================= 84 passed in 21.57s =============================
```

## Token Tracking

| Step | Agente | Modelo | Input Tokens | Output Tokens | Custo USD est. |
|---|---|---|---|---|---|
| OS Micro-step 1 — Contracts | Antigravity | Gemini 1.5 Pro | 185000 | 8500 | $0.27 |
| OS Micro-step 2 — Resolver | Antigravity | Gemini 1.5 Pro | 45000 | 3500 | $0.0825 |
| **TOTAL** | | | **230000** | **12000** | **$0.3525** |

**Custo BRL estimado:** R$ 2.47  
**Ledger entry:** `Vault/Token-Ledger/2026-06-04/OS-MADLAB-OS018-20260604-001-step-2.json`  

## Impacto Sistêmico

Com a introdução do `BuildPlanResolver` e das validações de limites de autoridade, garantimos que o Stories Builder apenas opere como um agente executivo. Qualquer tentativa do Stories Builder de iniciar componentes ou layouts sem rastreabilidade explícita em campos do blueprint do arquiteto falhará imediatamente nas gates de validação.

---
**Autoridade de Validação:** Antigravity  
**Gate:** MICRO-STEP 2 APROVADO  
