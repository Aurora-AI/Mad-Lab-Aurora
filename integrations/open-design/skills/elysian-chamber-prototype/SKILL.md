---
name: elysian-chamber-prototype
description: Generates a self-contained HTML prototype for one chamber of the Elysian Cinematic Sequence. Dual-world (parchment/obsidian), Fibonacci layout, t-mono HUD, halftone grain. Uses Elysian Design System tokens.
class: A
risk: LOW
mode: generative / on-demand
trigger: explicit human request with chamber spec
promotion_gate: PROMOTION_ALLOWED
design_system: elysian
# SES validation 2026-06-10: ses_certification: draft | score: 65 | pass_rate: 0.8
---

# Elysian Chamber Prototype

A self-contained HTML prototype for one chamber of the Elysian Cinematic Sequence. Each chamber is a 100vh stage — dual-world (parchment or obsidian), asymmetric Fibonacci layout, t-mono HUD overlay, halftone grain. No frameworks. No CDN scripts. One file.

## Pre-flight (read before generating anything)

**MANDATORY:** Before writing a single line of HTML, read `integrations/open-design/design-systems/elysian/DESIGN.md` in full. Every decision — color, type, spacing, motion — must be grounded in that document.

## Inputs

| Parameter | Type | Required | Notes |
|---|---|---|---|
| `chamber_id` | `C01` · `C02` · `C03` · `C04` · `C05` | yes | Determines layout archetype and default world |
| `world` | `light` · `dark` | yes | Overrides default if provided |
| `headline` | string | yes | Primary display text; may include one italic+moss accent word |
| `body_copy` | string | yes | Editorial or technical paragraph |
| `density` | `low` · `medium` · `high` | yes | Controls spacing multiplier and element count |
| `special` | `spring-fragments` · `fail-closed-gate` · `r3f-placeholder` | no | Activates chamber-specific animated element |

Density mapping:
- `low` → generous padding, single-focus layout, minimal metadata
- `medium` → standard Fibonacci spacing, secondary HUD elements
- `high` → tight spacing, all HUD pillars visible, supplementary mono labels

## Outputs

A single self-contained HTML file (`elysian-chamber-{id}.html`) that:

format: HTML5 — UTF-8, inline CSS only, no external JS, no external CSS (Google Fonts @import in `<style>` is allowed).

**Required sections in order:**
1. `<head>`: `<meta charset>`, `<meta viewport>`, Google Fonts `@import`, `<style>` with CSS token variables + utility classes
2. `<body class="world-{light|dark}">`: HUD label, main content section, halftone grain overlay
3. No `<script>` tags — static prototype only

**CSS token block that MUST appear in every output:**
```css
:root {
  /* Canvas */
  --parchment: #F8F7F3;
  --obsidian: #000000;
  /* Ink */
  --ink: #1A1A17;
  --parchment-text: #F2F2F2;
  /* Accent */
  --moss: #4E5B4B;
  --moss-bright: #6B7A66;
  /* Dark metallics */
  --silver-glimmer: #E5E7EB;
  --silver-technical: #9CA3AF;
  --gold-sovereign: #D4AF37;
  /* Fibonacci spacing */
  --sp-1: 8px; --sp-2: 13px; --sp-3: 21px;
  --sp-4: 34px; --sp-5: 55px; --sp-6: 89px;
}
```

**Minimal viable skeleton:**
```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Elysian — Chamber {id}</title>
  <style>
    /* PASTE TOKEN BLOCK HERE */
    body { margin: 0; height: 100vh; overflow: hidden; background: var(--{world}-canvas); }
    .hud { position: fixed; top: var(--sp-3); left: var(--sp-5); font-family: 'JetBrains Mono', monospace; font-size: 13px; letter-spacing: 0.18em; text-transform: uppercase; }
    .grain { position: fixed; inset: 0; pointer-events: none; opacity: 0.02; }
  </style>
</head>
<body>
  <div class="hud">[ STAGE: {CHAMBER_ID} ]</div>
  <!-- CHAMBER CONTENT -->
  <div class="grain" style="background-image: url('data:image/svg+xml,...')"></div>
</body>
</html>
```

