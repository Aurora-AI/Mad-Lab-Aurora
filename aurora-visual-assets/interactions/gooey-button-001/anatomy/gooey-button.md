# Anatomy: Gooey Button (interactions-gooey-button-001)

## Architecture
O `Gooey Button` utiliza filtros SVG avançados para mesclar elementos visualmente próximos através da manipulação do canal alpha. É uma técnica de design orgânico que remove a rigidez geométrica típica do CSS.

## Core Components
- **SVG Filter**: Um container estático contendo a definição do filtro `gooey`.
- **GooeyButton**: O componente funcional que aplica o filtro ao seu wrapper de conteúdo.

## Techniques & Patterns
- **P048: Alpha Channel Thresholding**: O uso de `feColorMatrix` com valores de contraste elevados (`18 -7`) no canal alpha converte um desfoque suave em uma borda sólida e "pegajosa".
- **P049: Composited Blobs**: Elementos secundários (blobs) que emergem de trás do botão principal e se fundem a ele durante o hover.

## Dependency Analysis
- **Nativa**: Não requer bibliotecas externas, processado diretamente pela engine de renderização do browser (Skia/Blink).

## Performance
- **GPU Bottlenecks**: Filtros SVG são intensivos em CPU se aplicados a grandes áreas. O componente isola o filtro apenas ao wrapper imediato do botão para minimizar o custo de re-layout.
