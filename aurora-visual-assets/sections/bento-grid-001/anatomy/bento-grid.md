# Anatomy: Bento Grid (sections-bento-grid-001)

## Architecture
O `Bento Grid` é uma estrutura de layout baseada em CSS Grid (4 colunas / 2 linhas na configuração desktop) que permite a agregação de conteúdos heterogêneos mantendo a coesão visual. É o padrão da Aurora para dashboards e seções de features.

## Core Components
- **BentoGrid**: O container que define as frações de grid e o gap rítmico.
- **BentoItem**: Células individuais com suporte a gradientes de hover e transições de borda.

## Techniques & Patterns
- **P050: Fractional Span Management**: O uso de spans variados (`col-span-*`) permite que itens ganhem peso visual hierárquico dentro da mesma seção.
- **P051: Subtle Gradient Overlays**: Uso de `bg-gradient-to-br` com opacidade ultra-baixa (`white/[0.02]`) que emerge no hover, simulando luz física.

## Dependency Analysis
- **Tailwind CSS**: Utilizado para o sistema de grid responsivo e utilitários de cor.

## Performance
- **Containment**: O uso de `overflow: hidden` e `relative positioning` nas células garante que animações internas não causem repaints agressivos no layout pai.
