# Composition Primitives (COM)

```yaml
- id: COM-001
  name: Split Assimétrico
  dimension: composition
  intent: Dividir o layout verticalmente em proporções desiguais (40/60 ou 35/65) separadas por um divisor fino para quebrar a simetria linear barata.
  emotion: [discipline, structural_tension, editorial]
  cost: low
  mobile: allowed (collapses to single column)
  anti_ai_score: 7
  dna_status: approved
  dna_condition: "Divisor de 0.5-1px máximo. Lado menor abriga a identidade visual periférica, lado maior o conteúdo operacional."
  anti_pattern: "Divisão simétrica 50/50 sem hierarquia espacial."
  references: [designmanualposthero.md]
  source_assets: [stack-feature, bento-grid-001]
  gsap_spec: "N/A"
  performance_budget: "CSS Grid or Flexbox, zero javascript overhead"
  prefers_reduced_motion: "Normal responsive collapse without layout shift"

- id: COM-002
  name: Pinned Statement
  dimension: composition
  intent: Fixar uma frase ou título de seção no topo-esquerdo enquanto o conteúdo operacional rola do lado direito.
  emotion: [anchoring, authority, focus]
  cost: low
  mobile: restricted (disable pinning on mobile viewport)
  anti_ai_score: 8
  dna_status: approved
  dna_condition: "Uso de tipografia pequena com tracking alto para o cabeçalho fixado."
  anti_pattern: "Centralização de parágrafo sob o título que rola simultaneamente."
  references: [designmanualposthero.md]
  source_assets: [header-editorial-001]
  gsap_spec: "gsap ScrollTrigger pin: true"
  performance_budget: "ScrollTrigger must use standard pinSpacing: true to prevent layout overlapping"
  prefers_reduced_motion: "Disable pinning, allow elements to flow inline naturally"

- id: COM-003
  name: Grid de Diagnóstico
  dimension: composition
  intent: Organizar dados e métricas em células retangulares delimitadas por bordas finas sem sombras, criando um console de auditoria técnica.
  emotion: [precision, auditability, control]
  cost: low
  mobile: allowed (wrap grid cells)
  anti_ai_score: 7
  dna_status: approved
  dna_condition: "Bordas de 0.5px, opacidade de 30% da cor base. NUNCA usar sombras sob os cards."
  anti_pattern: "Cards flutuantes com sombras suaves e border-radius alto (estilo SaaS comercial)."
  references: [designmanualposthero.md, art_production_report_elysian.md (C04_TruthReturned)]
  source_assets: [bento-grid-001]
  performance_budget: "Zero JS. CSS Grid layout."
  prefers_reduced_motion: "No layout impact"

- id: COM-004
  name: Liquid Glass Surface
  dimension: composition
  intent: Painéis de vidro translúcidos e finos que se sobrepõem criando profundidade material sem obscurecer a atmosfera de fundo.
  emotion: [depth, refinement, precision]
  cost: low
  mobile: allowed
  anti_ai_score: 8
  dna_status: conditional
  dna_condition: "Proibido sombras digitais genéricas pesadas e cantos arredondados acima de 4px. Borda externa ultrafina (máx 0.5px) com opacidade controlada."
  anti_pattern: "Cards de vidro com blur exagerado e sombras pretas digitais opacas de banco de imagens."
  references: [MS-001.md, mad-lab-aurora-dna.md]
  source_assets: [spotlight-card, bento-grid-001]
  performance_budget: "Use CSS backdrop-filter: blur() with hardware acceleration, monitor performance on mobile"
  prefers_reduced_motion: "Solid flat background color without glass transparency or blur filter"

- id: COM-005
  name: Pinned Diagonal Layout
  dimension: composition
  intent: Dividir o container principal com divisores finos em eixos não ortogonais (diagonais com angulações controladas de 15 a 30 graus) para guiar o olhar.
  emotion: [stress, dynamicism, vanguard]
  cost: low
  mobile: allowed (collapse to straight columns)
  anti_ai_score: 9
  dna_status: approved
  dna_condition: "Uso estrito de linhas finas de 0.5px. A angulação deve ser constante em todo o layout."
  anti_pattern: "Múltiplas diagonais com ângulos conflitantes sem grade unificada."
  references: [designmanualposthero.md, open-design catalog]
  source_assets: [stack-feature]
  performance_budget: "CSS clip-path or transform: skewY, avoid canvas calculation"
  prefers_reduced_motion: "Orthogonal layouts, remove angle skew"
```

