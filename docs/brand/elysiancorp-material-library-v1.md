# Material Library — ElysianCorp Portal v1.0

**OS-MADLAB-ELYSIANCORP-VISUAL-DNA-CANONIZATION-20260612-003**  
**Status:** Canonical (SSOT)  
**Version:** 1.0.0  

Este documento apresenta a biblioteca de materiais aprovados para uso visual na interface do portal, estabelecendo métricas de comparação (1 a 5) para guiar futuras curadorias e gerações de assets.

---

## Métricas de Avaliação (Score 1 a 5)

- **anti_ai:** Nível de resiliência do material contra a aparência de renderização genérica de IA (5 = Extremamente resistente, exige grão e textura tátil; 1 = Facilmente simulado por clichês planos de IA).
- **trustware:** Capacidade de passar a sensação de governança, integridade técnica e permanência.
- **operational_truth:** Aderência ao tom brutalista e utilitário de processamento real.
- **production_readiness:** Facilidade de integração técnica (safe area, contraste de texto, crops responsivos).

---

## Materiais Aprovados

### 1. Papel Prensado a Frio (cold_press_paper)
```yaml
material:
  name: cold_press_paper
  emotion:
    - tactile_intimacy
    - forensic_archive
    - permanence
  use_cases:
    - Fundos de seções de descompressão (Câmara 1, Câmara 4).
    - Base física para exibição de tipografia serifa com alto contraste.
  avoid_when:
    - Em câmaras focadas em confinamento de segurança pesada.
  scores:
    anti_ai: 5
    trustware: 5
    operational_truth: 4
    production_readiness: 5
```

---

### 2. Nanquim Técnico (technical_ink)
```yaml
material:
  name: technical_ink
  emotion:
    - precision
    - irreversible_record
    - auditability
  use_cases:
    - Glifos tipográficos erosionados, Data Matrix físico e diagramações técnicas.
  avoid_when:
    - Em elementos interativos dinâmicos de hover rápido.
  scores:
    anti_ai: 4
    trustware: 5
    operational_truth: 4
    production_readiness: 5
```

---

### 3. Ferro Fundido (cast_iron)
```yaml
material:
  name: cast_iron
  emotion:
    - brute_authority
    - heavy_containment
    - permanent_seal
  use_cases:
    - Metáfora de barreira inviolável e travas de segurança (carimbos físicos, blocos de pressão).
  avoid_when:
    - Em planos de fundo onde texto longo precisa ser exibido diretamente sobre o material.
  scores:
    anti_ai: 5
    trustware: 5
    operational_truth: 4
    production_readiness: 4
```

---

### 4. Concreto Bruto (concrete)
```yaml
material:
  name: concrete
  emotion:
    - monumental_scale
    - brutalist_honesty
    - immutability
  use_cases:
    - Paredes de contenção de infraestrutura, cantos estruturais de câmaras volumétricas (Câmara 3).
  avoid_when:
    - Câmaras com apelo gráfico editorial limpo.
  scores:
    anti_ai: 5
    trustware: 4
    operational_truth: 5
    production_readiness: 4
```

---

### 5. Aço Escovado (brushed_steel)
```yaml
material:
  name: brushed_steel
  emotion:
    - industrial_rigor
    - durability
    - safety
  use_cases:
    - Painéis de telemetria lateral e divisórias mecânicas de seções de processamento.
  avoid_when:
    - Se a superfície se tornar muito cromada ou altamente reflexiva (violando as proibições).
  scores:
    anti_ai: 4
    trustware: 4
    operational_truth: 4
    production_readiness: 4
```

---

### 6. Vidro Fumê (smoked_glass)
```yaml
material:
  name: smoked_glass
  emotion:
    - selective_visibility
    - technical_isolation
    - boundary
  use_cases:
    - Sobreposição de telemetria monospace (overlays técnicos) sem ocultar completamente a textura de fundo.
  avoid_when:
    - Se apresentar bordas arredondadas exageradas ou gradientes vibrantes estilo SaaS 2020.
  scores:
    anti_ai: 3
    trustware: 4
    operational_truth: 4
    production_readiness: 5
```

---

### 7. Madeira Arquitetônica (architectural_wood)
```yaml
material:
  name: architectural_wood
  emotion:
    - quiet_order
    - study_sanctuary
    - tactile_gravity
  use_cases:
    - Painéis de divisórias ou superfícies de flatlays (zenitais) simulando mesas de auditoria técnica.
  avoid_when:
    - Em áreas de telemetria industrial de fluxo contínuo.
  scores:
    anti_ai: 4
    trustware: 4
    operational_truth: 3
    production_readiness: 4
```
