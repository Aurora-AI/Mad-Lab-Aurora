# Aurora Visual Patterns — Ativos Dissecados: 20

## Protocolo de Governança — Aprovação Dual

Todo ativo na biblioteca passou por dois filtros obrigatórios antes de ser ingerido:

### CEO-Effects — Filtro de Intenção Dark Editorial
Pergunta central: *"Este efeito tem intenção — ou apenas impressiona por dois segundos e some da memória do visitante?"*

Critérios: Intenção articulável, narrativa além do visual, física com gravidade, silêncio trabalhando, permanência em 2 anos, performance sem GPU dedicada.

### CEO-Design — Filtro de Stress Estrutural
Pergunta central: *"Esta estrutura visual sobrevive ao colapso físico e preserva a autoridade do DNA visual do projeto?"*

Critérios para ativos de ATMOSFERA (efeitos, motion):
Apenas Teste 7 é obrigatório — alinhamento ao DNA do projeto. Testes 1-6 se aplicam quando o ativo contém forma, tipografia ou símbolo de identidade.

### Hierarquia de Aprovação
```
CEO-Design REJEITA → descarte imediato (DNA comprometido)
CEO-Effects REPROVA → descarte imediato (sem intenção real)
Ambos APROVAM → ingesta confirmada
Um com RESSALVAS → ingesta com ressalvas documentadas
```

---

## Padrões Identificados (Corpus Técnico)

**Atualizado em:** 2026-04-18  
**Ativos dissecados:** 7  

---

### P001 — Depth Map Parallax
**Ativo:** depth-map-parallax (Modular)  
**Técnica:** Deslocamento de UVs via Depth Map em escala de cinza.
```glsl
// TSL Implementation
const depth = texture(depthMap, uv()).r;
const displacedUv = uv().add(uMouse.mul(depth).mul(uIntensity));
```

### P002 — Cell Noise Dot Grid
**Ativo:** hero-futuristic  
**Técnica:** Cell noise procedural para intensidade orgânica em grids.
```tsx
const dot = float(smoothstep(0.5, 0.49, dist)).mul(brightness)
```

### P003 — Scan Line Progress Effect
**Ativo:** hero-futuristic  
**Técnica:** Uniform animado controlando revelação via faixa de transição suave.
```tsx
const flow = oneMinus(smoothstep(0, 0.02, abs(depth.sub(uProgress))))
```

### P004 — Screen Blend com TSL
**Ativo:** hero-futuristic  
**Técnica:** Blend mode nativo em shader para iluminação sem saturação excessiva.

### P005 — Bloom WebGPU (TSL)
**Ativo:** hero-futuristic  
**Técnica:** Pós-processamento nativo Three.js WebGPU.

### P006 — GSAP Curtain Reveal
**Ativo:** motion-footer  
**Técnica:** Revelação por scroll usando `clip-path` em containers fixos. `used_in_native: true`

### P007 — Magnetic Interaction Primitive
**Ativo:** motion-footer  
**Técnica:** Física de mola (GSAP elastic) baseada no centro do elemento.

### P008 — Scrub-Driven Cross-Fade Sequence
**Ativo:** aurora-hero  
**Técnica:** Sincronização de frames via timeline `scrub` (1.6s). `used_in_native: true`
```tsx
tl.to(frames[0], { opacity: 0, duration: 0.5 }, 0.4)
```

### P009 — Shader-Based Mouse Reveal
**Ativo:** sovereign-hero-webgl  
**Técnica:** Distância Euclidiana em fragment shader para lanterna de dados.
```glsl
float reveal = 1.0 - smoothstep(100.0, 380.0, distance(v_uv * u_res, u_mouse));
```

### P010 — Lenis-GSAP Synchronization Bridge
**Ativo:** aurora-hero / sovereign-hero-webgl  
**Técnica:** Update manual de `ScrollTrigger` no RAF do Lenis. `used_in_native: true`

### P011 — Fragment Shader Scramble Grid
**Ativo:** sovereign-hero-webgl  
**Técnica:** Textura dinâmica de caracteres (Canvas 2D) amostrada com ruído estocástico.

### P012 — Gaussian Proximity Wave
**Ativo:** stacked-panels  
**Técnica:** Campo de força via função Gaussiana aplicado em molas de proximidade.
```tsx
const influence = Math.exp(-(dist * dist) / (2 * SIGMA * SIGMA));
```

