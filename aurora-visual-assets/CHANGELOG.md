# Aurora Visual Assets — Changelog

## [1.5.1] — 2026-04-19

### Industrialização e Resiliência (AURORA_TRUSTWARE)
- **WebGL Scroll Sync**: 
  - Adicionada função `dispose()` para limpeza de event listeners e recursos do renderer.
  - Implementada detecção de `prefers-reduced-motion` para inibição de glitch cinético.
- **Depth Map Parallax**:
  - Implementada resiliência TSL (null-checks) para evitar crashes se texturas carregarem de forma assíncrona.
  - Integração de acessibilidade para zerar intensidade de parallax se o usuário preferir movimento reduzido.

## [1.5.0] — 2026-04-19

### Fase 2 — Expansão de Profundidade
- **effects/depth-map/depth-map-parallax** — Implementação canônica modular do padrão P001 (WebGPU/TSL).
  - Categorização: `effects/depth-map`.
  - Integração: Preparado para sincronização absoluta via P046.
  - Veredito CEO-Effects: APROVADO.
  - Veredito CEO-Design: APROVADO.

## [1.4.0] — 2026-04-18

### Fase 2 Iniciada — Biblioteca WebGL
- **effects/scroll-sync/webgl-scroll-sync** — sistema de sync canvas+DOM sem scroll-jacking
  - Origem: Lusion Ltd (MIT)
  - Padrões extraídos: P046, P047, P048, P049, P050, P051, P052
  - CEO-Effects: APROVADO COM RESSALVAS
  - CEO-Design: APROVADO (infraestrutura)
  - Total de padrões: P001–P052 (52 padrões)

### Marco
- Fase 2 (biblioteca WebGL) iniciada
- Primeiro ativo de infraestrutura WebGL ingerido
- Elo entre profundidade WebGL (P001–P005) e DOM estabelecido

## [1.40.0] — 2026-04-18

### MILSTONE: PRIMEIRO ATIVO AURORA-NATIVE
- Construção do ativo inaugural da Aurora Factory.
- Ativo: **heroes/aurora-native-hero**
- DNA: Dark Editorial (Silêncio Visual + Tipografia).

### Adicionado
- **heroes/aurora-native-hero** — Aurora Native Hero
  - Técnicas: 5-Frame GSAP Narrative, physical scrub (1.6), Lenis bridge.
  - Veredito CEO-Design: APROVADO 100%.
  - Padrões genuínos: P006, P008, P010, P015, P040, P042, P045.

---

## [1.20.0] — 2026-04-18
### Adicionado
- **typography/layered-text-001** — Layered Text Effect
  - Técnicas: Sheared Isometric Stacking, Vertical Layer Swap, Geometric Offset Mapping.
  - Padrões novos: P037, P038, P039.
  - Interação: GSAP-stagger transition com profundidade isométrica.

## [1.19.0] — 2026-04-18
### Adicionado
- **typography/vapour-text-001** — Vapour Text Effect
  - Técnicas: Canvas Pixel Sampling, Phase-Based Kinetic Typography.
  - Padrões novos: P035, P036.
  - Arquitetura: Inception of SEO-friendly canvas-based typography.

## [1.18.0] — 2026-04-18
### Adicionado
- **backgrounds/shader-lines** — Procedural Energy Flow with Mosaic Distortion.
  - Técnicas: Dynamic Script Loading, Mosaic Distortion, Harmonic Loops.
  - CEO-Effects: APROVADO — alinha com Dark Editorial.
  - CEO-Design: RESISTENTE.
  - Padrões novos: P033, P034.

## [1.17.0] — 2026-04-18
### Adicionado
- **backgrounds/plasma-grid** — Bare-Metal WebGL Plasma Grid
  - Técnicas: Bare-Metal WebGL, Normalized Coordinate Warp.
  - Anatomy: `backgrounds/plasma-grid/anatomy/plasma-grid.md`

