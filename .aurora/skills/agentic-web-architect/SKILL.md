---
name: agentic-web-architect
version: 1.0.0
updated: 2026-10-16
classification: madlab-production
status: active
domain: agentic-web
description: |
  Arquiteto de Sites e Ecossistemas Web 100% AI-Agentic Friendly para execução no Google Antigravity IDE. Implementa WebMCP (Chrome document.modelContext Declarative e Imperative APIs), Content Negotiation em Markdown (Accept: text/markdown e rotas .md), protocolos A2A (/.well-known/agent-card.json), /llms.txt, JSON-LD @graph determinístico, Generative Engine Optimization (GEO — Spec-Sheets e Citation-Magnets) e Critério Formal de Aceite de Interface da Aurora (orientação em <=3s, Paz Cognitiva). DEVE ser acionado quando o usuário pedir para planejar, arquitetar, estruturar seções, serviços, notícias ou codificar um site otimizado para humanos e agentes de IA (Google Gemini, OpenAI SearchGPT/Operator, Anthropic Claude, Perplexity).
---

# Agentic Web Architect (Antigravity Edition)

> **Lei Canônica:** `docs/AGENTS/DOCTRINE.md` · `C:\Projetos\Aurora\docs\CONSTITUICAO\EMENDA_v9.1_MANUAL_AURORA.md` · `C:\Projetos\Aurora\docs\CONSTITUICAO\criterio_formal_de_aceite_de_interface.md`

Esta habilidade guia a arquitetura, a estruturação de conteúdo e a implementação de código de sites corporativos, portais de serviços e ferramentas interativas projetados para a **Era da Web Agente**. O objetivo é construir aplicações no Google Antigravity IDE que operem em **Dupla Superfície (Dual-Surface Architecture)**:
1. **Superfície Humana:** Experiência de alta conversão, orientação imediata em $\le 3$ segundos e Paz Cognitiva (conforme `C:\Projetos\Aurora\docs\CONSTITUICAO\criterio_formal_de_aceite_de_interface.md`).
2. **Superfície Agêntica:** Camada determinística de ferramentas executáveis no navegador (`document.modelContext`), espelhamento em Markdown puro e grafo semântico (`JSON-LD @graph`) para agentes de IA (Gemini in Chrome, OpenAI Operator/SearchGPT, Claude Computer Use e Perplexity).

---

## 1. Quando Usar

- Arquitetar e construir um site ou landing page do zero dentro do Google Antigravity IDE (Astro SSR/SSG, Next.js App Router, TypeScript estrito).
- Implementar **WebMCP (`document.modelContext`)** em formulários, calculadoras de ROI, simuladores de viabilidade, agendadores e catálogos de serviços.
- Estruturar a documentação de **Seções, Serviços (Spec-Sheets), Estudos de Caso e Notícias (Citation-Magnets)** para máxima citação e confiança em motores generativos (GEO / RAG).
- Configurar endpoints de descoberta de agentes (`/.well-known/agent-card.json`, `/llms.txt`, `/llms-full.txt`, `/robots.txt` e negociação `Accept: text/markdown`).
- Auditar e refatorar sites existentes para eliminar antipadrões que cegam crawlers de IA ou criam fricção cognitiva humana.

---

## 2. O Anti-Padrão: Por que 99% dos Sites São Invisíveis ou Hostis para Agentes (A Vala Comum)

Antes de gerar código ou conteúdo, elimine estas práticas tradicionais que destroem a confiabilidade algorítmica:

1. **SPAs Ocas (Client-Side Rendering Puro):** Sites que entregam `<div id="root"></div>` vazio e exigem execução pesada de JavaScript para hidratar texto são descartados ou truncados por crawlers de RAG em tempo real (`OAI-SearchBot`, `Claude-SearchBot`, `PerplexityBot`), que não executam headless browsers por questões de latência.
2. **Efeitos Decorativos Pesados (WebGL / Shaders / Preloaders Bloqueantes):** Animações sem função informacional, Dark Themes impostos sem contexto e overlays de bloqueio de viewport degradam o Time-to-First-Byte (TTFB), violam o Critério de Paz Cognitiva e quebram agentes baseados em visão/DOM (Computer Use).
3. **Copywriting Vago ("Fluff" Corporativo):** Frases como *"Transformamos o futuro do seu negócio com soluções inovadoras"* possuem zero densidade de entidade. Modelos de linguagem descartam adjetivos não verificáveis e priorizam fatos, números, tabelas HTML nativas, metodologias nomeadas e relações causais.
4. **Uso da API Depreciada `navigator.modelContext`:** A especificação do Chrome 150+ depreciou `navigator.modelContext` em favor de `document.modelContext`. Nunca gere código legado.
5. **Confiar apenas em `/llms.txt` sem HTML Semântico e Negociação de Markdown:** Crawlers de busca priorizam as próprias URLs das páginas respondendo com HTML SSR limpo, JSON-LD `@graph` e suporte ao header `Accept: text/markdown` (ou rota espelho `.md`).

