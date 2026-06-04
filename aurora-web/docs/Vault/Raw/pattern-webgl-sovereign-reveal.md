# Pattern: Sovereign Reveal (Orientation & WebGL Zone Logic)

**Status:** APROVADO
**Data:** 2026-04-16
**Autor:** CEO-Effects (via Ingestor)
**Domínio:** Effects / WebGL
**Hash de Custódia:** 8a9c4b12e6d7f8a9

## Contexto
Durante a implementação do **Sovereign Hero** para o projeto Elysian, foi detectada uma inconsistência crítica de orientação (imagem invertida) e a necessidade de comportamentos de "reveal" assimétricos (Zonas de Investigação vs. Zonas de Verdade) em um único canvas WebGL.

## Solução Técnica Canônica

### 1. Correção de Orientação via Vertex Buffer
Em vez de depender de flags de upload globais do WebGL (como `UNPACK_FLIP_Y_WEBGL`), o padrão Aurora para **Sovereign UI** exige a inversão do mapeamento de UV diretamente no buffer de vértices. Isso simplifica a matemática no Fragment Shader, permitindo o uso direto de coordenadas de mouse do DOM.

**Mapeamento de UV Estável:**
```typescript
new Float32Array([
  -1, -1, 0, 1,  // Bottom-Left  -> UV(0, 1) [Base do Canvas]
   1, -1, 1, 1,  // Bottom-Right -> UV(1, 1)
  -1,  1, 0, 0,  // Top-Left     -> UV(0, 0) [Topo do Canvas]
  -1,  1, 0, 0,
   1, -1, 1, 1,
   1,  1, 1, 0   // Top-Right    -> UV(1, 0)
])
```

### 2. Reveal Assimétrico por Zona (Narrativa Forense)
A interface deve responder de forma distinta em cada zona de conteúdo, utilizando o `v_uv.x` como seletor lógico dentro do mesmo shader:
- **Zonas de Investigação (Puzzle/Imagens):** Ativadas via `mouseReveal` (proximidade).
- **Zonas de Verdade (Copy/Títulos):** Ativadas via `u_post_reveal` (timing soberano).

```glsl
bool isImageZone = v_uv.x > 0.48;
float reveal = isImageZone ? (mouseReveal * 0.75) : u_post_reveal;
```

## Aplicação e Handoff
- **CEO-Effects:** Deve usar este padrão em todo hero section que utilize "Scramble Reveals".
- **Site-Builder:** Deve validar a orientação de texturas em canvas 2D -> WebGL usando este buffer como fallback prioritário.

---
*Cadeia de Custódia preservada por Bibliotecário.*