## [1.16.0] — 2026-04-18
### Adicionado
- **backgrounds/paper-shaders** — GLSL Shader Plane & Energy Ring
  - Técnicas: Custom GLSL Shaders, Geometry Deformation, Procedural Noise.
  - Anatomy: `backgrounds/paper-shaders/anatomy/paper-shaders.md`

## [1.15.0] — 2026-04-18
### Adicionado
- **interactions/image-comparison-slider** — Vanilla React Image Comparison
  - Técnicas: Vanilla State Management, Global Event Capture.
  - Anatomy: `interactions/image-comparison-slider/anatomy/image-comparison-slider.md`

## [1.14.0] — 2026-04-18
### Adicionado
- **interactions/image-comparison** — Dual Clip-Path Comparison Slider
  - Técnicas: Dual Clip-Path Sync, Spring Physics, Context Slider.
  - Anatomy: `interactions/image-comparison/anatomy/image-comparison.md`

## [1.13.0] — 2026-04-18
### Adicionado
- **sections/stack-feature** — Multi-Orbit Feature Section
  - Técnicas: Multi-Orbit Rotation, Counter-Rotation Compensation.
  - Anatomy: `sections/stack-feature/anatomy/stack-feature.md`

## [1.12.0] — 2026-04-18
### Adicionado
- **backgrounds/falling-pattern** — Infinite Coordinate Sliding Background
  - Técnicas: Infinite Coordinate Sliding, Dot Matrix Overlay.
  - Anatomy: `backgrounds/falling-pattern/anatomy/falling-pattern.md`

## [1.11.0] — 2026-04-18
### Adicionado
- **interactions/spotlight-card** — Coordinate-Synced Glow Card
  - Técnicas: Fixed Coordinate Syncing, Advanced CSS Mask Compositing.
  - Anatomy: `interactions/spotlight-card/anatomy/spotlight-card.md`

## [1.10.0] — 2026-04-18
### Adicionado
- **borders/neon-button** — Gradient Border Glimmer (Edge Glow)
  - Técnicas: Gradient Border Glimmer, Edge Glow, CVA.
  - Anatomy: `borders/neon-button/anatomy/neon-button.md`

## [1.9.0] — 2026-04-18
### Adicionado
- **interactions/particle-text** — Physics-Based Particle Text transmutations
  - Técnicas: Text-to-Canvas Pixel Mapping, Physics-Based Steer Behaviors.
  - Anatomy: `interactions/particle-text/anatomy/particle-text.md`

## [1.8.0] — 2026-04-18
### Adicionado
- **backgrounds/spiral-animation** — Kinetic Wormhole 3D Canvas
  - Técnicas: 3D-to-2D Perspective Projection, GSAP-Driven Canvas State.
  - Anatomy: `backgrounds/spiral-animation/anatomy/spiral-animation.md`

## [1.7.0] — 2026-04-18

### Adicionado
- **backgrounds/entropy-001** — Order/Chaos Canvas Particles
  - Técnicas: Entropy Particle Physics, Canvas Proximity Networking.
  - Anatomy: `backgrounds/entropy-001/anatomy/entropy-001.md`

### Padrões documentados
- `P016` — Entropy Particle Physics
- `P017` — Canvas Proximity Networking

---

## [1.6.0] — 2026-04-18

### Adicionado
- **backgrounds/paths-001** — SVG Organic Flow + Staggered Typography
  - Técnicas: SVG Organic Flow, Staggered Typography.
  - Anatomy: `backgrounds/paths-001/anatomy/paths-001.md`

### Padrões documentados
- `P014` — Dynamic SVG Flow
- `P015` — Spring-Staggered Typography

---

## [1.5.0] — 2026-04-18

### Adicionado
- **interactions/stacked-panels** — Stacked Interactive Panels (moazamtrade)
  - Técnicas: Gaussian Wave, 3D Stacking, Multiply Blend Overlays.
  - Anatomy: `interactions/stacked-panels/anatomy/stacked-panels.md`

### Padrões documentados
- `P012` — Gaussian Proximity Wave
- `P013` — 3D Depth Stacking

