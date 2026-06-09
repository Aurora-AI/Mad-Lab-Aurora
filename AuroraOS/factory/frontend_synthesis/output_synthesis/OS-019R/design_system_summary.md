# Design System Summary — OS-019R
**Gerado em:** 2026-06-08 22:35:31
**Fonte:** M2 DevTools + M3 Synthesis
**Confiança:** Alta (dados computed do browser)

---

## 1. Sistema Tipográfico

### Fontes

| Família | Status | Uso |
|---|---|---|
| TWKLausanne (Lausanne-300/400/500) | ⛔ PROIBIDA | Proprietária da Exo Ape |
| Times New Roman | ⛔ NOT_CANONICAL | Browser default detectado |
| Substituição | usar fonte aprovada no projeto | Equivalência óptica requerida |

### Escala

| Nível | Tag | Tamanho (desktop) | Tamanho (mobile) | Tracking (desktop) | Weight | Uso |
|---|---|---|---|---|---|---|
| display_monumental | h1 | 250px | 62.4px | -11.5px | 400 | Hero, abertura |
| display_large | h2 | 144px | — | — | 400 | Motion reel, seções |
| label_section | h2 | 14px | — | — | 400 | Rótulo de seção |
| body | p | — | — | — | — | Corpo editorial |

### Fórmulas de tracking

```
desktop (> 768px):  letter-spacing = font-size × (-0.046)
mobile  (< 640px):  letter-spacing = font-size × (-0.025)
abaixo 40px:        letra-spacing = 0 a -0.01
line-height:        font-size × 0.904  (display monumental)
```

---

## 2. Paleta de Cores

| Token | Hex | Papel |
|---|---|---|
| `--color-dark-grey` | `#0d0e13` | Texto primário + superfície escura |
| `--color-white` | `#ffffff` | Background primário + texto sobre escuro |
| `--color-off-white` | `#f8f8f8` | Background suave alternativo |
| `--color-light-grey` | `#e4e0db` | Decorativo — nunca texto |
| *(editorial warm)* | `#e0ccbb` | Texto editorial grande (> 18px bold) |
| `--color-story` | `#070707` | Fundo seções escuras |

### Escala de opacidade (todos os tokens)

```
-02 = 20% → overlay fantasma
-04 = 40% → texto muted / placeholder
-06 = 60% → ícone inativo / texto secundário
-08 = 80% → quase opaco / overlay suave
```

### Pares de contraste (top 5)

| Par | Ratio | WCAG |
|---|---|---|
| story / white | 20.14 | AAA |
| dark_grey / white | 19.28 | AAA |
| off_white / story | 18.97 | AAA |
| dark_grey / off_white | 18.15 | AAA |
| light_grey / story | 15.33 | AAA |

---

## 3. Z-Index System

| Z | Semântica |
|---|---|
| 1 | base interativo |
| 2 | conteúdo elevado |
| 9 | navegação fixa |
| 14 | botão de menu |
| 20 | overlay / modal |

---

## 4. Tokens CSS — 56 custom properties

Arquivo canônico: `design_tokens.json`

Categorias:
- Semantic tokens (cores com papel)
- Opacity scale (-02/-04/-06/-08)
- Primitive tokens
- Motion tokens
- Radius tokens
- Unclassified

---

## Arquivos de referência

```
design_tokens.json          — tokens completos
typography_system.json      — escala tipográfica com evidence
color_semantics.json        — paleta com WCAG e semântica
spacing_system.json         — layout derivado de bounding boxes
surface_system.json         — superfícies e z-index
```
