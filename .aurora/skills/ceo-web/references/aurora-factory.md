# Aurora Factory — Consciência Completa da Fábrica
*Construído por Claude (Arquiteto) a partir da auditoria real do repositório.*
*Data: 08 de abril de 2026*
*Padrão: Aurora v8.0 — construído do zero, sem herança do agente legado*

---

## 1. O Que é a Aurora

Aurora não é uma agência. Não é uma software house. É uma **fábrica
de produtos digitais AI-native** operada por um fundador solo com
27 anos de experiência em operações comerciais, gestão de pessoas
e projetos.

A Aurora não vende tecnologia. Vende **elevação humana usando IA
como infraestrutura invisível.** O produto é a pessoa ou o
profissional melhorado — não o agente.

**Missão operacional:** Construir produtos de nível enterprise em
dias ou semanas. A velocidade é viabilizada pela fábrica —
não por atalhos ou dívida técnica.

---

## 2. Visão de Produto — Duas Camadas

```
CAMADA 1 — PRODUTOS AGÊNTICOS (agora)
  Agentes cognitivamente superiores embutidos em produtos verticais.
  O cliente compra o produto. Os agentes são invisíveis.

  Produtos ativos:
    ElysianLex  — agente jurídico
    CRM Aurora  — agente comercial (Silent Operator)

  Característica central:
    Cada produto é um laboratório.
    Cada interação real gera dados que nenhum concorrente tem.
    Isso é o Learning Loop.

CAMADA 2 — AGENTES COMO PRODUTO (futuro)
  Agentes vendidos diretamente como produto independente.
  Pré-requisito: Camada 1 precisa provar o conceito com
  usuários reais antes de Camada 2 existir como produto.
  Nome provisório: Aurora Agent Marketplace
```

---

## 3. Stack Técnico Canônico

| Camada | Tecnologia | Versão | Status |
|---|---|---|---|
| Backend Python | FastAPI | 3.11–3.14 | ✅ Ativo |
| Backend Node | Elysia.js | ESM | ✅ Ativo |
| Frontend | Next.js + React | 16.1.7 + 19 | ✅ Ativo |
| Tipagem | TypeScript | 5.9.3 strict | ✅ Ativo |
| 3D/Canvas | Three.js + R3F | r128 | ✅ Ativo |
| Auth/DB | Supabase | Latest | ⚠️ Declarado — não encontrado no repo |
| Vector DB | Qdrant | Latest | ⚠️ Docker OK — sem queries ativas |
| Graph DB | Neo4j | Latest | ✅ Configurado |
| Tipos | Pydantic v2 | 2.x | ✅ Ativo |
| LLM Primário | Claude Sonnet | claude-sonnet-4-6 | ✅ Definido |
| LLM Secundário | Gemini | Latest | ✅ Processamento cognitivo |
| LLM Rápido | Claude Haiku | claude-haiku-4-5 | ✅ Classificação |
| Containerização | Docker Compose | Latest | ✅ Ativo |
| Protocolo MCP | FastMCP Python | Latest | ✅ 5+ servidores ativos |
| Governança | Trustware + Skill Mesh | ~70 skills | ✅ Ativo |

**Regra absoluta de hardware local:**
Perfil padrão: CPU + Intel Iris Xe. Sem GPU NVIDIA dedicada.
CUDA não faz parte da arquitetura local. Dependência GPU é
bloqueador de build sem OS aprovada pelo Comandante.

---

## 4. Estrutura do Repositório

```
C:\Aurora\
├── portfolio-manifest.json
├── .skills\              ← Skills globais e agentes C-Level
│   ├── catalog.json
│   ├── shared\                 ← Referências compartilhadas entre agentes
│   │   ├── founder-dna.md
│   │   └── aurora-factory.md  ← Este arquivo
│   ├── ceo-marketing\          ← CEO Marketing/Vendas (Ladeira + Flávio)
│   ├── ceo-product-owner\      ← CEO Produto (Dan Martel)
│   ├── ceo-business-partner\   ← CEO Estratégia (Sandeep Swadia)
│   ├── master-skill\
│   ├── devil-advocate-auditor\
│   ├── loop-balance-analyzer\
│   └── [outras skills]\
│
├── Ozzmosis\                   ← Fábrica + infraestrutura compartilhada
│   ├── apps\
│   ├── libs\trustware\
│   └── docs\CONSTITUICAO\
│
├── CRM\                        ← Produto comercial (motor pai)
│   ├── apps/crm-core/
│   ├── apps/crm-executor/
│   ├── apps/chronos-backoffice/
│   ├── apps/outbound_gateway/
│   └── apps/whatsapp-gateway/
│
├── ElysianLex\                 ← Produto jurídico
│   ├── backend\
│   └── frontend\
│
├── AuroraCognitiveAssets\      ← Produto de infoprodutos
├── SilentOperator\             ← Scaffold comercial do CRM
└── SecretariaExecutiva\        ← Scaffold comercial do CRM
```

