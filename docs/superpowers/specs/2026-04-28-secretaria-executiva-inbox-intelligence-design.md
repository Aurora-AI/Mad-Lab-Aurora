# Design — SecretariaExecutiva: Inbox de Inteligência Comercial

**Data:** 2026-04-28
**Status:** Aprovado
**Fase:** 1 (Paralelo) — SecretariaExecutiva Wiring Inicial
**Referência:** `2026-04-27-crm-silentoperator-secretariaexecutiva-integration-design.md`

---

## 1. Contexto e Escopo

O `wh_queue_worker` (Phase 1) já recebe mensagens WhatsApp, emite `MESSAGE_RECEIVED_V1` no Event Store e executa `CommercialSignalAnalyzer`. Esta fase estende esse pipeline para:

1. Materializar projeções de leitura rápida (Inbox) sem espelhar mensagens brutas
2. Gerar narrativas progressivas (Story) via Claude, acionadas apenas por sinais comerciais relevantes
3. Expor endpoints de inteligência no `crm-core`
4. Exibir um painel de inteligência no `chronos-backoffice`

**Fora de escopo:** envio de respostas ao usuário, SSE (reservado para Fase 2), multi-canal (email, telefone).

---

## 2. Princípios Arquiteturais

- **Linha do Tempo Imutável:** cada sinal é um fato gravado no Event Store, nunca alterado. As projeções de inbox são rebuild possível a partir do Event Store.
- **StoryTelling Progressivo:** a narrativa do contato é sintetizada pelo Claude a partir da timeline de sinais — não é uma concatenação de textos, é inteligência estruturada.
- **Zero Espelhamento:** nenhuma mensagem bruta do WhatsApp é armazenada ou exibida. O operador vê sinais processados e narrativas, não conversas.
- **Custo LLM Controlado:** o Claude é acionado apenas quando há sinal comercial relevante (`intent != general_signal` ou `requires_human_review`). Ruído (small talk, saudações) é descartado antes da síntese.
- **Debounce Cognitivo:** rajadas de mensagens do mesmo contato geram uma única chamada ao Claude, consolidadas por janela de silêncio (padrão: 60s).

---

## 3. Fluxo de Processamento (4 Fases)

```
WhatsApp (Meta API)
        │ webhook POST
        ▼
┌─────────────────────────────────────────────────┐
│  wh_queue_worker  (modificado)                  │
│                                                  │
│  F1: MESSAGE_RECEIVED_V1 → Event Store          │ ← já implementado
│  F2: CommercialSignalAnalyzer → CompiledContext │ ← já implementado
│                                                  │
│  F3: upsert_conversation + insert_message_signal│ ← NOVO
│       (projeções de inbox, sem texto bruto)     │
│                                                  │
│  F4: intent == general_signal?                  │ ← NOVO
│       → FIM (sem LLM)                           │
│      interesse comercial / urgência / closing?   │
│       → emit STORY_SYNTHESIS_REQUESTED          │
│       → upsert synthesis_queue (pending)        │
│       → encerra                                 │
└──────────────────────┬──────────────────────────┘
                       │
           ┌───────────┴───────────┐
           ▼                       ▼
  ┌────────────────┐    ┌──────────────────────────┐
  │  Inbox Tables  │    │  story_synthesis_worker  │
  │  (leitura      │    │  (novo worker cognitivo) │
  │   imediata)    │    │                          │
  └───────┬────────┘    │  poll synthesis_queue    │
          │             │  debounce 60s            │
          │             │  lê timeline de sinais   │
          │             │  Claude Sonnet → Story   │
          │             │  concorrência otimista   │
          │             └────────────┬─────────────┘
          │                          │
          └────────────┬─────────────┘
                       ▼
            ┌──────────────────────┐
            │  crm-core API        │
            │  GET /v1/inbox/...   │
            └──────────┬───────────┘
                       ▼
            ┌──────────────────────┐
            │  chronos-backoffice  │
            │  Painel Inteligência │
            └──────────────────────┘
```

---

## 4. Modelo de Dados

### 4.1 `inbox_conversations` (refatorada)

Substitui o modelo atual que usa `scope_id` genérico e PK inteira.