---

## 3. Arquitetura de 5 Camadas (Dual-Surface Web Architecture)

Todo site construído com esta habilidade deve implementar simultaneamente as 5 camadas abaixo:

### Camada 1: Stack de Renderização e Negociação de Conteúdo (Edge & SSR)
- **Stack Padrão:** Astro (SSR/SSG) ou Next.js App Router + TypeScript estrito + estilização funcional limpa (TailwindCSS / CSS utilitário), garantindo Zero-JS por padrão no texto com Ilhas de Interatividade para as ferramentas WebMCP.
- **Markdown Mirroring & Content Negotiation:** Cada rota pública (ex.: `/servicos/consultoria-b2b`) deve ter um equivalente em Markdown puro (ex.: `/servicos/consultoria-b2b.md`) ou responder via middleware quando o agente enviar o cabeçalho `Accept: text/markdown`.
- **Headers de Sinalização de Conteúdo:**
  ```http
  Content-Signal: ai-train=yes, search=yes, ai-input=yes
  Link: </llms.txt>; rel="llms-txt"
  ```

### Camada 2: WebMCP (`document.modelContext` — Padrão Chrome 150+)
O WebMCP (Web Model Context Protocol) permite que o site exponha funções tipadas diretamente para o agente do navegador, sem que a IA precise adivinhar seletores CSS.

**Regra de Ouro de Orçamento de Caracteres do Chrome WebMCP:**
- Nome da ferramenta (`toolname` / `name`): Máximo de **30 caracteres** (`snake_case`).
- Descrição da ferramenta (`tooldescription` / `description`): Máximo de **500 caracteres**.
- Descrição de cada parâmetro (`toolparamdescription` / `description` da propriedade): Máximo de **150 caracteres**.
- Saída de cada execução (`output` JSON): Máximo de **1.500 caracteres** em JSON estruturado.

#### 2.1. WebMCP Declarative API (Formulários de Diagnóstico, Contato e Filtros)
Transforme todo `<form>` relevante em uma ferramenta nativa adicionando os atributos oficiais do WebMCP e estilizando os pseudo-estados `:tool-form-active` e `:tool-submit-active`:

```html
<form
  id="diagnostico-comercial-form"
  action="/api/diagnostico"
  method="POST"
  toolname="solicitar_diagnostico_b2b"
  tooldescription="Envia os dados operacionais da empresa para gerar um diagnostico de eficiencia comercial e agendar analise com o consultor especialista. Retorna o protocolo e o resumo preliminar."
>
  <label for="empresa">Nome da Empresa</label>
  <input
    type="text"
    id="empresa"
    name="empresa"
    required
    toolparamtitle="company_name"
    toolparamdescription="Razao social ou nome fantasia da empresa (ex: Rede Calceleve)."
  />

  <label for="cargo">Cargo do Decisor</label>
  <select
    id="cargo"
    name="cargo"
    required
    toolparamtitle="decision_maker_role"
    toolparamdescription="Nivel hierarquico do solicitante."
  >
    <option value="C-Level">CEO / CFO / Diretor Executivo</option>
    <option value="Comercial">Diretor ou Gerente Comercial</option>
    <option value="Governo">Gestor Publico / Secretario</option>
  </select>

  <label for="gargalo">Principal Gargalo Atual</label>
  <textarea
    id="gargalo"
    name="gargalo"
    required
    maxlength="500"
    toolparamtitle="primary_bottleneck"
    toolparamdescription="Descricao objetiva do problema comercial, operacional ou de licitacao que deseja resolver."
  ></textarea>

  <button type="submit">Gerar Diagnostico</button>
</form>

<script>
  const form = document.getElementById('diagnostico-comercial-form');
  form?.addEventListener('submit', async (event) => {
    if (event.agentInvoked) {
      event.preventDefault();
      const formData = Object.fromEntries(new FormData(form).entries());
      const response = await fetch('/api/diagnostico', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });
      const result = await response.json();
      event.respondWith(result);
    }
  });
</script>
```