**Placeholder prevention:** Não use placeholder, não omitir campos, não truncar output. Output must never contain Lorem Ipsum, `[INSERT COPY]`, `TODO`, or generic brand names (Acme / Contoso / Example Inc). All copy comes from the skill inputs.

---

### Full output specification

The output is a **single `.html` file** with no external dependencies except Google Fonts (one `@import` in `<style>`). All CSS is inlined in `<style>`. No React, no Tailwind, no CDN scripts.

### Required HTML structure

```
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>[ STAGE: {chamber_id} ] — Elysian</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Public+Sans:wght@300;400&family=JetBrains+Mono:wght@500&family=Crimson+Pro:wght@600&display=swap" rel="stylesheet" />
  <style>
    /* 1. CSS custom properties — tokens */
    /* 2. Reset + base */
    /* 3. Typography classes */
    /* 4. Spacing utilities */
    /* 5. Layout */
    /* 6. Chamber-specific components */
    /* 7. Grain overlay */
    /* 8. HUD */
    /* 9. Motion */
  </style>
</head>
<body>
  <!-- grain overlay (::before on body or .grain div) -->
  <!-- HUD label -->
  <!-- chamber layout -->
  <script>/* animation logic */</script>
</body>
</html>
```

### CSS custom properties (embed verbatim in every output)

```css
:root {
  /* Color tokens */
  --parchment:        #F8F7F3;
  --obsidian:         #000000;
  --ink:              #1A1A17;
  --parchment-text:   #F2F2F2;
  --moss:             #4E5B4B;
  --moss-bright:      #6B7A66;
  --silver-glimmer:   #E5E7EB;
  --silver-technical: #9CA3AF;
  --gold-sovereign:   #D4AF37;
  --rust:             #984731;
  --amber:            #D97706;

  /* Fibonacci spacing */
  --sp-1:  8px;
  --sp-2: 13px;
  --sp-3: 21px;
  --sp-4: 34px;
  --sp-5: 55px;
  --sp-6: 89px;

  /* Typography scale (Fibonacci on 21px base) */
  --fs-xs:   8px;
  --fs-sm:  13px;
  --fs-md:  21px;
  --fs-lg:  34px;
  --fs-xl:  55px;
  --fs-2xl: 89px;
}
```

### Typography classes (embed in every output)

```css
.t-display {
  font-family: 'Instrument Serif', serif;
  font-weight: 400;
  letter-spacing: -0.02em;
  line-height: 1.05;
}
.t-editorial {
  font-family: 'Public Sans', sans-serif;
  font-weight: 300;
  line-height: 1.6;
}
.t-mono {
  font-family: 'JetBrains Mono', monospace;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  font-size: var(--fs-sm);
}
.t-label {
  font-family: 'Public Sans', sans-serif;
  font-weight: 400;
  font-size: var(--fs-sm);
  text-transform: uppercase;
  letter-spacing: 0.12em;
}
.t-accent {
  font-family: 'Instrument Serif', serif;
  font-style: italic;
  color: var(--moss);   /* use var(--moss-bright) on dark world */
}
```

### Halftone grain overlay

Implement as a pseudo-element on `body` or as a `<div class="grain">`. Use an SVG `feTurbulence` filter or a repeating CSS noise pattern. Opacity must be exactly `0.02` (2%). It must not block pointer events (`pointer-events: none`). It must be fixed-position and cover the full viewport (`position: fixed; inset: 0; z-index: 9999`).

```css
.grain {
  position: fixed;
  inset: 0;
  z-index: 9999;
  pointer-events: none;
  opacity: 0.02;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
  background-size: 256px 256px;
}
```

### HUD label

Always present. Fixed to top-left. Mono, 13px, uppercase.

```css
.hud-stage {
  position: fixed;
  top: var(--sp-4);
  left: var(--sp-4);
  z-index: 1000;
  font-family: 'JetBrains Mono', monospace;
  font-weight: 500;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.18em;
}
```

```html
<div class="hud-stage">[ STAGE: C02 ]</div>
```

