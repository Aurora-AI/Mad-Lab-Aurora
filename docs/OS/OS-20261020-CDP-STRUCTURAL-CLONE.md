# ORDEM DE SERVIÇO TÉCNICA — OS-20261020-CDP-STRUCTURAL-CLONE

**Risco:** ALTO
**Origem:** Comandante (chat 2026-10-20T09:38-03:00), transcrita verbatim; respostas às ambiguidades em 2026-10-20T09:51-03:00:
1. HTML defeituoso anterior = `C:\Users\rodri\Downloads\index.html`
2. Re-extração ao vivo de `https://aoricreative.com/` autorizada
3. Artefatos gravados em pasta nova `Elysian Consult/`
4. Pergunta sobre skill em ambiente pessoal: desconsiderada

> **Alvo:** Refatoração Estrutural do Motor `mcp-design-extractor`, da Skill `cdp-design-system-extractor`, da Regra `.agents/rules/cdp-design-system.md` e do Gate `qa-review`
> **Prioridade:** CRÍTICA (Correção de Falha Sistêmica de Fidelidade Estética / "Compliance Washing")
> **Governança Canônica:** `docs/AGENTS/DOCTRINE.md` (Emenda v9.1) | Padrão Trustware STRICT

## 1. DIAGNÓSTICO DE CAUSA RAIZ
1. Destruição da Paleta Original por Hardcode (`#f8fafc`) em `compile_living_design_system_html`.
2. Cegueira Semântica na Tipografia (`fonts[0]` → `faracohand` virou `--ds-font-primary`).
3. Extração de Tokens Soltos sem Topologia de Layout (Síndrome de Caixas Empilhadas).
4. Teatro de Efeitos Visuais (Filtro SVG Órfão sem `filter: url(#...)`).
5. Gate de QA Cego para Design.

## 2. OBJETIVO (FORMA CLONADA × CONTEÚDO PRÓPRIO)
Clonar: paleta real por seção; tipografia em 4 papéis (`--ds-font-display`, `--ds-font-sans`, `--ds-font-mono`, `--ds-font-hand`) + `@font-face`/links; escalas; efeitos ativos; `section_blueprints` com slots `{{SLOT_*}}`.

## 3. MICRO-ETAPAS
- ME-01: Classificador tipográfico por papel + captura de font assets. Gate: fixture com `faracohand` em `<span>` e `Plus Jakarta Sans` em `<p>` → sans=Plus Jakarta Sans, hand=faracohand; senão EXIT=1.
- ME-02: `section_blueprints` (≥3) e `active_svg_filters` com regras CSS vinculadas em `design-telemetry.json`.
- ME-03: Compilador modo `clone-structure-and-style` sem hardcode; Blocos A–D; Paz Cognitiva não-destrutiva (contraste ≥ 4.5:1 só por luminosidade; `prefers-reduced-motion`). Gate: sem `#f8fafc` como canvas; `#0b0b0b`/`#7fa8f0` no `:root`; `--ds-font-sans` sem `faracohand`/`cursive`; todo `<filter id>` aplicado a elemento visível.
- ME-04: Atualizar `.agents/rules/cdp-design-system.md` e `.aurora/skills/cdp-design-system-extractor/SKILL.md` com protocolo Content-Over-Clone.
- ME-05: `tools/mcp-design-extractor/tests/test_aesthetic_fidelity_gate.py` (Playwright) com 6 anti-padrões; reprova o HTML antigo (AP 1,2,3,4) e aprova o novo.

## 4. CRITÉRIO DE ACEITE
1. `design-system.html` recompilado da telemetria ao vivo de `https://aoricreative.com/` com cores reais, tipografia por papel, filtro aplicado e esqueletos.
2. Gate reprova (EXIT=1) o HTML antigo e aprova (EXIT=0) o novo.
3. `node scripts/check-madlab-governance.mjs` e `node scripts/test-madlab-governance-reprova.mjs` com EXIT=0.

<!-- RESTRICOES:INICIO -->
- Nunca copiar textos comerciais, marcas registradas, imagens proprietárias ou dados de clientes da referência.
- Nunca copiar scripts externos de terceiros (analytics, trackers, bundles minificados) da referência.
- Proibido hardcode de paleta `#f8fafc`, `#0f172a` ou `--ds-shadow-card: none` no compilador.
- Proibido fonte cursive ou fantasy assumir `--ds-font-sans` ou `body`.
- Proibido declarar `<filter>` ou `@keyframes` sem aplicá-los visualmente em elemento renderizado.
- Proibido Card Stacking monotônico de mesma classe `.card` em coluna única.
- Proibido fallback para fontes de sistema quando houver tipografia na referência.
- Proibido usar `navigator.modelContext`; usar exclusivamente `document.modelContext`.
- Proibido ficar verde por remoção: nenhum teste ou passo existente pode ser apagado ou afrouxado.
<!-- RESTRICOES:FIM -->
