# Visual Decision Tree — ElysianCorp Portal v1.0

**OS-MADLAB-ELYSIANCORP-VISUAL-DNA-CANONIZATION-20260612-003**  
**Status:** Canonical (SSOT)  
**Version:** 1.0.0  

Este documento apresenta a árvore de decisão visual estruturada para auditoria e validação rápida de novas propostas de design ou assets de imagem.

---

```yaml
visual_decision_tree:

  - step: 1
    question: "Representa algo físico ou possui materialidade palpável?"
    branches:
      yes:
        action: "continue"
      no:
        action: "REJECT"
        reason: "O design da ElysianCorp proíbe abstrações flutuantes desprovidas de corpo ou textura (anti-vetor/anti-SaaS plano)."

  - step: 2
    question: "Existe equivalente ou correspondente físico real para o elemento cênico?"
    branches:
      yes:
        action: "continue"
      no:
        action: "REVIEW_ESTHETIC"
        reason: "Elementos fantásticos sem base em física realista (como campos de força, neon cênico flutuante ou chips flutuando no ar) devem ser revisados e substituídos por equivalentes brutais reais."

  - step: 3
    question: "A composição apresenta simetria perfeita axial gerada de forma algorítmica ou névoa volumétrica artificial de difusão de imagem?"
    branches:
      yes:
        action: "REJECT"
        reason: "Violação do padrão de assimetria. Simetria e névoa volumétrica excessiva são marcas de IA genérica (Midjourney templates) e devem ser trocadas por perspectivas oblíquas, cantos e imperfeições reais."
      no:
        action: "continue"

  - step: 4
    question: "O asset contém algum clichê bloqueado do Anti-AI Gate?"
    note: "Consultar os clichês listados em elysiancorp-anti-patterns-v1.md (ex: cérebro digital, escudos brilhantes, neon cyberpunk, dashboards SaaS genéricos)."
    branches:
      yes:
        action: "REJECT"
        reason: "Presença de clichês bloqueados pelo filtro negativo da marca."
      no:
        action: "APPROVE_ASSET"
        reason: "O asset atende a todas as diretrizes de matéria, luz, textura e assimetria do inquérito forense."
```