Color: `var(--silver-technical)` on dark world, `var(--moss)` on light world.

### Layout rules

- **100vh** minimum height. Never overflow-hidden on the root chamber.
- **Asymmetric only.** Use CSS Grid with an asymmetric column definition (e.g., `13fr 8fr`, `8fr 5fr 2fr`, `1fr 2fr 1fr` with content spanning non-center tracks). Never `repeat(3, 1fr)` for the primary layout.
- Content axis is always left-anchored or right-anchored. Centered text blocks are forbidden except for the lone wordmark in C05.
- `border-radius`: 0 for CTA buttons and image frames; 3–5px maximum for card surfaces; `9999px` only for status indicator dots.
- Spacing between major zones: use `--sp-5` (55px) or `--sp-6` (89px). Never arbitrary pixel values.

### Motion rules

- Duration: 1.2s default. Use `cubic-bezier(0.76, 0, 0.24, 1)` (expo.inOut equivalent).
- Entrance: `translateY(21px) → translateY(0)` + `opacity 0 → 1`.
- Hover: slow tonal crossfade (~0.5s ease). Moss fill on CTAs at hover.
- Animate only `transform` and `opacity` (GPU-composited). No `width`, `height`, or `color` transitions on performance-critical elements.
- No bounce. No spring jitter. No elastic overshoot. See BANNED section.

---

## Chamber Archetypes

### C01 — Spring Fragments (light world)

**Canvas:** `--parchment` (`#F8F7F3`). Text: `--ink`.

**Concept:** Scattered Portuguese workplace words (`reunião`, `planilha`, `relatório`, `aprovação`, `prazo`, `delegação`) orbit the viewport, then a gravitational editorial headline assembles at center-left. The fragments represent the cognitive load that Aurora absorbs.

**Layout:**
- Full-bleed 100vh stage
- Words placed via absolute positioning at varied x/y coordinates — use a grid of non-uniform anchor points, not a random scatter. Suggested anchors: top 15% / left 22%; top 38% / left 68%; top 62% / left 11%; top 78% / left 55%; top 25% / right 18%; top 52% / right 8%
- Editorial headline: `t-display`, `font-size: var(--fs-2xl)` (89px), left-aligned, positioned at vertical center-left (`top: 40%; left: var(--sp-6)`)
- Body copy below headline: `t-editorial`, `max-width: 44ch`

**`special: spring-fragments` behavior:**
- On load, fragment words start at `opacity: 0, scale: 0.6` with staggered delays (0ms, 120ms, 240ms, …)
- They animate to `opacity: 0.18, scale: 1` — they are **background texture**, not foreground content
- Hover on any fragment: raise to `opacity: 0.55`, `t-mono` style, `color: var(--moss)`
- Headline fades in last (after all fragments) at full `opacity: 1`

**Without `special`:** Fragments are static at `opacity: 0.18`.

---

### C02 — Fail-Closed Gate (dark world)

**Canvas:** `--obsidian` (`#000000`). Text: `--parchment-text`.

**Concept:** The sovereignty chamber. A gate motif (two vertical bars that close and lock) introduces the controlled-agency thesis. Five HUD pillars run along the bottom edge.

**Layout:**
- Gate element: centered on horizontal axis, upper 55% of viewport
- Headline: `t-display`, `font-size: var(--fs-xl)` (55px), left-anchored below gate, `left: var(--sp-6)`
- Body copy: `t-editorial`, below headline, `max-width: 52ch`, `color: var(--silver-technical)`
- HUD pillars: five mono labels in a row along bottom edge, `padding-bottom: var(--sp-4)`

**LOCKED COPY — reproduce verbatim, do not paraphrase:**

Headline (Portuguese):
> A inteligência não é deixar a IA decidir mais. É definir exatamente o que ela não pode decidir.

Body (English):
> We study controlled agency: systems that can reason, plan and simulate, but cannot mutate production without deterministic gates.

HUD pillars (bottom row, left to right, t-mono 13px, `color: var(--silver-technical)`):
```
fail-closed · human approval · auditability · evaluation gates · bounded autonomy
```
Render each pillar as a separate `<span class="t-mono">` separated by hairline `<span class="pillar-sep"> · </span>`.

