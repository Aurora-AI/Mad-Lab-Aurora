# OS-019R — Reference Intelligence Before Generation

**ID canônico:** OS-MADLAB-REFERENCE-INTELLIGENCE-BEFORE-GENERATION-20260608-019R  
**Data de abertura:** 2026-06-08  
**Predecessor:** OS-019 (encerrada por correção de escopo)  
**Branch:** a definir na M1  

---

## Objetivo Canônico

Extrair dados técnicos, visuais, estruturais e cinéticos de uma referência real para formar
uma base sólida de Design System, DevTools Data, Motion Grammar e Agent Handoff Package.

**Esta OS não constrói tela. Ela prepara os agentes que construirão depois.**

---

## Status Atual

```
OS-019R — ENCERRADA
Reference URL: https://www.exoape.com
promotion_allowed: false (permanente)
Produto: Agent Handoff Package completo

M1: CONCLUÍDA (12/12 gates) — 2026-06-08
M2: CONCLUÍDA (15/15 gates) — 2026-06-08
M3: CONCLUÍDA (17/17 gates) — 2026-06-08
M4: CONCLUÍDA (19/19 gates) — 2026-06-08
M5: CONCLUÍDA (21/21 gates) — 2026-06-08
M6: CONCLUÍDA (15/15 gates) — 2026-06-08

TOTAL: 99 gates — 99/99
Próxima OS: OS-MADLAB-BUILD-001 — Mad Lab Theme Implementation
```

---

## Artefatos Preservados da OS-019

| Artefato | Status | Uso na OS-019R |
|---|---|---|
| `1_blueprint.json` | RETIDO | Intenção de navegação — input para M4 |
| `4_code_spec.json` | RETIDO | Tokens iniciais — ponto de partida para M3 |
| `5_component_tree.json` | RETIDO | Mapa de padrões — referência para M5 |
| Contrato `reducedMotion fail-closed` | RETIDO | Contrato de acessibilidade para M4 |
| TSX candidate | SUPERSEDED | exploratory render evidence |
| Screenshot (M4.1) | SUPERSEDED | exploratory render evidence |
| Perceptual report | SUPERSEDED | exploratory only |
| HUMAN_REVIEW_PACKAGE | SUPERSEDED | — |
| promotion_metadata | SUPERSEDED | promotion_allowed=false preservado |

---

## Micro-Etapas

| Etapa | Nome | Produto Principal | Status |
|---|---|---|---|
| M1 | Reference Acquisition | `raw_html`, `screenshots`, `asset_inventory` | CONCLUÍDA 12/12 |
| M2 | DevTools Structural Extraction | `dom_tree`, `computed_styles`, `layout_boxes`, `a11y_tree` | CONCLUÍDA 15/15 |
| M3 | Design System Synthesis | `design_tokens`, `typography_system`, `color_semantics` | CONCLUÍDA 17/17 |
| M4 | Motion & Interaction Grammar | `motion_grammar`, `scroll_behavior`, `timing_curves` | CONCLUÍDA 19/19 |
| M5 | Component & Pattern Map | `component_pattern_map`, `section_taxonomy` | CONCLUÍDA 21/21 |
| M6 | Agent Handoff Package | `AGENT_HANDOFF_MANIFEST.md`, `BUILD_CONSTRAINTS.md` | CONCLUÍDA 15/15 |

---

## Critérios de Aceite Globais

```
[ ] captura auditável da referência
[ ] HTML bruto capturado (não inferido)
[ ] screenshots apenas como evidência (não produto)
[ ] DOM tree extraída do browser real
[ ] CSSOM / computed styles extraídos
[ ] layout boxes extraídos
[ ] accessibility tree extraída
[ ] asset inventory completo
[ ] font inventory com evidência
[ ] color usage com papel semântico
[ ] typography system com 4+ níveis
[ ] spacing / grid system
[ ] motion grammar como fenômeno (não instrução)
[ ] interaction map
[ ] component pattern map com evidência DOM
[ ] anti-clone constraints explícitos
[ ] agent handoff package completo
[ ] promotion_allowed=false preservado em todos os artefatos
```

---

## Critérios de Rejeição da M1

A M1 deve falhar se:
```
[ ] tentar gerar TSX
[ ] tentar gerar landing
[ ] tentar fazer redesign
[ ] tentar aprovar estética
[ ] não capturar HTML real
[ ] não capturar screenshot desktop/mobile
[ ] não registrar origem da referência
[ ] não preservar promotion_allowed=false
```

---

## Invariante Permanente

```
promotion_allowed: false
Esta OS não gera candidato final.
Produto final: Agent Handoff Package para agentes construtores.
```

---

## Frase Canônica

> OS-019 tentou construir cedo demais.  
> OS-019R volta ao fundamento correto:  
> primeiro capturar, medir e entender;  
> depois outros agentes constroem.
