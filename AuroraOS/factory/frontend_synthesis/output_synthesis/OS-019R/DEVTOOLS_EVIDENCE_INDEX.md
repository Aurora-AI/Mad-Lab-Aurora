# DevTools Evidence Index — OS-019R
**Gerado em:** 2026-06-08 22:35:31
**Total de artefatos de evidência:** 24

---

## Aviso de uso

Os screenshots desta OS são **evidências de observação**, não candidatos visuais.
Não devem ser usados como alvo de reprodução por agentes construtores.

---

## Índice de Evidências

| Arquivo | Fase | Conteúdo |
|---|---|---|
| `raw_html.html` | M1 | HTML bruto capturado do servidor |
| `screenshot_desktop.png` | M1 | Evidência visual 1440×900 — não é candidato |
| `screenshot_mobile.png` | M1 | Evidência visual 390×844 — não é candidato |
| `network_manifest.json` | M1 | 51 requests: 3 fontes, 17 scripts, 16 imagens, 8 vídeos |
| `asset_inventory.json` | M1 | Inventário completo de assets |
| `capture_metadata.json` | M1 | Metadados de captura e sumário |
| `dom_tree.json` | M2 | Árvore DOM pós-render, profundidade 6 |
| `computed_styles.json` | M2 | Estilos computados por seletor relevante |
| `layout_boxes.json` | M2 | Bounding boxes de 31 regiões |
| `accessibility_tree.json` | M2 | Landmarks, 7 headings, 30 interativos |
| `font_inventory.json` | M2 | 4 famílias: TWKLausanne-300/400/500, Times NR |
| `color_usage.json` | M2 | 12 cores únicas por frequência |
| `media_inventory.json` | M2 | 8 vídeos + 8 imagens com classificação |
| `viewport_state_desktop.json` | M2 | Estado viewport 1440×900 + 56 CSS vars |
| `viewport_state_mobile.json` | M2 | Estado viewport 390×844 |
| `devtools_extraction_report.md` | M2 | Relatório consolidado de extração |
| `motion_grammar.json` | M4 | IO confirmado, will-change=68, transforms |
| `scroll_behavior.json` | M4 | Snapshots em 5 posições de scroll |
| `interaction_map.json` | M4 | Hover, menu, CTAs testados |
| `timing_curves.json` | M4 | CSS transitions: 0.5s ease |
| `media_runtime_behavior.json` | M4 | Autoplay JS confirmado + Times NR resolvido |
| `viewport_motion_matrix.json` | M4 | Desktop vs mobile H1 comparison |
| `reduced_motion_observations.json` | M4 | CSS scan + contrato Mad Lab |
| `m4_runtime_trace.json` | M4 | IO events brutos, scroll snapshots, hover tests |

---

## Achados-chave por fase

### M1 — Reference Acquisition
- URL: https://www.exoape.com
- Title: Exo Ape - Global Digital Design Studio
- 51 requests capturados: 3 fontes woff2, 17 scripts, 16 imagens, 8 vídeos
- CSS bundled em JS (Next.js) — sem arquivos CSS separados

### M2 — DevTools Extraction
- H1: 250px / weight 400 / tracking -11.5px / lh-ratio 0.904
- 56 CSS custom properties no `:root`
- Paleta: `#0d0e13` (freq 267) + `#ffffff` (freq 257)
- Z-index landscape: [1, 2, 9, 14, 20]

### M3 — Design System Synthesis
- 4 níveis tipográficos normalizados
- Tracking rule derivada de dados reais
- 6 cores canônicas com papel semântico
- Times New Roman classificado como NOT_CANONICAL

### M4 — Motion Grammar
- IntersectionObserver: 1 instância, 21 eventos confirmados
- 8/8 vídeos playing após scroll — JS_INTERSECTION_OBSERVER_AUTOPLAY
- 68 elementos com `will-change: transform`
- CSS transition única: `opacity 0.5s ease`
- H1 mobile: 62.4px / -1.56px tracking

---

## Artefatos NÃO presentes nesta OS (como esperado)

```
SynthesizedPage.client.tsx  — NÃO existe (correto)
rendered_screenshot.png     — NÃO existe como candidato (correto)
promotion_metadata.json     — NÃO existe (correto)
Human Review Package        — NÃO existe (correto)
```
