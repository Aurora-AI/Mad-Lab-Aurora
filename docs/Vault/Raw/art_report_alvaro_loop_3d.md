# ART PRODUCTION REPORT: ALVARO COGNITIVE LOOP 3D
**ID:** ART-REPORT-ALVARO-LOOP-3D-001  
**Agente:** `ceo-art-direction`  
**Status:** 🟢 CANONIZADO — REVISÃO SOBRIEDADE EDITORIAL (v2.2.0)  
**DNA Visual:** Dark Editorial / Swiss Grid / Forensic Blueprint (v2.1.0)  
**Projeto de Referência:** `C:\Projetos\MadLabAurora\ElysianCorp`

---

## 1. Diretriz de Intenção e Sobriedade Editorial (Veto ao Sci-Fi)

A proposta anterior foi revisada e expurgada de elementos fantasiosos ou clichês de ficção científica (glows excessivos, tubos de energia, núcleos brilhantes). O 3D do Álvaro deve ser um **esquema técnico tridimensional de alta precisão (forensic blueprint)**, que se comporta como um desenho industrial real projetado no espaço.

A peça deve assemelhar-se a uma **maquete física de arame e blocos de metal/concreto** usada em exposições de arquitetura modernista (estilo Dieter Rams / Escola de Ulm), assentada sobre papel editorial creme ou obsidian técnico áspero, sem emanação de luz digital ou efeitos holográficos.

---

## 2. Paleta Cromática e Materialidade Sólida (Sem Luz Emitida)

Substituímos toda emissão de luz artificial (glow/emission) por contraste de materiais foscos e marcações mecânicas:

| Elemento | Mundo Luminoso (Off-White Editorial) | Mundo Dark (Obsidian Technical) |
|---|---|---|
| **Background** | Papel creme texturizado (`#F8F7F3`) com grão de fibra | Slate escuro áspero (`#0D0D0D`) com micro-textura de concreto |
| **Material dos Nós** | Blocos de ferro fundido poroso ou grafite escuro | Aço laminado fosco com marcas de laminação |
| **Acento Ativo** | Marcação em laca fosca **Elysian Moss** (`#4E5B4B`) | Marcação mecânica em tom ferrugem (`#984731`) ou ouro latão |
| **Conexões (Linhas)** | Arame de aço galvanizado fino (cinza fosco) | Hastes metálicas cinza técnico (`#535F6F`) de 0.5px |
| **Marcações Técnicas** | Tipografia monospace e cruzes de grid em cinza médio | Coordenadas e miras finas em branco técnico 40% opacidade |

---

## 3. Especificação Arquitetural e Geometria Rígida

### 3.1 Os Nós (Nodes)
*   **Geometria:** Icosaedros de baixa resolução (`subdivisions=1` no script Blender) ou blocos cúbicos chanfrados. A geometria deve parecer **cortada à mão ou usinada**, com arestas vivas bem definidas.
*   **Nós do Loop (5):** Diâmetro `0.12` unidades. Sem núcleos brilhantes internos. Em vez disso, nós ativos possuem uma **pequena marcação circular em baixo relevo** (engraved dot, diâmetro `0.03`) preenchida com a cor de acento do respectivo estado (Moss ou Rust), como um botão de controle físico.
*   **Nós de Princípio/Satélites (6):** Pequenos cubos chanfrados (`0.05` de diâmetro), representando limitadores mecânicos estáveis.

### 3.2 As Conexões (Edges)
*   **Geometria:** Cilindros ultrafinos (`tube_radius = 0.008`) simulando hastes de aço de suporte estrutural.
*   **Estilo das Linhas:** Sem glows, sem partículas fluindo. A direção do fluxo é indicada por **pequenos cones mecânicos (setas físicas de 1px)** posicionados no centro da haste, orientando a leitura.
*   **Conexões de Satélite:** Linhas tracejadas geradas via shader de textura (preto/branco alternado fosco), simulando fios de medição física sob tensão.

### 3.3 Layout e Alinhamento no Grid
*   A estrutura pentagonal de `1.6` unidades de raio reside no plano horizontal XZ, com inclinação de `12°` no eixo X para criar perspectiva espacial.
*   O alinhamento é estrito e segue regras de desenho técnico: os satélites conectam-se às suas bases de forma perpendicular ou radial perfeita.

---

## 4. Dinâmica de Movimento: O Silêncio Físico (Resting State)

Eliminamos movimentos de órbita celestes ou oscilações de flutuação mágica:

1.  **Sem Micro-Oscilação (Static Rigidity):**
    *   A malha 3D permanece perfeitamente estática em seu estado ocioso. A sensação de dinamismo é gerada exclusivamente pela **interação física do usuário** (rotação por arrasto do mouse ou parallax de câmera muito sutil).
2.  **Transições de Foco (GSAP):**
    *   Ao alternar ou clicar em um nó, a câmera transiciona com um movimento linear seco e amortecido (`power2.out`, `duration: 0.6s`), sem efeitos de bounce ou oscilações elásticas.
3.  **Indicadores de Estado:**
    *   Nós ativos apenas mudam a cor de sua marcação física entalhada. Se um fluxo é bloqueado, o acento correspondente muda de cor, sem flashes luminosos ou tremores de câmera.

---

## 5. Shader e Texturas Industriais (Non-Emissive)

1.  **Roughness & Bump Maps:** Uso obrigatório de mapas de ruído de concreto ou metal riscado para quebrar o reflexo da iluminação e evidenciar imperfeições de fabricação.
2.  **Shadows & Ambient Occlusion (AO):** Sombra de contato bem marcada (contact shadows) abaixo de cada nó no plano base, ancorando a maquete física ao fundo de papel/slate.

---

## 6. Contrato de Execução Limpo

```json
{
  "contract_id": "CON-ALVARO-LOOP-3D-SOBER-002",
  "geometry": {
    "total_vertex_count_limit": 8000,
    "forbidden_constructs": ["THREE.CapsuleGeometry", "MeshEmissionShader"],
    "allowed_primitives": ["CylinderGeometry", "BoxGeometry", "IcosahedronGeometry"]
  },
  "materials": {
    "metallic_factor": 0.7,
    "roughness_factor": 0.8,
    "emissive_intensity": 0.0
  },
  "interaction": {
    "hover_glow": false,
    "hover_scale_factor": 1.05,
    "camera_easing": "power2.out"
  }
}
```
