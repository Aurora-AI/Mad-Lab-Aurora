# Motion Primitives (MOT)

```yaml
- id: MOT-001
  name: Orbital Drift
  dimension: motion
  intent: Simular gravidade lenta com rotação suave ao redor de um centro para criar mistério e profundidade.
  emotion: [mystery, scale, sophistication]
  cost: medium
  mobile: restricted
  anti_ai_score: 8
  dna_status: approved
  dna_condition: "Apenas se usado com desaceleração e sem aceleração rápida. Opacidade menor que 0.4 no luminoso."
  anti_pattern: "Rotações rápidas de câmera 3D ou órbitas caóticas."
  references: [mad-lab-aurora-dna.md]
  source_assets: [spiral-animation, entropy]
  gsap_spec: "duration 15s+, ease power1.inOut, repeat -1"
  three_js_config: "mesh.rotation.y += 0.001"
  performance_budget: "60fps on low-end device, limit vertex count to 5k"
  prefers_reduced_motion: "Static angle, rotation = 0"

- id: MOT-002
  name: Proximity-Based Attraction
  dimension: motion
  intent: Simular física natural de atração gravitacional quando o cursor se aproxima de um elemento.
  emotion: [reactivity, intimacy]
  cost: high
  mobile: reduced
  anti_ai_score: 9
  dna_status: approved
  dna_condition: "Usar lerp rigoroso entre 0.05 e 0.08. Nunca snap instantâneo."
  anti_pattern: "Bounce elástico ao finalizar atração."
  references: [effects-playbook.md, founder-dna.md]
  source_assets: [gooey-button-001, magnetic-cards-001]
  gsap_spec: "lerp 0.05-0.08, never snap"
  performance_budget: "Max 2 draw calls for tracking, mouse velocity sync"
  prefers_reduced_motion: "Simple static layout, disable cursor force field"

- id: MOT-003
  name: Stagger Reveal
  dimension: motion
  intent: Entrada sequencial com peso e ritmo diferenciado entre elementos textuais e decorativos.
  emotion: [order, progression, pacing]
  cost: low
  mobile: allowed
  anti_ai_score: 6
  dna_status: approved
  dna_condition: "Decorativos devem animar DEPOIS do conteúdo principal."
  anti_pattern: "Fade-in simultâneo ou linear sem escalonamento."
  references: [effects-playbook.md, designmanualposthero.md]
  source_assets: [reveal-text-001, bento-grid-001]
  gsap_spec: "stagger: 80ms - 150ms, duration: 400ms - 700ms, ease: cubic-bezier(0.4, 0, 0.2, 1)"
  performance_budget: "GPU-accelerated transforms only (translateY, opacity)"
  prefers_reduced_motion: "Instant opacity = 1, skip animation"

- id: MOT-004
  name: Weighted Inertial Scroll
  dimension: motion
  intent: Simular inércia e peso físico no scroll, fazendo o conteúdo desacelerar progressivamente após a liberação da roda do mouse.
  emotion: [gravity, mass, control]
  cost: medium
  mobile: restricted
  anti_ai_score: 8
  dna_status: approved
  dna_condition: "Uso obrigatório de decay exponencial de velocidade. Sem lag ou quebra de scroll natural."
  anti_pattern: "Scroll-jacking total sem suporte a trackpad ou inércia nativa."
  references: [motion-narrative-delta.md, DESIGN_LIBRARY.md (P051)]
  source_assets: [scroll-sync, stacked-panels]
  gsap_spec: "gsap.to(target, {y: scrollVal, ease: power2.out, overwrite: 'auto'})"
  performance_budget: "Passive event listener, run on GSAP Ticker, throttle recalculations"
  prefers_reduced_motion: "Disable smooth scroll inertia, use native browser scroll behavior"

- id: MOT-005
  name: Scroll-Driven Glitch Distortion
  dimension: motion
  intent: Aplicar distorção ou ruído estocástico reativo à velocidade instantânea de scroll do usuário.
  emotion: [tension, instability, raw]
  cost: high
  mobile: restricted
  anti_ai_score: 9
  dna_status: approved
  dna_condition: "Distorção deve decair rapidamente assim que o scroll para. Amplitude máxima de 0.05 no shader."
  anti_pattern: "Glitch persistente e brilhante piscando sem sincronização de scroll."
  references: [DESIGN_LIBRARY.md (P050), motion-narrative-delta.md]
  source_assets: [scroll-sync]
  three_js_config: "Uniform float uVelocity synced with scroll speed. Custom vertex displacement."
  performance_budget: "Keep shader instruction count minimal, run in GPU"
  prefers_reduced_motion: "Disable shader glitch effect, static mesh rendering"
```