| Campo | Tipo | Restrição | Descrição |
|---|---|---|---|
| `id` | String (UUID) | PK | — |
| `contact_id` | String | NOT NULL, index | Escopo primário — o relacionamento |
| `deal_id` | String | nullable, index | Contexto de oportunidade (opcional) |
| `tenant_id` | String | NOT NULL | Isolamento multi-tenant |
| `source` | String | NOT NULL | `whatsapp` \| `email` |
| `external_ref` | String | nullable, index | `conversation_id` do provider |
| `status` | String | NOT NULL | `open` \| `pending` \| `closed` |
| `last_intent` | String | nullable | Último intent detectado |
| `last_urgency` | String | nullable | `high` \| `medium` \| `low` |
| `last_summary` | String(220) | nullable | Texto normalizado truncado do último sinal |
| `last_signal_at` | DateTime tz | nullable, index | Timestamp do último sinal |
| `story_version` | Integer | default 0 | Incrementado a cada síntese |
| `created_at` | DateTime tz | NOT NULL | — |
| `updated_at` | DateTime tz | NOT NULL | — |

**Índices compostos:** `(contact_id, status)`, `(deal_id, status)`, `(last_signal_at desc)`

**Nota de ordenação:** `last_urgency` é string. Queries de listagem usam `CASE WHEN last_urgency='high' THEN 1 WHEN last_urgency='medium' THEN 2 ELSE 3 END` para ordenação correta — nunca `ORDER BY last_urgency` diretamente.

### 4.2 `inbox_messages` (refatorada — sem corpo bruto)

Armazena sinais comerciais processados, não mensagens do WhatsApp.

| Campo | Tipo | Restrição | Descrição |
|---|---|---|---|
| `id` | String (UUID) | PK | — |
| `conversation_id` | String | FK `inbox_conversations.id`, NOT NULL, index | — |
| `contact_id` | String | NOT NULL, index | Denormalizado para query direta |
| `intent` | String | NOT NULL | Resultado do `CommercialSignalAnalyzer` |
| `urgency` | String | NOT NULL | `high` \| `medium` \| `low` |
| `closing_signal` | Boolean | NOT NULL, default false | — |
| `follow_up_requested` | Boolean | NOT NULL, default false | — |
| `requires_human_review` | Boolean | NOT NULL, default false | — |
| `signal_summary` | String(220) | NOT NULL | Texto normalizado truncado — nunca o body bruto |
| `recommended_action` | String | NOT NULL | Ex: `schedule_follow_up` |
| `trace_id` | String | NOT NULL | Link para `MESSAGE_RECEIVED_V1` no Event Store |
| `occurred_at` | DateTime tz | NOT NULL, index | Timestamp da mensagem original |
| `created_at` | DateTime tz | NOT NULL | — |

### 4.3 `contact_stories` (nova)

Projeção cognitiva gerada pelo Claude. Cada versão é imutável — novas sínteses inserem nova linha.

| Campo | Tipo | Restrição | Descrição |
|---|---|---|---|
| `id` | String (UUID) | PK | — |
| `contact_id` | String | NOT NULL, index | — |
| `deal_id` | String | nullable | Contexto no momento da síntese |
| `story_text` | Text | NOT NULL | Narrativa gerada pelo Claude |
| `version` | Integer | NOT NULL | Incrementa por `contact_id` |
| `signal_count` | Integer | NOT NULL | Quantos sinais foram sintetizados |
| `synthesis_trace_id` | String | NOT NULL | Rastreabilidade da chamada LLM |
| `synthesized_at` | DateTime tz | NOT NULL | — |

**Índice:** `(contact_id, version desc)` — leitura sempre busca a versão mais recente.

**Constraint única:** `UNIQUE (contact_id, version)` — garante que o worker não grava duas sínteses com o mesmo número de versão para o mesmo contato.

### 4.4 `synthesis_queue` (nova — debounce e concorrência)

Uma linha por `contact_id`. Upsert sempre força `requested_at` atual e `status = 'pending'`, mesmo durante `processing`.

| Campo | Tipo | Restrição | Descrição |
|---|---|---|---|
| `contact_id` | String | PK | Uma linha por contato |
| `requested_at` | DateTime tz | NOT NULL | Atualizado no upsert do webhook |
| `status` | String | NOT NULL | `pending` \| `processing` \| `done` |
| `last_synthesized_at` | DateTime tz | nullable | Timestamp da última síntese concluída |

