# DEC-MADLAB-AGENTIC-PIVOT-002
**Título:** Transição do Mad Lab Aurora para Engenharia de Presença Web Agêntica (WebMCP / GEO), Outbound Pós-IA e Doutrina Operacional Aurora v9.1  
**Status:** Aprovado  
**Data:** 16 de Outubro de 2026  
**OS de Referência:** `OS-MADLAB-AGENTIC-PIVOT-20261016-001`  
**Complementa:** `docs/Vault/Decisions/DEC-MADLAB-AGENTIC-MESH-001.md`

---

## 1. Decisão

Por determinação do Comandante, o **Mad Lab Aurora** encerra sua fase experimental centrada em estética artística (`Dark Editorial`, `Dark Theme`, `Mad Lab Theme`, `Three.js r128`, `WebGL`, `GSAP` decorativo) e passa a operar como **Unidade de Engenharia de Presença Digital Agêntica, Aquisição B2B/B2G e Conversão Determinística**, subordinada à **Doutrina Operacional Aurora (`C:\Projetos\Aurora\docs\AGENTS\DOCTRINE.md` e `EMENDA_v9.1_MANUAL_AURORA.md`)**.

1. **Preservação Integral das Conexões com a Fábrica Aurora (`C:\Projetos\Aurora`):**
   - Mantêm-se inalteradas as regras de soberania de domínio (`DEC-MADLAB-AGENTIC-MESH-001.md`), o consumo via `.aurora/toolbelt-consumer.json`, os servidores MCP, a regra append-only do Vault (`docs/Vault/`) e o registro em `docs/Vault/Token-Ledger/` e `docs/Vault/Threads/`.
2. **Adoção da Doutrina Operacional Unificada (`docs/AGENTS/DOCTRINE.md`):**
   - `AGENTS.md`, `GEMINI.md` e `CLAUDE.md` na raiz do `MadLabAurora` passam a ser sincronizados a partir de `docs/AGENTS/DOCTRINE.md`, incorporando as 13 cláusulas da Doutrina Aurora (Sem separação de papel por IDE, Execução como prova, Mapeamento 1:1 plano↔relatório, Proibido ficar verde por remoção, Vault append-only, Não-escopo explícito, Reformulação prévia, Twin check, Julgamento declarado, Parada em ambiguidade, Trustware, Contrato de repositório, e Validação em Duas Vias / Suíte de Sabotagem `reprova`).
3. **Arquitetura Web Dual-Surface (100% AI-Agentic Friendly) e Outbound Pós-IA:**
   - Todo site, landing page, catálogo de serviços ou portal construído no `MadLabAurora` deve seguir a arquitetura de 5 camadas guiada pela skill `agentic-web-architect`:
     - **Camada 1 (Edge & SSR):** HTML semântico imediato (Astro / Next.js App Router + TypeScript estrito), espelhamento nativo em Markdown (`Accept: text/markdown` e rotas `.md`) e header `Content-Signal: ai-train=yes, search=yes, ai-input=yes`.
     - **Camada 2 (WebMCP Chrome 150+):** Uso exclusivo de `document.modelContext` (Declarative API em `<form>` com `toolname`, `tooldescription`, `toolparamtitle`, `toolparamdescription`, `SubmitEvent.agentInvoked` e `respondWith`; Imperative API via `document.modelContext.registerTool` respeitando limites de 30/500/150/1500 caracteres). Proibido usar `navigator.modelContext`.
     - **Camada 3 (Anatomia RAG / GEO):** Páginas de serviço estruturadas como **Spec-Sheets** (TL;DR de 80 palavras, `<table>` nativa de escopo/KPIs, Matriz Comparativa, `<ol>` de metodologia nomeada, FAQPage) e notícias/estudos de caso estruturados como **Citation-Magnets** (Key Takeaways quantificados, `<h2>` em formato de pergunta do decisor, fontes primárias).
     - **Camada 4 (Grafo Semântico):** Injeção determinística de `<script type="application/ld+json">` com `@graph` (`Organization`, `ProfessionalService`, `Person`, `Service`, `TechArticle`, `FAQPage`).
     - **Camada 5 (Descoberta na Raiz):** `/.well-known/agent-card.json` (Google A2A v0.3+), `/llms.txt`, `/llms-full.txt`, e `/robots.txt` liberado para `OAI-SearchBot`, `ChatGPT-User`, `Claude-SearchBot`, `Claude-User`, `PerplexityBot`, `GoogleOther`, `Google-Extended`.
   - A interface humana rege-se pelo **Critério Formal de Aceite de Interface da Aurora** (`C:\Projetos\Aurora\docs\CONSTITUICAO\criterio_formal_de_aceite_de_interface.md`): Orientação Imediata (≤ 3s), Paz Cognitiva, Não-Punição Visual, Hierarquia Silenciosa, Economia Cognitiva e Auditabilidade de Verdade.
   - As campanhas de aquisição e prospecção regem-se pela skill `b2b-ai-outbound-architect` (Signal-Based Selling, Micro-Assets de Valor Assíncronos, Zero-HTML Plain-Text imune a EXCHANGELABS/Defender e otimização para AI Inbox Summarizers).
4. **Descontinuação sem Deleção (`deprecated: true`):**
   - Documentos e skills exclusivamente estéticos (`MANUAL_DA_AGENCIA.md`, `mad-lab-aurora-dna-v2.1.0.md`, `ceo-design`, `ceo-effects`, `ceo-3d`, `ceo-art-direction`, `cinematic-grammar`, `taste-design`, `design-md`, `ceo-critique-theater`) recebem `deprecated: true` / `status: deprecated`, preservando o histórico append-only.
