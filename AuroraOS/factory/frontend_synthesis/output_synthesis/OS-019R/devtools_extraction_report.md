# DevTools Extraction Report — OS-019R / M2
**Reference:** https://www.exoape.com
**Extraído em:** 2026-06-08 19:10:39
**Gate Matrix:** 15/15
**promotion_allowed:** false

---

## 1. Visão Geral

| Métrica | Valor |
|---|---|
| DOM extraído | ✅ pós-render |
| Computed styles | 23 elementos |
| Layout boxes | 31 regiões |
| Headings | 7 |
| Vídeos | 8 |
| Imagens | 8 |
| Fontes únicas | 4 |
| Cores únicas | 12 |
| CSS custom properties | 56 |
| Z-index layers | 5 |
| Page height (desktop) | 0px |
| Page height (mobile) | 0px |
| prefers-reduced-motion (default) | False |

---

## 2. Sistema Tipográfico

### Famílias identificadas
- `Times New Roman`
- `Lausanne-300`
- `Lausanne-400`
- `Lausanne-500`

### Headings extraídas

| Tag | Font-size | Font-weight | Texto |
|---|---|---|---|
| h1 | `250px` | `400` | Digital
Design
Experience |
| h2 | `14px` | `400` | Featured Projects |
| h3 | `250px` | `400` |  |
| h2 | `14px` | `400` | Work in motion |
| h2 | `144px` | `400` | Play
Reel |
| h2 | `14px` | `400` | In the media |
| h1 | `144px` | `400` |  |

### H1 computed
| Propriedade | Valor |
|---|---|
| font-family | `Lausanne-300` |
| font-size | `250px` |
| font-weight | `400` |
| letter-spacing | `-11.5px` |
| line-height | `226px` |
| text-transform | `none` |

---

## 3. Cores (Top 20 por frequência)

| Hex approx | RGB computed | Freq | Propriedade | Contexto |
|---|---|---|---|---|
| `#0d0e13` | `rgb(13, 14, 19)` | 267 | color | body |
| `#ffffff` | `rgb(255, 255, 255)` | 257 | background-color | body |
| `#e0cdbd` | `rgba(224, 205, 189, 0.8)` | 69 | color | p |
| `#e0ccbb` | `rgb(224, 204, 187)` | 61 | color | footer |
| `#e4e0db` | `rgb(228, 224, 219)` | 45 | color | section |
| `#0d0e13` | `rgba(13, 14, 19, 0.6)` | 24 | color | p |
| `#000000` | `rgb(0, 0, 0)` | 3 | color | html |
| `#ffffff` | `rgba(255, 255, 255, 0.6)` | 3 | color | div |
| `#0d0e13` | `rgba(13, 14, 19, 0.4)` | 2 | background-color | div |
| `#000000` | `rgba(0, 0, 0, 0.15)` | 1 | background-color | div |
| `#070707` | `rgb(7, 7, 7)` | 1 | background-color | footer |
| `#e0cdbd` | `rgba(224, 205, 189, 0.6)` | 1 | background-color | div |

---

## 4. Inventário de Mídia

### Vídeos (8)

| ID | Role | Dimensão | Atributos |
|---|---|---|---|
| video_0 | editorial_media | 584×729 | autoplay=False muted=True loop=True |
| video_1 | editorial_media | 379×473 | autoplay=False muted=True loop=True |
| video_2 | editorial_media | 481×600 | autoplay=False muted=True loop=True |
| video_3 | editorial_media | 276×344 | autoplay=False muted=True loop=True |
| video_4 | editorial_media | 360×225 | autoplay=False muted=True loop=True |
| video_5 | editorial_media | 379×213 | autoplay=False muted=True loop=True |
| video_6 | editorial_media | 379×379 | autoplay=False muted=True loop=True |
| video_7 | editorial_media | 1000×1000 | autoplay=False muted=True loop=True |

**Roles mapeados:**
- `editorial_media`: 8 vídeo(s)

### Imagens (8)
(ver `media_inventory.json` para lista completa)

---

## 5. CSS Custom Properties (Design Tokens)

  `--color-white`: `#fff`
  `--color-white-02`: `hsla(0,0%,100%,.2)`
  `--color-white-04`: `hsla(0,0%,100%,.4)`
  `--color-white-06`: `hsla(0,0%,100%,.6)`
  `--color-white-08`: `hsla(0,0%,100%,.8)`
  `--color-off-white`: `#f8f8f8`
  `--color-off-white-02`: `hsla(0,0%,97%,.2)`
  `--color-off-white-04`: `hsla(0,0%,97%,.4)`
  `--color-off-white-06`: `hsla(0,0%,97%,.6)`
  `--color-off-white-08`: `hsla(0,0%,97%,.8)`
  `--color-story`: `#070707`
  `--color-dark-grey`: `#0d0e13`
  `--color-dark-grey-02`: `rgba(13,14,19,.2)`
  `--color-dark-grey-04`: `rgba(13,14,19,.4)`
  `--color-dark-grey-06`: `rgba(13,14,19,.6)`
  `--color-dark-grey-08`: `rgba(13,14,19,.8)`
  `--color-light-grey`: `#e4e0db`
  `--color-light-grey-02`: `hsla(33,14%,88%,.2)`
  `--color-light-grey-06`: `hsla(33,14%,88%,.6)`
  `--color-light-grey-08`: `hsla(33,14%,88%,.8)`

---

## 6. Z-Index Landscape

Camadas identificadas: `[1, 2, 9, 14, 20]`

Elementos fixed/sticky:
- `html` . — position:fixed z:auto
- `div` .app is-light — position:fixed z:auto
- `button` .menu-button — position:fixed z:14
- `nav` .nav — position:fixed z:9
- `div` .scroll — position:fixed z:auto
- `div` .container — position:sticky z:auto

---

## 7. Viewport Comparativo

| Propriedade | Desktop (1440×900) | Mobile (390×844) |
|---|---|---|
| Page height | 0px | 0px |
| Scroll ratio | 0 | 0 |
| Device pixel ratio | 1 | 1 |

---

## 8. Accessibility Tree

| Tipo | Count |
|---|---|
| Landmarks | 6 |
| Headings visíveis | 7 |
| Elementos interativos | 30 |
| Imagens com alt | 8 de 8 |
| Vídeos com track | 0 de 8 |

---

## 9. Artefatos Gerados

| Arquivo | Conteúdo |
|---|---|
| `dom_tree.json` | Árvore DOM pós-render — profundidade 6 |
| `computed_styles.json` | Estilos computados por seletor relevante |
| `layout_boxes.json` | Bounding boxes de regiões semânticas + vídeos |
| `accessibility_tree.json` | Landmarks, headings, interativos, media a11y |
| `font_inventory.json` | Fontes em uso com sizes, weights, contexts |
| `color_usage.json` | Cores computadas com frequência e contexto |
| `media_inventory.json` | Vídeos e imagens com classificação de role |
| `viewport_state_desktop.json` | Estado viewport 1440×900 + CSS vars |
| `viewport_state_mobile.json` | Estado viewport 390×844 |

---

## 10. Status

```
OS-019R / M2 — CONCLUÍDA
Gate Matrix: 15/15
promotion_allowed: false
Próxima etapa: M3 — Design System Synthesis
```

> M1 capturou a referência.
> M2 mediu a referência.
> Ainda não construímos nada.
