---
trigger: always_on
---

# REGRA ALWAYS-ON — ARQUITETURA WEB AGÊNTICA, CONVERSÃO E ACEITE DE INTERFACE (MAD LAB AURORA v3.0)

> **Subordinação Canônica:** `docs/AGENTS/DOCTRINE.md` | `C:\Projetos\Aurora\docs\CONSTITUICAO\criterio_formal_de_aceite_de_interface.md` | `.aurora/skills/agentic-web-architect/SKILL.md`
> **Depreciação Explícita:** As regras antigas de `Dark Editorial`, `Dark Theme` imposto, `Mad Lab Theme`, `EQ de Frequências` escuro/claro cinematográfico, `Three.js r128` e efeitos WebGL/GSAP decorativos estão **descontinuadas (`deprecated: true`)**.

---

## 1. CRITÉRIO FORMAL DE ACEITE DE INTERFACE HUMANA (6 PRINCÍPIOS INEGOCIÁVEIS)

Toda página, ferramenta, calculadora ou sistema web construído no Mad Lab Aurora obedece a `C:\Projetos\Aurora\docs\CONSTITUICAO\criterio_formal_de_aceite_de_interface.md`:

1. **Orientação Imediata ($\le 3\text{s}$):** Nos primeiros 3 segundos, sem rolar e sem clicar, o visitante humano sabe: (a) onde está e o que este produto/serviço faz; (b) para quem é (ICP explícito); (c) qual é o próximo passo concreto.
2. **Paz Cognitiva:** Ausência de tensão visual desnecessária. Fundo claro funcional de alta legibilidade como padrão operacional; contraste WCAG AA/AAA; zero animações que sequestrem o scroll (proibido scroll-jacking, preloader bloqueante ou Canvas WebGL decorativo).
3. **Não-Punição Visual:** Erros de formulário ou estados vazios orientam a resolução em linguagem clara e calma, sem alarmismo visual.
4. **Hierarquia Silenciosa:** Espaçamento, tipografia funcional (sans-serif/serif de leitura imediata + monospace tabular `font-variant-numeric: tabular-nums` para dados) e tabelas HTML nativas organizam a atenção sem ornamentos.
5. **Economia Cognitiva:** Um único objetivo de conversão primário por tela/seção. Nenhum elemento decorativo compete com a prova factual ou com a ferramenta interativa.
6. **Auditabilidade de Verdade:** Nenhum número, métrica, prazo ou prova social pode ser fictício ou placeholder.

---

## 2. ARQUITETURA DUAL-SURFACE (100% AI-AGENTIC FRIENDLY)

Todo ativo web é construído simultaneamente para **Decisores Humanos** e **Agentes de IA** (Google Gemini, Anthropic Claude, OpenAI SearchGPT/Operator, Perplexity):

1. **SSR/SSG & Markdown Mirroring:**
   - Renderização imediata de HTML semântico (`<main>`, `<article>`, `<section>`, `<table>`, `<dl>`). Proibido entregar SPAs ocas (`<div id="root"></div>`).
   - Toda rota pública responde a `Accept: text/markdown` ou possui rota espelho `.md` com YAML Frontmatter + Markdown limpo + JSON-LD.
   - Headers HTTP: `Content-Signal: ai-train=yes, search=yes, ai-input=yes` e `Link: </llms.txt>; rel="llms-txt"`.
2. **WebMCP (`document.modelContext` — Padrão Chrome 150+):**
   - **Proibido** usar `navigator.modelContext` (depreciado). Usar exclusivamente `document.modelContext`.
   - **Orçamento de caracteres:** `name`/`toolname` $\le 30$ chars (`snake_case`); `description`/`tooldescription` $\le 500$ chars; `toolparamdescription` $\le 150$ chars; JSON output $\le 1.500$ chars.
   - Formulários usam a API Declarativa (`toolname`, `tooldescription`, `SubmitEvent.agentInvoked` + `event.respondWith`) e calculadoras/simuladores usam a API Imperativa (`document.modelContext.registerTool` com `readOnlyHint` e `consequentialHint`).
3. **Anatomia GEO (RAG-Ready em blocos autossuficientes de 200–400 tokens):**
   - **Páginas de Serviço = Spec-Sheets (6 blocos):** (1) TL;DR de 80 palavras; (2) Tabela HTML nativa `<table>` (Escopo, ICP, Prazo, Entregáveis, KPIs); (3) Matriz Comparativa tabular ("Vala Comum vs. Metodologia Aurora"); (4) Protocolo numerado `<ol>`; (5) Prova verificável quantificada; (6) `FAQPage` técnico.
   - **Artigos e Estudos de Caso = Citation-Magnets:** Key Takeaways quantificado no topo + `<h2>` como perguntas reais do decisor + fontes primárias oficiais e dados proprietários com `datePublished`/`dateModified`.
4. **Grafo Semântico & Endpoints de Raiz:**
   - Bloco único `<script type="application/ld+json">` com `@graph` (`Organization`, `ProfessionalService`, `Person`, `Service`, `Offer`, `TechArticle`, `FAQPage`).
   - Raiz `public/` com `/.well-known/agent-card.json` (A2A v0.3+), `/llms.txt`, `/llms-full.txt` e `/robots.txt` liberado para bots de busca e agentes de IA.