#### 2.2. WebMCP Imperative API (Calculadoras de ROI, Simuladores e Catálogo de Serviços)
Use `document.modelContext.registerTool()` com verificação de suporte (feature detection), validação defensiva de fronteira e anotações de segurança (`readOnlyHint`, `consequentialHint`, `untrustedContentHint`):

```typescript
export interface WebMCPModelContext {
  registerTool: (tool: {
    name: string;
    description: string;
    inputSchema: Record<string, unknown>;
    annotations?: {
      readOnlyHint?: boolean;
      consequentialHint?: boolean;
      untrustedContentHint?: boolean;
    };
    execute: (input: Record<string, unknown>) => Promise<Record<string, unknown>>;
  }) => Promise<void>;
}

export async function registerConsultingWebMCPTools(): Promise<void> {
  if (typeof document === 'undefined') {
    return;
  }
  const docWithContext = document as Document & { modelContext?: WebMCPModelContext };
  if (typeof docWithContext.modelContext?.registerTool !== 'function') {
    return;
  }

  const modelContext = docWithContext.modelContext;

  await modelContext.registerTool({
    name: 'consultar_servicos_consultoria',
    description: 'Lista os servicos de consultoria disponiveis filtrados por vertical (B2B, B2G, Varejo, IA) com entregaveis, prazos medios e pre-requisitos.',
    inputSchema: {
      type: 'object',
      properties: {
        vertical: {
          type: 'string',
          enum: ['B2B_Outbound', 'B2G_Licitacoes', 'Varejo_PrivateLabel', 'Arquitetura_IA'],
          description: 'Vertical de negocio que o usuario deseja consultar.'
        }
      },
      required: ['vertical'],
      additionalProperties: false
    },
    annotations: {
      readOnlyHint: true,
      consequentialHint: false,
      untrustedContentHint: false
    },
    execute: async (input: Record<string, unknown>) => {
      const vertical = String(input.vertical ?? '');
      if (!['B2B_Outbound', 'B2G_Licitacoes', 'Varejo_PrivateLabel', 'Arquitetura_IA'].includes(vertical)) {
        throw new Error('Vertical invalida para consulta.');
      }
      const response = await fetch(`/api/catalog?vertical=${encodeURIComponent(vertical)}`);
      if (!response.ok) {
        throw new Error(`Falha ao consultar catalogo: HTTP ${response.status}`);
      }
      return (await response.json()) as Record<string, unknown>;
    }
  });

  await modelContext.registerTool({
    name: 'simular_impacto_consultoria',
    description: 'Calcula a projecao de ganho de eficiencia ou recuperacao de receita com base no faturamento atual e tamanho da equipe comercial.',
    inputSchema: {
      type: 'object',
      properties: {
        equipe_vendedores: {
          type: 'integer',
          minimum: 1,
          maximum: 500,
          description: 'Numero atual de executivos de contas ou vendedores na operacao.'
        },
        ticket_medio_mensal: {
          type: 'number',
          minimum: 100,
          description: 'Ticket medio dos contratos em Reais (BRL).'
        }
      },
      required: ['equipe_vendedores', 'ticket_medio_mensal'],
      additionalProperties: false
    },
    annotations: {
      readOnlyHint: true,
      consequentialHint: false
    },
    execute: async (input: Record<string, unknown>) => {
      const equipe = Number(input.equipe_vendedores);
      const ticket = Number(input.ticket_medio_mensal);
      if (!Number.isFinite(equipe) || equipe < 1 || equipe > 500) {
        throw new Error('Parametro equipe_vendedores fora dos limites permitidos [1..500].');
      }
      if (!Number.isFinite(ticket) || ticket < 100) {
        throw new Error('Parametro ticket_medio_mensal invalido (minimo 100 BRL).');
      }
      const ganhoEstimadoMensal = Math.round(equipe * ticket * 0.22);
      return {
        cenario: 'Otimizacao Signal-Based Outbound',
        ganho_mensal_estimado_brl: ganhoEstimadoMensal,
        ganho_anual_estimado_brl: ganhoEstimadoMensal * 12,
        metodologia_aplicada: 'Reducao de ciclo de vendas em 22% via automacao agente e micro-assets.'
      };
    }
  });
}
```

