# ANATOMY: Spiral Animation (Kinetic Wormhole)
`ID: backgrounds-spiral-001`

## 1. RESUMO EXECUTIVO
O **Spiral Animation** é um motor de partículas cinético que simula uma viagem através de um túnel ou "wormhole" digital. Diferente de soluções 3D robustas (Three.js), este componente utiliza projeção matemática pura em Canvas 2D para converter coordenadas 3D em pontos 2D, resultando em uma performance excepcional mesmo com 5000 partículas simultâneas.

## 2. ESPECIFICAÇÕES TÉCNICAS
- **Core**: GSAP para controle de tempo + Canvas 2D para renderização.
- **3D Projection**: 
  - Cálculo de profundidade: `depth = position.z - cameraZ`.
  - Projeção 2D: `x = zoom * pos.x / depth`.
- **Sistemas de Partículas**:
  - `Stars`: 5000 pontos com ciclo de vida de nascimento em espiral e expansão elástica.
  - `Spiral Path`: Algoritmo baseado em `turns * sqrt(p)` para distribuição harmônica.
- **Easing**: Mix de `linear`, `power2` e `elasticOut` para simular aceleração física natural.

## 3. PADRÕES IDENTIFICADOS
- **P018: 3D-to-2D Perspective Projection**: Técnica matemática de converter um espaço tridimensional para um plano bidimensional sem o overhead de uma engine 3D completa.
- **P019: GSAP-Driven Canvas State Machine**: Uso do GSAP não para animar propriedades DOM, mas como um "clock" central que orquestra estados complexos recalculados a cada frame do Canvas.

## 4. VEREDITO CEO-EFFECTS
> [!IMPORTANT]
> **STATUS: APROVADO**
> 
> O efeito de "vórtice" é uma ferramenta narrativa poderosa. Ele cria um ponto focal no centro da tela que naturalmente guia o olhar do usuário para o CTA (ex: botão "Enter"). A transição de velocidade é o que separa este componente de simples backgrounds de partículas.

---

## 5. VEREDITO CEO-DESIGN
> [!IMPORTANT]
> **STATUS: APROVADO (NATIVE)**
> 
> Padrão Dark Editorial purista. A densidade de partículas (5000) cria uma textura visual rica que parece "fumaça digital" ou "nebulosa" dependendo da velocidade. Altamente recomendado para telas de abertura (Splash Screens) ou backgrounds de Hero minimalistas.

## 6. INSTRUÇÕES DE INSTALAÇÃO
1. Copiar `index.tsx` para `components/ui/spiral-animation.tsx`.
2. Instalar a dependência `gsap`.
3. O componente é responsivo e recalcula as dimensões do canvas via `ResizeObserver` (através de `dims` state).
