# Reference: Do Not Copy — OS-019R
**Referência:** https://www.exoape.com
**Gerado em:** 2026-06-08 22:35:31

---

## Princípio

A Exo Ape foi usada como referência técnica e de linguagem visual, não como template.
Este documento é o contrato permanente do que pode e do que não pode ser derivado dela.

---

## ✅ Técnicas permitidas (domínio público / princípios de design)

- Escala tipográfica extrema com tracking negativo (é técnica, não identidade)
- IntersectionObserver para gating de vídeo (é padrão de performance)
- will-change: transform para GPU compositing (é arquitetura de engenharia)
- Paleta near-monocromática (é princípio de design, não identidade)
- Estrutura de seções (hero / works / reel / footer) — estrutura genérica de portfolio
- Nav fixa z:9 + menu z:14 — estrutura funcional padrão

Estas técnicas existem independentemente da Exo Ape. São princípios tipográficos,
padrões de Web Performance e arquitetura de UI que qualquer projeto pode usar.

---

## 🚫 Identidade proibida (Hard Prohibitions)

### AC-001: Tipografia TWKLausanne
**Motivo:** Fonte proprietária da Exo Ape — não está disponível para uso externo
**Alternativa:** Usar fonte aprovada no handoff que tenha equivalência de contraste e peso

### AC-002: Assets visuais (vídeos, imagens, fotografias)
**Motivo:** Conteúdo de propriedade intelectual da Exo Ape
**Alternativa:** Usar mídia própria ou licenciada — nunca hotlink ou cópia de assets

### AC-003: Copy e textos
**Motivo:** Textos como 'Digital Design Experience', 'Exo Ape', copy de projetos são marca registrada
**Alternativa:** Usar copy próprio do Mad Lab Aurora

### AC-004: Identidade visual (logo, cores de marca, nome)
**Motivo:** Marca da Exo Ape — proteção legal e ética
**Alternativa:** Identidade exclusiva do Mad Lab Aurora


---

## ⚠️ Restrições soft (usar com cuidado)

### AC-005: Layout de hero com H1 monocousal + vídeo na mesma composição exata
**Razão:** Composição muito próxima pode ser identificável como clone
**Orientação:** Usar a mesma escala tipográfica mas composição e conteúdo distintos

### AC-006: Footer com background --color-story (#070707) + mesmo grid
**Razão:** A combinação específica é assinatura da referência
**Orientação:** Dark footer é permitido; usar cor e layout diferentes

### AC-007: Grid de portfolio com as mesmas proporções de vídeo
**Razão:** A combinação exata de proporções é identidade editorial
**Orientação:** Variable media grid é o padrão — usar proporções distintas


---

## Checklist pré-entrega para agentes construtores

Antes de submeter qualquer candidato visual derivado deste handoff:

```
[ ] A fonte usada não é TWKLausanne
[ ] Nenhum asset (vídeo/imagem) é da Exo Ape
[ ] O copy/texto é original do Mad Lab Aurora
[ ] O logo não replica o da Exo Ape
[ ] O grid de portfolio tem proporções distintas
[ ] O hero usa composição diferente (outro texto, outra mídia, outro layout)
[ ] O footer usa cor e grid distintos
[ ] O sistema tipográfico usa as fórmulas de tracking, não os valores absolutos da referência
```

---

## O que fazer se houver dúvida

Se um elemento do candidato parecer "muito parecido" com a referência:

1. Verificar se é técnica (tracking, IO, GPU) → permitido
2. Verificar se é identidade (fonte, asset, copy, logo) → **proibido**
3. Verificar se é composição (arranjo específico + conteúdo específico) → **risco, rever**

Em caso de dúvida: divergir. O Mad Lab Theme tem identidade própria.