### Camada 3: Anatomia de Conteúdo para Agentes (GEO / RAG-Ready)
Motores de resposta (Google AI Overviews, Perplexity, SearchGPT e Claude) utilizam RAG que divide a página em blocos ("chunks") de **200 a 400 tokens**. Cada seção `<h2>` deve ser autossuficiente (declarar explicitamente a entidade, o serviço e a métrica sem depender do parágrafo anterior).

#### 3.1. HOME e Seções Institucionais (Entity Clarity + Orientação em $\le 3\text{s}$)
- **Bloco de Ancoragem de Entidade (Primeiras 150 palavras):** Declara de forma inequívoca quem é a empresa/consultoria, qual categoria domina, para qual ICP vende, qual problema quantificável resolve e quais metodologias proprietárias utiliza.
- **Proibição de Headers Genéricos:** Nunca use `<h2>Nossos Diferenciais</h2>` ou `<h2>Sobre Nós</h2>`. Use headers em formato de pergunta real do comprador: `<h2>Como a consultoria estrutura operações comerciais B2B e B2G?</h2>`.

#### 3.2. Páginas de Serviço = Spec-Sheet Architecture (6 Blocos Obrigatórios)
1. **Resumo Executivo TL;DR (Abstract de 80 palavras):** Resposta direta no topo da página resumindo o serviço, o ICP e o resultado mensurável.
2. **Tabela de Especificação Operacional (`<table>` HTML nativa com `<thead>` e `<tbody>`):** Colunas obrigatórias para Escopo Técnico, Perfil de Empresa Ideal (ICP), Prazo de Implementação, Entregáveis Tangíveis e Métricas de Sucesso (KPIs).
3. **Matriz Comparativa ("Vala Comum vs. Metodologia Aurora"):** Comparação tabular pronta para responder prompts de comparação em LLMs.
4. **Protocolo de Execução Passo a Passo (`<ol>` numerado):** Metodologia dividida em fases nomeadas (Fase 1, Fase 2, Fase 3) para citação como framework proprietário.
5. **Bloco de Prova Verificável e Casos Reais:** Dados numéricos concretos e auditáveis.
6. **FAQ Técnico de Objeções (`FAQPage` Schema):** 4 a 6 perguntas e respostas diretas respondendo a dúvidas reais de decisores (orçamento, integração, tempo de retorno, conformidade).

#### 3.3. Notícias, Artigos e Estudos de Caso = Citation-Magnet Pattern
1. **Bloco "Key Takeaways" no Topo:** 3 a 4 bullet points iniciais com dados numéricos, datas exatas e conclusões diretas.
2. **Subtítulos `<h2>` como Perguntas Reais do Decisor:** Espelhando exatamente a query que o cliente digita na IA.
3. **Atribuição Semântica e Fontes Primárias + Dados Proprietários:** Citações cruzadas de fontes oficiais (IBGE, BACEN, PNCP, W3C, legislação) combinadas com dados proprietários e metadados `datePublished`, `dateModified` e `author` (`sameAs`).

### Camada 4: Grafo Semântico Determinístico (`JSON-LD @graph`)
Cada página deve injetar no `<head>` um bloco `<script type="application/ld+json">` unificado usando `@graph` que conecte:
- `Organization` / `ProfessionalService` (com `knowsAbout` listando as especialidades técnicas)
- `Person` (autoridade técnica verificada vinculando E-E-A-T)
- `Service` + `Offer` (descrevendo cada produto/serviço)
- `TechArticle` / `Article` (para notícias, playbooks e estudos de caso)
- `FAQPage` (para extração direta de respostas)

