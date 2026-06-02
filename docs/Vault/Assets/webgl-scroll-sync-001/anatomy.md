# Anatomy — WebGL Scroll Sync (Lusion)

## Identificação
- **Asset ID:** webgl-scroll-sync-001
- **Categoria:** effects/scroll-sync
- **Origem:** externa — Lusion Ltd (Bristol, UK)
- **Licença:** MIT ✅
- **Stack:** Three.js + WebGL + Vanilla JS

## O Problema Resolvido
Canvas WebGL `position: fixed` + scroll nativo = **drift**. O scroll acontece no thread do browser, enquanto o rAF (rendering) pode ter um ligeiro atraso, fazendo com que objetos 3D descoleem dos elementos DOM.

## A Solução Lusion (Padrões P046 - P052)
A Lusion utiliza um **Canvas Absoluto** que rola fisicamente com a página, eliminando o drift entre frames. Um **Offset Compensatório** via `transform: translate` é aplicado a cada rAF para manter o conteúdo visível na viewport.

### Padrões Extraídos
- **P046 — Absolute Canvas Scroll Sync**: Canvas `position: absolute` + offset por `scrollY`.
- **P047 — Vertical Canvas Padding Buffer**: Renderização de 25% de pixels extras (top/bottom) para evitar clipping.
- **P048 — Single Canvas Multi-DOM Anchoring**: Ancoragem de múltiplos objetos 3D a bounding boxes DOM via um único canvas.
- **P049 — DOM-to-NDC Vertex Mapping**: Conversão de coordenadas de pixel DOM para NDC no Vertex Shader.
- **P050 — Scroll-Driven Glitch Shader**: Distorção proporcional à velocidade de scroll.
- **P051 — Scroll Strength Decay**: Decaimento exponencial da força da animação.
- **P052 — Frustum Culling Manual**: Gerenciamento manual de visibilidade de meshes.

## Veredito CEO-Effects
**APROVADO COM RESSALVA**: Proporciona uma conexão tátil única entre o scroll e a imagem (feedback físico). Ressalva para performance mobile devido ao custo de fragment por pixel (motion blur loop).

## Veredito CEO-Design
**APROVADO (Infraestrutura)**: Ativo de infraestrutura invisível que habilita a "Profundidade Impossível" com precisão de pixel.
