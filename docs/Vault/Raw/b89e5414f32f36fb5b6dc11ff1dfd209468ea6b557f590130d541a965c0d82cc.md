# MANUAL OPERACIONAL: PIPELINE HÍBRIDA 3D (CEO-3D + ARC)
**Código de Conhecimento:** KNL-MADLAB-3D-PIPELINE-001  
**Autoridade:** Mad Lab Aurora / Governança do Trustware  
**Status:** 🟢 CANONIZADO (SSOT)  
**Versão:** 1.0.0  
**Destinatários:** Agentes de IA da Aurora (`antigravity`, `site-builder`, `ceo-effects`, `taste-design`, `qa-review`)

---

## 1. Visão Geral do Sistema

O **Sistema Híbrido de Visualização 3D (CEO-3D + ARC)** é um ecossistema de renderização semântica projetado para representar a topologia, governança e estados cognitivos de agentes autônomos (como o loop Álvaro e telemetrias da rede). 

O sistema integra o **Blender Headless (Background Execution)** para geração e otimização matemática de malhas 3D (GLB) com o **React Three Fiber (R3F) + GSAP** no frontend para exibição interativa.

```text
  ESTADO COGNITIVO
(SemanticState/ARC)
        │
        ▼
   BLENDER CLI     ───►  ARQUIVO GLB  ───►   R3F CANVAS
(alvaro_loop_3d.py)      (public/models/)     (AlvaroMesh3D.tsx)
                                                  │ (project 3D->2D)
                                                  ▼
                                            CARDS HTML/DOM
                                           (MeshNodeCard.tsx)
```

---

## 2. Capacidades do Sistema

### A. Geração Headless Matemática (`ceo-3d`)
*   **Construção via Bmesh:** Geração procedural de geometrias complexas (icosaedros, tubos, treliças, cilindros) por coordenadas puramente matemáticas, dispensando o contexto de interface gráfica (`view3d`).
*   **Baking de Texturas e AO:** Capacidade de assar oclusão de ambiente (Ambient Occlusion), sombras de contato e texturas ásperas diretamente nos arquivos GLB.
*   **Otimização Poligonal:** Pipeline nativo para decimator de malhas, garantindo modelos ultraleves.

### B. Renderização Híbrida Inteligente (`packages/arc-renderer-r3f`)
*   **Fallback Dinâmico:** Se a GPU do dispositivo for classificada como de baixa performance (`degraded` / mobile lento) ou se a rede falhar, o sistema desativa o Canvas 3D e renderiza um layout equivalente bidimensional (SVG ou Canvas 2D) instantaneamente.
*   **Carregamento Assíncrono:** Uso de `<Suspense>` e loaders não-bloqueantes para carregamento progressivo dos ativos `.glb`.

### C. Projeção de Coordenadas Bidirecional
*   **Ancoragem de UI Híbrida:** O R3F calcula as posições dos nós em coordenadas tridimensionais (X, Y, Z) e as projeta para coordenadas de tela 2D do navegador. Isso permite renderizar cards HTML normais (`MeshNodeCard`) flutuando exatamente acima dos nós 3D, garantindo responsividade e acessibilidade completas.

### D. Sobriedade Estética Integrada
*   O sistema força a neutralização de pirotecnias visuais por meio de shaders de materiais de alta rugosidade, sombreamento realista e eliminação total de glows de ficção científica.

---

## 3. Quando e Quem Deve Usar

### Quem Deve Usar:
*   **Agente `site-builder`:** Para integrar exibições topológicas e painéis de dados nas páginas web.
*   **Agente `ceo-effects`:** Para ajustar comportamentos interativos (parallax, drag-orbit, transições de câmera).
*   **Agente `taste-design`:** Para inspecionar se a estética cumpre as diretrizes da marca.
*   **Desenvolvedores Humanos:** Como guia SSOT de integridade da pipeline.

