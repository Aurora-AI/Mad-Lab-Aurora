# Transition Primitives (TRN)

```yaml
- id: TRN-001
  name: Weighted Page Transition
  dimension: transition
  intent: Mudança de contexto de página com peso e desaceleração controlada, evitando cortes abruptos ou fade in genéricos.
  emotion: [sober, continuity, focus]
  cost: medium
  mobile: allowed
  anti_ai_score: 8
  dna_status: approved
  dna_condition: "Utilizar easing com gravidade power3.inOut ou cubic-bezier de quarta ordem. Duração de 0.6s a 1.0s."
  anti_pattern: "Fade to black abrupto sem justificativa narrativa ou wipes rápidos."
  references: [effects-playbook.md, motion-narrative-delta.md]
  source_assets: [scroll-sync, fluid-menu-001]
  gsap_spec: "duration: 0.8s, ease: power3.inOut"
  performance_budget: "Max 1 full screen redraw during transition"
  prefers_reduced_motion: "Instant switch, skip page transition overlay"

- id: TRN-002
  name: Dissolution Fade (Nanquim Erosion)
  dimension: transition
  intent: Elementos tipográficos ou blocos se dissolvem e se espalham de forma orgânica simulando erosão física ou dispersão de nanquim.
  emotion: [decay, elegance, truth]
  cost: high
  mobile: restricted
  anti_ai_score: 10
  dna_status: approved
  dna_condition: "Uso de shaders de transição ou máscaras SVG baseadas em ruído. Proibido fade linear simples."
  anti_pattern: "Fade linear simples sem ruído ou dispersão física."
  references: [art_production_report_elysian.md (C01_Dispersion), effects-playbook.md]
  source_assets: [reveal-text-001, paper-shaders]
  three_js_config: "Fragment shader with noise threshold mapping alpha channel"
  performance_budget: "Run on GPU, restrict texture checks, check frame drops"
  prefers_reduced_motion: "CSS opacity fade-in 400ms, skip shader dissolution"

- id: TRN-003
  name: Scroll Sync Anchored Slide
  dimension: transition
  intent: Sincronizar o deslizamento de blocos de conteúdo com o scroll de forma elástica, mantendo o controle sob a inércia do usuário.
  emotion: [pacing, control, logic]
  cost: medium
  mobile: restricted
  anti_ai_score: 8
  dna_status: approved
  dna_condition: "Deve utilizar lenis ou outro scroll suave para estabilizar a velocidade de scroll (deltaY)."
  anti_pattern: "Scroll-jacking completo que bloqueia a rolagem natural do navegador."
  references: [motion-narrative-delta.md, DESIGN_LIBRARY.md (P046)]
  source_assets: [scroll-sync, stacked-panels]
  gsap_spec: "gsap.to(target, {y: scrollPosition, ease: power2.out, scrub: 0.5})"
  performance_budget: "Zero layout calculations in the scroll listener, use passive scroll events"
  prefers_reduced_motion: "Static layouts, disable scroll event sync"

- id: TRN-004
  name: Fluid Mesh Transition
  dimension: transition
  intent: Transição de formas ou malhas 3D através de deformação de vértices por simplex noise quando a seção se torna ativa.
  emotion: [vanguard, organic, surprise]
  cost: high
  mobile: restricted
  anti_ai_score: 9
  dna_status: approved
  dna_condition: "A amplitude máxima da deformação de vértices deve ser limitada a 0.2 no Vertex Shader. Transição total em no máximo 1.2s."
  anti_pattern: "Deformação caótica infinita que deforma a malha de forma irreconhecível."
  references: [effects-playbook.md, motion-narrative-delta.md]
  source_assets: [sovereign-hero-webgl, paper-shaders]
  three_js_config: "Simplex noise function inside vertex shader. Uniform transitionProgress animated by GSAP."
  performance_budget: "Strictly run on GPU, max vertex count 30k for target meshes"
  prefers_reduced_motion: "CSS cross-fade opacity 400ms, bypass vertex displacement animation"

- id: TRN-005
  name: Cross-fade Image Dissolve
  dimension: transition
  intent: Transição suave de uma imagem ou textura para outra utilizando uma máscara de dissolução baseada em ruído de Perlin.
  emotion: [reveal, tactile, logic]
  cost: medium
  mobile: allowed
  anti_ai_score: 8
  dna_status: approved
  dna_condition: "Deve durar de 0.8s a 1.2s. A transição deve ser sutil e o ruído não deve apresentar serrilhamento de pixels."
  anti_pattern: "Fades lineares simples ou transições de slides em 3D de banco de imagens."
  references: [art_production_report_elysian.md (C01_Dispersion), effects-playbook.md]
  source_assets: [depth-map, reveal-text-001]
  three_js_config: "Fragment shader mix(texture1, texture2, smoothstep(threshold - edge, threshold + edge, noiseVal))"
  performance_budget: "2 texture bindings max in the shader, keep resolution below 2048x2048"
  prefers_reduced_motion: "CSS standard fade-in without noise dissolve"
```
