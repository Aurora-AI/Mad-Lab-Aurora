# Aurora Evolution Delta
Data: 2026-06-26T16:53:30-03:00
Documento origem: Manual Operacional: Pipeline Híbrida 3D (CEO-3D + ARC)
Cientista versao: V8.0

## Melhorias Cirurgicas
- **Enforçamento de Sobriedade Visual e Veto a Antipadrões**: Atualizar as regras locais em `.aurora/skills/ceo-design/` e `.aurora/skills/ceo-effects/` para banir terminantemente clichês de "IA Genérica", especificamente grafos plexus luminosos, efeitos holográficos flutuantes (HUDs circulares neon) e glows emissivos.
- **Implementação do Resting State (0.8s)**: Garantir que toda animação interativa nas interfaces da ElysianCorp e Mad Lab respeite um tempo mínimo de repouso operacional de 0.8s antes de iniciar qualquer movimento físico, conferindo peso e seriedade técnica ao sistema.
- **Conformidade de Geometria com Three.js r128**: Vedar o uso de `THREE.CapsuleGeometry` (incompatível com a versão r128 fixada no projeto) em scripts de modelagem Blender e R3F. A modelagem de articulações de hastes deve ser feita puramente combinando `CylinderGeometry` com `IcosahedronGeometry`.

## Novos Componentes Tecnicos
- **AlvaroMesh3D (R3F Component)**: Componente React Three Fiber para carregar e renderizar os modelos GLB sóbrios gerados via pipeline headless do Blender, implementando controle de câmera por arrasto e parallax sutil via cursor.
- **Dynamic Coordinate Projector**: Utilitário matemático R3F que projeta vetores de posição 3D (`X, Y, Z`) do grafo para posições de tela 2D (`top, left` em pixels), viabilizando a renderização de cards explicativos HTML (`MeshNodeCard.tsx`) perfeitamente alinhados na viewport.

## Feature Requests Fundamentais
- **Sincronização de Telemetria de Estado**: Acoplar o estado cognitivo e operacional em tempo real do ecossistema Aurora (ARC Semantic State) aos indicadores físicos entalhados no modelo 3D (laca Moss para operação estável, laca Rust para alertas/bloqueios).

## Skills para Construir ou Atualizar
- **ceo-3d (Atualização)**: Enriquecer com as diretrizes do manual de sobriedade mecânica, modelagem via `bmesh` headless, texturas metálicas/gesso porosas rugosas (`roughness = 0.8`) e contact shadows assadas.
- **site-builder (Atualização)**: Adicionar lógica de fallback automático para carregar renderizações SVG/Canvas 2D finas caso o dispositivo seja de baixo desempenho ou o usuário tenha ativado a diretriz de acessibilidade *prefers-reduced-motion*.
- **taste-design (Atualização)**: Atualizar o template canônico de `DESIGN.md` para abranger os parâmetros e limites físicos das maquetes técnicas tridimensionais (forensic blueprints).
