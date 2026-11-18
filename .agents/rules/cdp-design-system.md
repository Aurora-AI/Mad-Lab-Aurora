---
trigger: always_on
---

# REGRA DE ENGENHARIA REVERSA VISUAL E CLONAGEM ESTRUTURAL DE DESIGN SYSTEM (CDP + CONTENT-OVER-CLONE)

> **Subordinação Canônica:** `docs/AGENTS/DOCTRINE.md` | `C:\Projetos\Aurora\docs\CONSTITUICAO\EMENDA_v9.1_MANUAL_AURORA.md` | `C:\Projetos\Aurora\docs\CONSTITUICAO\criterio_formal_de_aceite_de_interface.md` | `.aurora/skills/cdp-design-system-extractor/SKILL.md`

---

## 1. PRECEDÊNCIA CONSTITUCIONAL E CANÔNICA

Quando qualquer agente no Google Antigravity for instruído a extrair design de referências visuais (Awwwards, Godly, Stripe, Linear) ou gerar um Design System em HTML, vigora a seguinte ordem de precedência:

$$\text{Doutrina e Emenda v9.1} \;\longrightarrow\; \text{Paz Cognitiva (Aceite de Interface)} \;\longrightarrow\; \text{Regras de Governança} \;\longrightarrow\; \text{Design System Aprovado} \;\longrightarrow\; \text{Implementação}$$

Nenhum elemento decorativo externo, tema escuro de alta tensão visual, animação de scroll (scroll-jacking) ou efeito WebGL invasivo pode sobrepor os princípios de **Orientação em $\le 3\text{s}$**, **Legibilidade WCAG AA/AAA** e **Paz Cognitiva**.

---

## 2. ARQUITETURA OBRIGATÓRIA DE 4 ARTEFATOS + TOPOLOGIA ESTRUTURAL

Toda extração visual via Chrome DevTools Protocol (CDP) e Playwright deve preservar a separação epistemológica entre a **telemetria observada** (imutável) e os **artefatos compilados** (adaptados à Aurora):

1. **`design-telemetry.json` (`cdp.telemetry.v1`):** Observação bruta e auditável extraída diretamente do motor Blink. Contém tokens computados, curvas `cubic-bezier`, durações de transição, `@keyframes`, deltas medidos via `CSS.forcePseudoState`, **`typography_roles` (4 papéis semânticos)**, **`font_assets`**, **`section_blueprints` (DOM/CSS Skeletons)** e **`active_svg_filters` (filtros vinculados a regras CSS)**.
2. **`visual-shader-manifest.json` (`cdp.shaders.v1`):** Código-fonte GLSL puro de Shaders WebGL1/WebGL2 interceptados em runtime, dimensões de viewport e screenshots 2x DPI emparelhados (repouso vs. hover).
3. **`design-tokens.json` (`w3c.design-tokens.v1`):** Contrato semântico estruturado para CSS Variables e design systems agênticos (`colors`, `typography`, `spacing`, `radii`).
4. **`design-system.html` (`html5.living-spec.v1`):** Living Style Guide executável em arquivo único contendo:
   - Tokens `:root` populados com as cores reais da referência (sem destruição por hardcodes `#f8fafc`).
   - 4 Variáveis tipográficas estritas: `--ds-font-display`, `--ds-font-sans`, `--ds-font-hand`, `--ds-font-mono`.
   - Demonstração ativa de filtros SVG extraídos aplicados em classes CSS (`.ds-effect-{id}`).
   - Catálogo de Blueprints de Seção com slots tipados (`{{SLOT_TITLE}}`, `{{SLOT_BODY}}`, etc.).
   - Suporte a formulários declarativos WebMCP (`:tool-form-active`).

---

## 3. PROTOCOLO DE TRANSPLANTE DE CONTEÚDO (CONTENT-OVER-CLONE)

A squad de agentes opera no modelo **Content-Over-Clone**, garantindo separação absoluta entre forma e conteúdo:

1. **Proibição de "Card Stacking" Monotônico:** É estritamente proibido construir uma página inteira empilhando repetidamente `<section class="card">` idênticos em coluna única. A página final DEVE seguir a sequência e a variedade dos `section_blueprints` extraídos da referência (Hero imersivo, grids assimétricos, faixas de contexto/tickers e tabelas técnicas).
2. **Proibição de Efeitos Órfãos (Dead SVG/CSS Rule):** É proibido declarar tags `<svg><filter>` ou `@keyframes` no HTML sem que estejam efetivamente aplicadas em elementos renderizados e visíveis via CSS `filter: url(#...)` ou `animation`.
3. **Proibição de Fallback para Fontes de Sistema sem Tentativa de Webfont:** É proibido rebaixar silenciosamente a tipografia para `Segoe UI`, `Arial` ou `Times New Roman` quando a referência declarou e utilizou webfonts. O extrator captura as tags `<link>` e `@font-face` necessárias.
4. **Proibição de Contaminação por Fontes Decorativas:** Fontes do tipo `cursive`, `fantasy` ou caligráficas (ex.: `faracohand`, `Caveat`) são restritas a detalhes marginais e callouts (`--ds-font-hand`). Nunca podem assumir o `body` ou `--ds-font-sans`.
5. **Fluxo de Trabalho em 3 Passos da Squad:**
   - **Passo 1 (`cdp-design-system-extractor`):** Extrai a topologia física, cores reais, curvas de física e `section_blueprints` parametrizados com slots.
   - **Passo 2 (`ceo-marketing` + `ceo-copy`):** Redige a estratégia de mensagem e argumentos em um spec de conteúdo sem opinar sobre layout ou estilização.
   - **Passo 3 (`agentic-web-architect` + `ceo-web`):** Transplanta o conteúdo do spec dentro dos slots dos `section_blueprints` clonados da referência, integrando a camada agêntica (`document.modelContext`, JSON-LD `@graph`, `/llms.txt`).

---

## 4. PROIBIÇÕES E REGRAS DE SEGURANÇA

1. **Proibido SPAs Ocas:** Todo componente ou página derivada deve renderizar HTML semântico imediato. É expressamente proibido entregar contêineres vazios (`<div id="root"></div>`).
2. **Proibido Injeção de Scripts Externos:** Nenhum script JavaScript, listener ou biblioteca de terceiros extraída da URL de referência pode ser injetada no `design-system.html`. O arquivo mestre utiliza unicamente o motor Vanilla JS padrão do extrator.
3. **Proibido Scroll-Jacking e WebGL Decorativo Bloqueante:** Animações não podem travar o scroll natural nem competir com a leitura de conteúdo.
4. **Bloqueio Anti-SSRF:** URLs de referência devem ser públicas (`http://` ou `https://`). Endereços IP locais, privados (RFC 1918), loopback (`127.0.0.1`, `localhost`) ou metadados de nuvem são estritamente proibidos fora de suítes de teste controladas (`CDP_TEST_MODE=1`).

---

## 5. INTEGRAÇÃO COM WEBMCP (CHROME 150+)

Componentes interativos gerados no Living Style Guide (como simuladores, calculadoras e formulários) devem ser instrumentados com WebMCP:
- Atributos declarativos em formulários: `toolname`, `tooldescription`, `toolparamtitle`, `toolparamdescription`.
- Interceptação de eventos de submissão agêntica via `SubmitEvent.agentInvoked` respondendo com `event.respondWith()`.
- Ferramentas imperativas registradas em `document.modelContext.registerTool()` (nunca `navigator.modelContext`).
