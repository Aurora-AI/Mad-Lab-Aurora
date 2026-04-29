# OS Evidence: OS-006 — SecretariaExecutiva Inbox Intelligence (Phase 1b)

**OS ID:** OS-CRM-INBOX-INTELLIGENCE-20260429-006
**Status:** CONCLUÍDO ✅
**Data de Execução:** 2026-04-29
**Executor:** Claude Sonnet 4.6 (Full-Spectrum Agent — Override Executivo §2.4)
**Branch de Origem:** `feature/phase-1-inbox-intelligence`
**Merge Commit:** `bc2b115`
**Suite de Testes (pós-merge main):** 143 passed, 0 failed

---

## 1. Resumo da Execução

Esta OS estendeu o `wh_queue_worker` (Phase 1) com duas novas fases de processamento e construiu a infraestrutura completa de inteligência comercial — desde a persistência imutável de sinais até a síntese narrativa via Claude e o painel visual no backoffice.

### Princípios Arquiteturais Satisfeitos:
- **Linha do Tempo Imutável:** Cada sinal é um fato imutável no Event Store — `STORY_SYNTHESIS_REQUESTED` registrado com `aggregate_id=contact_id`.
- **StoryTelling Progressivo:** `ContactStory` versionada gerada via Claude Sonnet — narrativa real, não concatenação de texto.
- **Zero Espelhamento:** Nenhum corpo de mensagem WhatsApp armazenado — apenas `signal_summary` truncado em 220 chars.
- **Debounce Cognitivo:** `synthesis_queue.requested_at` atualizado a cada sinal; worker só processa após janela de 60s de silêncio.
- **Concorrência Otimista:** Worker relê `synthesis_queue.status` após Claude retornar — preserva `pending` se nova mensagem chegou durante a chamada.

---

## 2. Gates de Qualidade Satisfeitos

| Gate | Critério | Status |
|:-----|:---------|:------:|
| G1 — Contrato Antes de Código | Spec `2026-04-28-secretaria-executiva-inbox-intelligence-design.md` aprovada antes da implementação | ✅ |
| G2 — TDD | Todos os módulos implementados test-first (RED → GREEN) | ✅ |
| G3 — Suite Verde | 143 tests passed pós-merge em main | ✅ |
| G4 — Sem Dívida Técnica | Zero TODOs, zero placeholders, zero mocks de produção | ✅ |

---

## 3. Inventário de Artefatos

### crm-core (Python / FastAPI)

| Artefato | Tipo | Descrição |
|:---------|:-----|:----------|
| `src/models/event_types.py` | Modified | +`STORY_SYNTHESIS_REQUESTED` enum |
| `src/schemas/event_contracts.py` | Modified | +`StorySynthesisRequestedPayload` (Pydantic v2) |
| `alembic/versions/20260428_0018_refactor_inbox_tables.py` | Created | Refatora `inbox_conversations` + `inbox_messages` — String PKs, contact_id scope, signal fields |
| `alembic/versions/20260428_0019_create_contact_stories_synthesis_queue.py` | Created | Cria `contact_stories` (versionada, UniqueConstraint contact+version) + `synthesis_queue` |
| `src/models/inbox.py` | Rewritten | `Conversation`, `Message`, `ContactStory`, `SynthesisQueue` — SQLAlchemy 2.x, UUID PKs, timezone-aware |
| `src/services/inbox_service.py` | Created | `upsert_conversation`, `insert_message_signal`, `upsert_synthesis_queue` |
| `src/workers/wh_queue_worker.py` | Modified | +F3 inbox materialization, +F4 intelligence gate (`_SYNTHESIS_INTENTS`) |
| `src/workers/story_synthesis_worker.py` | Created | Debounce 60s, Claude Sonnet call, `ContactStory` persistida, concorrência otimista |
| `src/api/v1/inbox.py` | Created | 5 endpoints: `/conversations`, `/conversations/{id}/signals`, `/conversations/{id}/story`, `/follow-ups`, `/stream` (501 stub) |
| `src/main.py` | Modified | +`inbox_router` registrado em `/v1` |

### chronos-backoffice (Next.js / TypeScript)

