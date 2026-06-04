# Anatomy: Footer Dark (navigation-footer-dark-001)

## Architecture
O `Footer Dark` é um componente estrutural de encerramento de página que prioriza o silêncio e o peso tipográfico. Ele utiliza um layout dual (Marca vs. Links) com espaçamento generoso para manter o padrão *editorial*.

## Core Components
- **Footer Container**: Grid responsivo com bordas ultra-finas (`white/5`).
- **Status Indicator**: Micro-componente de feedback visual que simula monitoramento sistêmico.

## Techniques & Patterns
- **P052: Modular Link Architecture**: Organização de links em colunas puras com hierarquia tipográfica via `font-mono` e `tracking-[0.4em]`.
- **P053: Dynamic Contextual Metadata**: Inclusão de ano dinâmico e indicadores de sistema no rodapé para reforçar a identidade "software-like".

## Dependency Analysis
- **Nativa**: Baseado em Tailwind CSS e React puro.

## Performance
- **Static Composition**: Quase zero custo de execução JS (apenas o Date para o ano), servindo como uma seção de baixo custo computacional após cenas pesadas do Hero.