### Quando Usar:
*   **Visualização de Fluxo de Dados/Agentes:** Sempre que for necessário exibir a mente de um agente autônomo, estruturas de tomada de decisão (grafos) ou pipelines de governança.
*   **Painéis Técnicos e Dashboards:** Onde a apresentação fria, precisa e forense de dados estruturados for prioritária sobre o marketing genérico.

---

## 4. Como Operar o Pipeline (Manual Técnico)

### 4.1 Geração de Ativos no Blender (Headless)
Ao gerar ou modificar o script Blender (`alvaro_loop_3d_generator.py`), execute-o passando a flag de background para o executável do Blender:

```powershell
blender --background --python C:\Projetos\MadLabAurora\aurora-visual-assets\blender_scripts\primitives\alvaro_loop_3d_generator.py -- --state STABLE_OPERATION --output C:\Projetos\MadLabAurora\aurora-web\public\models\alvaro\loop_stable.glb
```

**Regras de escrita do script Python:**
1.  **Limpeza Incondicional:** Sempre inicie o script limpando a cena padrão (`bpy.ops.wm.read_factory_settings(use_empty=True)`).
2.  **Uso de `bmesh`:** Nunca utilize comandos de interface (`bpy.ops.object.*`, `bpy.ops.mesh.select_all`) que dependam de foco de tela ou modo de edição interativo. Crie e manipule a geometria no objeto de dados direto:
    ```python
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.12)
    # ... manipulação matemática de vértices ...
    bm.to_mesh(mesh)
    bm.free()
    ```

### 4.2 Projeção de Coordenadas 3D para 2D no Frontend
Para alinhar elementos HTML aos nós tridimensionais, utilize o seguinte padrão R3F dentro do loop de animação:

```typescript
import { useFrame, useThree } from '@react-three/fiber';
import * as THREE from 'three';

// No componente do nó ou no orquestrador do Canvas:
const { camera, size } = useThree();
const tempV = new THREE.Vector3();

useFrame(() => {
  // 1. Obter a posição 3D do objeto
  meshRef.current.getWorldPosition(tempV);
  
  // 2. Projetar a coordenada para a câmera
  tempV.project(camera);
  
  // 3. Converter para coordenadas de pixel CSS
  const x = (tempV.x *  .5 + .5) * size.width;
  const y = (tempV.y * -.5 + .5) * size.height;
  
  // 4. Atualizar o estado ou DOM do card explicativo
  updateCardPosition(nodeId, x, y);
});
```

---

## 5. Limites e Restrições Críticas (Vetos do Trustware)

> [!IMPORTANT]
> **Bloqueio de Versão do Three.js (r128)**
> O projeto está fixado no Three.js versão **r128**. 
> * **Proibido** utilizar `THREE.CapsuleGeometry` (introduzido apenas no r142).
> * **Solução:** Use cilindros (`CylinderGeometry`) com esferas/icosaedros nas pontas para simular junções capsulares.

> [!WARNING]
> **Veto Estético de "IA Genérica"**
> Não crie nem integre os seguintes antipadrões estéticos sob nenhuma hipótese:
> *   **Glows Emissivos e Neon:** Materiais não devem emitir brilho volumétrico exagerado (cuidado com intensidades altas de emissão).
> *   **Malhas Plexus Translúcidas:** Grafos complexos flutuantes com dezenas de partículas digitais e linhas luminosas.
> *   **Fundo Chapado #000000:** Use cinza editorial áspero ou concreto texturizado.

> [!CAUTION]
> **Regra do Resting State (0.8s)**
> Todo movimento interativo deve respeitar o silêncio de repouso mínimo de **0.8 segundos** antes de iniciar qualquer animação, transmitindo peso físico e rigidez mecânica.

> [!NOTE]
> **Orçamento de Polígonos (Budget)**
> *   Limite máximo de contagem de vértices por modelo exportado: **15.000 vértices** para evitar gargalos na renderização web em dispositivos móveis.
> *   Tamanho máximo de arquivo GLB por ativo: **1.5 MB**.
