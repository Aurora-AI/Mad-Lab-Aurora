# Anatomy: Magnetic Cards (interactions-magnetic-cards-001)

## Architecture
O `Magnetic Cards` é um sistema de grid interativo onde cada elemento responde individualmente à proximidade do cursor, criando uma sensação de "campo magnético" sobre o layout. É ideal para portfólios ou seções de ativos.

## Core Components
- **MagneticCards (Container)**: Captura a posição global do cursor e a distribui para os filhos.
- **Card**: Célula individual com lógica de cálculo de proximidade e molas internas.

## Techniques & Patterns
- **P059: Radial Influence Field**: Cada card calcula sua distância radial até o cursor. Se menor que `300px`, aplica um deslocamento proporcional à proximidade.
- **P060: Distributed Physics State**: Diferente de um efeito global, cada card possui sua própria instância de `useSpring`, permitindo que o grid "respire" de forma não-uniforme.

## Dependency Analysis
- **Framer Motion**: Necessário para a orquestração física das molas.

## Performance
- **Selective Activation**: O cálculo de mola só é disparado quando o cursor entra no raio de influência, otimizando o processamento do loop de animação em grids densos.
