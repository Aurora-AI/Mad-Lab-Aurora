# DESIGN SYSTEM — Tone Lab OS (Marshall-Derived)

## 1. Visual Principle
Brutalismo comercial refinado + editorial musical + produto premium.
- Alto contraste.
- Preto dominante, branco como contraponto.
- Imagens muito grandes (foco total em produto e fotografia).
- Tipografia sans-serif pesada (Inter), títulos em caixa alta.
- Pouquíssimos elementos decorativos; sem "cards SaaS" com sombras.
- Bordas e divisões simples, layout modular em grandes blocos.

## 2. Typography
- **Primary Font**: "Inter", Arial, sans-serif.
- **Display/Hero**: Heavy, uppercase, tight line-height (e.g., 700 weight, -0.04em tracking).
- **Headlines (H1/H2/H3)**: Bold (700), uppercase, line-height ~1.
- **Product Title**: 16px, Bold (700), uppercase.
- **Body**: 16px, Regular (400), line-height 1.45.
- **Small/Metadata**: 12px, SemiBold (600), uppercase, 0.02em tracking.

## 3. Color Tokens
- **Core Neutrals**:
  - Black: `#000000`
  - Near Black: `#111111`
  - Charcoal: `#1a1a1a`
  - Graphite: `#2b2b2b`
  - Grays: `#4a4a4a`, `#777777`, `#bdbdbd`, `#d9d9d9`, `#efefef`
  - Off-white: `#f7f7f5`
  - White: `#ffffff`
- **Accent**: No vibrant colors (no copper/bronze). Identity comes from the product photography itself.

## 4. Spacing & Radius
- **Spacing Scale**: 8px base (4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px, 96px).
- **Border Radius**: Sharp and brutalist. `0px` default, `2px` to `4px` absolute maximum. Avoid rounded pills or 12px+ radii.
- **Shadows**: `box-shadow: none`. Separation via color blocks, 1px lines, or spacing.

## 5. UI Components
- **Buttons**: Flat, sharp edges (`border-radius: 0`). Solid black or white backgrounds. Uppercase, bold text. No pills.
- **Product Tiles**: Flat background (`#2b2b2b`), absolute positioning for title (top-left, uppercase, white), large centered product image. Hover effect: slight image scale (1.025), no heavy shadows.
- **Data Tables**: Flat background, thin lines, uppercase headers, monospace values optional.

## 6. Visual Modes

### A. Marshall Catalog Mode
- **Usage**: Equipment Catalog, Galleries (Guitars, Amps, Pedals).
- **Vibe**: DARK (`#000000`, `#111111`), LARGE IMAGES, UPPERCASE, MINIMAL METADATA, NO ELEVATED CARDS.
- **Grid**: 3-column modular grid with 1px gaps (background `#444` acting as borders).

### B. Engineering Mode
- **Usage**: Equipment Detail, Projects, Experiments, Measurements, Research, Documentation.
- **Vibe**: OFF-WHITE / CHARCOAL (`#f7f7f5`, `#1a1a1a`), DENSE DATA TABLES, DIAGRAMS, SOURCES, VERSIONING. Clean contrast for readability.
