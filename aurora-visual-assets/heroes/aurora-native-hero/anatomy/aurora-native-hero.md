# Aurora Native Hero — Anatomy

**Asset ID:** hero-aurora-native-001
**Categoria:** heroes
**Origem:** aurora-native
**Gerado em:** 2026-04-18
**OS:** OS-CLAUDECODE-AURORA-VISUAL-ASSETS-20260418-009

## Conceito
"A fábrica se revela"
Este componente não é apenas um cabeçalho; é uma narrativa de entrada. Ele utiliza o scroll do visitante como motor de uma montagem editorial, onde o conteúdo emerge de um vácuo inicial (silêncio visual) para uma estrutura tipográfica de alto peso.

## Padrões Utilizados

| Padrão | Técnica | Aplicação |
|---|---|---|
| P006 | Curtain Reveal | Revelação da linha divisória via clip-path. |
| P008 | Scrub Cross-Fade | Transição suave das sublines vinculada ao scroll. |
| P010 | Lenis Sync | Sincronização de inércia para fluidez ininterrupta. |
| P015 | Staggered Typography | Revelação caractere por caractere da headline. |
| P040 | Expansion Staggering | Sequenciamento da entrada do CTA e suporte. |
| P042 | Spring-Loaded Entry | Física de mola (elastic ease) para conferir massa às letras. |
| P045 | Minimalist Constraint | Exclusão total de gradientes e imagens decorativas. |

## Decisões de Design
- **Tipografia Central**: A fonte é o único elemento visual, eliminando a dependência de imagens de estoque que diluem a marca.
- **Scrub 1.6**: Definido para criar um "arrasto" editorial, exigindo intenção do usuário para avançar a narrativa.
- **Silêncio Visual**: Ocupa os primeiros 15% e os últimos 10% do scroll para garantir que a percepção de qualidade venha do vazio, não do ruído.

## Decisões Técnicas
- **React + GSAP**: Escolhido pela precisão determinística em layouts complexos de scroll.
- **Lenis Integration**: Implementado como um bridge direto no ticker do GSAP para evitar conflitos de RAF.
- **Reduce Motion**: Fallback estático para acessibilidade industrial.

## VEREDITO CEO-EFFECTS
"A física do scrub (1.6) permite uma conexão tátil entre o scroll do usuário e a emergência da headline. O stagger via elastic out no Frame 1 confere massa e peso à tipografia. Implementação técnica impecável."

## VEREDITO CEO-DESIGN
"O silêncio visual do Frame 0 estabelece o tom editorial. A tipografia como único vetor de informação reforça a hierarquia sem distrações ornamentais. Aprovação 100% conforme o DNA Dark Editorial."

## Dependências
- `gsap`: ^3.12.5
- `lenis`: ^1.1.0
- `react`: ^18.0.0

## Como Usar
```tsx
import { AuroraNativeHero } from './heroes/aurora-native-hero';

export default function Home() {
  return (
    <AuroraNativeHero 
      headline="MadLab"
      sublines={['Onde ideias viram metal.', 'Engenharia de precisão.']}
      ctaLabel="Explore a Galeria"
    />
  );
}
```

## Limitações Conhecidas
- O componente requer um container root com altura suficiente para permitir o scroll de 500vh (pinning).
- Não suporta backgrounds de vídeo por design (conflito com DNA Editorial).
