# Narrative Primitives (NAR)

```yaml
- id: NAR-001
  name: Regra do Silêncio (0.8s)
  dimension: narrative
  intent: Garantir que o visitante sinta o peso do silêncio visual antes de qualquer animação ou reveal ocorrer.
  emotion: [sober, expectation, weight]
  cost: low
  mobile: allowed
  anti_ai_score: 9
  dna_status: approved
  dna_condition: "Regra absoluta: atrasar qualquer animação ativa por pelo menos 0.8s após o carregamento da seção."
  anti_pattern: "Animações instantâneas que começam no frame 0, competindo com a renderização da página."
  references: [effects-playbook.md, mad-lab-aurora-dna.md]
  source_assets: [aurora-hero, aurora-native-hero]
  gsap_spec: "delay: 0.8s"
  performance_budget: "N/A"
  prefers_reduced_motion: "No delay, show static state immediately"

- id: NAR-002
  name: Pacing Cênico Multi-Fase (Preloader)
  dimension: narrative
  intent: Dividir a introdução do site em fases bem demarcadas (escuridão -> emergência -> consciência -> dissolução) para contar uma história.
  emotion: [anticipation, narrative_climax, authority]
  cost: high
  mobile: restricted (simplified phase timing)
  anti_ai_score: 10
  dna_status: approved
  dna_condition: "Deve seguir a estrutura 5-fases do preloader âncora (Mulher Puzzle) com duração total de 6.0s a 8.0s."
  anti_pattern: "Splash screen simples de loading com spinner de banco de dados."
  references: [effects-playbook.md, founder-dna.md]
  source_assets: [aurora-hero]
  gsap_spec: "Timeline com staggers controlados: Fase 1 (1.5s), Fase 2 (2s), Fase 3 (2s), Fase 4 (1.5s)"
  performance_budget: "Max 1 heavy preloader per site session, cache status in sessionStorage"
  prefers_reduced_motion: "Skip preloader, enter directly at Fase 5 (site content)"

- id: NAR-003
  name: EQ de Frequências de Seção
  dimension: narrative
  intent: Alternar a densidade visual e a tensão entre seções adjacentes para permitir respiração e foco.
  emotion: [rythmic, balance, fatigue_prevention]
  cost: low
  mobile: allowed
  anti_ai_score: 8
  dna_status: approved
  dna_condition: "Nunca posicionar duas seções de alta densidade visual seguidas. Seção pós-hero deve ser de baixa densidade (descompressão)."
  anti_pattern: "Toda a página com alta densidade de efeitos e informações (poluição visual)."
  references: [designmanualposthero.md]
  source_assets: [stacked-panels, bento-grid-001]
  performance_budget: "Zero JS cost"
  prefers_reduced_motion: "No impact"

- id: NAR-004
  name: Wayfinding Telemetry Chapters
  dimension: narrative
  intent: Dividir a navegação vertical em capítulos ou eixos numerados, utilizando tipografia Voz 2 capslock, criando uma sensação de progresso estruturado.
  emotion: [discipline, sequence, clarity]
  cost: low
  mobile: allowed
  anti_ai_score: 7
  dna_status: approved
  dna_condition: "Uso obrigatório de monospace ou sans geométrico de 8-12px com tracking de 0.3-0.5em. Posicionar nas bordas periféricas."
  anti_pattern: "Textos de rodapé ou metadados gigantes de leitura corrida com fonte display serif."
  references: [designmanualposthero.md, elysiancorp-visual-vocabulary-v1.md]
  source_assets: [header-editorial-001, footer-dark-001]
  performance_budget: "Zero JS overhead"
  prefers_reduced_motion: "No impact"

- id: NAR-005
  name: Interactive Silence Counter
  dimension: narrative
  intent: Exibir um contador numérico minimalista e preciso de tempo/carregamento para impor um compasso de espera dramático ao visitante.
  emotion: [anticipation, precision, solemnity]
  cost: low
  mobile: allowed
  anti_ai_score: 8
  dna_status: approved
  dna_condition: "Incremento numérico suave sincronizado com a Fase 2 (emergência) do preloader. Sem animações de rotação ou cores piscantes."
  anti_pattern: "Loading spinners circulares coloridos comuns do bootstrap ou animações caóticas."
  references: [effects-playbook.md, founder-dna.md]
  source_assets: [aurora-hero]
  gsap_spec: "gsap.to(counter, {val: 100, duration: 3.5, ease: power1.inOut})"
  performance_budget: "Use single dynamic state, avoid layout repaints during text changes"
  prefers_reduced_motion: "Instant 100% display, skip countdown animation"
```
