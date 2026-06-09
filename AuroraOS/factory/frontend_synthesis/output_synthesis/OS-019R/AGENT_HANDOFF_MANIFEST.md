# Agent Handoff Manifest — OS-019R
**Referência extraída:** https://www.exoape.com
**Gerado em:** 2026-06-08 22:35:31
**OS:** OS-019R — Reference Intelligence Before Generation
**Status:** M6 — HANDOFF READY
**promotion_allowed:** false

---

## Para o Agente Construtor

Este pacote contém tudo o que você precisa para construir o Mad Lab Theme sem consultar
a referência diretamente. Os dados foram extraídos via DevTools reais, normalizados em
Design System e mapeados em padrões reutilizáveis com restrições anti-clone explícitas.

**Você pode construir. Não pode clonar.**

---

## O que está disponível

### Design System (M3)
| Artefato | Conteúdo |
|---|---|
| `typography_system.json` | 4 níveis tipográficos com tracking calculado |
| `design_tokens.json` | 56 CSS custom properties categorizadas |
| `color_semantics.json` | Paleta semântica com pares WCAG e áreas de risco |
| `spacing_system.json` | Layout derivado de bounding boxes reais |
| `surface_system.json` | Camadas z-index + sistema de tema |
| `media_design_tokens.json` | Tokens de mídia e risco a11y |

### Motion Grammar (M4)
| Artefato | Conteúdo |
|---|---|
| `motion_grammar.json` | Primitivos: IO confirmado, will-change, transforms |
| `scroll_behavior.json` | Snapshots de scroll em 5 posições |
| `interaction_map.json` | Hover, menu, CTAs testados em runtime |
| `timing_curves.json` | CSS transitions: 0.5s ease (única confirmada) |
| `media_runtime_behavior.json` | Autoplay JS confirmado, Times New Roman resolvido |
| `viewport_motion_matrix.json` | Desktop vs mobile H1 comparison |
| `reduced_motion_observations.json` | Status CSS + contrato Mad Lab |

### Pattern Map (M5)
| Artefato | Conteúdo |
|---|---|
| `component_pattern_map.json` | 7 padrões com source_trace, budget, anti-clone |
| `section_taxonomy.json` | 5 seções identificadas com papéis e motion |
| `layout_archetypes.json` | 4 arquetipos de layout derivados de M2 |
| `typography_pattern_map.json` | Sistema tipográfico + fórmulas de tracking |
| `media_pattern_map.json` | Padrão IO-gated video + imagens com alt |
| `motion_pattern_map.json` | 4 padrões de motion com timing e reduced-motion |
| `interaction_role_map.json` | Nav, menu, CTA, video surface |
| `gpu_layer_strategy.json` | Budget low/medium/high/reduced |
| `anti_clone_constraints.json` | Hard prohibitions + permitted derivations |

### Evidência DevTools (M1–M2)
| Artefato | Conteúdo |
|---|---|
| `raw_html.html` | HTML bruto capturado |
| `screenshot_desktop.png` | Evidência visual 1440×900 |
| `screenshot_mobile.png` | Evidência visual 390×844 |
| `dom_tree.json` | Árvore DOM pós-render |
| `computed_styles.json` | Estilos computados por seletor |
| `layout_boxes.json` | Bounding boxes de regiões semânticas |
| `accessibility_tree.json` | Landmarks, headings, interativos |
| `font_inventory.json` | Fontes em uso |
| `color_usage.json` | Cores computadas com frequência |
| `media_inventory.json` | Vídeos e imagens classificados |
| `network_manifest.json` | 51 requests capturados |
| `asset_inventory.json` | Inventário de assets |
| `m4_runtime_trace.json` | IO events, scroll snapshots, hover tests |

---

## O que já foi decidido

| Decisão | Valor |
|---|---|
| Fonte primária | TWKLausanne — **PROIBIDA** (proprietária). Usar substituto aprovado. |
| H1 tamanho desktop | 250px |
| H1 tamanho mobile | 62.4px |
| H1 tracking desktop | -11.5px (ratio -0.046) |
| H1 tracking mobile | -1.56px (ratio -0.025) |
| H1 line-height ratio | 0.904 |
| Cor dominante | `#0d0e13` texto / `#ffffff` background |
| Escala de opacidade | -02/-04/-06/-08 (20%/40%/60%/80%) |
| Video autoplay | JS IntersectionObserver — **não atributo HTML** |
| Times New Roman | BROWSER_DEFAULT — **NOT_CANONICAL** |
| Reduced motion | fail-closed — contrato OS-019 M0 preservado |
| GPU budget (high) | 20 layers máximo |
| Z-index layers | [1, 2, 9, 14, 20] |
| Nav z-index | 9 |
| Menu button z-index | 14 |

---

## O que NÃO está resolvido

- Custom cursor behavior — não testado
- Keyboard focus states — não testado
- CSS-in-JS animation details — stylesheet scan limitado
- Tracking intermediário 60–100px — não observado nesta faixa

---

## Quais dados são confiáveis?

| Dado | Confiança | Método |
|---|---|---|
| Typography computed styles | ✅ Alta | Browser computed, não inferido |
| CSS custom properties | ✅ Alta | JS :root extraction |
| Video autoplay mechanism | ✅ Alta | IO spy + runtime scroll test |
| Times New Roman status | ✅ Alta | Runtime confirmation |
| Layout bounding boxes | 🟡 Média | Derivado de posição, não de CSS direto |
| Timing curves | 🟡 Média | Computed styles neutro — hover pode diferir |
| Spacing rhythm | 🟡 Média | Derivado de Y positions, não de margin/padding |
| Tracking mobile | ✅ Alta | Computed styles 390px viewport |
| Reduced motion CSS | 🟡 Média | Possível CSS-in-JS não escaneado |

---

## Como usar este pacote

```
1. Leia BUILD_CONSTRAINTS.md antes de qualquer implementação
2. Use REFERENCE_DO_NOT_COPY.md como checklist de revisão
3. DESIGN_SYSTEM_SUMMARY.md é o ponto de entrada para tokens
4. MOTION_GRAMMAR_SUMMARY.md define o comportamento esperado
5. PATTERN_MAP_SUMMARY.md lista os padrões com fórmulas
6. DEVTOOLS_EVIDENCE_INDEX.md para consultar dados brutos
```

---

## promotion_allowed

```
false — permanente nesta OS
Esta OS não gera candidato final.
Produto final: este Agent Handoff Package.
```

---

> M5 transformou dados em padrões.
> M6 transformou padrões em instrução operacional para agentes.
> Ainda não existe construção.