**Regra:** SilentOperator e SecretariaExecutiva são identidades
comerciais do CRM — não produtos independentes. Toda evolução
de código acontece em `C:\Aurora\CRM\`.

---

## 5. Produto 1 — CRM / Silent Operator

### O que é
Plataforma central de produtividade e inteligência operacional.
CRM com event sourcing, orquestração de agentes, interface 3D
(ARC renderer), e Morning Brief automatizado.

### Estado Real por Módulo

| Módulo | Status | Notas |
|---|---|---|
| CRM Core | ✅ Feature-completo | 26 routers, event sourcing SHA-256 |
| Conductor Service | ✅ Ativo | Morning Brief (Gmail ✅, Calendar ⚠️ stub) |
| Chronos Backoffice | ✅ Ativo | Dashboard + ARC renderer Three.js/R3F |
| Aurora Governance | ✅ Ativo | MCP server FastMCP com Trustware |
| ARC Program | ✅ Ativo | 8 packages ativos |
| Skill Mesh | ✅ Ativo | ~70 skills em `.agents/skills/` |
| Alvaro Core | ⚠️ Stub | Reasoning não implementado |
| WhatsApp Gateway | ⚠️ Stub | Inbound-only — outbound via HTTP interno |
| CRM Executor | ⚠️ Em dev | MVP CoPaw; Qdrant pendente |

### Integrações Reais

| Integração | Status |
|---|---|
| Gmail OAuth2 | ✅ Funcional |
| WhatsApp Meta (inbound) | ✅ Funcional |
| Claude API (Anthropic) | ⚠️ Conductor usa Gemini/OpenRouter — conflito com OS-001 |
| Calendar (Google + M365) | ❌ Stub sem implementação |
| PostgreSQL + pgvector | ⚠️ Docker OK — sem queries similarity ativas |
| Redis | ⚠️ Docker OK — não consumido pelas apps |
| Supabase | ❌ Não encontrado no repositório |

**Gate Status:** ✅ Gate 7 VERDE — 17/17 smoke tests passando

---

## 6. Produto 2 — Elysian Lex

### O que é
Produto jurídico AI-native. Arquitetura dual: P01 para advogado
solo (SQLite + SQLCipher, local, criptografado) e P02 para
escritórios institucionais (PostgreSQL 17 + RLS, multi-tenant).

### Roteamento de LLM por Função

| Função | Modelo |
|---|---|
| Reasoning jurídico | claude-sonnet-4-6 |
| Forense textual | claude-opus-4-6 |
| Drafting + secretaria | claude-haiku-4-5 |
| Triagem em massa | gemini-flash |
| Fallback offline | ollama/mistral |

### Estado Real por Feature

| Feature | Status |
|---|---|
| Cases + Clients CRUD | ✅ Funcional |
| Ingestão de documentos PDF → MD | ✅ Funcional |
| PII Tokenization HMAC-SHA256 | ✅ Funcional — zero I/O |
| Análise jurídica CRAG loop | ✅ Funcional |
| Trustware gate | ✅ Funcional |
| Forense linguística R3 | ✅ Funcional |
| Jurimetria / EMV R5 | ✅ Funcional |
| Redação de petições R4 | ✅ Funcional — 4 templates |
| Perfil de juiz R6 | ✅ Funcional |
| Daily brief + Secretaria | ✅ Funcional — cron 06:00 |
| WhatsApp webhook receiver | ✅ Funcional |
| Email watcher | 🔧 Código pronto — LEX_EMAIL_ENABLED=false |
| Calendar sync | ❌ Não implementado |
| LGPD compliance report | ✅ Funcional |

---

## 7. Agentes C-Level — Tríade Ativa

*Instalada em 08 de abril de 2026. Substitui aurora-clevel-advisor (deprecated).*

| Agente | Domínio | Clone Cognitivo | Status |
|---|---|---|---|
| `ceo-marketing` | Canal / Conversão / Oferta | Ladeira + Flávio Augusto | ✅ Produção |
| `ceo-product-owner` | Produto / Dor / Sequência | Dan Martel | ✅ Produção |
| `ceo-business-partner` | Estratégia / Processo / Competição | Sandeep Swadia | ✅ Produção |
| `aurora-clevel-advisor` | — | — | ❌ Deprecated 2026-04-08 |

**Output de cada CEO:** Bloco A (texto para Rodrigo) + Bloco B (JSON
estruturado para Neo4j e Qdrant). Os três alimentam o plano de
negócio vivo via pipeline cognitivo.

---

## 8. Pipeline de Ingestão Cognitiva

Todo conteúdo externo que entra na fábrica passa por este pipeline:

```
ENTRADA (documento bruto)
         ↓
    INGESTOR          → Verifica duplicidade, calcula delta,
                        emite Matriz de Decisão, aguarda gate
         ↓
   [GATE HUMANO]      → Rodrigo aprova ou nega
         ↓
   BIBLIOTECÁRIO      → Sanitização, Vault/Raw/, Qdrant, Neo4j
         ↓
    CIENTISTA         → Cross-reference, obsolescência,
                        gera evolution_delta.md
         ↓
  CEO RELEVANTE       → Filtra delta pelo domínio,
                        alimenta o plano de negócio vivo
