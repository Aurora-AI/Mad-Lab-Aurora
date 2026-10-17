# CLAUDE.md — Doutrina e Governança Mad Lab Aurora para Claude Code

> Gerado a partir de `docs/AGENTS/DOCTRINE.md`. **Não edite este arquivo isoladamente** — edite a fonte
> e rode `node scripts/sync-doctrine.mjs`. O gate `scripts/check-madlab-governance.mjs` falha se divergir.
> Todo agente, em qualquer IDE, opera sob estas regras. Não há papel exclusivo por ferramenta.

<!-- DOCTRINE:START -->
## Lei e Subordinação Canônica

- **Fábrica Mãe (Ozzmosis / Aurora):** `C:\Projetos\Aurora`
- **Manual e Emenda Vigentes da Fábrica:** `C:\Projetos\Aurora\docs\CONSTITUICAO\MANUAL_DE_CONSTRUCAO_AURORA_v9.0.md` e `C:\Projetos\Aurora\docs\CONSTITUICAO\EMENDA_v9.1_MANUAL_AURORA.md` (**a Emenda v9.1 prevalece sobre o Manual**)
- **Doutrina da Fábrica:** `C:\Projetos\Aurora\docs\AGENTS\DOCTRINE.md`
- **Critério Formal de Aceite de Interface:** `C:\Projetos\Aurora\docs\CONSTITUICAO\criterio_formal_de_aceite_de_interface.md`
- **Schema de Contratos de Skills:** `C:\Projetos\Aurora\docs\specs\skill_mesh\skill.schema.json`
- **Decisão de Soberania e Integração Local:** `docs/Vault/Decisions/DEC-MADLAB-AGENTIC-MESH-001.md` e `docs/Vault/Decisions/DEC-MADLAB-AGENTIC-PIVOT-002.md`
- **Política de Domínio e Toolbelt Consumer:** `.aurora/domain-policy.json` e `.aurora/toolbelt-consumer.json`
- **Regra Always-On de Arquitetura Web Agêntica:** `.agents/rules/designmanualposthero.md`

> **Regra de Conflito:** Qualquer documento legado em `docs/brand/` ou referências antigas a `Dark Editorial`, `Dark Theme`, `Mad Lab Theme`, `Three.js r128` ou efeitos WebGL decorativos estão **descontinuados (`deprecated: true`)** e são integralmente sobrepostos por esta Doutrina.

---

## Parte I — Doutrina Operacional Aurora (Sincronizada com a Emenda v9.1)

### 1. Sem separação de papel por IDE
Não existe "a IDE que planeja" e "a IDE que executa". Qualquer agente, em qualquer IDE (Antigravity, Claude Code, CODEX), é executor pleno: analisa, planeja, executa e prova, usando o motor nativo da IDE sem introduzir chaves de API hardcoded no código.

### 2. O código é a realidade; a execução é a prova
- **Antes de responder, planejar ou escrever SPEC: leia o código no disco.** Contexto de conversa não substitui o estado do repositório.
- **Antes de afirmar que algo funciona: execute e cole a saída.** Ler código e concluir que está correto não é evidência. Relatório de agente não é evidência.
- **Checagem literal de referências:** Nunca declarar um ponteiro ou caminho como válido sem testar a existência física da string literal no disco (`Test-Path`).
- **Execução obrigatória de scripts:** Nunca classificar um script como operacional sem executá-lo no terminal e verificar `EXIT=$?`. Nunca capturar resultado com pipe (`cmd | tail`); use execução direta ou redirecionamento verificando o código de saída.

### 3. Plano ↔ relatório em mapeamento 1:1
Todo relatório de conclusão enumera **cada item do plano** e marca um dos três estados:
- `feito` — com a evidência de execução anexada (saída de comando colada)
- `não feito` — com o motivo
- `parcial` — com o que ficou de fora, explicitamente

### 4. Proibido ficar verde por remoção
É proibido fazer um gate passar removendo o que ele verifica: apagar o passo que falha, excluir o campo que aponta lacuna, reduzir a suíte ou afrouxar o critério. Gate verde por subtração mente.

