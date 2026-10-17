# Elysian Design System

> Category: Aurora Ecosystem
> Governed AI infrastructure — dual-world cyber-industrial-meets-luxury-editorial. Validated Operational Memory, fail-closed agents, deterministic gates.

## 1. Visual Theme & Atmosphere

Two worlds. **Luminous (light):** parchment canvas `#F8F7F3`, ink text `#1A1A17`, warm neutrals. **Sovereign (dark):** pure black `#000000`, paper `#F2F2F2` text, silver/gold metallics. The sole accent in both worlds is **Elysian Moss `#4E5B4B`** (lifted to `#6B7A66` on black). Sections alternate worlds to create rhythm. No neon, no emerald, no purple gradients. Imagery is black-and-white / grayscale. Halftone grain at ~2% opacity is the connective tissue.

## 2. Color Palette

| Token | Value | Role |
|---|---|---|
| `--parchment` | `#F8F7F3` | Primary light canvas |
| `--obsidian` | `#000000` | Primary dark canvas |
| `--ink` | `#1A1A17` | Primary text on light |
| `--parchment-text` | `#F2F2F2` | Primary text on dark |
| `--moss` | `#4E5B4B` | The only brand accent |
| `--moss-bright` | `#6B7A66` | Moss lifted for dark bg |
| `--silver-glimmer` | `#E5E7EB` | Dark world only — metallic highlight |
| `--silver-technical` | `#9CA3AF` | Dark world only — muted metadata |
| `--gold-sovereign` | `#D4AF37` | Dark world only — ceremonial |
| `--rust` | `#984731` | Diagnostic critical |
| `--amber` | `#D97706` | Diagnostic caution |

## 3. Typography

Four voices only. Fibonacci scale on 21px base: 8 · 13 · 21 · 34 · 55 · 89 · 144.

| Voice | Family | Weight | Use |
|---|---|---|---|
| Brand (`t-brand`) | Lanche → Instrument Serif fallback | 400 | Wordmark, monumental headlines |
| Display (`t-display`) | Instrument Serif | 400 | Editorial headlines, accent word in *italic + moss* |
| Body (`t-editorial`) | Public Sans | 300–400 | Running text |
| Mono (`t-mono`) | JetBrains Mono | 500 | Metadata, labels, coordinates, build IDs — UPPERCASE, tracked 0.18em |
| Legal (`t-legal`) | Crimson Pro | 600 | Lex vertical only |

Serifs shine at regular weight. Mono is **always** uppercase + tracked. Never use system fonts (Inter, Roboto, Arial) as display voices.

## 4. Spacing & Layout

Fibonacci on 8px base: 8 · 13 · 21 · 34 · 55 · 64 · 104 · 168 · 272. Grids are asymmetric 13-column CSS Grid. Never 3-equal-column card grids. Never centered hero text columns (the wordmark is the one centered exception). Radii near-zero: 0 for CTAs/imagery, 3–5px for cards, 9999px only for status dots.

## 5. Interaction & Motion

"Liquid" — long durations (1.2s default), monumental easing. Signature: `expo.inOut` for world transitions. Hover: slow tonal crossfade to moss/black (~0.4–0.7s). No bounce, no spring jitter, no CRT scanlines, no character scramble on visible UI.

## 6. Voice & Copy

Sober, technical, authoritative. Institutional third person + imperative. Short sentences. Brackets on labels: `[ 02 // The Integrity Gap ]`, `[ DEPLOY SOVEREIGNTY ]`. Vocabulary: Determinism, Auditability, Sovereignty, Governance, Validated Operational Memory. Avoid: "chatbot", "AI-powered", "innovation", military cosplay, exclamation marks, emoji.

## 7. Dark World Rules

Depth on black via hairline borders (`rgba(255,255,255,0.08)`) and 5%-white top-edge highlights — shadows vanish on black. Metallics (silver, gold) appear **only** in the dark world.

## 8. Component Signatures

- **Buttons:** `rounded-sm` (2px), moss fill, `t-mono` label, `[ DEPLOY_SOVEREIGNTY ]` editorial bracket style.
- **Cards:** deep lifted shadow (`0 34px 89px -21px rgba(0,0,0,.15)`) on light; hairline border on dark.
- **MetaLabel:** `[ 02 // ... ]` mono wayfinder pattern.
- **Status dot:** 5–7px round, diagnostic color, pulsing, beside mono label.

## 9. Anti-Patterns (banned)

Symmetric linear layouts without axis breaks · System fonts as display voices · Neon SaaS gradients (purple→blue→green) · Commercial template border-radius/shadows · Bounce/elastic motion without reason · `#000000` as dark-mode substitute without narrative posture · Emoji · `snake_case` in UI copy.
