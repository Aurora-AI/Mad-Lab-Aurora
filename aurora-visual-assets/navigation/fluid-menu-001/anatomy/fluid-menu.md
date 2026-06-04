# Anatomy: Fluid Menu (navigation-fluid-menu-001)

## Architecture
O `Fluid Menu` é um componente de navegação vertical baseado em expansão sequencial. Ele utiliza o princípio de **Additive Reveal**, onde cada item é empilhado abaixo do gatilho principal.

## Core Components
- **FluidMenu**: O container que orquestra o estado de expansão e a transição do grupo.
- **FluidMenuItem**: Itens individuais que aceitam ícones e labels mono.

## Techniques & Patterns
- **P040: Expansion Staggering**: O uso de delay escalonado (`index * 50ms`) na propriedade `transform` para criar uma sensação de fluido.
- **P041: Circular Constraint Mapping**: Aplicação de `clip-path: circle(50% at 50% 50%)` para garantir que todos os itens mantenham a geometria circular durante a transição, independente do conteúdo.
- **Physics**: Utiliza a curva Bezier `(0.19, 1, 0.22, 1)` (Power4.out) para um movimento "expensive".

## Dependency Analysis
- **Framer Motion**: (Opcional, implementado em CSS Transition para performance bare-metal).
- **Lucide React**: Para iconografia.

## Performance
- **Will-Change**: Aplicado a `transform` nos itens para garantir aceleração de hardware durante a expansão em dispositivos móveis.
