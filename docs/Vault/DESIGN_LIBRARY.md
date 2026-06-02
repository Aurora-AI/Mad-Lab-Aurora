# Aurora Design Library — Padrões e Ativos

Este documento é o Single Source of Truth (SSOT) para padrões técnicos e funcionais da Aurora.

---

## 🚀 Biblioteca Canônica (Ativos Vivos)
A biblioteca completa de componentes, shaders e interações está localizada em:
**Path:** `aurora-visual-assets/`  
**Manifesto:** [manifest.json](file:///C:/Projetos/Aurora/MadLabAurora/aurora-visual-assets/manifest.json)

---

## [P046 - P052] Padrões de Sincronização WebGL (Lusion)

### P046 — Absolute Canvas Scroll Sync
**Problema:** Drift visual entre elementos DOM e objetos WebGL devido à dessincronização entre o thread de scroll e o loop de renderização (rAF).
**Solução:** Utilizar um canvas com `position: absolute` que rola naturalmente com a página. A cada frame do `requestAnimationFrame`, aplicar um `transform: translate` compensatório baseado no `scrollY` atual para manter o canvas fixo na viewport de forma simulada, mas sincronizada fisicamente com o fluxo de scroll.
**Contexto:** Essencial para layouts Dark Editorial onde a tipografia DOM deve ancorar meshes 3D com precisão de pixel.

### P047 — Vertical Canvas Padding Buffer
**Problema:** Clipping de meshes durante scrolls rápidos quando o canvas tem exatamente o tamanho da viewport.
**Solução:** Renderizar o canvas com um padding vertical (ex: 25% ou 50% extra no topo e base). Isso cria uma "margem de segurança" para objetos que estão entrando ou saindo da viewport.
**Trade-off:** Aumenta o pixel budget. Requer monitoramento em GPUs mobile integradas.

### P048 — Single Canvas Multi-DOM Anchoring
**Problema:** Múltiplos canvas WebGL degradam a performance (`Too many contexts`).
**Solução:** Gerenciar múltiplos objetos 3D dentro de um único canvas global, rastreando as bounding boxes (`getBoundingClientRect`) de elementos "placeholder" no DOM e mapeando-as para coordenadas NDC dentro do shader.

### P049 — DOM-to-NDC Vertex Mapping
**Problema:** Coordenadas de pixels do browser (top-left) são diferentes das coordenadas NDC do WebGL (center, -1 a 1).
**Solução:** Implementar a lógica de conversão diretamente no Vertex Shader para garantir que a mesh acompanhe o elemento DOM em tempo real sem latência de CPU.
```glsl
vec2 pixelXY = u_domXY - u_scrollOffset + u_domWH * 0.5;
pixelXY.y = u_resolution.y - pixelXY.y;
vec2 xy = pixelXY / u_resolution * 2. - 1.;
```

### P050 — Scroll-Driven Glitch Shader
**Efeito:** Distorção visual (glitch/offset horizontal) que reage à velocidade do scroll.
**Implementação:** Calcular a velocidade do scroll (`deltaY / dt`) e passá-la como uniform para o shader, modulando um ruído estocástico que desloca linhas horizontais.

### P051 — Scroll Strength Decay
**Efeito:** Persistência suave do efeito após a parada do scroll.
**Lógica:** Aplicar um decaimento exponencial (`strength *= Math.exp(-dt * speed)`) para que a energia do movimento não pare abruptamente, conferindo "massa" e inércia visual.

### P052 — Frustum Culling Manual (GPU Prep)
**Problema:** Renderizar objetos fora da viewport consome ciclos de GPU desnecessários.
**Solução:** Definir `mesh.visible = false` para qualquer objeto cujas coordenadas de bounding box estejam fora da área ativa do canvas (incluindo o buffer de padding).

---

## [T001] Repertório Técnico: WebGL Stack S-Tier
Para casos de uso que exigem performance extrema, fidelidade física absoluta ou manipulação artística de pixels além do escopo do Three.js, consulte o catálogo de ferramentas selecionadas:

- **Local:** [webgl_s_tier_repertoire.md](file:///C:/Projetos/Aurora/MadLabAurora/docs/Vault/Knowledge/webgl_s_tier_repertoire.md)
- **Categorias:** Sovereign Efficiency, Editorial Fidelity, Chaos Artistry.