**`special: fail-closed-gate` behavior:**
- Gate: two vertical rectangles (`width: 3px`, `height: 180px`, `background: var(--silver-glimmer)`) start 120px apart
- On load after 600ms delay: they slide together (`gap → 0`) over 1.4s `cubic-bezier(0.76, 0, 0.24, 1)`
- A horizontal `1px` hairline crossbar fades in at the midpoint after the close completes
- Headline and body fade in sequentially after gate closes

**Without `special`:** Gate is static (bars already closed, crossbar visible).

---

### C03 — Conveyor Stage (dark world)

**Canvas:** `--obsidian`. Text: `--parchment-text`.

**Concept:** A horizontal conveyor belt of stage labels (`[ INTAKE ]`, `[ VALIDATE ]`, `[ EXECUTE ]`, `[ AUDIT ]`, `[ RETURN ]`) scrolls from right to left. Álvaro's narrative appears in the left column. A designated region on the right holds the R3F placeholder.

**Layout (asymmetric grid):**
```css
.c03-grid {
  display: grid;
  grid-template-columns: 5fr 3fr;
  grid-template-rows: auto 1fr auto;
  height: 100vh;
  padding: var(--sp-6) var(--sp-5);
  gap: var(--sp-4);
}
```
- Left column: Álvaro narrative text (headline + body copy), vertically centered
- Right column: R3F placeholder region — a `1px solid rgba(255,255,255,0.08)` bordered rectangle labeled `[ R3F: 3D SCENE ]` in `t-mono`, centered within the box
- Conveyor: full-width horizontal strip, `height: 55px`, positioned at bottom of viewport above HUD

**Álvaro narrative:** The headline and body_copy inputs populate the left column. If no body_copy provided, use: *"Every agent that touches a production system carries a constitutional obligation — not to a company, but to the humans whose work it affects."*

**`special: r3f-placeholder` behavior:**
- The right-column box renders as a **2D flat version** of the intended 3D scene
- Use SVG perspective grid lines (`stroke: rgba(255,255,255,0.06)`) to suggest depth
- A single centered label `[ 3D SCENE PENDING ]` in `t-mono` over the grid
- This is intentionally inert — no animation, no interaction — it is a compositional reserve

**Conveyor animation (always active in C03):**
- A flex row of stage labels repeats twice for seamless loop
- `@keyframes conveyor { from { transform: translateX(0) } to { transform: translateX(-50%) } }`
- Duration: 28s linear infinite
- Labels: `t-mono`, `color: var(--silver-technical)`, separated by 89px gaps

---

### C04 — Product Witness (light world)

**Canvas:** `--parchment`. Text: `--ink`.

**Concept:** Product capability cards arranged in an asymmetric bento — uneven row heights, 1px hairline dividers, no card shadows (light world uses `box-shadow: 0 34px 89px -21px rgba(0,0,0,.12)`). An editorial declaration anchors the left column.

**Layout:**
```css
.c04-grid {
  display: grid;
  grid-template-columns: 8fr 5fr;
  grid-template-rows: auto auto;
  min-height: 100vh;
  padding: var(--sp-6);
  gap: var(--sp-4);
}
```
- Left column (top): editorial headline `t-display`, `font-size: var(--fs-xl)`
- Left column (bottom): body copy `t-editorial`, `max-width: 46ch`
- Right column: 2–4 product cards, uneven heights (alternate `min-height: 144px` and `min-height: 89px`), `border: 1px solid rgba(26,26,23,0.1)`, `border-radius: 4px`, `padding: var(--sp-4)`
- Cards contain: a `t-label` category tag, a `t-editorial` description (2–3 sentences), no icons, no images

**Card contents for density `medium` (default):**
- Card 1: `[ ORCHESTRATION ]` — Aurora coordinates multi-agent workflows with deterministic task routing.
- Card 2: `[ MEMORY ]` — Validated Operational Memory persists context across sessions without hallucination drift.
- Card 3: `[ GOVERNANCE ]` — Every decision tree carries an audit trail. No black-box actions.

