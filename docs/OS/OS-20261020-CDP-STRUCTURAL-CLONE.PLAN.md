# PLAN — OS-20261020-CDP-STRUCTURAL-CLONE

## Fontes lidas (2026-10-20)
- `docs/OS/OS-20261020-CDP-STRUCTURAL-CLONE.md` (inteira)
- `tools/mcp-design-extractor/server.py` L1-946: hardcode confirmado L740-756 e L787-799; `raw_font = fonts[0]` L723; tipografia L361-377; SVG filters só no manifesto visual L244-250, sem vínculo CSS.
- `tools/mcp-design-extractor/tests/test_reprova.py` L1-182 (S1–S5, D1); `tests/test_functional.py` asserts L66-114 (exige header "AURORA LIVING DESIGN SYSTEM" e form `simulate_roi`).
- `scripts/run_extract_aori.py` L1-82.
- `Referências/Sites/aoricreative/design-telemetry.json`: `0b0b0b`=1, `7fa8f0`=2, `f3f1ec`=0, `_R_iivb_`=0, `faracohand`=8 (Select-String 09:40).
- `C:\Users\rodri\Downloads\index.html` (42616 bytes): `#f8fafc` L81, `<filter id="elysian-ink-subtle">` L584, 8× `<section class="card...">` L611-852.
- `C:\Projetos\Aurora\packages\tooling\scripts\check-plan-conformance.mjs` (inteiro).

## Reformulação
Reescrever extrator/compilador para clonagem estrutural content-agnostic, atualizar regra e skill, criar gate estético Playwright com reprova. Não é página final de produto. Suposição: `@font-face`/links são registrados e referenciados (não baixados); o novo `index.html` é demonstrativo com conteúdo genérico Elysian Consult injetado nos blueprints.

## O que este plano NÃO faz (nao-escopo)
- Não copia textos comerciais, marcas registradas, imagens proprietárias ou dados de clientes da referência.
- Não copia scripts externos de terceiros (analytics, trackers, bundles minificados).
- Não altera `scripts/check-madlab-governance.mjs` nem sua reprova; não toca `docs/Vault/`; não faz git push/commit.
- Não sobrescreve `Referências/Sites/aoricreative/` (preservado como evidência histórica).

## Restrições herdadas (verbatim da OS, bloco RESTRICOES)
- Nunca copiar textos comerciais, marcas registradas, imagens proprietárias ou dados de clientes da referência.
- Nunca copiar scripts externos de terceiros (analytics, trackers, bundles minificados) da referência.
- Proibido hardcode de paleta `#f8fafc`, `#0f172a` ou `--ds-shadow-card: none` no compilador.
- Proibido fonte cursive ou fantasy assumir `--ds-font-sans` ou `body`.
- Proibido declarar `<filter>` ou `@keyframes` sem aplicá-los visualmente em elemento renderizado.
- Proibido Card Stacking monotônico de mesma classe `.card` em coluna única.
- Proibido fallback para fontes de sistema quando houver tipografia na referência.
- Proibido usar `navigator.modelContext`; usar exclusivamente `document.modelContext`.
- Proibido ficar verde por remoção: nenhum teste ou passo existente pode ser apagado ou afrouxado.

## Micro-etapas
| # | Ação | Gate | Condição de falha | Rollback |
|---|---|---|---|---|
| ME-01 | Classificador tipográfico 4 papéis (`typography_roles`) + `font_assets` (links + `@font-face`) em `_extract_cssom_and_computed` | `tests/test_structural_clone.py` com fixture `typography_fixture.html`: sans=Plus Jakarta Sans, hand=faracohand | sans contém faracohand/cursive → EXIT=1, bloqueia ME-03 | `git checkout -- tools/mcp-design-extractor/server.py` |
| ME-02 | `section_blueprints` (bg/text, layout, grid cols, gap, padding, template com `{{SLOT_*}}`, texto e `img src` removidos) + `active_svg_filters` (id, markup, seletores com `filter:url(#id)`) | mesmo teste: ≥3 blueprints; filtro da fixture vinculado a seletor | <3 blueprints ou filtro sem vínculo → EXIT=1, bloqueia | idem |
| ME-03 | Compilador `mode="clone-structure-and-style"` sem hardcode; `--ref-*`, 4 fontes, Blocos A–D, contraste ≥4.5:1 por luminosidade HSL, `prefers-reduced-motion` | teste: compilado sem `#f8fafc`, cores da fixture no `:root`, filtro aplicado em elemento visível; `test_reprova.py` e `test_functional.py` EXIT=0 | qualquer assert falha → EXIT=1, bloqueia ME-05 | idem |
| ME-04 | Atualizar regra `.agents/rules/cdp-design-system.md` e `SKILL.md` com Content-Over-Clone | `node scripts/check-madlab-governance.mjs` EXIT=0 | EXIT≠0 → reverter edição e reportar | `git checkout --` dos 2 arquivos |
| ME-05 | `tests/test_aesthetic_fidelity_gate.py` (6 AP) + re-extração ao vivo Aori em `Elysian Consult/aori-clone/` + `Elysian Consult/index.html` | gate: HTML antigo EXIT=1 com AP1-4; novos design-system.html e index.html EXIT=0 | antigo passa → gate cego, bloqueia OS; novo reprova → corrigir artefato (nunca o gate) | remover arquivos novos (com confirmação) |

## Critério de aceite
1. `python scripts/run_extract_aori_clone.py > log 2>&1; EXIT=0`, `design-system.html` contém `#0b0b0b`/`#7fa8f0` (ou RGB) no `:root`, 4 fontes, `filter: url(#` aplicado, `section_blueprints`.
2. `python tests/test_aesthetic_fidelity_gate.py --telemetry ... --html C:\Users\rodri\Downloads\index.html` → EXIT=1 (AP1,2,3,4); com novos artefatos → EXIT=0.
3. `node scripts/check-madlab-governance.mjs` e `node scripts/test-madlab-governance-reprova.mjs` → EXIT=0.
Se `#f3f1ec` ou o id `_R_iivb_` não existirem na página ao vivo, o item é reportado como não feito com motivo (id React gerado), sem forjar.

## Destino da evidência
`Elysian Consult/evidence/` (logs `*.log` com EXIT) e `Elysian Consult/aori-clone/` (artefatos).

<!-- BLAST_RADIUS:INICIO -->
- Modificados: `tools/mcp-design-extractor/server.py`, `.agents/rules/cdp-design-system.md`, `.aurora/skills/cdp-design-system-extractor/SKILL.md`
- Novos: `tools/mcp-design-extractor/tests/test_structural_clone.py`, `tests/test_aesthetic_fidelity_gate.py`, `tests/fixtures/typography_fixture.html`, `scripts/run_extract_aori_clone.py`, `Elysian Consult/**`, `docs/OS/OS-20261020-CDP-STRUCTURAL-CLONE*.md`
- Contratos: schema `cdp.telemetry.v1` ganha chaves aditivas (`typography_roles`, `font_assets`, `section_blueprints`, `active_svg_filters`); assinatura de `compile_living_design_system_html` ganha parâmetro `mode` com default novo.
<!-- BLAST_RADIUS:FIM -->