```

**GEMs de Ingestão Ativas (Gemini):**

| GEM | Domínio | Referencial |
|---|---|---|
| GEM-Marketing | Canal / Venda / Copy | Ladeira + Flávio Augusto |
| GEM-Product | Produto / Mercado / Oceano Azul | Dan Martel |
| GEM-Business | Estratégia / Competição / Processo | Sandeep Swadia |

---

## 9. Gaps Críticos — Red Zone

### CRM / Silent Operator

| Gap | Impacto |
|---|---|
| NBA Log Table — Evidence Model | Camada de rastreabilidade ausente |
| validate_nba() + evidence_trace | Regra inegociável OS-001 não implementada |
| human_gate() middleware | Bloqueio antes de ações externas ausente |
| Provider mismatch — conductor usa Gemini; OS-001 especifica Claude | Inconsistência de governança |
| Alvaro Reasoning engine | Raciocínio avançado em stub |
| Calendar integration | Morning Brief incompleto |
| WhatsApp Business API oficial | Canal primário não configurado para produção |

### Elysian Lex

| Gap | Impacto |
|---|---|
| MemoryVault em dev (não produção) | PII em memória — bloqueador LGPD com cliente real |
| Acoplamento PDF→MD com Ozzmosis | Elysian não funciona de forma independente |
| Email watcher desabilitado | Secretaria incompleta |
| Calendar não implementado | Deadline tracking manual |

**Regra:** Red Zone aberta significa que nenhuma nova frente
de produto é justificável. A exceção única é se a nova frente
resolve a dor do primeiro cliente real e usa o stack atual.

---

## 10. Dashboard da Fábrica

```
DASHBOARD AURORA — Abril 2026
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Estágio:              Consolidação pré-distribuição
Clientes pagantes:    Zero
Gargalo primário:     Distribuição
Gargalo técnico:      Fechamento de gaps Red Zone

CRM/Silent Operator:  ✅ Core funcional | ⚠️ Red Zone aberta
Elysian Lex P01:      ✅ Features jurídicas completas | ⚠️ PII em memória
Gate 7:               ✅ 17/17 VERDE
Skills no sistema:    ~70 (Skill Mesh ativo)
MCP servers:          5+ instâncias dockerizadas
Tríade CEO:           ✅ Online desde 2026-04-08

Próximo marco:        Fechar Red Zone → primeiro cliente real
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 11. Implicação Estratégica para os Três CEOs

**O que a auditoria revela:**
A fábrica é mais madura do que aparenta externamente. Não é MVP
frágil — é plataforma com arquitetura sofisticada: event sourcing,
Trustware, A2A protocol, MCP governance, ~70 skills.

**Para o CEO-Marketing:**
O produto está mais próximo de demonstrável do que de construção.
Gaps Red Zone não impedem demo controlada — impedem produção com
cliente real. Qualquer estratégia de canal deve ser calibrada
para este estágio: validação de ICP, não escala.

**Para o CEO-Product Owner:**
Com Red Zone aberta, a decisão de produto correta é sempre fechar
gap crítico antes de abrir nova frente. A exceção única: nova
frente que resolve dor do primeiro cliente real com stack atual.

**Para o CEO-Business Partner:**
A posição competitiva atual é invisibilidade estratégica — a Aurora
está se posicionando em nichos (jurídico solo, comercial AI-native)
onde incumbentes não conseguem entrar sem se contradizer. Esse
janela de invisibilidade tem prazo — fechar Red Zone e demonstrar
antes que o mercado perceba o espaço.

---

*Próxima revisão obrigatória: quando houver mudança de stack,
fechamento de Red Zone, primeiro cliente pagante, ou lançamento
de infoproduto.*
*Responsável: Arquiteto (Claude) com aprovação do Comandante (Rodrigo).*