**density `high`** adds Card 4: `[ LEGAL ]` — Lex vertical for contract review, compliance flagging, NDA triage.

---

### C05 — Sovereign Wordmark (dark world)

**Canvas:** `--obsidian`. Text: `--parchment-text`.

**Concept:** Monumental. The Elysian wordmark dominates at maximum scale. A single CTA. Nothing else competes.

**Layout:**
- Wordmark: centered (the one permitted centered exception), `t-display`, `font-size: clamp(89px, 14vw, 180px)`, `letter-spacing: -0.03em`, `color: var(--parchment-text)`
- One accent word or phrase in `.t-accent` (italic, `--moss-bright`) within or below the wordmark
- Category label above wordmark: `t-mono`, `color: var(--silver-technical)`, `font-size: 13px`
- CTA button below wordmark: `t-mono` label `[ REQUEST PARTNERSHIP ]`, `background: var(--moss)`, `color: var(--parchment-text)`, `border-radius: 2px`, `padding: var(--sp-2) var(--sp-4)`
- The wordmark is the only centered element. The CTA may be centered beneath it.
- Supplementary: a hairline horizontal rule (`1px solid rgba(255,255,255,0.08)`) above the CTA band

**Hover state on CTA:** `background` transitions to `var(--moss-bright)` over 0.5s ease. No shadow. No scale.

---

## Hard Anti-Patterns — BANNED

These patterns are absolutely forbidden regardless of chamber, world, or input. If a generation produces any of the following, it is incorrect and must be revised.

| Category | Banned |
|---|---|
| **Backgrounds** | Neon/gradient SaaS backgrounds: purple, blue, electric green, cyan. Glassmorphism blur panels. Dark-mode purple (`#1a1a2e`, `#0d0d1a`, etc.) |
| **Border radius** | `border-radius > 5px` on card surfaces. `rounded-xl`, `rounded-2xl`, `rounded-full` on anything that is not a status dot |
| **Typography** | System fonts (Inter, Roboto, Arial, Helvetica) used as display or headline voices. Google Fonts that are not in the approved Elysian set |
| **Motion** | Bounce easing (`cubic-bezier` with overshoot), spring jitter, elastic animations, `animation-timing-function: spring(...)`. Any animation that overshoots its endpoint |
| **Layout** | Symmetric 3-equal-column `repeat(3, 1fr)` grids as the primary layout. Centered text-column hero layouts (except C05 wordmark). Full-bleed dark background with centered white text block — this is generic SaaS |
| **Copy** | Emoji anywhere in the UI. `snake_case` in visible copy. AI clichés: "seamless", "unleash", "next-gen", "AI-powered", "innovation" |
| **Components** | Drop shadows on dark world cards (use hairline borders instead). `box-shadow` with color (blue glow, purple glow, etc.) |

---

## Pre-flight checklist

Before returning the HTML file, verify:

- [ ] `DESIGN.md` was read before generation started
- [ ] Correct canvas: light → `#F8F7F3`, dark → `#000000`
- [ ] All color tokens present as CSS custom properties
- [ ] Google Fonts import includes all four families
- [ ] All five typography classes present (`.t-display`, `.t-editorial`, `.t-mono`, `.t-label`, `.t-accent`)
- [ ] Grain overlay present at `opacity: 0.02`, `pointer-events: none`
- [ ] `[ STAGE: {chamber_id} ]` HUD label present, top-left, 13px t-mono
- [ ] Fibonacci spacing variables `--sp-1` through `--sp-6` present
- [ ] Layout is asymmetric (no `repeat(3, 1fr)` primary grid)
- [ ] No banned border-radius, fonts, motion, or copy patterns
- [ ] C02: locked Portuguese headline and English body reproduced verbatim
- [ ] C02: all five HUD pillars present
- [ ] File is self-contained (no external scripts, no CDN JS)

---

## Referências

- [DESIGN.md](file:///C:/Projetos/MadLabAurora/integrations/open-design/design-systems/elysian/DESIGN.md) — Elysian Design System tokens, typography, spacing, motion rules. **MANDATORY read before generating any chamber.**
