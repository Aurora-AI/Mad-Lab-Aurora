# Anatomy: Hero Futuristic
**Asset ID:** hero-futuristic-001  
**Origem:** David Hakobyan (@reapollo) — https://21st.dev/r/reapollo/hero-futuristic  
**Dissecado em:** 2026-04-18  
**Dissecado por:** Claude (Arquiteto Aurora)  

---

## O que este ativo faz

Uma hero section full-screen que exibe uma imagem 3D com:
1. **Parallax por depth map** — a imagem "respira" conforme o mouse se move
2. **Scan line animada** — uma varredura vertical revela/processa a imagem
3. **Dot grid overlay** — grade de pontos com cell noise cobre a imagem com efeito de scanner
4. **Bloom pós-processamento** — brilho WebGPU nativo sobre a cena
5. **Texto animado** — palavras do título aparecem em sequência (word-by-word reveal)
6. **Fade-in de cena** — a imagem aparece suavemente após carregar as texturas

---

## Arquitetura de Componentes

```
Html (export default)
├── Overlay HTML (posição absoluta z-60)
│   ├── Título animado (word reveal via useState + setTimeout)
│   └── Subtítulo animado (fade após título completo)
├── Botão "Scroll to explore" (CSS animation)
└── Canvas (Three.js WebGPU)
    ├── PostProcessing
    │   ├── ScenePass (captura output da cena)
    │   ├── BloomPass (glow nos elementos brilhantes)
    │   └── ScanLine overlay (red tint animado sobre toda a cena)
    └── Scene
        └── Mesh (plane geometry)
            └── MeshBasicNodeMaterial
                ├── rawMap (textura principal) com UV deslocado pelo depth
                ├── depthMap (depth map para parallax)
                └── Dot grid com cell noise blendado por screen mode
```

---

## Fluxo de Dados

```
Mouse position → uPointer uniform → UV displacement → parallax effect
Clock elapsed  → uProgress uniform → scan line position → dot reveal mask
Texture load   → setVisible(true) → opacity lerp 0→1 → fade in
```

---

## Técnicas Utilizadas

| Técnica | Implementação | Padrão Aurora |
|---|---|---|
| Depth map parallax | TSL: `tDepthMap.r.mul(uPointer).mul(strength)` | P001 |
| Cell noise dot grid | TSL: `mx_cell_noise_float` + smoothstep | P002 |
| Scan line progress | TSL: `smoothstep(0, 0.02, abs(depth.sub(uProgress)))` | P003 |
| Screen blend | TSL: `blendScreen(tMap, mask)` | P004 |
| Bloom WebGPU | TSL: `bloom(scenePassColor, strength, 0.5, threshold)` | P005 |
| Fade in suave | `THREE.MathUtils.lerp(opacity, target, 0.07)` per frame | — |
| Word reveal | `useState + setTimeout` chain | — |

---

## Dependências e Requisitos

**Browser:** Chrome 113+ (WebGPU). Safari/Firefox: não suportado sem flags.  
**Three.js:** Import de `three/webgpu` — API diferente do Three padrão.  
**TSL:** Three Shading Language — substitui GLSL na API WebGPU.  

### Conflito com Stack Aurora

O aurora-web usa `three: "0.183.2"` — compatível.  
Atenção: `import * as THREE from 'three/webgpu'` é diferente de `'three'` padrão.
Não misturar os dois no mesmo arquivo.

---

## Variáveis de Customização

| Variável | Localização | Efeito |
|---|---|---|
| `TEXTUREMAP.src` | Topo do arquivo | Imagem principal |
| `DEPTHMAP.src` | Topo do arquivo | Depth map da imagem |
| `strength` (parallax) | `Scene.useMemo` | Intensidade do parallax (padrão: 0.01) |
| `scaleFactor` | `Scene return` | Tamanho da mesh na tela (padrão: 0.40) |
| `tiling` | `Scene.useMemo` | Densidade do dot grid (padrão: 120.0) |
| `bloom strength` | `PostProcessing` | Intensidade do bloom (padrão: 1) |
| `titleWords` | `Html` | Texto do título |
| `subtitle` | `Html` | Texto do subtítulo |

---

## Como Adaptar para Aurora

