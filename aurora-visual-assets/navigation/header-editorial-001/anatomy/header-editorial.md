# Anatomy: Editorial Header (navigation-header-editorial-001)

## Architecture
O `Editorial Header` é o ponto de entrada visual padrão para aplicações Aurora. Ele utiliza `mix-blend-difference` para garantir legibilidade automática sobre qualquer fundo (vídeos, 3D ou seções claras/escuras).

## Core Components
- **Header Editorial**: O container fixo/absoluto com compositing de mistura de cor.
- **Nav Links**: Lista de links com micro-animações de entrada e hover.

## Techniques & Patterns
- **P045: Minimalist Constraint**: Redução ao essencial — apenas tipografia e marcadores de estado.
- **P054: Mix-Blend Difference Integration**: Uso de `mix-blend-difference` no CSS para que o texto branco inverta a cor ao passar por fundos claros, eliminando a necessidade de lógica de "inversion" manual.

## Dependency Analysis
- **Framer Motion**: Utilizado para o stagger inicial de entrada.

## Performance
- **CSS Compositing**: O uso de `mix-blend` é acelerado via hardware, mas requer cuidado com a hierarquia de `z-index` e `isolation` para não "sumir" sob outras camadas misturadas.
