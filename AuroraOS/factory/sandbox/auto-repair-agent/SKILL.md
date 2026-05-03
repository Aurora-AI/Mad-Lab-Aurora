---
name: auto-repair-agent
description: |
  Executor de sandbox para reparo autônomo de micro-tarefas falhas.
  Subordinado ao product-integrity-engineer. Recebe evidência de falha,
  classifica modo de sandbox, executa até 3 tentativas de reparo com
  timeouts rígidos, e delega persistência de anti-patterns ao
  agent-reflexion-code. Escala para humano quando falha persistente.
  DEVE ser acionado pelo product-integrity-engineer quando uma falha
  localizada é detectada e o reparo pode ser tentado em sandbox isolado.
---

# auto-repair-agent — Executor de Sandbox para Reparo Autônomo

## Mesh Contract

```json
{
  "schema_version": "1.0.0",
  "id": "auto-repair-agent",
  "activation": {
    "mode": "delegated",
    "activated_by": ["product-integrity-engineer"],
    "semantic_triggers": ["@auto-repair", "/repair-sandbox"],
    "auto_activate": false
  },
  "capabilities": {
    "provides": ["sandbox_repair_execution", "repair_checkpoint"],
    "depends_on": ["product-integrity-engineer", "agent-reflexion-code"],
    "can_delegate_to": ["agent-reflexion-code"],
    "blocking_gates": ["qa-review"],
    "emits_artifacts": [
      "repair_state.json",
      "activity.jsonl entries"
    ]
  },
  "runtime": {
    "min_python": "3.14",
    "requires_docker": false,
    "requires_git": true
  },
  "quality": {
    "contracts": "contracts.py (Pydantic v2)",
    "tests": "scripts/test_classifier.py",
    "observability": "activity.jsonl events"
  }
}
```

## Semantic Triggers

- `@auto-repair` — Acionado pelo product-integrity-engineer
- `/repair-sandbox` — Comando explícito para iniciar reparo em sandbox

## Protocolo de Execução

### 1. Receber RepairRequest
Validar input contra schema `RepairRequest` (contracts.py).

### 2. Classificar Modo de Sandbox
Usar `scripts/classify_mode.py` para determinar `SandboxMode`.

### 3. Executar Loop de Reparo
- Até `max_attempts` tentativas
- Cada tentativa gera `AttemptResult`
- Checkpoint em `repair_state.json` após cada tentativa (idempotência)
- Evento emitido no `activity.jsonl` após cada tentativa

### 4. Headless QA Hand-off (OS-004)
- **Quando o teste passa (status == "fixed"):** 
  - O script gera um arquivo `artifacts/qa_request_{task_id}_{attempt}.json` contendo o patch e o output do teste.
  - O script bloqueia (polling síncrono, timeout de 5 min) aguardando o agente QA processar o request.
  - O agente/orquestrador (atuando como QA) deve ler o `qa_request`, invocar a skill `qa-review`, gerar o schema `QAHeadlessVerdict` e gravá-lo como `artifacts/qa_verdict_{task_id}_{attempt}.json`.
- **Vereditos:**
  - `APPROVED`: O reparo é selado e o anti-pattern é persistido.
  - `REJECTED`: A tentativa falha, as notas do QA entram no stderr e o loop tenta a próxima hipótese.
  - `NEEDS_REVIEW`: Escala imediatamente para o `product-integrity-engineer`.

### 5. Pós-Reparo
- **Se aprovado (QA APPROVED):** Delegar `/reflexion-capture` ao `agent-reflexion-code` para tratar o `AntiPatternCandidate`.
- **Se falhou / timeout:** Escalar ao `product-integrity-engineer` com `RepairResult` em `ESCALATION.md`.

## Modos de Sandbox

| Modo | Quando usar | Timeout padrão |
|---|---|---|
| `memory` | Teste unitário puro, sem I/O de disco | 30s |
| `worktree` | Teste precisa do repo real (imports, configs) | 120s |
| `container` | Teste precisa de serviços (DB, Redis, rede) | 300s |