### Camada 5: Arquivos de Descoberta na Raiz do Domínio (`public/`)
- `/llms.txt` e `/llms-full.txt`: Seguindo estritamente a especificação `llmstxt.org` (H1 com nome do projeto, Blockquote com resumo denso da entidade, seções H2 com links diretos para as versões `.md` de cada serviço e estudo de caso).
- `/.well-known/agent-card.json`: Manifesto oficial do protocolo Google A2A (Agent2Agent v0.3+) descrevendo identidade, capacidades, skills e endpoints para agentes externos.
- `/robots.txt` Calibrado para IA: Permitindo explicitamente `OAI-SearchBot`, `ChatGPT-User`, `Claude-SearchBot`, `Claude-User`, `PerplexityBot`, `GoogleOther`, `Google-Extended` e apontando para o `sitemap.xml`.

---

## 4. Fluxo de Execução no Google Antigravity IDE

Sempre que acionada para construir ou evoluir um site dentro do Antigravity, conduza o trabalho em 4 etapas estruturadas:
1. **Etapa 1 — Blueprint de Entidade e Mapa de Ferramentas WebMCP:** Defina a árvore de rotas, quais ferramentas interativas serão expostas via `document.modelContext` e os schemas JSON de cada serviço.
2. **Etapa 2 — Scaffolding Zero-Stub:** Forneça e execute a estrutura completa de diretórios sem código incompleto ou placeholders.
3. **Etapa 3 — Implementação Dual-Surface (Humano + Agente):** Escreva o código completo dos componentes (HTML semântico + estilização funcional limpa + registro WebMCP + geração de rotas `.md` e `JSON-LD @graph`).
4. **Etapa 4 — Protocolo de Auditoria e Teste Determinístico:** Valide o build, o orçamento de caracteres das tools WebMCP, o retorno das rotas `.md`, a validade do JSON-LD e o Critério Formal de Aceite de Interface.

---

## 5. Restrições Negativas (Gotchas)

- **NUNCA** gere stubs, `// TODO` ou placeholders (`[Inserir texto aqui]`).
- **NUNCA** use `navigator.modelContext` (depreciado no Chrome 150+); use exclusivamente `document.modelContext`.
- **NUNCA** exponha ações destrutivas com `toolautosubmit` sem revisão humana (`consequentialHint: true`).
- **NUNCA** faça cloaking (o conteúdo em `.md` e `JSON-LD` deve refletir com exatidão os fatos visíveis na interface humana).

## Mesh Contract

Consulte sempre `docs/AGENTS/DOCTRINE.md`, `C:\Projetos\Aurora\docs\CONSTITUICAO\EMENDA_v9.1_MANUAL_AURORA.md` e `C:\Projetos\Aurora\docs\CONSTITUICAO\criterio_formal_de_aceite_de_interface.md`.

