# OS-Evidence: Stories Builder Domain Separation

**ID:** OS-MADLAB-OS018-20260604-001
**Status:** MICRO-STEP 3 CONCLUÍDO ✅ (OS EM ANDAMENTO)
**Data:** 2026-06-05
**Executor:** Antigravity (Gemini 1.5 Pro)

## Descrição do Resultado

Esta Ordem de Serviço formaliza a separação de domínio do Stories Builder para evitar que decisões arquiteturais (layout, motion, navegação e temas) vazem para o executor de código.

- **Micro-step 1 (Contracts & Authority Boundary):** Criação dos contratos formais (`StoriesBuildPlan`, `BuildPlanTraceabilityItem`, `BuilderCapability`, `BuilderConstraint`) no arquivo [stories_builder_contracts.py](file:///C:/Projetos/Aurora/AuroraOS/factory/frontend_synthesis/contracts/stories_builder_contracts.py). Foram implementadas validações estritas no Pydantic que emitem P0 `BUILDER_ARCHITECTURE_LEAK` se uma decisão arquitetural for marcada como de posse do `stories_builder`.
- **Micro-step 2 (BuildPlanResolver):** Criação do [build_plan_resolver.py](file:///C:/Projetos/Aurora/AuroraOS/factory/stories_builder/build_plan_resolver.py) que traduz um `ExperienceBlueprint` em um `StoriesBuildPlan` concreto com rastreabilidade detalhada, aplicando assinatura hash SHA256 determinística para associar fisicamente o plano de execução ao blueprint de entrada.
- **Micro-step 3 (StoriesBuilderGate):** Criação do [stories_builder_gate.py](file:///C:/Projetos/Aurora/AuroraOS/factory/stories_builder/stories_builder_gate.py) que implementa a validação do `StoriesBuildPlan` e gera `StoriesBuilderGateReport`. O gate valida a assinatura de blueprint hash, restrições obrigatórias (`forbidden_decisions`), integridade e autoria da rastreabilidade (`BUILDER_ARCHITECTURE_LEAK`, `RAW_REFERENCE_AUTHORITY_LEAK`, `AUTO_PROMOTION_ATTEMPT`, `MOTION_WITHOUT_PERFORMANCE_BUDGET`, `LAYOUT_WITHOUT_RESPONSIVE_STRATEGY`).

## Evidências de Execução

### Arquivos Criados/Modificados
1. [stories_builder_contracts.py](file:///C:/Projetos/Aurora/AuroraOS/factory/frontend_synthesis/contracts/stories_builder_contracts.py) — Contratos e modelos de validação.
2. [test_stories_builder_contracts.py](file:///C:/Projetos/Aurora/AuroraOS/factory/frontend_synthesis/contracts/test_stories_builder_contracts.py) — Testes unitários para validação de limites de autoridade.
3. [__init__.py](file:///C:/Projetos/Aurora/AuroraOS/factory/stories_builder/__init__.py) — Módulo `stories_builder`.
4. [build_plan_resolver.py](file:///C:/Projetos/Aurora/AuroraOS/factory/stories_builder/build_plan_resolver.py) — Resolvedor que traduz blueprint em plano.
5. [test_build_plan_resolver.py](file:///C:/Projetos/Aurora/AuroraOS/factory/stories_builder/test_build_plan_resolver.py) — Testes de resolução para múltiplos perfis de superfície (landing, canvas, dashboard, portal).
6. [stories_builder_gate.py](file:///C:/Projetos/Aurora/AuroraOS/factory/stories_builder/stories_builder_gate.py) — Validador autônomo do plano de construção.
7. [test_stories_builder_gate.py](file:///C:/Projetos/Aurora/AuroraOS/factory/stories_builder/test_stories_builder_gate.py) — Testes unitários do validador.

### Output do Terminal (pytest)
```txt
collected 92 items

factory\frontend_synthesis\acquisition\test_asset_kit_acquisition_agent.py . [  1%]
...
factory\experience_architect\test_experience_architect.py ..             [ 84%]
factory\stories_builder\test_build_plan_resolver.py ......               [ 91%]
factory\stories_builder\test_stories_builder_gate.py ........            [100%]

======================== 92 passed in 84.33s (0:01:24) ========================
```

## Token Tracking

| Step | Agente | Modelo | Input Tokens | Output Tokens | Custo USD est. |
|---|---|---|---|---|---|
| OS Micro-step 1 — Contracts | Antigravity | Gemini 1.5 Pro | 185000 | 8500 | $0.27 |
| OS Micro-step 2 — Resolver | Antigravity | Gemini 1.5 Pro | 45000 | 3500 | $0.0825 |
| OS Micro-step 3 — Gate | Antigravity | Gemini 1.5 Pro | 65000 | 5000 | $0.1275 |
| **TOTAL** | | | **295000** | **17000** | **$0.48** |

**Custo BRL estimado:** R$ 3.36  
**Ledger entry:** `Vault/Token-Ledger/2026-06-05/OS-MADLAB-OS018-20260604-001-step-3.json`  

## Impacto Sistêmico

Com a introdução do `StoriesBuilderGate`, estabelecemos uma barreira de integridade que bloqueia automaticamente qualquer plano de construção que apresente vazamento arquitetural (`BUILDER_ARCHITECTURE_LEAK`), atalhos não-rastreados (`STORIES_UNTRACED_IMPLEMENTATION`), ou tentativas de autoproteção de código. O construtor é obrigado a ser 100% passivo e aderente ao blueprint aprovado.

---
**Autoridade de Validação:** Antigravity  
**Gate:** MICRO-STEP 3 APROVADO COM OBSERVAÇÃO OPERACIONAL NÃO BLOQUEANTE  
