# Design Spec — Elysian Institutional Page
Date: 2026-04-14
Status: Approved
Output target: Google Stichi prompt + implementation reference

---

## Context

Institutional landing page for Elysian (Aurora ecosystem). Primary audience: accelerator programs (Google for Startups, Anthropic). Secondary: general market / press.

Primary CTA: schedule a conversation (calendar booking).

Narrative approach: **The Manifesto** — declaration of principles → proof → invitation.

---

## Design System

### Colors
| Token | Hex | Usage |
|---|---|---|
| White Absolute | `#FFFFFF` | Primary background (odd sections) |
| Black Piano | `#000000` | Primary text, even section backgrounds |
| Cyan Aqua | `#00FFEF` | Accent, CTA section background, active states |
| Alert Red | `#FF0000` | Reserved — not used on this page |

### Typography — LayGrotesk
| Role | Weight | Size | Leading | Tracking |
|---|---|---|---|---|
| Display / H1 | Semibold | 12–17vw | 90–100% | -0.04em |
| H2 | Semibold | 5–8vw | 100–110% | -0.03em |
| H3 | Medium | 1.5–2.5rem | 110% | -0.01em |
| Body | Regular | 1–1.2rem | 150% | 0 |
| Micro / Label | Regular Uppercase | 0.6–0.75rem | — | 0.3–0.5em |

### Spacing
- Base unit: 8px / 10px
- Section macro-padding: 50px vertical (mobile), 100px (desktop)
- Grid: 12-col desktop, 4-col mobile, no gutters between cells in data grids

### Components
- **Buttons**: 0px border-radius (sharp). Primary = black bg + white text. Outline = transparent + 1px black border. Hover: directional fill toward cyan.
- **Cards**: 0px border-radius, 1px border in black/10 (light sections) or white/10 (dark sections). Left-border cyan accent on hover.
- **Labels / Tags**: ALL CAPS, LayGrotesk Regular, 0.65rem, tracked wide. Prefixed with `[ ]` brackets.
- **Icons**: SVG inline, 1px stroke, no fill. Thin elongated arrows for directional cues.
- **Dividers**: 1px lines, black/10 or white/10.

### Motion
- Scroll reveal: mask wipe bottom-to-top, 0.6s ease-out, staggered per element
- State transitions: opacity fade, 300ms
- Hover fills: directional background sweep, 400ms cubic-bezier(0.76, 0, 0.24, 1)
- No parallax, no bounce — linear, clinical

---

## Page Structure — 9 Blocks

