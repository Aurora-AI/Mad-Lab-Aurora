# Anatomy: Magnetic Button (interactions-magnetic-button-001)

## Architecture
O `Magnetic Button` é um wrapper de interação que utiliza a posição do mouse em relação ao centro do componente para aplicar uma força de atração. É um padrão clássico de interfaces premium para guiar o foco do usuário.

## Core Components
- **MagneticButton**: O container que detecta o hover e calcula o offset.
- **useSpring**: Gancho de física do Framer Motion para garantir que o retorno ao centro não seja linear.

## Techniques & Patterns
- **P046: Proximity-Based Attraction**: O deslocamento é calculado como uma fração (`distance`) da distância absoluta entre o cursor e o centro do elemento.
- **P047: Damped Origin Return**: Uso de molas com `mass: 0.1` e `stiffness: 150` para criar um efeito de snap "leve" mas reativo.

## Dependency Analysis
- **Framer Motion**: Necessário para `useSpring` e manipulação de `x/y`.

## Performance
- **Event Throttling**: Como o cálculo ocorre no `onMouseMove`, o uso de MotionValues do Framer Motion garante que as atualizações de DOM ocorram fora do ciclo de render do React, mantendo 60fps.