---

## [1.4.0] — 2026-04-18

### Adicionado
- **heroes/hero-davincho** — Davincho Parallax Hero (cnippet.dev)
  - Técnicas: Scroll-Driven Parallax, Mix-Blend Difference, Clip-Path Masking.
  - Anatomy: `heroes/hero-davincho/anatomy/hero-davincho.md`

### Padrões documentados
- `P010` — Scroll-Driven Transform Parallax
- `P011` — Typography Mix-Blend Difference

---

## [1.3.0] — 2026-04-18

### MILSTONE: CORPUS INICIAL FINALIZADO
- Biblioteca atingiu o threshold de 3 ativos canônicos.
- Ativação do status **Native (Corpus-trained)** para o agente CEO-Design.

### Adicionado
- **interactions/team-marquee** — Creative Team Section (cnippet.dev)
  - Técnicas: Seamless Marquee, Grayscale Reveal, SVG Organic Strokes.
  - Anatomy: `interactions/team-marquee/anatomy/team-marquee.md`

### Padrões documentados
- `P008` — Seamless Card Marquee
- `P009` — SVG Masked Decorators

---

## [1.2.0] — 2026-04-18

### Adicionado
- **interactions/motion-footer** — Cinematics Volvox Footer (easemize)
  - Técnicas: Curtain Reveal, Magnetic Interaction, ScrollTrigger Parallax.
  - Anatomy: `interactions/motion-footer/anatomy/motion-footer.md`
  - Veredito CEO-Effects: APROVADO
  - Veredito CEO-Design: RESISTENTE

### Padrões documentados
- `P006` — GSAP Curtain Reveal
- `P007` — Magnetic Interaction Primitive

### Governança
- Ativos aprovados: 2/3 (Corpus de aprendizado CEO-Design expandido).
- Threshold para ativação do CEO-Design Native: -1 ativo restante.

---

## [1.1.0] — 2026-04-18

### Adicionado
- `agent-asset-ingestor` — skill de ingestão automática via `/ingest-asset`
  - 9 passos de protocolo com aprovação dual CEO obrigatória
  - Gate de verificação: 7x ✅ por ingestão
  - Localização: `C:\Projetos\Aurora\.agent-skills\agent-asset-ingestor\`

### Atualizado
- `_ASSET_TEMPLATE/anatomy/ASSET_TEMPLATE.md` — blocos VEREDITO CEO-EFFECTS
  e VEREDITO CEO-DESIGN adicionados como seções obrigatórias
- `heroes/hero-futuristic/anatomy/hero-futuristic.md` — vereditos duais
  preenchidos retroativamente como aprovação inaugural de referência
- `manifest.json` — campo `governance` com protocolo dual formalizado
- `PATTERNS.md` — seção de governança adicionada antes dos padrões técnicos

### Governança estabelecida
- Protocolo de Aprovação Dual CEO-Effects + CEO-Design: ativo
- Comando de ingestão: `/ingest-asset [url | código | path]`
- Assets aprovados: 1/3 (mínimo para ativação do corpus CEO-Design native)

---

## [1.0.0] — 2026-04-18

### Adicionado
- Estrutura inicial da biblioteca (`heroes/`, `effects/`, `scenes/`, `interactions/`, `typography/`)
- `manifest.json` — catálogo canônico
- `README.md` — filosofia e protocolo
- `PATTERNS.md` — padrões técnicos (P001–P005 do hero-futuristic)
- `_ASSET_TEMPLATE/` — template padronizado para novos ativos
- **heroes/hero-futuristic** — primeiro ativo canônico (David Hakobyan / @reapollo)
  - Técnicas documentadas: depth map parallax, cell noise, scan line, screen blend, bloom WebGPU
  - Anatomy: `heroes/hero-futuristic/anatomy/hero-futuristic.md`

### Estrutura estabelecida
- Protocolo de adição de ativos definido
- CEO-Design agent: corpus mínimo 1/3 ativos necessários
