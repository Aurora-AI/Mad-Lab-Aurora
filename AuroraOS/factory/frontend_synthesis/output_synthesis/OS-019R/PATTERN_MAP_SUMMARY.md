# Pattern Map Summary — OS-019R
**Gerado em:** 2026-06-08 22:35:31
**Fonte:** M5 Synthesis (todos os dados M1–M4)

---

## 7 Padrões Canônicos

---

### P-001 — Monumental Editorial Hero
**Categoria:** typography
**Função cognitiva:** Criar impacto visual imediato através de tipografia de escala extrema. O tamanho não é decorativo — é a mensagem primária. O conteúdo entra pelo tamanho antes de ser lido pelo significado.

**Evidência:**
- `font_size_desktop`: `250px`
- `font_size_mobile`: `62.4px`
- `letter_spacing_desktop`: `-11.5px`
- `letter_spacing_mobile`: `-1.56px`
- `font_family`: `TWKLausanne / Lausanne-300`
- `font_weight_computed`: `400`
- `line_height_ratio`: `0.904`
- `tracking_ratio_desktop`: `-0.046`
- `tracking_ratio_mobile`: `-0.025`

**Uso permitido:**
- Título de abertura de seção hero
- Manifesto ou declaração institucional
- Nome de projeto em abertura de case study
- Qualquer texto de no máximo 3–5 palavras em escala monumental

**Proibido:**
- Corpo de texto ou parágrafos
- Labels ou metadados
- Texto abaixo de 80px que não recalibrou tracking

**Risco de clone:** MEDIUM — escala extrema com tracking negativo é a assinatura da referência. Usar com conteúdo diferente e composição diferente.

**Instruções para agentes:**
- Usar Lausanne-300 como família ou equivalente aprovado no handoff
- Calcular letter-spacing como: tamanho_px × (-0.046) para desktop, × (-0.025) para mobile
- line-height = font-size × 0.904 (tight editorial)
- font-weight: 400 — não usar bold em escala monumental



---

### P-002 — Intersection-Gated Editorial Media
**Categoria:** media
**Função cognitiva:** Mídia só entra em atividade quando o usuário chega na zona de interesse. Cria sensação de revelação progressiva — cada seção 'acorda' ao ser alcançada. Economiza performance e cria ritmo de descoberta.

**Evidência:**
- `mechanism`: `IntersectionObserver (JS) — não atributo HTML autoplay`
- `io_instances`: `1`
- `io_events_captured`: `21`
- `videos_playing_after_scroll`: `8`
- `autoplay_html_attribute`: `False`
- `pattern`: `muted + loop + IO-triggered = ambient editorial loops`

**Uso permitido:**
- Vídeos de projeto/case study em cards editoriais
- Background ambient de seções sem narração
- Demonstração de produto em contexto de portfolio

**Proibido:**
- Autoplay via atributo HTML sem IntersectionObserver
- Mídia com narração/áudio sem controles visíveis
- Autoplay fora da viewport (desperdício de performance)

**Risco de clone:** LOW — o padrão é técnico (IntersectionObserver), não visual. Implementar com conteúdo próprio.

**Instruções para agentes:**
- Implementar IntersectionObserver para acionar play() quando ratio >= 0.3
- Sempre muted=true para autoplay permitido pelos browsers
- loop=true para ambient media
- preload='none' até o elemento entrar no threshold

**Budget/Fallback:**
- `reduced_motion`: `poster_static_only`
- `low_bandwidth`: `poster_static_with_play_button`

---

### P-003 — Minimal Sticky Navigation
**Categoria:** navigation
**Função cognitiva:** Presença persistente que não compete com o conteúdo principal. A navegação existe como acesso seguro, não como âncora visual. O conteúdo é a cena — a nav é a saída de emergência.

**Evidência:**
- `position`: `fixed`
- `z_index`: `9`
- `menu_button_z`: `14`
- `theme`: `adapts via .is-light / .is-dark on .app element`
- `height`: `21`

**Uso permitido:**
- Navegação principal fixa com menu hamburger
- Nav que adapta contraste ao contexto da seção atual
- Logo + links essenciais + CTA único

**Proibido:**
- Nav com altura superior a 80px
- Nav com elementos visuais pesados (gradientes, sombras profundas)
- Nav que compete visualmente com hero ou seção ativa

**Risco de clone:** LOW — estrutura funcional padrão. Risco apenas se copiar identidade visual (logo, cores, copy).

**Instruções para agentes:**
- position: fixed, z-index: 9 para nav principal
- z-index: 14 para trigger de menu (deve estar acima da nav)
- Implementar theme toggle (.is-light / .is-dark) baseado na seção ativa
- Altura máxima recomendada: 64px–80px



---

### P-004 — GPU-Composited Scroll Field
**Categoria:** motion
**Função cognitiva:** A página inteira é um campo físico onde elementos se movem com física própria durante o scroll. Não é slideshow. Não são cards. É um campo contínuo de camadas compostas que respondem ao input do usuário.

**Evidência:**
- `will_change_elements`: `68`
- `will_change_value`: `transform`
- `h1_transform_at_rest`: `matrix(1,0,0,1,-20,0) = translateX(-20px)`

**Uso permitido:**
- Reveal de elementos ao entrar na viewport (translateY, opacity, scale)
- Parallax sutil em media ou backgrounds (< 10% do scroll delta)
- Depth layers no hero (Z-axis do Mad Lab Theme)
- Entrance animations vinculadas ao IntersectionObserver

**Proibido:**
- will-change em todos os elementos sem budget definido
- Mais de 20 GPU layers simultâneos sem teste de performance
- Scroll-linked transforms sem useReducedMotion() fail-closed