### 00 — HEADER
- Position: fixed, full-width, z-index top
- Height: 72px
- Background: transparent on load → white (#FFF) after 50px scroll, 1px black/10 bottom border appears
- Left: "ELYSIAN" logotype, LayGrotesk Semibold, 1.1rem, black, letter-spacing -0.02em
- Right: nav links ("Ecossistema" · "Produtos" · "Método") in LayGrotesk Regular 0.75rem uppercase + CTA button "Agendar" (black bg, white text, 0px radius, px-6 py-2)

---

### 01 — HERO DECLARATION (100vh)
- Background: `#FFFFFF`
- Layout: left-aligned, full viewport
- Top-left micro-label: `[ AURORA ECOSYSTEM // 2026 ]` — LayGrotesk uppercase, 0.65rem, black/40, tracked wide
- Main headline (fills ~60% of viewport height):
  ```
  Não
  construímos
  software.
  Construímos
  infraestrutura
  cognitiva.
  ```
  LayGrotesk Semibold, ~13vw, leading 0.92, black, tracking -0.04em. Word breaks are intentional — each line is a breath.
- Subtitle (below headline, max-width 480px): "A Aurora projeta ecossistemas digitais que unem operação, inteligência aplicada, governança e ativos cognitivos." — LayGrotesk Regular, 1.1rem, black/60, leading 1.5
- Bottom-left: thin vertical line (1px black/20, 64px tall) + "scroll" micro-text rotated 90deg
- Bottom-right: "01" — LayGrotesk Semibold, 8vw, black/08, absolute positioned
- No image, no texture — the typography IS the hero

---

### 02 — DIAGNOSIS (~70vh)
- Background: `#000000`
- Label: `[ DIAGNÓSTICO // MERCADO BR ]` — cyan, 0.65rem, uppercase, tracked
- Headline (2 lines, large):
  ```
  O mercado brasileiro de IA
  está cheio de promessas.
  Vazio de infraestrutura.
  ```
  LayGrotesk Semibold, ~5vw, white, leading 1.0, tracking -0.03em
- Body (2-column grid, col-span 8 of 12):
  "Ferramentas genéricas adaptadas ao problema errado. Automações que falham quando o processo fica sério. IA sem governança, sem auditabilidade, sem contrato de confiabilidade. O mercado cresceu em promessa. Não em método."
  — LayGrotesk Regular, 1.1rem, white/55, leading 1.6
- Bottom stat line (full-width, thin border-top white/10):
  Left: `"R$ 8B investidos em tecnologia corporativa em 2025"` — mono, white/30, small
  Right: `"Zero padrão de governança para IA crítica"` — mono, cyan, small
- Section number: "02" bottom-right, white/06, large

---

### 03 — OUR ANSWER (~80vh)
- Background: `#FFFFFF`
- Label: `[ NOSSA RESPOSTA ]`
- Headline: "Um ecossistema. Quatro camadas." — LayGrotesk Semibold, ~4vw, black
- Subtext (max-width 560px): "Enquanto o mercado vendia peças isoladas, construímos um sistema. Cada camada tem uma função. Nenhuma existe sem a outra."
- 4-column grid (each col = one layer), bordered cells, 1px black/10:
  | Col | Number | Name | Description |
  |---|---|---|---|
  | 1 | `01` | AURORA GOVERNANCE | Direção estratégica, política de portfólio e governança de ecossistema. |
  | 2 | `02` | OZZMOSIS | A fábrica de capacidades reutilizáveis. A base tecnológica que sustenta todos os produtos. |
  | 3 | `03` | PRODUCTS | Sistemas especializados por domínio: comercial, jurídico e cognitivo. |
  | 4 | `04` | MADLAB | A camada criativa e institucional. Onde tecnologia encontra narrativa e presença. |
- Each cell: number in LayGrotesk mono 0.7rem black/30, title in Semibold uppercase 1rem, description in Regular 0.9rem black/60, all left-aligned, padding 40px
- Hover: left-border turns cyan (2px), bg becomes black/02

---

### 04 — WHAT WE'VE BUILT (~80vh)
- Background: `#000000`
- Label: `[ PORTFÓLIO // 2026 ]` — cyan
- Headline: "Não é visão. É o que já existe." — LayGrotesk Semibold, ~5vw, white
- 3 product cards, full-width row (or 2+1 on mobile), no gap, 1px white/10 border between:
  
  **Card 1 — Aurora CRM**
  - Tag: `OPERAÇÕES COMERCIAIS`
  - Name: "Aurora CRM" — LayGrotesk Semibold, 2rem, white
  - Description: "Operação comercial e execução outbound. Da proposta ao relacionamento, com automação, governança e integração nativa com WhatsApp."
  - Status indicator: `[ ATIVO ]` — cyan dot + cyan text, mono
  
  **Card 2 — Elysian Lex**
  - Tag: `INTELIGÊNCIA JURÍDICA`
  - Name: "Elysian Lex" — LayGrotesk Semibold, 2rem, white
  - Description: "Inteligência legal aplicada a workflows jurídicos. Análise, suporte operacional e governança com auditabilidade estruturada."
  - Status indicator: `[ EM DESENVOLVIMENTO ]` — white/40 dot + white/40 text, mono
  
  **Card 3 — Cognitive Assets**
  - Tag: `ATIVOS COGNITIVOS`
  - Name: "Aurora Cognitive Assets" — LayGrotesk Semibold, 2rem, white
  - Description: "Produção, empacotamento e distribuição de ativos cognitivos. Conhecimento estratégico que escala com método e rastreabilidade."
  - Status indicator: `[ EM DESENVOLVIMENTO ]` — white/40 dot + white/40 text, mono
  
- Each card: padding 48px, left-border 2px white/0 → cyan on hover, bg white/0 → white/04 on hover
- No images — product identity comes from the copy and structural clarity

---

### 05 — HOW WE BUILD (~90vh)
- Background: `#FFFFFF`
- Layout: asymmetric — left 55% text, right 45% diagram
- Label: `[ MÉTODO DE CONSTRUÇÃO ]`
- Headline: "Construído sobre contratos, não sobre improviso." — LayGrotesk Semibold, ~4vw, black
- Body (left column): "Cada produto do ecossistema é sustentado por uma plataforma interna de capacidades reutilizáveis. APIs tipadas. Contratos explícitos. Governança de IA com auditabilidade embutida. Não reinventamos o problema a cada produto — aceleramos a solução."
- 4 platform components listed (left column, below body), horizontal rules between:
  | Component | Description |
  |---|---|
  | **OZZMOSIS** | Fábrica de bibliotecas, contratos e runtimes compartilhados entre produtos |
  | **AURORA CONDUCTOR** | Camada de síntese que transforma intenção em plano e artefato executável |
  | **TRUSTWARE** | Contrato de confiabilidade e revisão estruturada entre produção e aprovação |
  | **ALVARO CORE** | Núcleo de raciocínio auditável para fluxos deterministas |
  Each row: component name in Semibold uppercase, description in Regular black/60, thin rule below

- Right column: abstract layer diagram — 4 horizontal bands stacked, thin 1px black borders, labels inside, thin arrow lines connecting bands, cyan dots at connection points. Clean, minimal, SVG-style.

---

### 06 — MARKET MOAT (~70vh)
- Background: `#000000`
- Label: `[ POR QUE ESTAMOS À FRENTE ]`
- Headline: "Três razões concretas." — LayGrotesk Semibold, ~4vw, white
- 3 items, stacked, separated by 1px white/10 horizontal rules:
  
  ```
  01  Plataforma própria de capacidades reutilizáveis.
      Não reconstruímos do zero. Cada produto novo
      acelera os próximos.
  
  02  Governança de IA embutida desde o início.
      Enquanto o mercado improvisa, operamos com
      trustware, trilhas de auditoria e decisão governada.
  
  03  Convergência entre operação, inteligência e presença.
      A maioria resolve um problema.
      Nós arquitetamos o ecossistema.
  ```
  
  Numbers: LayGrotesk Semibold, 5rem, white/15, inline with text
  Text: LayGrotesk Regular, 1.1rem, white/70
  Highlighted first sentence of each: white/100, Semibold

---

### 07 — THE BUILDER (~80vh)
- Background: `#FFFFFF`
- Layout: 2-column — left 45% portrait, right 55% text
- Label: `[ QUEM CONSTRÓI ]`
- Left: portrait photograph, grayscale, high-contrast, 3:4 ratio, 1px black border, no border-radius, no rounded corners. Overlaid thin grid texture (SVG, 1px lines, black/04).
- Right:
  - Overline: founder name + title in mono uppercase, black/40, small
  - Quote (large): "O futuro é determinista. Construímos sistemas que tornam o erro matematicamente improvável." — LayGrotesk Semibold, ~2.2rem, black, leading 1.1, tracking -0.02em
  - Body: "Rodrigo construiu a Aurora a partir de uma convicção: sistemas de IA precisam de método, governança e arquitetura — não apenas de um bom modelo. Do código à narrativa institucional, cada camada do ecossistema foi desenhada para durar."
  - LayGrotesk Regular, 1rem, black/60, leading 1.6
  - Bottom: thin horizontal line + "Aurora Factory // MadLab Research Group" micro-label

---

### 08 — CTA (~60vh)
- Background: `#00FFEF` (cyan — the only full-bleed color moment)
- Everything on this section is BLACK text
- Headline: "Vamos conversar sobre o que estamos construindo." — LayGrotesk Semibold, ~5vw, black, leading 0.95
- Subtext: "Se você está avaliando parceiros, investimentos ou programas de aceleração — esta é a conversa certa." — LayGrotesk Regular, 1.1rem, black/70
- CTA Button: `Agendar uma conversa →` — black bg, white text, sharp corners, large (px-10 py-5), hover: bg-white text-black
- Secondary: "ou escreva para contato@aurora.com.br" — mono, black/50, 0.75rem, below button
- Section number: "08" bottom-right, black/08, large
- No texture, no illustration — the pure cyan does the work

---

### 09 — FOOTER
- Background: `#000000`
- Top border: 1px white/10
- Left: "ELYSIAN" logotype, white, LayGrotesk Semibold, 1rem
- Center: minimal nav — "Ecossistema · Produtos · Método · Agendar" — mono uppercase, white/30, 0.65rem, tracked
- Right: "© 2026 Aurora Factory / MadLab Research Group" — mono, white/20, 0.65rem
- Height: ~80px

---

## Scroll Behavior & Animations

- **Entry animations**: every section's headline and body triggers a mask-wipe reveal (bottom → top) on scroll enter, 0.6s, ease-out. Stagger 80ms per element.
- **Header**: smooth opacity + background transition on scroll. No jump.
- **Product cards (04)**: sequential reveal left-to-right on scroll, 120ms stagger.
- **Architecture diagram (05)**: bands draw in sequentially on scroll, 200ms stagger per layer.
- **Market moat items (06)**: fade + translate-y(20px → 0) on scroll, 150ms stagger.
- **CTA section (08)**: headline split into words, each word animates up with 60ms stagger.

---

## Copy Notes for Accelerator Audience

The following phrases must appear verbatim or in close paraphrase:
- "infraestrutura cognitiva" (not "software", not "soluções")
- "governança embutida" (demonstrates operational maturity)
- "contratos tipados / APIs tipadas" (demonstrates engineering discipline)
- "auditabilidade" (key for Anthropic's trust/safety focus)
- "plataforma própria" (demonstrates technical moat)
- Product status should be honest: CRM = active, Lex + Cognitive Assets = in development

Do NOT use:
- "desenvolvemos soluções digitais"
- "fazemos IA para empresas"
- "plataforma inovadora"
- "transformação digital"

---

## Files
- Design doc: `docs/superpowers/specs/2026-04-14-elysian-institutional-design.md`
- Target implementation: `src/App.tsx` + section components in `src/components/`
- Reference tokens: `src/index.css`
