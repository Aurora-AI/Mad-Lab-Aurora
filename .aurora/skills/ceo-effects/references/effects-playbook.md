# Effects Playbook — Aurora Dark Editorial

**Versão:** 1.0.0  
**Skill:** ceo-effects  
**Status:** 🟢 Production  

> Biblioteca de efeitos aprovados, técnicas validadas e padrões de implementação para o domínio Dark Editorial.

---

## O Caso Âncora — Preloader da Mulher Puzzle

Este é o benchmark de intenção máxima para efeitos Aurora:

```
FASE 1 — ESCURIDÃO (0.0s - 1.5s)
  Tela completamente preta.
  Silêncio visual total como intenção — não como loading.

FASE 2 — EMERGÊNCIA (1.5s - 3.5s)
  Figura feminina emerge das sombras por fragmentos.
  Acumulação progressiva. A forma existe antes de ser reconhecida.

FASE 3 — CONSCIÊNCIA (3.5s - 5.5s)
  Ela está presente e percebe que você está ali.
  Follow do mouse — lerp 0.05-0.08, nunca snap.

FASE 4 — DISSOLUÇÃO (5.5s - 7.0s)
  Ela se dissolve como névoa que o vento leva.
  No espaço: a primeira palavra do manifesto.

FASE 5 — A PÁGINA (7.0s+)
  Hero section com o mesmo peso do preloader.
```

**Stack:** Three.js r128 + R3F + GSAP + Raycasting para mouse follow  
**Fallback:** CSS puro para `prefers-reduced-motion`

---

## Efeitos Aprovados por Categoria

### Scroll Reveals
- Stagger 80-150ms entre elementos de peso diferente
- Duration: 400-700ms
- Entrada: `cubic-bezier(0.4,0,0.2,1)` (power2.inOut)
- Saída: `cubic-bezier(0.4,0,1,1)` (power2.out)
- Decorativos animam DEPOIS do conteúdo

### Transições de Página
- Duration: 0.6s - 1.0s
- Easing: `power2.inOut`
- Proibido: fade to black sem narrativa

### Mouse Follow / Parallax Real
- Lerp: 0.05 - 0.08 (suave, nunca snap)
- 5-8 camadas com física de câmera real
- O mouse move a câmera — os objetos ficam onde estão
- NUNCA parallax de 2 camadas (versão commodity)

### Hover States
- Response: 0.15s - 0.25s
- CTA inline: underline scaleX esquerda→direita
- CTA ghost: clip-path de dentro para fora
- Decorativos: pulse 2-4s em seções de tensão

### Partículas (quando usadas)
- Desktop: máx 2000-5000 partículas
- Mobile: máx 200-500 partículas
- Comportamento: física simulada > decorativo
- Cor: escuridão com temperatura, não branco puro

---

## Padrões WebGL Validados (P046-P052)

Ver: `../../../../docs/Vault/DESIGN_LIBRARY.md`

- **P046** — Absolute Canvas Scroll Sync: canvas com `position: absolute` + `transform: translate` compensatório
- **P047** — Vertical Canvas Padding Buffer: 25-50% extra para evitar clipping
- **P048** — Single Canvas Multi-DOM Anchoring: um canvas global, múltiplos objetos 3D
- **P049** — DOM-to-NDC Vertex Mapping: conversão no Vertex Shader
- **P050** — Scroll-Driven Glitch Shader: velocidade de scroll → uniform → noise estocástico
- **P051** — Scroll Strength Decay: `strength *= Math.exp(-dt * speed)` para inércia visual
- **P052** — Frustum Culling Manual: `mesh.visible = false` fora da viewport

---

## Stack Técnico Canônico

```
Three.js        r128 — VERSÃO FIXA — NÃO ATUALIZAR
                NÃO usar: THREE.CapsuleGeometry (disponível em r142+)
                Usar: CylinderGeometry, SphereGeometry

R3F             React Three Fiber
                Canvas, useFrame, useThree, useLoader

GSAP            + ScrollTrigger para animações de scroll
                + Timeline para sequências complexas
                + Ticker para sincronização com R3F loop

GLSL            Fragment shader: atmosfera, dissolução, cor, noise
                Vertex shader: deformação de geometria com peso
                Noise: perlin/simplex para movimento orgânico

CSS             Fallbacks e efeitos simples
                prefers-reduced-motion: OBRIGATÓRIO em todo efeito

PROIBIDO        CUDA, nvidia-*, torch
                Dependências GPU pesadas
                Bounce/elastic sem razão narrativa
                Parallax de 2 camadas
```

---

## Regra do Silêncio (0.8s)

Todo ativo Aurora-native tem estado de repouso mínimo de **0.8 segundos**
antes de qualquer animação (scroll, hover, tempo).

O visitante precisa sentir o peso do silêncio antes de sentir o peso do efeito.

---

## Calibração por Produto

| Produto | Tom | Efeitos Aprovados | Proibidos |
|---|---|---|---|
| Elysian.ai.br | Narrativo + preloader | Preloader da mulher, storytelling cinético | Parallax excessivo, partículas decorativas |
| Elysian Lex | Autoridade silenciosa | Scroll reveals pesados, transições precisas | Qualquer coisa que pareça startup |
| CRM / Silent Operator | Controle operacional | Micro-interações precisas, dados que surgem com propósito | Exuberância visual |
| Infoprodutos | Autoridade do fundador | Entrada de texto com peso, scroll com intenção | Template de curso online |
