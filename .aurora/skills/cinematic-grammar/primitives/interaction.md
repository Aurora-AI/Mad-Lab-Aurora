# Interaction Primitives (INT)

```yaml
- id: INT-001
  name: Cursor Inertial Response
  dimension: interaction
  intent: Elementos acompanham o movimento do cursor com inércia física real para criar resposta responsiva e fluida.
  emotion: [immersion, tactile, refinement]
  cost: medium
  mobile: restricted (disable cursor tracking on touch screens)
  anti_ai_score: 9
  dna_status: approved
  dna_condition: "Lerp configurado estritamente em 0.05-0.08. Nunca snap."
  anti_pattern: "Seguimento seco instantâneo sem desaceleração física."
  references: [effects-playbook.md, founder-dna.md]
  source_assets: [magnetic-button-001, magnetic-cards-001]
  gsap_spec: "gsap.to(target, {x: mouse.x, y: mouse.y, duration: 0.8, ease: power2.out})"
  performance_budget: "Use requestAnimationFrame or GSAP Ticker, throttle mouse events to prevent layout thrashing"
  prefers_reduced_motion: "Static positioning, disable mouse event listener"

- id: INT-002
  name: CSS Clip-Path Reveal
  dimension: interaction
  intent: Revelação de conteúdo ou botão através de uma máscara geométrica que expande a partir do ponto de interação.
  emotion: [craft, surprise, logic]
  cost: low
  mobile: allowed
  anti_ai_score: 8
  dna_status: approved
  dna_condition: "O clip-path deve expandir com easing de gravidade. Limitar a formas retangulares ou poligonais."
  anti_pattern: "Efeitos de bola brilhante crescendo de forma orgânica disforme."
  references: [effects-playbook.md, designmanualposthero.md]
  source_assets: [gooey-button-001, image-comparison-slider]
  gsap_spec: "duration: 0.3s, ease: power2.inOut"
  performance_budget: "Hardware accelerated clip-path only"
  prefers_reduced_motion: "Instant toggle states, disable clip-path morphing"

- id: INT-003
  name: Kinetic Underline
  dimension: interaction
  intent: Sublinhado de link inline que cresce de uma borda a outra horizontalmente no hover e se recolhe no out.
  emotion: [focus, speed, precision]
  cost: low
  mobile: allowed (trigger on touch press)
  anti_ai_score: 6
  dna_status: approved
  dna_condition: "Utilizar `scaleX` com origem à esquerda no hover, e origem à direita no exit."
  anti_pattern: "Bordas que piscam ou aparecem instantaneamente."
  references: [designmanualposthero.md, effects-playbook.md]
  source_assets: [reveal-text-001, header-editorial-001]
  gsap_spec: "scaleX: 0 -> 1 on enter, 1 -> 0 on exit, ease: power3.inOut"
  performance_budget: "Use transform: scaleX, do not animate width property"
  prefers_reduced_motion: "Static border-bottom with fixed low opacity, no transition scale"

- id: INT-004
  name: Magnetic Button Pull
  dimension: interaction
  intent: Atrair o botão em direção ao cursor quando este entra em uma área de aproximação (bounding box), criando feedback cinético responsivo.
  emotion: [tactile, surprise, precision]
  cost: medium
  mobile: restricted
  anti_ai_score: 9
  dna_status: approved
  dna_condition: "Deslocamento máximo limitado a 15px. Use GSAP para suavizar o retorno ao centro (ease: elastic.out)."
  anti_pattern: "Deslocamento excessivo que faz o botão escapar do cursor."
  references: [effects-playbook.md, founder-dna.md]
  source_assets: [magnetic-button-001, gooey-button-001]
  gsap_spec: "gsap.to(target, {x: deltaX * 0.3, y: deltaY * 0.3, duration: 0.3, ease: power2.out})"
  performance_budget: "Listen to button container hover area only, avoid document-wide listeners"
  prefers_reduced_motion: "Disable magnetic translation, standard cursor pointer styling"

- id: INT-005
  name: Scroll-Driven Zoom Sync
  dimension: interaction
  intent: Sincronizar o zoom ou escala de um elemento visual (imagem ou wireframe) com a porcentagem de scroll do usuário.
  emotion: [continuity, investigation, reveal]
  cost: medium
  mobile: restricted
  anti_ai_score: 8
  dna_status: approved
  dna_condition: "A escala máxima deve ser limitada a 1.2x. Transição suave."
  anti_pattern: "Imagens que estouram a tela ou ampliam instantaneamente com scroll vertical."
  references: [motion-narrative-delta.md, designmanualposthero.md]
  source_assets: [scroll-sync, image-comparison-slider]
  gsap_spec: "gsap.to(target, {scale: calculatedScale, ease: none, scrub: true})"
  performance_budget: "CSS transform: scale, prevent layout repaint"
  prefers_reduced_motion: "Disable scale animation, render static full size image"
```