### 1. Substituir texturas
```tsx
const TEXTUREMAP = { src: '/assets/aurora-hero-texture.png' }
const DEPTHMAP = { src: '/assets/aurora-hero-depth.webp' }
```

### 2. Ajustar copy
```tsx
const titleWords = 'Aurora. Elevação. Inteligência.'.split(' ')
const subtitle = 'Infraestrutura cognitiva para quem constrói o futuro.'
```

### 3. Aumentar parallax para mais dramaticidade
```tsx
const strength = 0.025 // era 0.01
```

### 4. Ajustar bloom para identidade Aurora (mais sutil)
```tsx
<PostProcessing strength={0.6} threshold={0.9} />
```

---

## Limitações Conhecidas

1. **WebGPU only** — fallback necessário para Safari/Firefox
2. **Performance mobile** — Canvas WebGPU é pesado em dispositivos low-end
3. **Texturas externas** — URLs de `i.postimg.cc` não são confiáveis em produção; hospedar localmente
4. **Animação da scan line** — sincronizada com clock, não com scroll; considerar adaptar para Lenis

---

## VEREDITO CEO-EFFECTS

```
FILTRO DE TRANSPLANTE (CEO-Effects) — Aprovação Inaugural
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PERGUNTA 1 — Intenção:
  Sim — "Uma imagem que respira e revela seus segredos
  conforme o visitante se aproxima."

PERGUNTA 2 — Narrativa:
  Sim — sem o scan e o parallax, é apenas uma imagem estática.
  O efeito É o que torna a imagem viva.

PERGUNTA 3 — Física:
  Gravidade — lerp 0.07 no fade-in, movimento de mouse suave.
  Não é snap. Tem inércia.

PERGUNTA 4 — Silêncio:
  Presente — o fundo preto é parte do efeito. A imagem emerge,
  não aparece. O silêncio antes do reveal é intencional.

PERGUNTA 5 — Permanência:
  Inevitável — depth map parallax é técnica com fundação física
  real, não trend de UI. WebGPU é direção do ecossistema.

PERGUNTA 6 — Performance:
  Não testado localmente — WebGPU requer Chrome 113+.
  Fallback necessário para Safari/Firefox/mobile low-end.

VEREDITO: APROVADO COM RESSALVAS
Ressalva principal: implementar fallback WebGL ou CSS
para browsers sem WebGPU antes de usar em produção.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## VEREDITO CEO-DESIGN

```
FILTRO DE STRESS ESTRUTURAL (CEO-Design) — Aprovação Inaugural
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Contexto: Ativo de ATMOSFERA/EXPERIÊNCIA — não de identidade visual.
Avaliado como camada sensorial, não como sistema de marca.

TESTE 1 — Colapso Utilitário:    N/A
  Ativo de efeito — sem forma estática para colapso.

TESTE 2 — Silêncio Tipográfico:  N/A
  Sem tipografia própria no componente 3D.
  Tipografia overlay (título) deve ser avaliada separadamente.

TESTE 3 — Gancho de Casaco:      Suporte
  O efeito não chama atenção para si — serve a imagem/produto.
  O visitante lembra da imagem, não do scan.

TESTE 4 — Auditoria Geométrica:  N/A
  Sem geometria de marca — planeGeometry é suporte técnico.

TESTE 5 — Holding Space:         N/A
  Sem símbolo ou ícone para avaliar.

TESTE 6 — DNA Compartilhado:     N/A
  Sem tipografia própria no componente.

TESTE 7 — DNA do Projeto:
  Alinha com Dark Editorial — profundidade sem complexidade,
  beleza sem ornamento, mundo que parece existir antes do
  visitante chegar. O scan revela em vez de mostrar.
  Ressalva: depende da imagem e depth map escolhidos —
  com texturas erradas pode virar pirotecnia SaaS.

VEREDITO: RESISTENTE COM RESSALVA
Ressalva: aprovação condicionada à curadoria das texturas.
Texturas genéricas ou gradientes SaaS invalidam o ativo.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Próxima Evolução Aurora-Native

Com base nos padrões P001-P005 extraídos, o CEO-Design agent poderá:
- Criar hero sections com depth map de produtos Aurora reais (Lex, CRM)
- Variar o dot grid para hexagonal ou triangular
- Sincronizar a scan line com o scroll em vez do clock
- Adicionar audio-reactive se o contexto pedir
