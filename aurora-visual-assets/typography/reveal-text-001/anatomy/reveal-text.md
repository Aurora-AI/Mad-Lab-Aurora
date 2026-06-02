# Anatomy: Reveal Text (typography-reveal-text-001)

## Architecture
O `Reveal Text` é um componente de tipografia imersiva que vincula o progresso do scroll do usuário à visibilidade de cada palavra. Ele utiliza o padrão de **Progressive Disclosure via Scroll**, comum em narrativas digitais premium.

## Core Components
- **RevealText**: O orquestrador que detecta o viewport e calcula o progresso global.
- **Motion Words**: Spans individuais animados que recebem frações do progresso total.

## Techniques & Patterns
- **P057: Scroll-to-Opacity Mapping**: Mapeamento linear do `scrollYProgress` para `opacity [0.1 -> 1]`. O valor base de 0.1 garante que o texto seja legível (fantasma) antes da ativação completa.
- **P058: Staggered Viewport Entry**: Uso de `useTransform` com ranges dinâmicos `[start, end]` baseados no índice da palavra, garantindo que a "revelação" siga a ordem de leitura.

## Dependency Analysis
- **Framer Motion**: Requisito essencial para `useScroll` e `useTransform`.

## Performance
- **Passive Listeners**: O Framer Motion otimiza o listener de scroll para ocorrer fora da thread principal sempre que possível, garantindo que o efeito de revelação não introduza jank na navegação.
