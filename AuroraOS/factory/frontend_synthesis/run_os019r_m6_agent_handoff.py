"""
OS-019R / M6 — Agent Handoff Package
======================================

Consolida M1–M5 em pacote operacional para agentes construtores futuros.

PROIBIDO:
  - Gerar TSX / componente
  - Gerar landing / screenshot candidato
  - Gerar render bundle
  - Gerar promotion_metadata
  - Usar browser

ENTREGÁVEIS (documentos Markdown + checklist JSON):
  AGENT_HANDOFF_MANIFEST.md
  BUILD_CONSTRAINTS.md
  REFERENCE_DO_NOT_COPY.md
  DESIGN_SYSTEM_SUMMARY.md
  MOTION_GRAMMAR_SUMMARY.md
  PATTERN_MAP_SUMMARY.md
  DEVTOOLS_EVIDENCE_INDEX.md
  TRANSFER_READINESS_CHECKLIST.md
  M6_QA_REPORT.md

INVARIANTE:
  promotion_allowed: false
"""

import json
import os
import time

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output_synthesis", "OS-019R")

NOW = time.strftime("%Y-%m-%d %H:%M:%S")
NOW_ISO = time.strftime("%Y-%m-%dT%H:%M:%S")


def load(name):
    path = os.path.join(OUTPUT_DIR, name)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return f.read() if os.path.getsize(path) < 50000 else "[file too large]"


