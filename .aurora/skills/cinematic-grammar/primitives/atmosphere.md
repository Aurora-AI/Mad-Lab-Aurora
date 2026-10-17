# Atmosphere Primitives (ATM)

```yaml
- id: ATM-001
  name: Analog Halftone Grain
  dimension: atmosphere
  intent: Subtextura sutil de grão de filme analógico ou ruído estático sobreposto em baixa opacidade para eliminar o aspecto liso digital.
  emotion: [materiality, craftsmanship, imperfection]
  cost: medium
  mobile: allowed (if performance optimized)
  anti_ai_score: 9
  dna_status: approved
  dna_condition: "Opacidade extremamente baixa (max 3%). Recomenda-se grão dinâmico gerado via fragment shader ou SVG noise."
  anti_pattern: "Padrão de pontos repetidos ou diagonais estáticos (SaaS clichê)."
  references: [mad-lab-aurora-dna-v2.1.0.md, motion-narrative-delta.md]
  source_assets: [noise-grain-001]
  three_js_config: "Fragment shader with Perlin/Simplex noise or SVG filter feTurbulence"
  performance_budget: "If using fragment shader, limit instruction count. Prefer dynamic SVG background noise."
  prefers_reduced_motion: "Static noise background texture, disable animation loop"

- id: ATM-002
  name: Warm Obsidian Darkness
  dimension: atmosphere
  intent: Fundo escuro com temperatura física real (charcoal, rocha vulcânica) em oposição ao preto chapado digital.
  emotion: [editorial_weight, comfort, gravity]
  cost: low
  mobile: allowed
  anti_ai_score: 8
  dna_status: approved
  dna_condition: "Utilizar cores como #0A0A0A, #0D0D0D ou #111110. Proibido #000000 absoluto exceto em transições de silêncio."
  anti_pattern: "#000000 puro sem textura como substituto de Dark Editorial."
  references: [mad-lab-aurora-dna.md, designmanualposthero.md]
  source_assets: [background-paths, noise-grain-001]
  performance_budget: "CSS custom properties, zero cost"
  prefers_reduced_motion: "No impact"

- id: ATM-003
  name: Hazy Volumetric Dust
  dimension: atmosphere
  intent: Atmosfera com névoa sutil ou partículas em suspensão suspensas, iluminadas por focos direcionais para criar sensação de espaço físico real.
  emotion: [suspense, scale, density]
  cost: high
  mobile: restricted (limit particles count)
  anti_ai_score: 9
  dna_status: approved
  dna_condition: "Partículas devem simular gravidade real. Proibido movimento caótico ou faíscas brilhantes."
  anti_pattern: "Partículas voadoras coloridas sem física de gravidade."
  references: [motion-narrative-delta.md, art_production_report_elysian.md (C03_GovernedFactory)]
  source_assets: [falling-pattern, spiral-animation]
  three_js_config: "BufferGeometry with custom vertex shader simulating wind/gravity force"
  performance_budget: "Max 3k particles on desktop, 300 on mobile. Avoid CPU position calculations, run in GPU."
  prefers_reduced_motion: "Pre-rendered static background mesh without particles movement"

- id: ATM-004
  name: Analog Vignette Shading
  dimension: atmosphere
  intent: Escurecimento periférico não linear suave do enquadramento, direcionando a luz para o centro da composição e simulando limitações de lentes analógicas.
  emotion: [containment, intimacy, vintage]
  cost: low
  mobile: allowed
  anti_ai_score: 7
  dna_status: approved
  dna_condition: "Deve ser calibrado com cores escuras quentes. Proibido vinhetas coloridas."
  anti_pattern: "Filtro de vinheta dura com bordas pretas muito demarcadas e circulares."
  references: [mad-lab-aurora-dna.md]
  source_assets: [noise-grain-001]
  three_js_config: "Custom shader post-processing or CSS radial-gradient overlay"
  performance_budget: "If using fragment shader vignette, run in post-processing pass combined with chromatic aberration"
  prefers_reduced_motion: "No impact"

- id: ATM-005
  name: Tactile Paper Texture Map
  dimension: atmosphere
  intent: Misturar uma textura física real de papel de fibra vegetal ou linho prensado ao fundo Obsidian Dark para criar rugosidade.
  emotion: [craftsmanship, organic, truth]
  cost: low
  mobile: allowed
  anti_ai_score: 9
  dna_status: approved
  dna_condition: "A textura deve estar em baixa opacidade (max 4%) e ser de cor quente para contrastar sutilmente com o obsidian."
  anti_pattern: "Texturas de papel limpas e brancas demais ou texturas repetitivas gerando serrilhamento."
  references: [mad-lab-aurora-dna-v2.1.0.md, elysiancorp-material-library-v1.md]
  source_assets: [paper-shaders]
  performance_budget: "Compressed webp texture map (max 50kb)"
  prefers_reduced_motion: "No impact"
```