**Padrão de concorrência otimista:** o worker, ao terminar a chamada Claude, faz `SELECT status FOR UPDATE`. Se `status == 'processing'` → marca `done`. Se `status == 'pending'` → salva a Story mas mantém `pending` para o próximo ciclo capturar o sinal retardatário.

### 4.5 Novo `EventType`

```python
STORY_SYNTHESIS_REQUESTED = "STORY_SYNTHESIS_REQUESTED"
```

Payload: `contact_id`, `conversation_id`, `deal_id` (nullable), `signal_count`, `trace_id`.

---

## 5. Modificações no `wh_queue_worker`

Fase 3 e 4 adicionadas ao final de `process_item`, após a emissão dos eventos Harness.

### Novo módulo: `src/services/inbox_service.py`

Funções extraídas para testabilidade independente do worker:

```python
async def upsert_conversation(
    db, *, contact_id, deal_id, tenant_id, source, external_ref, signal
) -> Conversation

async def insert_message_signal(
    db, *, conversation_id, contact_id, signal, trace_id, occurred_at
) -> Message

async def upsert_synthesis_queue(db, *, contact_id) -> None
# Sempre força status='pending' e atualiza requested_at
```

### Gate de inteligência (F4)

```python
SYNTHESIS_INTENTS = {
    "closing", "proposal_review", "commercial_interest", "objection", "follow_up"
}

if signal["intent"] in SYNTHESIS_INTENTS or signal["requires_human_review"]:
    await emit_story_synthesis_requested(db, contact_id=..., ...)
    await upsert_synthesis_queue(db, contact_id=...)
# intent == "general_signal" sem flags → encerra sem LLM
```

---

## 6. `story_synthesis_worker` (novo)

**Arquivo:** `src/workers/story_synthesis_worker.py`

**Variáveis de ambiente:**
- `CRM_STORY_DEBOUNCE_SECONDS` (padrão: `60`)
- `CRM_STORY_BATCH_SIZE` (padrão: `5`)
- `CRM_STORY_MODEL` (padrão: `claude-sonnet-4-6`)

**Fluxo de `run_once()`:**

```
1. SELECT * FROM synthesis_queue
   WHERE status='pending' AND requested_at < now() - debounce
   FOR UPDATE SKIP LOCKED
   LIMIT batch_size

2. SET status='processing', COMMIT

3. Para cada item:
   a. Lê inbox_messages WHERE contact_id ORDER BY occurred_at
   b. Lê contact_stories mais recente (contexto progressivo)
   c. Chama Claude Sonnet com prompt de StoryTelling
   d. INSERT contact_stories (nova versão)
   e. UPDATE inbox_conversations SET story_version += 1
   f. SELECT status FROM synthesis_queue FOR UPDATE
      - status == 'processing' → UPDATE status='done', last_synthesized_at=now()
      - status == 'pending'    → salva Story, mantém pending (sinal retardatário)
   g. COMMIT
```

**Prompt de StoryTelling (estrutura):**

```
Você é o analisador de inteligência comercial da Aurora.
Abaixo está a linha do tempo de sinais comerciais de um contato.
[Story anterior, se existir]
[Lista de sinais: intent, urgency, summary, occurred_at]

Gere uma narrativa progressiva e coerente sobre este contato.
A narrativa deve responder: quem é, o que quer, como está evoluindo,
o que é urgente, qual é o próximo passo recomendado.
Máximo 400 palavras. Tom analítico e direto.
```

---

## 7. API Endpoints

Arquivo: `src/api/v1/inbox.py` — prefixo `/v1/inbox`

### `GET /v1/inbox/conversations`

Lista conversas ordenadas por `last_urgency` (high→low) e `last_signal_at` desc.

**Query params:** `contact_id`, `deal_id`, `tenant_id`, `status`, `limit` (default 20), `offset`

**Response:** `{ total, items: [{ id, contact_id, deal_id, status, source, last_intent, last_urgency, last_summary, last_signal_at, story_version, has_story }] }`

### `GET /v1/inbox/conversations/{id}/signals`

