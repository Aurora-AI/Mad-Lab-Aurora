# Lighting Primitives (LGT)

```yaml
- id: LGT-001
  name: Volumetric Side Light (Chiaroscuro)
  dimension: lighting
  intent: Feixe direcional intenso lateral que intersecta o ambiente gerando chiaroscuro drástico e sombras alongadas.
  emotion: [materiality, drama, depth]
  cost: medium
  mobile: reduced
  anti_ai_score: 9
  dna_status: approved
  dna_condition: "Deve ser calibrado com cores quentes ou neutras. Proibido realces de luz frios ou dispersos."
  anti_pattern: "Iluminação plana de estúdio em render digital homogêneo."
  references: [art_production_report_elysian.md (C02_FailClosed), mad-lab-aurora-dna-v2.1.0.md]
  source_assets: [hero-futuristic, scroll-sync]
  three_js_config: "DirectionalLight + SpotLight + shadow map enabled"
  performance_budget: "Max 2 dynamic shadows casting lights, use shadow map resolution 1024x1024 max"
  prefers_reduced_motion: "Pre-baked shadow texture mapping"

- id: LGT-002
  name: Amber Spotlight (Zenital)
  dimension: lighting
  intent: Foco de luz âmbar de tungstênio projetado de cima para baixo simulando console técnico ou feixe de fenda industrial.
  emotion: [gravity, safety, authority]
  cost: low
  mobile: allowed
  anti_ai_score: 8
  dna_status: approved
  dna_condition: "Apenas um acento único âmbar ou dourado por seção. Temperatura quente em oposição ao escuro."
  anti_pattern: "Múltiplos focos de luz colorida que poluem a tela com neon."
  references: [art_production_report_elysian.md (C05_Category), ELYSIAN_BRAND_KIT_v1.1.md]
  source_assets: [spotlight-card]
  gsap_spec: "N/A"
  performance_budget: "CSS radial-gradient or simple point light in R3F"
  prefers_reduced_motion: "Static radial gradient position"

- id: LGT-003
  name: Monoline Glow (Perimeter)
  dimension: lighting
  intent: Sinalização de luz muito fina que demarca fronteiras ou dados de telemetria sem emitir brilho volumétrico exagerado.
  emotion: [precision, technicality]
  cost: low
  mobile: allowed
  anti_ai_score: 7
  dna_status: approved
  dna_condition: "Espessura de linha max 1px. Opacidade sutil (max 60%)."
  anti_pattern: "Efeitos neon volumosos de ficção científica (estilo cyberpunk clichê)."
  references: [mad-lab-aurora-dna.md]
  source_assets: [neon-button, shader-lines]
  performance_budget: "CSS drop-shadow filter limited, prefer SVG glow filter"
  prefers_reduced_motion: "Pre-rendered SVG lines with fixed low-opacity stroke"

- id: LGT-004
  name: Chiaroscuro Rim Highlight
  dimension: lighting
  intent: Luz de contra (backlight) muito afiada e fina que contorna silhuetas escuras, destacando-as do fundo escuro sem clarear a cena.
  emotion: [materiality, focus, isolation]
  cost: medium
  mobile: allowed (using static CSS or shaders)
  anti_ai_score: 9
  dna_status: approved
  dna_condition: "Deve contornar apenas as arestas externas. Cor fria sutil ou off-white quente."
  anti_pattern: "Brilhos espessos homogêneos ao redor de todo o objeto (efeito stroke simples)."
  references: [mad-lab-aurora-dna-v2.1.0.md, founder-dna.md]
  source_assets: [hero-futuristic, sovereign-hero-webgl]
  three_js_config: "Rim light material shader calculation: dot(normal, viewDir)"
  performance_budget: "Perform in fragment shader, zero dynamic light CPU overhead"
  prefers_reduced_motion: "CSS box-shadow fallback with low opacity"

- id: LGT-005
  name: Chromatic Aberration Fringe
  dimension: lighting
  intent: Simular imperfeição de lente analógica, aplicando distorção e franjas de cores (vermelho/azul) nas bordas de alta luz.
  emotion: [imperfection, memory, lens]
  cost: medium
  mobile: reduced
  anti_ai_score: 8
  dna_status: approved
  dna_condition: "Apenas em elementos periféricos de telemetria ou na borda do viewport. Desvio máximo de 2px."
  anti_pattern: "Aberração cromática excessiva que deforma a leitura de textos do corpo."
  references: [art_production_report_elysian.md (Visual World Bible)]
  source_assets: [hero-futuristic]
  three_js_config: "Post-processing shader (RGB Shift / Chromatic Aberration pass)"
  performance_budget: "Limit pass to full viewport, disable on low GPU check"
  prefers_reduced_motion: "Disable chromatic shift pass"
```