### 5. Vault é append-only
Nada é deletado nem reescrito em `docs/Vault/`. Documento ou skill obsoleta recebe `deprecated: true`. Registro histórico (caminho, hash, data de execução) é fato do passado — não se corrige, complementa-se com campo ou adendo novo.

### 6. Toda OS declara o que NÃO faz e o Blast Radius
Toda OS de risco MÉDIO+ exige seção de não-escopo explícita, bloco `<!-- RESTRICOES:INICIO --> ... <!-- RESTRICOES:FIM -->` e, no `PLAN.md`, o bloco `<!-- BLAST_RADIUS:INICIO --> ... <!-- BLAST_RADIUS:FIM -->`, validados via `C:\Projetos\Aurora\packages\tooling\scripts\check-plan-conformance.mjs`.

### 7. Reformule antes de construir
Antes de escrever a primeira linha de plano ou código, devolva: o que entendeu em termos literais, o que isto explicitamente **não** é, e quais suposições fez onde o pedido era omisso.

### 8. Twin check
Ao corrigir um defeito, procure o mesmo padrão no resto do repositório e reporte o que achou.

### 9. Chamada de julgamento é declarada, nunca disfarçada
Distinga **Lacuna** (falta o dado → peça o dado) de **Fora do campo** (o dado está completo e a variável decisiva não está nele → escale para o Comandante).

### 10. Ambiguidade: pare e reporte
Se a OS ou o pedido é ambíguo, não interprete. Pare, aponte a ambiguidade e proponha as leituras possíveis.

### 11. Trustware — confirmação humana
Exigem confirmação explícita: `rm`/`rmdir`/`del`, `git push`, `git reset --hard`, rebase, alterações em secrets/env e qualquer ação destrutiva ou irreversível. Livres: leitura, lint, typecheck, teste, build, `npm ci`.

### 12. Regras de Fronteira com a Fábrica (`C:\Projetos\Aurora`)
- **Proibido** recriar ou instanciar cópias do runtime do Álvaro localmente.
- **Proibido** criar MCP Gateway de observabilidade próprio.
- **Proibido** instanciar Qdrant ou Vault global paralelo sem OS formal.
- **Proibido** executar auto-repair autônomo em produção.
- **Proibido** promover KIs automaticamente para a memória global da fábrica.
- **Proibido** entregar código incompleto, stubs (`// TODO`, `pass`, placeholders) ou componentes sem tipagem estrita (Zero-Stub).
- Consumo da fábrica: exclusivamente via `.aurora/toolbelt-consumer.json`. Ausência de serviço gera `FACTORY_TOOL_UNAVAILABLE` com fallback explícito.

### 13. Validação em Duas Vias e Suíte de Sabotagem (`reprova`)
Todo validador, formatador, calculadora ou gate novo nasce com um caso adversarial que o force a `EXIT=1` (suíte `reprova`). Auditar que o gate roda (`EXIT=0`) não prova que o gate pega violações (`EXIT=1`).

---

## Parte II — Diretriz de Engenharia do Mad Lab Aurora: Produção, Conversão e Web 100% AI-Agentic Friendly

### 1. Identidade Operacional
O **Mad Lab Aurora** é a **Unidade de Engenharia de Presença Digital Agêntica, Aquisição B2B/B2G e Sistemas de Conversão da Aurora**.
Construímos sites, landing pages, portais de serviços, simuladores de negócio e máquinas de prospecção voltados para **produtividade, resultados, pesquisa e descoberta por Humanos e Agentes de IA** (Google Gemini, Anthropic Claude, OpenAI SearchGPT/Operator, Perplexity).

### 2. Arquitetura Web Dual-Surface (5 Camadas Obrigatórias)
Todo site ou landing page construído neste repositório segue obrigatoriamente a skill `.aurora/skills/agentic-web-architect/SKILL.md`:

1. **Camada 1 — Stack SSR/SSG & Negociação de Conteúdo:**
   - Renderização imediata de HTML semântico (Astro SSR/SSG ou Next.js App Router + TypeScript estrito + estilização funcional limpa). Proibido entregar SPAs ocas (`<div id="root"></div>` vazio).
   - **Markdown Mirroring:** Toda rota pública (ex.: `/servicos/x`) deve responder ao header `Accept: text/markdown` ou possuir rota espelho `/servicos/x.md` com YAML Frontmatter + Markdown limpo + JSON-LD.
   - **Headers HTTP:** `Content-Signal: ai-train=yes, search=yes, ai-input=yes` e `Link: </llms.txt>; rel="llms-txt"`.
2. **Camada 2 — WebMCP (`document.modelContext` — Padrão Chrome 150+):**
   - **Proibido** usar `navigator.modelContext` (depreciado). Usar exclusivamente `document.modelContext`.
   - **Orçamento de caracteres:** `name`/`toolname` ≤ 30 chars (`snake_case`); `description`/`tooldescription` ≤ 500 chars; `toolparamdescription` ≤ 150 chars; JSON output ≤ 1.500 chars.
   - **Declarative API:** Formulários HTML instrumentados com `toolname`, `tooldescription`, `toolparamtitle`, `toolparamdescription`, interceptando `SubmitEvent.agentInvoked` e respondendo via `event.respondWith(payload)`.
   - **Imperative API:** Simuladores de ROI, calculadoras e catálogos registrados via `document.modelContext.registerTool()` com `inputSchema` estrito e `annotations: { readOnlyHint, consequentialHint }`.
3. **Camada 3 — Anatomia de Conteúdo para RAG e Citação (GEO):**
   - Blocos autossuficientes de 200–400 tokens (alta densidade de entidade, zero adjetivos vazios).
   - **Páginas de Serviço = Spec-Sheets:** (1) Resumo Executivo TL;DR de 80 palavras; (2) Tabela HTML nativa `<table>` com Escopo, ICP, Prazo, Entregáveis e KPIs; (3) Matriz Comparativa tabular ("Vala Comum vs. Metodologia Aurora"); (4) Protocolo de execução numerado `<ol>`; (5) Prova verificável com números reais; (6) FAQ técnico (`FAQPage`).
   - **Notícias e Estudos de Caso = Citation-Magnets:** (1) Bloco Key Takeaways quantificado no topo; (2) Subtítulos `<h2>` como perguntas reais do decisor; (3) Citação de fontes primárias oficiais + dados proprietários com `datePublished` e `dateModified`.
4. **Camada 4 — Grafo Semântico Determinístico (`JSON-LD @graph`):**
   - Bloco `<script type="application/ld+json">` unificado conectando `Organization`, `ProfessionalService` (com `knowsAbout`), `Person`, `Service` + `Offer`, `TechArticle` e `FAQPage`.
5. **Camada 5 — Endpoints de Descoberta na Raiz (`public/`):**
   - `/.well-known/agent-card.json` (Protocolo Google A2A v0.3+).
   - `/llms.txt` e `/llms-full.txt` (padrão llmstxt.org apontando para as rotas `.md`).
   - `/robots.txt` permitindo explicitamente `OAI-SearchBot`, `ChatGPT-User`, `Claude-SearchBot`, `Claude-User`, `PerplexityBot`, `GoogleOther` e `Google-Extended`.

### 3. Interface Humana e Outbound Pós-IA
- **Aceite de Interface Humana:** Toda tela obedece a `C:\Projetos\Aurora\docs\CONSTITUICAO\criterio_formal_de_aceite_de_interface.md` — Orientação Imediata em ≤ 3s, Paz Cognitiva (ausência de tensão, sem dark theme imposto, sem animações decorativas ou bloqueio de viewport), Não-Punição Visual, Hierarquia Silenciosa, Economia Cognitiva e Auditabilidade de Verdade.
- **Outbound Pós-IA:** Toda campanha comercial e fluxo de prospecção obedece a `.aurora/skills/b2b-ai-outbound-architect/SKILL.md` — Signal-Based Selling, Micro-Assets de Valor Assíncronos, protocolo Zero-HTML Plain-Text (sem tracking pixels, sem mceWrapper, sem links no 1º contato frio) e 1ª frase projetada para o AI Inbox Summarizer (Gemini Workspace / Microsoft Copilot).