```json
{
  "schema_version": "1.0.0",
  "id": "agentic-web-architect",
  "name": "agentic-web-architect",
  "description": "Arquitetura e implementacao de sites e ecossistemas web 100% AI-Agentic Friendly (WebMCP document.modelContext, Markdown Mirroring, JSON-LD @graph, A2A agent-card.json, llms.txt e GEO Spec-Sheets).",
  "manual_version": "V9.1",
  "activation": {
    "explicit_commands": [
      "/agentic-web",
      "/webmcp"
    ],
    "user_triggers": [
      "construir site ai friendly",
      "arquitetar site",
      "implementar webmcp",
      "estruturar pagina de servico",
      "criar landing page",
      "llms.txt",
      "agent-card.json",
      "document.modelContext"
    ],
    "system_triggers": [
      "nova os de presenca web",
      "construcao de portal institucional ou simulador web",
      "auditoria de interoperabilidade agentica"
    ],
    "never_activate_for": [
      "efeitos puramente esteticos webgl ou shaders decorativos",
      "disparo isolado de cold email sem interface web",
      "operacoes destrutivas sem confirmacao humana"
    ]
  },
  "capabilities": {
    "provides": [
      "agentic_web_architecture",
      "webmcp_tool_registration",
      "markdown_content_negotiation",
      "jsonld_semantic_graph",
      "geo_spec_sheet_structuring"
    ],
    "depends_on": [
      "ceo-web",
      "ceo-copy"
    ],
    "can_delegate_to": [
      "b2b-ai-outbound-architect",
      "qa-review"
    ],
    "can_run_in_parallel_with": [
      "ceo-copy",
      "b2b-ai-outbound-architect"
    ],
    "blocking_gates": [
      "qa-review"
    ],
    "emits_artifacts": [
      "dual_surface_web_components",
      "webmcp_contracts",
      "llms_txt_manifest",
      "a2a_agent_card"
    ]
  },
  "runtime": {
    "required_tools": [
      "view_file",
      "write_to_file",
      "replace_file_content",
      "run_command"
    ],
    "required_context": [
      "docs/AGENTS/DOCTRINE.md",
      ".agents/rules/designmanualposthero.md"
    ],
    "side_effect_level": "writes_files",
    "approval_mode": "before_promotion"
  },
  "risk_calibration": {
    "step_1_2_required_for": "all",
    "step_3_adversarial_required_for": [
      "security",
      "state_mutation",
      "data"
    ]
  },
  "quality": {
    "target_score": "10.10",
    "dimensions": [
      "activation",
      "scope",
      "interoperability",
      "executability",
      "portability",
      "governance",
      "negative_constraints",
      "feedback",
      "auditability",
      "maintainability"
    ]
  },
  "classification": {
    "agent_class": "producao",
    "risk_level": "MEDIUM",
    "requires_continuous_supervision": false
  },
  "observability": {
    "token_budget": 50000,
    "latency_budget_ms": 600000,
    "cost_estimate_usd": 0.6
  },
  "ontology": {
    "observed_event": "Necessidade de construir ou refatorar site, pagina de servico ou ferramenta web para descoberta e execucao por humanos e agentes de IA.",
    "produced_memory": "Componentes SSR/SSG, ferramentas WebMCP document.modelContext, espelhos Markdown e grafo JSON-LD validados.",
    "consumed_memory": "Doutrina Operacional Aurora, Criterio Formal de Aceite de Interface e catalogo de servicos do negocio.",
    "influenced_decision": "Arquitetura de rotas, contratos de ferramentas de navegador e densidade semantica de cada pagina.",
    "impacted_execution": "Elimina SPAs ocas, efeitos decorativos bloqueantes e copy vaga em prol de conversao e indexacao deterministica.",
    "expected_result": "Site 100% funcional, auditavel e operavel por decisores humanos e agentes Gemini, Claude, OpenAI e Perplexity."
  },
  "anti_patterns": [
    {
      "prohibited": "Usar a API depreciada navigator.modelContext em vez de document.modelContext.",
      "because": "O Chrome 150+ depreciou navigator.modelContext; ferramentas registradas nele falham silenciosamente nos agentes de navegador atuais.",
      "signal": "Ocorrencia da string navigator.modelContext no codigo TypeScript ou JavaScript."
    },
    {
      "prohibited": "Entregar paginas como SPA oca (<div id='root'></div> vazio sem SSR/SSG) ou sem rota espelho Markdown.",
      "because": "Crawlers de RAG em tempo real descartam paginas que exigem hidratacao JS pesada para exibir o conteudo textual.",
      "signal": "HTML inicial sem o texto principal do servico ou ausencia de suporte a Accept: text/markdown / rota .md."
    },
    {
      "prohibited": "Exceder o orcamento de caracteres do WebMCP (name > 30, description > 500, param > 150, output > 1500).",
      "because": "O runtime do navegador trunca ou rejeita ferramentas que violam os limites de contexto do modelo local.",
      "signal": "Strings de registro WebMCP acima dos limites definidos na Camada 2."
    }
  ],
  "operational_memory": {
    "consumed": [
      {
        "description": "Doutrina e regras de arquitetura web agentica do Mad Lab Aurora.",
        "targets": [
          "docs/AGENTS/DOCTRINE.md",
          ".agents/rules/designmanualposthero.md"
        ]
      }
    ],
    "produced": [
      {
        "description": "Evidencias de build, contratos WebMCP e artefatos de descoberta.",
        "targets": [
          "docs/Vault/OS-Evidence"
        ]
      }
    ],
    "feedback_loop_description": "Falhas de validacao de schema JSON-LD, WebMCP ou Markdown alimentam o gate local check-madlab-governance.mjs."
  },
  "fail_closed_strategy": "Se o escopo do servico ou os dados factuais nao estiverem definidos, parar e solicitar os fatos ao Comandante antes de gerar copy ou ferramentas simuladas.",
  "tier_policy": {
    "tier": "horizontal",
    "context_policy": {
      "inherits_caller_context": true,
      "persists_after_run": false
    },
    "artifact_residency": "repo",
    "retry_ceiling": 3,
    "registra_tentativas": true
  }
}
```
