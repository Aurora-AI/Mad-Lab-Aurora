# Anatomy: Noise Grain (backgrounds-noise-grain-001)

## Architecture
O `Noise Grain` é um overlay de textura gerado proceduralmente via filtros SVG. Ele simula o grão de película cinematográfica, adicionando "vibração" e "vida" a gradientes digitais que de outra forma pareceriam estáticos ou excessivamente limpos.

## Core Components
- **feTurbulence**: Primitiva SVG para geração de ruído de Perlin/Fractal.
- **Grain Animation**: Loop de tradução agressiva com `steps(10)` para simular a mudança de frames física.

## Techniques & Patterns
- **P055: Procedural Texture Overlay**: Uso de `fractalNoise` com base frequency elevada (`0.65`) para um grão fino.
- **P056: Stepped Animation Jitter**: O uso de `steps()` no CSS Animation evita o interpolar suave, criando o efeito de "treme-treme" característico de material analógico.

## Dependency Analysis
- **Nativa**: Implementado inteiramente com SVG e CSS.

## Performance
- **GPU Painting**: Embora seja leve, o `feTurbulence` força o browser a re-pintar a tela. O uso de `pointer-events: none` e `fixed positioning` garante que ele não interfira no pipeline de eventos da página.
