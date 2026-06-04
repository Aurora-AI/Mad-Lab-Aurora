# Anti-Padrão: Ruído Visual e Pirotecnia SaaS (Filtro Negativo)

**Documento:** Extração Rigorosa de Veto
**Fonte:** Tutorial Cinematográfico (Evervault Patterns)
**Classificação:** Tendência Estética / Baixa Densidade
**Status:** BLOQUEADO (DNA Conflict)

---

## 1. Identidade do Problema
O design baseado em "truques" interativos (blend modes, máscaras dinâmicas, texto randômico) mascara a ausência de uma base tipográfica monumental. É um processo aditivo que resulta em fragilidade estrutural: o design morre se a interatividade for removida ou se for reduzido a mídias estáticas.

## 2. Heurísticas de Rejeição (Filtro do CEO-Design)

### A. O Teste do Offline/Estático
- **Pergunta:** Se removermos o hover e o JavaScript, o que resta tem autoridade?
- **Critério:** Se o design depende do balanço do mouse para provar que está vivo, ele deve ser **REJEITADO**.

### B. O Teste da Permanência
- **Pergunta:** Este efeito parecerá datado em 24 meses? (Padrão SaaS 2023-2024)
- **Critério:** Efeitos baseados em tendências tecnológicas efêmeras de código não são design; são pirotecnia. **VETO**.

### C. O Princípio da Eliminação Draplin
- **Ação:** Tire o blend mode, tire a máscara, tire o gradiente vibrante.
- **Resultado:** Se sobrar apenas um layout genérico, o design falhou no teste de caráter.

## 3. Especificação de Veto para o Agente

O CEO-Design deve reconhecer os seguintes padrões de "Interferência Interativa" e aplicar o corte imediato:
- **Ruído Tipográfico Randômico:** Uso de texto sem semântica apenas para gerar textura dinâmica.
- **Gradient Masks atreladas ao Cursor:** Simulação de lanterna ou refração de luz digital sem peso utilitário.
- **Blend Modes Aditivos:** Dependência de filtros de cor para legibilidade ou destaque.

---

## 4. Nó de Ingestão (JSON)

```json
{
  "agent": "ceo-design",
  "node_type": "AntiTendencia",
  "domain": "design",
  "core_insight": "Efeitos visuais dependentes de interatividade e camadas de opacidade (blend modes) mascaram a ausência de engenharia tipográfica real e falham no teste de permanência estrutural.",
  "dark_editorial_alignment": "conflita",
  "action": {
    "what": "Registrar padrão 'Evervault hover / Gradientes SaaS' como antipadrão bloqueado.",
    "deadline_days": 0,
    "owner": "rodrigo"
  },
  "tags": ["anti-hype", "veto-saas", "eliminação", "design-genérico"]
}
```