**Risco de clone:** LOW — arquitetura técnica. Não há visual único para clonar — apenas o padrão de engenharia.

**Instruções para agentes:**
- Aplicar will-change: transform apenas nos elementos que serão animados (não global)
- Definir budget por qualidade: low=5 layers, medium=12 layers, high=20 layers
- Sempre incluir @media (prefers-reduced-motion: reduce) { transition: none; animation: none; }
- Usar transform (não top/left) para todas as animações de posição

**Budget/Fallback:**
- `quality_low`: `max 5 GPU layers, sem parallax`
- `quality_medium`: `max 12 GPU layers, parallax sutil`
- `quality_high`: `max 20 GPU layers, full scroll physics`
- `reduced_motion`: `static — nenhuma transform animada`
- `cleanup`: `remove will-change after animation complete`

---

### P-005 — Responsive Optical Tracking
**Categoria:** typography
**Função cognitiva:** Compensação óptica do espaço entre letras em função do tamanho do display. Em escala extrema, o espaçamento padrão cria 'frouxidão' visual. O tracking negativo restaura a coesão da palavra como unidade visual.

**Evidência:**
- `rule`: `tracking é função não linear do tamanho — diminui proporcionalmente em mobile`

**Uso permitido:**
- Qualquer display acima de 40px que precise de compensação óptica
- Sistema tipográfico editorial com escalas extremas

**Proibido:**
- Tracking negativo em corpo de texto (< 18px)
- Tracking fixo sem variação por breakpoint
- letter-spacing positivo em display extremo

**Risco de clone:** LOW — é uma regra técnica tipográfica, não uma identidade visual.

**Instruções para agentes:**
- Fórmula desktop (> 768px): letter-spacing = font-size × (-0.046)
- Fórmula mobile (< 640px): letter-spacing = font-size × (-0.025)
- Interpolar entre 0.025 e 0.046 para breakpoints intermediários
- Abaixo de 40px: tracking-ratio neutro (0 a -0.01)



---

### P-006 — Monochromatic Semantic Palette
**Categoria:** color
**Função cognitiva:** Hierarquia visual construída inteiramente por escala e peso, não por cor. A ausência de cor saturada força o olho a usar tamanho, peso e posição como único vocabulário de atenção. Cria sofisticação editorial.

**Evidência:**
- `dominant_duo`: `#0d0e13 (escuro) + #ffffff (branco)`
- `warm_editorial`: `#e0ccbb (bege quente para texto editorial/footer)`
- `accent`: `none — ênfase via escala tipográfica`
- `token_count`: `56`

**Uso permitido:**
- Sistemas editoriais e de portfolio sem necessidade de cor-marca forte
- Contextos onde a mídia (foto/vídeo) é a cor — não a UI
- Dark sections como --color-story (#070707) para contraste editorial

**Proibido:**
- Usar #e4e0db ou #e0ccbb como cor de texto em body size (falha WCAG)
- Adicionar cores saturadas sem revisar o sistema completo
- Usar Times New Roman — NOT_CANONICAL confirmado

**Risco de clone:** LOW — paleta monocromática é princípio de design, não identidade. Aplicar com brand colors próprias.

**Instruções para agentes:**
- Primary text: --color-dark-grey (#0d0e13)
- Background: --color-white (#ffffff) ou --color-off-white (#f8f8f8)
- Editorial warm: usar apenas em texto de apoio grande (> 18px bold) — WCAG risco em body
- Dark sections: --color-story (#070707) com texto claro



---

### P-007 — Section-Label Taxonomy
**Categoria:** content
**Função cognitiva:** Labels de seção em 14px com peso normal servem como âncoras de orientação silenciosas. O contraste de escala entre o label (14px) e o título da seção (144px ou 250px) cria ritmo editorial imediato.

**Evidência:**
- `label_font_size`: `14px`
- `label_font_weight`: `400`
- `contrast_ratio`: `label 14px vs display 250px = ratio 1:17.9`

**Uso permitido:**
- Rótulo de seção antes do título principal
- Categoria ou metadado de contexto
- Timestamp ou indicação de ordenação

**Proibido:**
- Labels como CTA (não são clicáveis por padrão)
- Labels para informação crítica (baixo contraste em fundo claro)
- Mais de 3 palavras por label

**Risco de clone:** LOW — padrão de UX writing universal. Risco apenas se copiar o copy exato.

**Instruções para agentes:**
- font-size: 14px, font-weight: 400
- Usar como elemento de abertura de seção antes do título
- Não usar a mesma copy da referência ('Featured Projects', etc.)




---

## Seções identificadas

| ID | Nome | Role | Heading |
|---|---|---|---|
| S-01 | Hero / Manifesto | institutional_opening | H1 |
| S-02 | Featured Work Grid | portfolio_showcase | H2 |
| S-03 | Motion Reel | motion_showcase | H2 |
| S-04 | Press / Media | credibility_social_proof | H2 |
| S-05 | Footer | navigation_closure | — |

---

## Layout Archetypes

| ID | Nome | Uso |
|---|---|---|
| LA-01 | Full-Bleed Editorial | Conteúdo cobre 100% da viewport sem margens laterais. Usado ... |
| LA-02 | Contained Content Column | Conteúdo em coluna centralizada com margens generosas. Usado... |
| LA-03 | Variable Media Grid | Grid de mídia com proporções intencionalmente variadas — não... |
| LA-04 | Sticky Nav Layer | Camada de navegação fixa acima do conteúdo, invisível mas se... |

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