### P013 — 3D Depth Stacking
**Ativo:** stacked-panels  
**Técnica:** `perspective` + `translateZ` com `transform-style: preserve-3d`.

### P014 — Dynamic SVG Flow
**Ativo:** background-paths  
**Técnica:** Animação de `pathOffset` infinito em vetores tecnológicos.

### P015 — Spring-Staggered Typography
**Ativo:** background-paths  
**Técnica:** Entrada de chars usando física de mola com micro-atrasos. `used_in_native: true`

### P016 — Entropy Particle Physics
**Ativo:** entropy  
**Técnica:** Lógica dual (Ordem vs Caos) baseada em vetores de proximidade.

### P017 — Canvas Proximity Networking
**Ativo:** entropy  
**Técnica:** Renderização de vizinhos via raio de distância em Canvas 2D.

### P018 — 3D-to-2D Perspective Projection
**Ativo:** spiral-animation  
**Técnica:** Projeção matemática sem motor 3D: `x = (zoom * pos.x) / (pos.z - cameraZ)`.

### P019 — GSAP-Driven Canvas State
**Ativo:** spiral-animation  
**Técnica:** GSAP como clock central para state management de Canvas.

### P020 — Text-to-Canvas Pixel Mapping
**Ativo:** particle-text  
**Técnica:** Extração de coordenadas via `getImageData` de buffer invisível.

### P021 — Physics-Based Particle Steering
**Ativo:** particle-text  
**Técnica:** Steering behaviors (Arrive/Flee) baseados em massa e aceleração.

### P022 — Gradient Border Glimmer
**Ativo:** neon-button  
**Técnica:** Edge Glow via gradientes transparentes e opacidade em hover.

### P023 — Fixed Coordinate Syncing
**Ativo:** spotlight-card  
**Técnica:** Coordenadas globais via CSS variables para iluminação contínua.

### P024 — Advanced CSS Mask Compositing
**Ativo:** spotlight-card  
**Técnica:** `mask-composite: intersect` para bordas de precisão sub-pixel.

### P025 — Infinite Coordinate Sliding
**Ativo:** falling-pattern  
**Técnica:** Animação de `background-position` em strings de coordenadas massivas.

### P026 — Multi-Orbit Geometric Rotation
**Ativo:** stack-feature  
**Técnica:** Counter-rotation em camadas orbitais para legibilidade centrada.

### P027 — Dual Clip-Path Synchronization
**Ativo:** image-comparison  
**Técnica:** Recortes complementares (`inset`) sincronizados via MotionValue.

### P028 — Global Event Capture
**Ativo:** image-comparison-slider  
**Técnica:** Delegação de `mouseup` ao `window` para resets determinísticos.

### P029 — Custom GLSL Shader Material
**Ativo:** paper-shaders  
**Técnica:** Injeção de lógica matemática pura no pipeline da GPU.

### P030 — Geometry Deformation (Vertex-Level)
**Ativo:** paper-shaders  
**Técnica:** Manipulação de vértices (`attr.position`) via seno/tempo.

### P031 — Bare-Metal WebGL Integration
**Ativo:** plasma-grid  
**Técnica:** Uso direto da API `WebGLRenderingContext` sem abstrações.

### P032 — Normalized Coordinate Warp
**Ativo:** plasma-grid  
**Técnica:** Distorção trigonométrica em espaço UV.

### P033 — Dynamic External Script Injection
**Ativo:** shader-lines  
**Técnica:** Lazy-loading de bibliotecas via CDN no mount do componente.

### P034 — Fragment Shader Mosaic Distortion
**Ativo:** shader-lines  
**Técnica:** Pixelização procedural via agrupamento `floor` em UVs.

### P035 — Canvas Pixel Sampling Particle Mapping
**Ativo:** kinetic-typography  
**Técnica:** Samostragem baseada em DPR para sistemas de partículas reversíveis.

### P036 — Phase-Based Typography State Machine
**Ativo:** kinetic-typography  
**Técnica:** Estados determinísticos (Static | Vaporizing | Reconstructing) com SEO mirroring.