Timeline imutável de sinais de uma conversa, `occurred_at asc`.

**Response:** `{ conversation_id, items: [{ id, intent, urgency, closing_signal, follow_up_requested, requires_human_review, signal_summary, recommended_action, trace_id, occurred_at }] }`

### `GET /v1/inbox/conversations/{id}/story`

Narrativa sintetizada mais recente. `404` se ainda não sintetizada.

**Response:** `{ contact_id, deal_id, version, signal_count, story_text, synthesized_at }`

### `GET /v1/inbox/follow-ups`

Sinais com `follow_up_requested=true` ou `recommended_action` de ação. Na Fase 1, retorna **todos** os sinais que qualificam — não há estado de "resolvido" ainda. O mecanismo de resolução (POST para `crm-executor`) é implementado na Fase 2.

**Query params:** `contact_id`, `deal_id`, `urgency`, `limit` (default 20)

**Response:** `{ items: [{ conversation_id, contact_id, deal_id, urgency, recommended_action, signal_summary, occurred_at }] }`

### `GET /v1/inbox/stream` *(reservado)*

Retorna `501 Not Implemented` com `X-Planned-Phase: 2`. Path reservado para SSE na Fase 2 sem breaking change.

---

## 8. Painel de Inteligência (`chronos-backoffice`)

**Localização:** `app/secretaria-executiva/inteligencia/`

### Zona 1 — Radar Comercial

Cards de conversas ativas ordenados por urgência. Cores: `high` → vermelho, `medium` → âmbar, `low` → cinza neutro. Cada card: nome do contato (via `contact_id`), intent atual, summary do último sinal, tempo decorrido desde `last_signal_at`. Clique abre o painel lateral (Zona 2).

### Zona 2 — Story do Contato (painel lateral)

- Cabeçalho: nome, deal vinculado (se houver), versão da story
- Corpo: `story_text` gerado pelo Claude. Se `story_version == 0`: skeleton + "Inteligência sendo processada..."
- Rodapé: timeline de sinais em ordem cronológica — apenas `intent`, `urgency`, `signal_summary` e `occurred_at` por item. Sem corpo bruto de mensagem.

### Zona 3 — Follow-ups Pendentes

Lista de ações derivadas de `GET /v1/inbox/follow-ups`. Agrupadas por urgência. Botão "Marcar como resolvido" (stub para Fase 2 — POST para `crm-executor`).

### Estratégia de dados

- Polling REST a cada 10s nas zonas 1 e 3
- Zona 2 carregada sob demanda (clique no card)
- Componente preparado para substituir polling por SSE no endpoint `/v1/inbox/stream` na Fase 2 — sem mudança de estrutura de componente

---

## 9. Migrações Alembic

| Revisão | Descrição |
|---|---|
| `20260428_0018_refactor_inbox_tables` | Drop/recreate `inbox_conversations` e `inbox_messages` com novo schema |
| `20260428_0019_create_contact_stories_synthesis_queue` | Cria `contact_stories` e `synthesis_queue` |

`down_revision` de 0018: `20260427_0017` (wh_queue)

---

## 10. Testes

| Arquivo | Cobertura |
|---|---|
| `tests/test_inbox_service.py` | `upsert_conversation`, `insert_message_signal`, `upsert_synthesis_queue` — unitários com SQLite |
| `tests/test_story_synthesis_worker.py` | `run_once` com Claude mockado, debounce, concorrência otimista |
| `tests/test_inbox_api.py` | Todos os endpoints com SQLite, sem LLM |
| `tests/test_secretaria_inteligencia.py` | (backoffice) render do painel, estados de loading |

---

## 11. Ordem de Implementação

1. Migrações Alembic (0018 + 0019)
2. Modelos SQLAlchemy refatorados (`inbox.py`) + `ContactStory`, `SynthesisQueue`
3. `src/services/inbox_service.py` + testes unitários
4. Modificações no `wh_queue_worker` (F3 + F4) + testes integração
5. `src/workers/story_synthesis_worker.py` + testes
6. `src/api/v1/inbox.py` + registro em `main.py` + testes de API
7. `STORY_SYNTHESIS_REQUESTED` em `event_types.py` + schema Pydantic
8. Painel `app/secretaria-executiva/inteligencia/` no backoffice
