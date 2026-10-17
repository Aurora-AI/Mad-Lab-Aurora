# Camera Primitives (CAM)

```yaml
- id: CAM-001
  name: Slow Forward Push (Dolly In)
  dimension: camera
  intent: Câmera avança lentamente em profundidade ao longo de um eixo Z para induzir descoberta e revelação.
  emotion: [discovery, monumentality, focus]
  cost: medium
  mobile: restricted
  anti_ai_score: 8
  dna_status: approved
  dna_condition: "Deve ser acoplado ao scroll linear do usuário. Proibido aceleração brusca."
  anti_pattern: "Snap zoom ao rolar a página ou trepidação lateral da câmera."
  references: [art_production_report_elysian.md (C03_GovernedFactory), motion-narrative-delta.md]
  source_assets: [sovereign-hero-webgl, scroll-sync]
  gsap_spec: "scrub: true, ease: power1.out, max translation 10% depth"
  three_js_config: "camera.position.z -= scrollVelocity * 0.05"
  performance_budget: "Render logic must run on GSAP Ticker sync, skip rendering if mesh out of viewport"
  prefers_reduced_motion: "Static camera depth, disable scroll sync on Z-axis"

- id: CAM-002
  name: Shallow Depth of Field (DOF)
  dimension: camera
  intent: Desfocar o plano de fundo ou elementos secundários para guiar a atenção cirurgicamente ao primeiro plano.
  emotion: [editorial, intimacy, drama]
  cost: high
  mobile: reduced
  anti_ai_score: 9
  dna_status: approved
  dna_condition: "Manter desfoque óptico sutil e realista (bokeh mecânico), não efeito borrão digital."
  anti_pattern: "Filtros blur gaussianos estáticos pesados aplicados diretamente em CSS."
  references: [art_production_report_elysian.md (C02_FailClosed)]
  source_assets: [hero-futuristic, depth-map-parallax]
  three_js_config: "BokehPass (three/examples/jsm/postprocessing/BokehPass)"
  performance_budget: "Max 1 DOF post-processing pass, disable on mobile"
  prefers_reduced_motion: "Pre-rendered image with static depth mapping"

- id: CAM-003
  name: Multi-Layer Parallax Depth
  dimension: camera
  intent: Deslocar múltiplas camadas visuais em velocidades calculadas de acordo com a profundidade real para simular física espacial tridimensional.
  emotion: [depth, scale, structure]
  cost: high
  mobile: restricted
  anti_ai_score: 10
  dna_status: approved
  dna_condition: "Mínimo de 5 camadas, com velocidades proporcionais a f(z) = 1/(1+z). Proibido parallax de 2 camadas."
  anti_pattern: "Parallax de 2 camadas tipo template comercial SaaS."
  references: [mad-lab-aurora-dna.md, motion-narrative-delta.md]
  source_assets: [hero-davincho, depth-map-parallax]
  gsap_spec: "ease: none, scrub: true"
  performance_budget: "Hardware-accelerated CSS transforms (translate3d) or WebGL layers, avoid raw top/left edits"
  prefers_reduced_motion: "Pre-flattened static layers, disable parallax shift"

- id: CAM-004
  name: Cursor-Driven Camera Orbit
  dimension: camera
  intent: Rotação sutil da câmera ao redor do ponto central em resposta à posição do cursor para dar profundidade e resposta física.
  emotion: [immersion, agency, space]
  cost: medium
  mobile: restricted
  anti_ai_score: 8
  dna_status: approved
  dna_condition: "Lerp configurado estritamente em 0.05-0.08. Rotação máxima em yaw/pitch limitada a 5 graus."
  anti_pattern: "Rotação excessiva e rápida de câmera 3D que causa tontura."
  references: [effects-playbook.md, founder-dna.md]
  source_assets: [sovereign-hero-webgl]
  three_js_config: "camera.position.x += (mouseX - camera.position.x) * 0.05"
  performance_budget: "Use requestAnimationFrame or GSAP Ticker, throttle mouse events to prevent layout thrashing"
  prefers_reduced_motion: "Fixed camera angle, disable cursor tracking"

- id: CAM-005
  name: Dolly Zoom (Vertigo Effect)
  dimension: camera
  intent: Afastamento/aproximação física da câmera simultaneamente com a varvação oposta do Field of View para criar distorção de perspectiva dramática.
  emotion: [tension, surprise, vertigo]
  cost: high
  mobile: restricted
  anti_ai_score: 10
  dna_status: approved
  dna_condition: "Uso restrito a momentos de clímax narrativo na transição de seções de alta tensão."
  anti_pattern: "Dolly zoom constante e reativo a qualquer movimento."
  references: [mad-lab-aurora-dna.md, motion-narrative-delta.md]
  source_assets: [scroll-sync]
  three_js_config: "camera.fov = calculatedFov; camera.position.z = calculatedZ; camera.updateProjectionMatrix();"
  performance_budget: "Check frame drops on recalculation of projection matrix"
  prefers_reduced_motion: "Standard linear slide, disable FOV morphing"
```