### P037 — Sheared Isometric Stacking
**Ativo:** typography-stack  
**Técnica:** Alternação de `skew` e `scaleY` para ilusão de dobradura 3D.

### P038 — Vertical Layer Swap Timelines
**Ativo:** typography-stack  
**Técnica:** Troca mecânica de camadas via stagger vertical em clip-path.

### P039 — Geometric Offset Mapping for 3D
**Ativo:** typography-stack  
**Técnica:** `translateX` baseado na proximidade ao centro visual.

---

### Navigation & Structural Motion (P040-P045)
- **P040: Expansion Staggering**: Sequenciamento de atrasos para menus fluídos. `used_in_native: true`
- **P041: Circular Constraint Mapping**: Uso de `clip-path: circle()` em transições.
- **P042: Spring-Loaded Entry**: Substituição de eases por física de mola real. `used_in_native: true`
- **P043: Backdrop Blur Compositing**: Divisão de camadas por desfoque e opacidade.
- **P044: Hidden-to-Visible Transition**: Emersão via escala/opacidade síncrona.
- **P045: Minimalist Constraint**: Exclusão do excesso para maximizar o luxo editorial. `used_in_native: true`

---

## Padrões WebGL — Fase 2 (P046+)

*Ingeridos de: Lusion Ltd, github.com/lusionltd/WebGL-Scroll-Sync*
*OS de ingestão: OS-ANTIGRAVITY-AURORA-VISUAL-ASSETS-20260418-010*

### P046 — Absolute Canvas Scroll Sync
**Ativo:** webgl-scroll-sync
**Técnica:** Canvas `position: absolute` com `transform: translate(scrollX, scrollY)`
a cada rAF. Zero drift porque canvas e DOM compartilham o mesmo fluxo de scroll.
```javascript
canvas.style.transform = `translate(${scrollOffset.x}px, ${scrollOffset.y}px)`
```

### P047 — Vertical Canvas Padding Buffer
**Ativo:** webgl-scroll-sync
**Técnica:** Canvas renderiza 25% extra acima e abaixo do viewport para absorver
clipping durante scroll rápido.
```javascript
const canvasHeight = viewportHeight * (1 + padding * 2) // padding = 0.25
```

### P048 — Single Canvas Multi-DOM Anchoring
**Ativo:** webgl-scroll-sync
**Técnica:** `getBoundingClientRect()` + `scrollOffset` = posição absoluta no documento.
Um canvas ancora múltiplos elementos DOM com precisão de pixel.
```javascript
item.x = rect.left + scrollOffset.x
item.y = rect.top + scrollOffset.y
```

### P049 — DOM-to-NDC Vertex Mapping
**Ativo:** webgl-scroll-sync
**Técnica:** Vertex shader converte coordenadas DOM (pixels) para NDC sem JS de posicionamento.
```glsl
vec2 pixelXY = u_domXY - u_scrollOffset + u_domWH * 0.5;
pixelXY.y = u_resolution.y - pixelXY.y;
pixelXY += position.xy * u_domWH;
vec2 xy = pixelXY / u_resolution * 2. - 1.;
```

### P050 — Scroll-Driven Glitch Shader
**Ativo:** webgl-scroll-sync
**Técnica:** Distorção proporcional à velocidade de scroll via hash noise + acumulação
de 5 amostras. Brightness aumenta com u_strength.
```glsl
for (int i = 0; i < NUM_SAMPLES; i++) {
    color += texture2D(u_texture, uv).rgb;
    uv += uvOffset;
}
color /= float(NUM_SAMPLES);
gl_FragColor = vec4(color * (1. + u_strength * 2.), 1.);
```

### P051 — Scroll Strength Exponential Decay
**Ativo:** webgl-scroll-sync
**Técnica:** Força que sobe com scroll e decai exponencialmente — comportamento físico real.
```javascript
strength *= Math.exp(-dt * 10)
strength += Math.min(targetStrength, 5)
```

### P052 — Frustum Culling Manual
**Ativo:** webgl-scroll-sync
**Técnica:** `mesh.visible = false` para elementos fora do viewport. Zero custo de render.
```javascript
item.mesh.visible = item.y < canvasBottom && item.y + item.height > canvasTop
```

---

## Backlog de Documentação
- [ ] Particle system com instancing (Three.js r128+)
- [ ] Noise-driven mesh displacement maps
