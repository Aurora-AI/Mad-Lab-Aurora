# Repertório Técnico: Stack WebGL S-Tier (Aurora)

Este documento cataloga ferramentas e bibliotecas WebGL selecionadas para o ecossistema Aurora, priorizando o DNA **Dark Editorial**, performance soberana e fidelidade visual.

## 1. Sovereign Efficiency (Micro-Frameworks)
*Para componentes isolados de altíssima performance onde o Three.js é excessivo.*

- **[OGL](https://github.com/oframe/ogl):** Minimalista, veloz e focado no essencial de WebGL. Ideal para componentes de portfólio e heróis com lógica de shader sob medida.
- **[regl](https://github.com/regl-project/regl):** WebGL funcional. Excelente para pipelines de renderização complexos e manipulação de estado determinística.
- **[nanogl](https://github.com/plepers/nanogl):** Micro-framework focado em modularidade.

## 2. Editorial Fidelity (PBR & High-End)
*Para renderização com qualidade cinematográfica e física de luz real.*

- **[Filament](https://github.com/google/filament/):** Motor de renderização baseada em física (PBR) da Google. O padrão ouro para materiais metálicos, translúcidos e iluminação ambiental realista.
- **[ClayGL](https://github.com/pissang/claygl):** Focado em escalabilidade e aplicações 3D de alta qualidade visual.

## 3. Chaos & Shader Artistry (Effects)
*Para partículas, ruído e transições cinéticas.*

- **[phenomenon-px](https://github.com/vaneenige/phenomenon-px):** A forma mais rápida de criar pixel shaders. Perfeito para o efeito de "Desordem vs. Ordem" (Chaos to Order).
- **[Alfrid](https://github.com/yiwenl/Alfrid):** Conjunto de ferramentas WebGL para experimentação artística e motion design S-Tier.

## 4. Physical Sovereignty (Physics Engines)
*Para gravidade, colisões e interações táteis.*

- **[Ammo.js](https://github.com/kripken/ammo.js/):** Port direto do motor Bullet (C++). Poder computacional bruto para simulações complexas.
- **[Phaser](https://github.com/photonstorm/phaser):** Referência para lógica de jogos 2D acelerados por GPU (se necessário em interfaces interativas).

---
> [!TIP]
> **Recomendação de Fluxo:** Utilize Three.js/R3F como base. Transicione para OGL em seções onde a pontuação do Lighthouse (Performance) for crítica e o componente for visualmente isolado.