### 4. Os 4 Gates de Qualidade de Produção (Não Negociáveis)

| Gate | Agente / Skill | Pergunta Central de Validação |
|---|---|---|
| **1. Arquitetura & Zero-Stub** | `agentic-web-architect` | "O código está 100% completo, tipado, sem stubs (`TODO`/placeholders) e renderiza em SSR/SSG imediato?" |
| **2. Interoperabilidade Agêntica** | `agentic-web-architect` / `ceo-web` | "As ferramentas `document.modelContext`, rotas `.md`, JSON-LD `@graph`, `/llms.txt` e `/.well-known/agent-card.json` estão válidos e testáveis?" |
| **3. Densidade de Entidade & Paz Cognitiva** | `ceo-copy` / `ceo-web` | "Cada página opera como Spec-Sheet ou Citation-Magnet e atende ao Critério Formal de Aceite de Interface (orientação ≤ 3s, zero ruído)?" |
| **4. Distribuição & QA em Contexto Frio** | `b2b-ai-outbound-architect` / `qa-review` | "O ativo possui Micro-Asset / fluxo Plain-Text anti-spam e passou pela reprodução adversarial do `qa-review`?" |

### 5. Skills Operacionais no Repositório (`.aurora/skills/`)

| Skill | Status | Papel na Produção |
|---|---|---|
| `agentic-web-architect` | **active** | Arquitetura Web Dual-Surface, WebMCP (`document.modelContext`), GEO, JSON-LD `@graph`, `llms.txt`, `agent-card.json` |
| `b2b-ai-outbound-architect` | **active** | Outbound Pós-IA, Signal-Based Selling, Micro-Assets e sequências Zero-HTML Plain-Text |
| `ceo-web` | **active** | Arquitetura de conversão, clareza em 3s, estrutura de rotas e jornada do decisor |
| `ceo-copy` | **active** | Escrita técnica de alta densidade de entidade (Spec-Sheets, Citation-Magnets, FAQs, teses executivas) |
| `ceo-marketing` | **active** | Canal, distribuição, ICP e Account-Based Intelligence |
| `ceo-product-owner` | **active** | Escopo de produto, priorização de calculadoras, simuladores e micro-ferramentas |
| `ceo-business-partner` | **active** | Estratégia competitiva, precificação e viabilidade comercial |
| `ceo-discovery-specialist` | **active** | Turn-1 discovery, extração de requisitos técnicos e sinais de mercado |
| `engenheiro-reverso` | **active** | Engenharia reversa de sistemas legados, funis concorrentes e extração de ontologia |
| `qa-review` | **active** | Gate de aceitação em contexto frio (3 degraus + reprodução adversarial) |
| `agent-reflexion-cost` | **active** | Registro de custo no Token Ledger (`docs/Vault/Token-Ledger/`) |
| `agent-thread-recorder` | **active** | Registro de memória de sessão (`docs/Vault/Threads/`) |
| `ceo-design`, `ceo-effects`, `ceo-3d`, `ceo-art-direction`, `cinematic-grammar`, `taste-design`, `design-md`, `ceo-critique-theater` | **deprecated** | Descontinuadas (`deprecated: true`) — preservadas apenas para conformidade histórica append-only |

### 6. Comandos de Verificação Local

```powershell
# 1. Verificar conformidade entre OS e PLAN (usando o gate canônico da fábrica Aurora)
node "C:\Projetos\Aurora\packages\tooling\scripts\check-plan-conformance.mjs" --os <caminho-os.md> --plan <caminho-plan.md>

# 2. Verificar sincronia da doutrina, contratos de skills WebMCP/GEO e depreciações no MadLabAurora
node scripts/check-madlab-governance.mjs

# 3. Executar suíte de sabotagem (reprova / EXIT=1) do gate de governança
node scripts/test-madlab-governance-reprova.mjs
```
<!-- DOCTRINE:END -->
