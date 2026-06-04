---
ki_id: KI-MADLAB-001
title: "Regra do Silêncio — 0.8s antes de qualquer efeito"
domain: motion-design
source_os: "mad-lab-aurora-dna-v2.1.0.md + CEO-Effects SKILL.md"
approved_at: "2026-05-30"
approved_by: "antigravity-sprint3"
status: approved
confidence: 0.97
evidence_type: "Regra operacional documentada no DNA v2.1.0 + utilizada em CEO-Effects"
applicable_to: ["ceo-effects", "aurora-web", "ElysianCorp", "todo ativo com animação"]
---

# KI-MADLAB-001 — Regra do Silêncio Operacional

## O Aprendizado

Todo ativo Aurora-native deve ter um estado de repouso de **mínimo 0.8 segundos**
antes de qualquer animação iniciar — seja por scroll, hover ou tempo.

Isso não é delay técnico. É **física narrativa**.

O silêncio antes do efeito comunica:
- O elemento tem peso — não é decoração
- O visitante teve tempo de sentir a ausência antes de sentir a presença
- O efeito, quando vem, tem mais impacto porque existe contraste com o silêncio

## Por Que Isso É Um KI (Não Apenas Documentação)

Este padrão é contraintuitivo: designers tendem a animar imediatamente para "mostrar vida".
A Aurora inverte: o silêncio é a prova de que o elemento tem gravidade.

Sem este KI, agentes produzirão efeitos que começam imediatamente — tecnicamente corretos,
mas narrativamente vazios.

## Aplicação Prática

```javascript
// CORRETO — 0.8s de repouso antes do efeito
gsap.fromTo('.hero-element',
  { opacity: 0, y: 40 },
  {
    opacity: 1,
    y: 0,
    duration: 0.7,
    ease: 'power2.out',
    delay: 0.8   // ← Regra do Silêncio
  }
);

// ERRADO — animação imediata
gsap.fromTo('.hero-element',
  { opacity: 0 },
  { opacity: 1, duration: 0.5 }  // sem delay = sem peso
);
```

```css
/* Fallback para prefers-reduced-motion — OBRIGATÓRIO junto com a regra */
@media (prefers-reduced-motion: reduce) {
  .hero-element {
    opacity: 1;
    transform: none;
    transition: none;
  }
}
```

## Anti-Padrão que Este KI Previne

- Efeitos que começam no momento em que o usuário chega na seção
- Stagger sem delay inicial (o primeiro elemento aparece antes do usuário perceber o espaço)
- Preloaders que terminam diretamente para o conteúdo sem pausa de transição

## Evidência de Origem

- `docs/brand/mad-lab-aurora-dna-v2.1.0.md` — Seção 8: Motion, "Regra Absoluta"
- `.aurora/skills/ceo-effects/SKILL.md` — Parâmetro calibrado: `delay: 0.8s`
- `.aurora/skills/ceo-effects/references/motion-narrative-delta.md` — Seção Timing