| Artefato | Tipo | Descrição |
|:---------|:-----|:----------|
| `src/app/api/inbox/_proxy.ts` | Created | Proxy multi-candidato para crm-core (env + fallback local) |
| `src/app/api/inbox/conversations/route.ts` | Created | GET `/api/inbox/conversations` |
| `src/app/api/inbox/conversations/[id]/signals/route.ts` | Created | GET `/api/inbox/conversations/{id}/signals` |
| `src/app/api/inbox/conversations/[id]/story/route.ts` | Created | GET `/api/inbox/conversations/{id}/story` |
| `src/app/api/inbox/follow-ups/route.ts` | Created | GET `/api/inbox/follow-ups` |
| `src/lib/inbox-api.ts` | Created | Schemas Zod + fetch helpers tipados (`fetchConversations`, `fetchSignals`, `fetchStory`, `fetchFollowUps`) |
| `src/hooks/useInboxIntelligence.ts` | Created | Hook com polling 10s, seleção de conversa, carregamento de story |
| `src/components/inbox/RadarComercial.tsx` | Created | Zona 1 — cards de urgência ordenados (high/medium/low) |
| `src/components/inbox/StoryPanel.tsx` | Created | Zona 2 — narrativa + linha do tempo de sinais |
| `src/components/inbox/FollowUpsList.tsx` | Created | Zona 3 — ações pendentes derivadas de sinais |
| `src/components/inbox/IntelligenciaSurface.tsx` | Created | Grid 12 colunas, 3 zonas, status ao vivo |
| `src/app/secretaria-executiva/inteligencia/page.tsx` | Created | Página `/secretaria-executiva/inteligencia` |

---

## 4. Cobertura de Testes

| Arquivo de Teste | Testes | Resultado |
|:-----------------|:------:|:---------:|
| `test_story_synthesis_requested_schema.py` | 3 | ✅ PASSED |
| `test_inbox_service.py` | 5 | ✅ PASSED |
| `test_wh_queue_worker.py` | 7 (+2 novos) | ✅ PASSED |
| `test_story_synthesis_worker.py` | 4 | ✅ PASSED |
| `test_inbox_api.py` | 7 | ✅ PASSED |
| **Total Phase 1b** | **26** | ✅ |
| **Total suite crm-core** | **143** | ✅ |

---

## 5. Log de Commits (Phase 1b)

```
bc2b115 feat(crm): merge Phase 1b — Inbox Intelligence (F3+F4, story synthesis, API, backoffice panel)
af8c8d4 feat(backoffice): add secretaria-executiva/inteligencia page with three-zone intelligence panel
2d1c514 feat(backoffice): add inbox components — RadarComercial, StoryPanel, FollowUpsList, useInboxIntelligence hook
4bb8ba1 feat(backoffice): add inbox API proxy routes and typed inbox-api lib
04ac8e1 feat(crm): add inbox API endpoints — conversations, signals, story, follow-ups, stream stub
98b52dd feat(crm): add story_synthesis_worker with debounce and optimistic concurrency
95da081 feat(crm): wh_queue_worker F3+F4 — inbox materialization and intelligence gate
316036b feat(crm): add inbox_service with upsert_conversation, insert_message_signal, upsert_synthesis_queue
c79b244 feat(crm): refactor inbox SQLAlchemy models — contact_id scope, signal fields, ContactStory, SynthesisQueue
278d69f feat(crm): migration 0019 — create contact_stories and synthesis_queue
4e40bb7 feat(crm): migration 0018 — refactor inbox tables for intelligence projection
42cbf87 feat(crm): add STORY_SYNTHESIS_REQUESTED event type and Pydantic schema
```

---

## 6. Deltas de Evolução do Sistema

### Antes (Phase 1 — wh_queue)
- Webhook WhatsApp enfileira mensagens em `wh_queue`
- `wh_queue_worker` processa → emite `DEAL_INGESTED` + `MESSAGE_RECEIVED_V1` no Event Store (Harness)
- Nenhuma inteligência derivada, nenhuma projeção de inbox

### Depois (Phase 1b — Inbox Intelligence)
- F3: Cada mensagem processada materializa `inbox_conversations` + `inbox_messages` (sinal semântico, sem corpo bruto)
- F4: Sinais comerciais relevantes (`closing`, `proposal_review`, `commercial_interest`, `objection`, `follow_up`) disparam `STORY_SYNTHESIS_REQUESTED` + entrada na `synthesis_queue`
- `story_synthesis_worker` sintetiza narrativas progressivas via Claude com janela de debounce de 60s e concorrência otimista
- 5 endpoints REST expõem a inteligência: conversas, sinais, story, follow-ups, stream (stub Phase 2)
- Painel `secretaria-executiva/inteligencia` exibe Radar Comercial + Narrativa + Follow-ups com polling de 10s

### Próximas Fases Planejadas
- **Phase 2 — SSE Stream:** `/v1/inbox/stream` (evento-driven, sem polling)
- **Phase 2 — Executor:** Botão "Resolver →" em `FollowUpsList` conectado ao `crm-executor`
- **Phase 2 — Multi-deal cross-contact:** Cruzamento de narrativas por oportunidade no funil

---

## 7. Notas de Auditoria Trustware

- **PII:** Nenhum número de telefone armazenado em plaintext — `contact_phone_hash` = SHA-256(tenant_id + phone). Mensagens WhatsApp nunca persistidas.
- **Mutações críticas:** Todas as operações de DB ocorrem em transações explícitas com `await db.commit()` após cada item.
- **Fallback F4:** Intent `general_signal` (pequena conversa) não dispara Claude — custo LLM zero para ruído.
- **Audit Token Alembic:** `art_0018_inbox_refactor`, `art_0019_contact_stories`.