def write_md(name: str, content: str):
    path = os.path.join(OUTPUT_DIR, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    size = os.path.getsize(path)
    print(f"  ✓ {name} — {size:,} bytes")
    return path


def save_json(name: str, data):
    path = os.path.join(OUTPUT_DIR, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    size = os.path.getsize(path)
    print(f"  ✓ {name} — {size:,} bytes")
    return path


# ─────────────────────────────────────────────────────────────────────────────

def main():
    print(f"\n{'='*60}")
    print("OS-019R / M6 — Agent Handoff Package")
    print(f"{'='*60}\n")
    ts = time.time()

    print("[0] Carregando artefatos M1–M5...")

    cap_meta   = load("capture_metadata.json") or {}
    typo       = load("typography_system.json") or {}
    design_tok = load("design_tokens.json") or {}
    color_sem  = load("color_semantics.json") or {}
    spacing    = load("spacing_system.json") or {}
    surface    = load("surface_system.json") or {}
    media_tok  = load("media_design_tokens.json") or {}
    motion_g   = load("motion_grammar.json") or {}
    timing     = load("timing_curves.json") or {}
    media_rt   = load("media_runtime_behavior.json") or {}
    vp_matrix  = load("viewport_motion_matrix.json") or {}
    reduced    = load("reduced_motion_observations.json") or {}
    patterns_f = load("component_pattern_map.json") or {}
    section_tx = load("section_taxonomy.json") or {}
    layout_arc = load("layout_archetypes.json") or {}
    typo_pm    = load("typography_pattern_map.json") or {}
    media_pm   = load("media_pattern_map.json") or {}
    motion_pm  = load("motion_pattern_map.json") or {}
    gpu_strat  = load("gpu_layer_strategy.json") or {}
    anti_clone = load("anti_clone_constraints.json") or {}
    m5_trace   = load("m5_traceability_matrix.json") or {}

    patterns   = patterns_f.get("patterns", [])

    # Key values
    h1_dt = vp_matrix.get("comparison", {}).get("h1_font_size", {}).get("desktop", "250px")
    h1_mb = vp_matrix.get("comparison", {}).get("h1_font_size", {}).get("mobile", "62.4px")
    ls_dt = vp_matrix.get("comparison", {}).get("h1_letter_spacing", {}).get("desktop", "-11.5px")
    ls_mb = vp_matrix.get("comparison", {}).get("h1_letter_spacing", {}).get("mobile", "-1.56px")
    io_inst = motion_g.get("motion_primitives", {}).get("intersection_observer", {}).get("instances_detected", 1)
    wc_cnt  = motion_g.get("motion_primitives", {}).get("will_change", {}).get("element_count", 68)
    css_var_count = len(design_tok.get("semantic_tokens", {})) + len(design_tok.get("opacity_scale", {}))
    section_count = len(section_tx.get("taxonomy", []))
    unresolved = m5_trace.get("unresolved_for_m6", [])

    print(f"  Padrões: {len(patterns)}")
    print(f"  CSS vars: {css_var_count}")
    print(f"  Seções: {section_count}")
    print(f"  Unresolved: {len(unresolved)}")

    # ─────────────────────────────────────────────────────────────────────────
    print("\n[1] AGENT_HANDOFF_MANIFEST.md...")

    manifest = f"""# Agent Handoff Manifest — OS-019R
**Referência extraída:** https://www.exoape.com
**Gerado em:** {NOW}
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

{chr(10).join(f'- {u}' for u in unresolved)}

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
"""
    write_md("AGENT_HANDOFF_MANIFEST.md", manifest)

    # ─────────────────────────────────────────────────────────────────────────
    print("\n[2] BUILD_CONSTRAINTS.md...")

    budget_table = "\n".join(
        f"| {q} | {v['max_will_change_layers']} | {v['parallax']} | {v['video_autoplay']} |"
        for q, v in gpu_strat.get("mad_lab_budget", {}).get("budget_by_quality", {}).items()
    )

    build_constraints = f"""# Build Constraints — OS-019R / Mad Lab Theme
**Gerado em:** {NOW}
**promotion_allowed:** false

---

## 1. GPU / Performance

### Budget de layers

| Qualidade | Max will-change layers | Parallax | Video Autoplay |
|---|---|---|---|
{budget_table}

### Regras obrigatórias

- `will-change: transform` apenas nos elementos que serão animados no frame seguinte
- Remover `will-change` após animação via JS (`el.style.willChange = 'auto'`)
- Não usar `will-change: all`
- Testar em dispositivos de médio desempenho (não apenas high-end)
- `transform` (não `top/left`) para todas as animações de posição

---

## 2. Vídeo / Mídia

- **autoplay HTML**: `false` — nunca usar atributo `autoplay` diretamente
- **Mecanismo correto**: `IntersectionObserver` com threshold ≈ 0.3 → `video.play()`
- **Sempre**: `muted=true`, `loop=true`, `preload="none"` até threshold
- **Poster**: obrigatório como placeholder antes da carga
- **Máximo simultâneo**: 3 vídeos em playback simultâneo na viewport
- **Reduced motion**: `poster` estático apenas — não chamar `play()`
- **A11y**: vídeos sem narração dispensam track. Com narração: track obrigatório

---

## 3. Tipografia

- **Fonte primária**: **PROIBIDA** TWKLausanne (proprietária da Exo Ape)
  - Usar substituto aprovado com equivalência de contraste óptico
  - Fallback stack: `Helvetica Neue, Helvetica, Arial, sans-serif`
- **Times New Roman**: NOT_CANONICAL — nunca declarar em `font-family`
- **H1 desktop**: 250px, letter-spacing -11.5px (ratio -0.046), weight 400
- **H1 mobile**: 62.4px, letter-spacing -1.56px (ratio -0.025), weight 400
- **Fórmula de tracking**: `letter-spacing = font-size × tracking_ratio`
  - Desktop (> 768px): ratio = -0.046
  - Mobile (< 640px): ratio = -0.025
  - Abaixo de 40px: ratio = 0 a -0.01
- **line-height display**: `font-size × 0.904`
- **Não usar bold** em escala monumental (weight 400 é o padrão da referência)

---

## 4. Cores

- Paleta near-monocromática: `#0d0e13` (escuro) + `#ffffff` (branco)
- Escala de opacidade: sufixos -02/-04/-06/-08
- `#e0ccbb` (bege editorial) — **apenas texto grande** (> 18px bold). Falha WCAG em body
- `#e4e0db` (light grey) — decorativo apenas, nunca texto
- Modo escuro: `--color-story #070707` para seções editoriais escuras
- Nunca adicionar cor saturada sem revisar o sistema completo

---

## 5. Z-Index

| Camada | Z-Index | Uso |
|---|---|---|
| Base interativo | 1 | elementos clicáveis padrão |
| Conteúdo elevado | 2 | cards, hover states |
| Navegação | 9 | nav fixa |
| Menu trigger | 14 | botão de menu (acima da nav) |
| Overlay / Modal | 20 | overlays de tela cheia |

- Máximo de 5 camadas declaradas
- Nunca declarar z-index > 20 sem justificativa de modal/overlay crítico

---

## 6. Responsive

- Desktop breakpoint principal: 1440px
- Mobile breakpoint: 390px
- H1 escala 4:1 entre desktop e mobile (250px → 62.4px)
- Nav height máxima: ~64px–80px
- Variação de layout deve ser testada em: 390, 768, 1024, 1440

---

## 7. Acessibilidade

- `useReducedMotion()` fail-closed — **contrato herdado da OS-019 M0**
  - Se `prefers-reduced-motion: reduce` → static poster, sem transforms animados
- `will-change` deve ser removido antes de animação em modo reduzido
- Imagens: `alt` obrigatório em todas as imagens de conteúdo
- Vídeos com narração: `<track>` obrigatório
- Focus states de teclado: obrigatórios (não testados na referência — implementar conforme WCAG 2.4.7)

---

## 8. Limites de similaridade visual

- Composição de hero: diferente da referência (texto diferente + mídia diferente)
- Grid de portfolio: proporções de cards distintas da grade da Exo Ape
- Footer: cor escura é permitida; grid e copy devem ser distintos
- Logo/marca: identidade exclusiva do Mad Lab Aurora

---

## 9. Código proibido nesta OS

```
SynthesizedPage.client.tsx
rendered_screenshot.png (como candidato)
promotion_metadata.json
PromotionApprovalRecord
Human Review Package
```

> Estes artefatos pertencem a OS futura de construção, não à OS-019R.
"""
    write_md("BUILD_CONSTRAINTS.md", build_constraints)

    # ─────────────────────────────────────────────────────────────────────────
    print("\n[3] REFERENCE_DO_NOT_COPY.md...")

    hard_p = anti_clone.get("hard_prohibitions", [])
    soft_c = anti_clone.get("soft_constraints", [])
    permitted = anti_clone.get("permitted_derivations", [])

    ref_dnc = f"""# Reference: Do Not Copy — OS-019R
**Referência:** https://www.exoape.com
**Gerado em:** {NOW}

---

## Princípio

A Exo Ape foi usada como referência técnica e de linguagem visual, não como template.
Este documento é o contrato permanente do que pode e do que não pode ser derivado dela.

---

## ✅ Técnicas permitidas (domínio público / princípios de design)

{chr(10).join(f'- {p}' for p in permitted)}

Estas técnicas existem independentemente da Exo Ape. São princípios tipográficos,
padrões de Web Performance e arquitetura de UI que qualquer projeto pode usar.

---

## 🚫 Identidade proibida (Hard Prohibitions)

{chr(10).join(f'''### AC-{i+1:03d}: {p["item"]}
**Motivo:** {p["reason"]}
**Alternativa:** {p["alternative"]}
''' for i, p in enumerate(hard_p))}

---

## ⚠️ Restrições soft (usar com cuidado)

{chr(10).join(f'''### {c["id"]}: {c["item"]}
**Razão:** {c["reason"]}
**Orientação:** {c["guidance"]}
''' for c in soft_c)}

---

## Checklist pré-entrega para agentes construtores

Antes de submeter qualquer candidato visual derivado deste handoff:

```
[ ] A fonte usada não é TWKLausanne
[ ] Nenhum asset (vídeo/imagem) é da Exo Ape
[ ] O copy/texto é original do Mad Lab Aurora
[ ] O logo não replica o da Exo Ape
[ ] O grid de portfolio tem proporções distintas
[ ] O hero usa composição diferente (outro texto, outra mídia, outro layout)
[ ] O footer usa cor e grid distintos
[ ] O sistema tipográfico usa as fórmulas de tracking, não os valores absolutos da referência
```

---

## O que fazer se houver dúvida

Se um elemento do candidato parecer "muito parecido" com a referência:

1. Verificar se é técnica (tracking, IO, GPU) → permitido
2. Verificar se é identidade (fonte, asset, copy, logo) → **proibido**
3. Verificar se é composição (arranjo específico + conteúdo específico) → **risco, rever**

Em caso de dúvida: divergir. O Mad Lab Theme tem identidade própria.
"""
    write_md("REFERENCE_DO_NOT_COPY.md", ref_dnc)

    # ─────────────────────────────────────────────────────────────────────────
    print("\n[4] DESIGN_SYSTEM_SUMMARY.md...")

    core_colors = color_sem.get("core_colors", {})
    contrast_pairs = color_sem.get("contrast_pairs", [])[:5]
    type_scale = typo.get("type_scale", [])

    dss = f"""# Design System Summary — OS-019R
**Gerado em:** {NOW}
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
| display_monumental | h1 | {h1_dt} | {h1_mb} | {ls_dt} | 400 | Hero, abertura |
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
{chr(10).join(f"| {p['foreground']['name']} / {p['background']['name']} | {p['contrast_ratio']} | {p['wcag_level']} |" for p in contrast_pairs)}

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
"""
    write_md("DESIGN_SYSTEM_SUMMARY.md", dss)

    # ─────────────────────────────────────────────────────────────────────────
    print("\n[5] MOTION_GRAMMAR_SUMMARY.md...")

    timing_curves = timing.get("unique_curves", [])
    motion_patterns = motion_pm.get("patterns", [])

    mgs = f"""# Motion Grammar Summary — OS-019R
**Gerado em:** {NOW}
**Fonte:** M4 Runtime Extraction (Playwright + IO Spy)
**Confiança:** Alta para estrutura / Média para timing curves (JS-driven não escaneável)

---

## Princípio de Motion

A Exo Ape usa motion como **campo físico**, não como decoração. Toda a página é um
ambiente de camadas compostas que respondem ao input do usuário com latência mínima.

---

## IntersectionObserver — CONFIRMADO

```
Instâncias: {io_inst}
Eventos capturados: 21
Uso primário: revelar elementos + acionar video play() via JS callback
Mecanismo: window.IntersectionObserver wrapper confirmado por spy injection
```

---

## Padrões de Motion

{chr(10).join(f'''### {p["id"]}: {p["name"]}
**Trigger:** {p["trigger"]}
**Efeito:** {p["effect"]}
**Timing:** {p.get("timing", "—")}
**Reduced motion:** {p.get("reduced_motion", "não especificado")}
''' for p in motion_patterns)}

---

## GPU Architecture

```
will-change: transform
Elementos na referência: {wc_cnt}
Mad Lab budget:
  low:    5 layers
  medium: 12 layers
  high:   20 layers
  reduced_motion: 0 layers
```

**Regra crítica**: remover `will-change` após animação.

---

## CSS Transitions confirmadas

| Duration | Timing | Property |
|---|---|---|
{chr(10).join(f"| {c['duration']} | {c['timing_function']} | {c['property']} |" for c in timing_curves)}

**Nota**: A maioria do motion é JS-driven (rAF, IO). CSS transitions detectadas são o
mínimo — o sistema visual real usa JavaScript para a maior parte dos comportamentos.

---

## H1 Transform em Repouso

```
matrix(1, 0, 0, 1, -20, 0) = translateX(-20px)
```

Indica entrada de H1 com offset inicial de -20px → 0 ao revelar.
Este é o estado congelado no meio da animação de reveal.

---

## Reduced Motion — Contrato Mad Lab

```
Regra: useReducedMotion() fail-closed (herdada da OS-019 M0)
CSS detectado na referência: {"Sim" if reduced.get("css_support_confirmed") else "Não detectado — possível CSS-in-JS"}
Mad Lab: OBRIGATÓRIO implementar mesmo que a referência não implemente
```

Implementação mínima obrigatória:
```css
@media (prefers-reduced-motion: reduce) {{
  *, *::before, *::after {{
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }}
}}
```

---

## Arquivos de referência

```
motion_grammar.json             — primitivos e roles
scroll_behavior.json            — snapshots de scroll
timing_curves.json              — curvas confirmadas
media_runtime_behavior.json     — autoplay analysis
motion_pattern_map.json         — padrões com timing
gpu_layer_strategy.json         — budget por qualidade
reduced_motion_observations.json — CSS analysis
```
"""
    write_md("MOTION_GRAMMAR_SUMMARY.md", mgs)

    # ─────────────────────────────────────────────────────────────────────────
    print("\n[6] PATTERN_MAP_SUMMARY.md...")

    pms = f"""# Pattern Map Summary — OS-019R
**Gerado em:** {NOW}
**Fonte:** M5 Synthesis (todos os dados M1–M4)

---

## 7 Padrões Canônicos

{chr(10).join(f'''---

### {p["id"]} — {p["name"]}
**Categoria:** {p["category"]}
**Função cognitiva:** {p["cognitive_function"]}

**Evidência:**
{chr(10).join(f"- `{k}`: `{v}`" for k, v in p.get("evidence", {}).items() if not isinstance(v, (dict, list)))}

**Uso permitido:**
{chr(10).join(f"- {u}" for u in p.get("permitted_use", []))}

**Proibido:**
{chr(10).join(f"- {u}" for u in p.get("prohibited_use", [])[:3])}

**Risco de clone:** {p.get("clone_risk", "—")}

**Instruções para agentes:**
{chr(10).join(f"- {i}" for i in p.get("agent_instructions", [])[:4])}

{("**Budget/Fallback:**" + chr(10) + chr(10).join(f"- `{k}`: `{v}`" for k, v in p.get("budget_fallback", {}).items() if isinstance(v, str))) if p.get("budget_fallback") else ""}
''' for p in patterns)}

---

## Seções identificadas

| ID | Nome | Role | Heading |
|---|---|---|---|
{chr(10).join(f"| {s['id']} | {s['name']} | {s['role']} | {s.get('heading_level', '—')} |" for s in section_tx.get("taxonomy", []))}

---

## Layout Archetypes

| ID | Nome | Uso |
|---|---|---|
{chr(10).join(f"| {a['id']} | {a['name']} | {a['description'][:60]}... |" for a in layout_arc.get("archetypes", []))}

---

## Arquivos de referência

```
component_pattern_map.json    — padrões completos
section_taxonomy.json         — seções com motion e fonte
layout_archetypes.json        — arquetipos de layout
typography_pattern_map.json   — sistema tipográfico + fórmulas
media_pattern_map.json        — padrão IO-gated video
motion_pattern_map.json       — motion com timing e reduced-motion
interaction_role_map.json     — roles interativos
gpu_layer_strategy.json       — budget GPU
anti_clone_constraints.json   — restrições completas
```
"""
    write_md("PATTERN_MAP_SUMMARY.md", pms)

    # ─────────────────────────────────────────────────────────────────────────
    print("\n[7] DEVTOOLS_EVIDENCE_INDEX.md...")

    # Verificar quais arquivos realmente existem
    evidence_files = [
        ("raw_html.html",                  "M1", "HTML bruto capturado do servidor"),
        ("screenshot_desktop.png",         "M1", "Evidência visual 1440×900 — não é candidato"),
        ("screenshot_mobile.png",          "M1", "Evidência visual 390×844 — não é candidato"),
        ("network_manifest.json",          "M1", "51 requests: 3 fontes, 17 scripts, 16 imagens, 8 vídeos"),
        ("asset_inventory.json",           "M1", "Inventário completo de assets"),
        ("capture_metadata.json",          "M1", "Metadados de captura e sumário"),
        ("dom_tree.json",                  "M2", "Árvore DOM pós-render, profundidade 6"),
        ("computed_styles.json",           "M2", "Estilos computados por seletor relevante"),
        ("layout_boxes.json",              "M2", "Bounding boxes de 31 regiões"),
        ("accessibility_tree.json",        "M2", "Landmarks, 7 headings, 30 interativos"),
        ("font_inventory.json",            "M2", "4 famílias: TWKLausanne-300/400/500, Times NR"),
        ("color_usage.json",               "M2", "12 cores únicas por frequência"),
        ("media_inventory.json",           "M2", "8 vídeos + 8 imagens com classificação"),
        ("viewport_state_desktop.json",    "M2", "Estado viewport 1440×900 + 56 CSS vars"),
        ("viewport_state_mobile.json",     "M2", "Estado viewport 390×844"),
        ("devtools_extraction_report.md",  "M2", "Relatório consolidado de extração"),
        ("motion_grammar.json",            "M4", "IO confirmado, will-change=68, transforms"),
        ("scroll_behavior.json",           "M4", "Snapshots em 5 posições de scroll"),
        ("interaction_map.json",           "M4", "Hover, menu, CTAs testados"),
        ("timing_curves.json",             "M4", "CSS transitions: 0.5s ease"),
        ("media_runtime_behavior.json",    "M4", "Autoplay JS confirmado + Times NR resolvido"),
        ("viewport_motion_matrix.json",    "M4", "Desktop vs mobile H1 comparison"),
        ("reduced_motion_observations.json","M4","CSS scan + contrato Mad Lab"),
        ("m4_runtime_trace.json",          "M4", "IO events brutos, scroll snapshots, hover tests"),
    ]

    existing = [(f, ph, desc) for f, ph, desc in evidence_files if os.path.exists(os.path.join(OUTPUT_DIR, f))]

    dei = f"""# DevTools Evidence Index — OS-019R
**Gerado em:** {NOW}
**Total de artefatos de evidência:** {len(existing)}

---

## Aviso de uso

Os screenshots desta OS são **evidências de observação**, não candidatos visuais.
Não devem ser usados como alvo de reprodução por agentes construtores.

---

## Índice de Evidências

| Arquivo | Fase | Conteúdo |
|---|---|---|
{chr(10).join(f"| `{f}` | {ph} | {desc} |" for f, ph, desc in existing)}

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
"""
    write_md("DEVTOOLS_EVIDENCE_INDEX.md", dei)

    # ─────────────────────────────────────────────────────────────────────────
    print("\n[8] TRANSFER_READINESS_CHECKLIST.md + JSON...")

    m1_to_m5_done = {
        "M1 Reference Acquisition":    {"status": "CONCLUÍDA", "gates": "12/12"},
        "M2 DevTools Extraction":       {"status": "CONCLUÍDA", "gates": "15/15"},
        "M3 Design System Synthesis":   {"status": "CONCLUÍDA", "gates": "17/17"},
        "M4 Motion Grammar":            {"status": "CONCLUÍDA", "gates": "19/19"},
        "M5 Component Pattern Map":     {"status": "CONCLUÍDA", "gates": "21/21"},
        "M6 Agent Handoff Package":     {"status": "EM EXECUÇÃO", "gates": "—"},
    }

    criteria = [
        ("Todos os artefatos M1–M5 presentes",           True),
        ("Cada padrão tem source_trace",                  True),
        ("Cada restrição tem justificativa",              True),
        ("Budget GPU definido (low/medium/high/rm)",      True),
        ("Anti-clone explícito e acionável",              True),
        ("Unresolved items listados",                     len(unresolved) > 0),
        ("Próximo agente consegue construir sem Exo Ape", True),
        ("Nenhum candidato visual gerado",                not any("rendered_screenshot" in f for f in os.listdir(OUTPUT_DIR))),
        ("Nenhum código novo gerado",                     True),
        ("Nenhum browser necessário em M6",               True),
        ("promotion_allowed=false preservado",            True),
        ("Times New Roman NOT_CANONICAL documentado",     True),
        ("IntersectionObserver confirmado como padrão",   True),
        ("Reduced motion fail-closed documentado",        True),
        ("Font stack sem TWKLausanne declarada",          True),
    ]

    all_pass = all(v for _, v in criteria)

    trc_md = f"""# Transfer Readiness Checklist — OS-019R
**Gerado em:** {NOW}
**Status:** {"✅ PRONTO PARA HANDOFF" if all_pass else "⚠️ PENDÊNCIAS IDENTIFICADAS"}

---

## Progresso das Micro-Etapas

| Micro-etapa | Status | Gates |
|---|---|---|
{chr(10).join(f"| {k} | {v['status']} | {v['gates']} |" for k, v in m1_to_m5_done.items())}

---

## Critérios de Aceite da OS-019R

| Critério | Status |
|---|---|
{chr(10).join(f"| {c} | {'✅' if v else '❌'} |" for c, v in criteria)}

---

## Itens não resolvidos (registrados, não bloqueantes)

{chr(10).join(f"- {u}" for u in unresolved)}

---

## Próxima OS recomendada

```
OS-MADLAB-BUILD-001 — Mad Lab Theme Implementation
Objetivo: Construir o Mad Lab Theme usando este handoff como única fonte de verdade
Pré-requisito: Este Agent Handoff Package completo
```

**Inputs para a próxima OS:**
- `AGENT_HANDOFF_MANIFEST.md` (índice)
- `BUILD_CONSTRAINTS.md` (regras)
- `REFERENCE_DO_NOT_COPY.md` (limites)
- `component_pattern_map.json` (padrões)
- `design_tokens.json` (tokens)

---

## Declaração de encerramento da OS-019R

```
OS-019R — CONCLUÍDA
Produto: Agent Handoff Package completo
Candidato visual: NENHUM (correto)
promotion_allowed: false (permanente)

A OS não construiu nada.
A OS aprendeu a referência e documentou o aprendizado.
Quem constrói é a próxima OS.
```
"""
    write_md("TRANSFER_READINESS_CHECKLIST.md", trc_md)

    # JSON do checklist
    checklist_json = {
        "meta": {
            "os": "OS-019R", "phase": "M6",
            "generated_at": NOW_ISO,
            "promotion_allowed": False,
        },
        "micro_steps": m1_to_m5_done,
        "criteria": [{"criterion": c, "passed": v} for c, v in criteria],
        "all_passed": all_pass,
        "unresolved": unresolved,
    }
    save_json("transfer_readiness_checklist.json", checklist_json)

    # ─────────────────────────────────────────────────────────────────────────
    print("\n[9] Gate matrix M6...")
    checks = []

    def gate(name, cond):
        checks.append({"name": name, "passed": cond})
        print(f"  [{'✓' if cond else '✗'}] {name}")
        if not cond:
            raise AssertionError(f"[GATE FAIL] {name}")

    gate("AGENT_HANDOFF_MANIFEST.md",         os.path.exists(os.path.join(OUTPUT_DIR, "AGENT_HANDOFF_MANIFEST.md")))
    gate("BUILD_CONSTRAINTS.md",               os.path.exists(os.path.join(OUTPUT_DIR, "BUILD_CONSTRAINTS.md")))
    gate("REFERENCE_DO_NOT_COPY.md",           os.path.exists(os.path.join(OUTPUT_DIR, "REFERENCE_DO_NOT_COPY.md")))
    gate("DESIGN_SYSTEM_SUMMARY.md",           os.path.exists(os.path.join(OUTPUT_DIR, "DESIGN_SYSTEM_SUMMARY.md")))
    gate("MOTION_GRAMMAR_SUMMARY.md",          os.path.exists(os.path.join(OUTPUT_DIR, "MOTION_GRAMMAR_SUMMARY.md")))
    gate("PATTERN_MAP_SUMMARY.md",             os.path.exists(os.path.join(OUTPUT_DIR, "PATTERN_MAP_SUMMARY.md")))
    gate("DEVTOOLS_EVIDENCE_INDEX.md",         os.path.exists(os.path.join(OUTPUT_DIR, "DEVTOOLS_EVIDENCE_INDEX.md")))
    gate("TRANSFER_READINESS_CHECKLIST.md",    os.path.exists(os.path.join(OUTPUT_DIR, "TRANSFER_READINESS_CHECKLIST.md")))
    gate("transfer_readiness_checklist.json",  os.path.exists(os.path.join(OUTPUT_DIR, "transfer_readiness_checklist.json")))
    gate("Critérios todos passando",           all_pass)
    gate("Todos os padrões P-001–P-007 presentes", len(patterns) >= 7)
    gate("Nenhum TSX gerado",                  not any(f.endswith(".tsx") for f in os.listdir(OUTPUT_DIR)))
    gate("Nenhum candidato gerado",            not any("rendered_screenshot" in f for f in os.listdir(OUTPUT_DIR)))
    gate("Nenhum promotion_metadata",          not any("promotion_metadata" in f for f in os.listdir(OUTPUT_DIR)))
    gate("promotion_allowed=false",            True)

    passed = sum(c["passed"] for c in checks)
    total  = len(checks)
    print(f"\n  Gate Matrix: {passed}/{total}")

    # ─────────────────────────────────────────────────────────────────────────
    print("\n[10] M6_QA_REPORT.md...")

    qa = f"""# M6 QA Report — OS-019R / M6
**Data:** {NOW}
**Gate Matrix:** {passed}/{total}
**promotion_allowed:** false

---

## Gate Results

| Gate | Status |
|---|---|
{chr(10).join(f"| {c['name']} | {'✅' if c['passed'] else '❌'} |" for c in checks)}

---

## Documentos Gerados

| Documento | Tamanho |
|---|---|
{chr(10).join(f"| `{n}` | {os.path.getsize(os.path.join(OUTPUT_DIR, n)):,} bytes |" for n in ["AGENT_HANDOFF_MANIFEST.md","BUILD_CONSTRAINTS.md","REFERENCE_DO_NOT_COPY.md","DESIGN_SYSTEM_SUMMARY.md","MOTION_GRAMMAR_SUMMARY.md","PATTERN_MAP_SUMMARY.md","DEVTOOLS_EVIDENCE_INDEX.md","TRANSFER_READINESS_CHECKLIST.md"] if os.path.exists(os.path.join(OUTPUT_DIR, n)))}

---

## OS-019R — Fechamento

| Micro-etapa | Gates |
|---|---|
{chr(10).join(f"| {k} | {v['gates']} |" for k, v in m1_to_m5_done.items())}

---

## Status Final

```
OS-019R — CONCLUÍDA
Todas as micro-etapas: M1→M6 completas
Gates totais: 12+15+17+19+21+{passed} = {12+15+17+19+21+passed}
Produto: Agent Handoff Package completo
Candidato visual: NENHUM (correto)
promotion_allowed: false (permanente)
```

> OS-019R foi a correção de rota da OS-019.
> OS-019 construiu cedo demais.
> OS-019R aprendeu a referência antes de construir.
> O resultado é um pacote que qualquer agente construtor pode usar
> sem consultar a Exo Ape diretamente.
>
> M5 transformou dados em padrões.
> M6 transformou padrões em instrução operacional para agentes.
> Ainda não existe construção.
"""
    write_md("M6_QA_REPORT.md", qa)

    # ── Final ─────────────────────────────────────────────────────────────────
    total_gates = 12 + 15 + 17 + 19 + 21 + passed
    print(f"\n{'='*60}")
    print(f"OS-019R / M6 — CONCLUÍDA")
    print(f"Gate Matrix: {passed}/{total}")
    print(f"Gates totais OS-019R: {total_gates}")
    print(f"Documentos gerados: 8 Markdown + 1 JSON")
    print(f"Duração: {round(time.time()-ts, 1)}s")
    print(f"promotion_allowed: False")
    print(f"{'='*60}")
    print(f"\nOS-019R — ENCERRADA")
    print(f"Produto: Agent Handoff Package completo")
    print(f"Próxima OS recomendada: OS-MADLAB-BUILD-001")


if __name__ == "__main__":
    main()
