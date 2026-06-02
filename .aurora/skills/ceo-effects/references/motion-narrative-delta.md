# Motion Narrative Delta — Parâmetros Calibrados Aurora

**Versão:** 1.0.0  
**Skill:** ceo-effects  
**Status:** 🟢 Production  

> Parâmetros numéricos calibrados para o DNA Dark Editorial. Ponto de partida — não regra rígida.
> Atualizar quando a experiência real revelar o que estes números não anteciparam.

---

## Timing

```
Preloader total:         6.0s - 8.0s
  Fase 1 (escuridão):    0.0s - 1.5s
  Fase 2 (emergência):   1.5s - 3.5s
  Fase 3 (consciência):  3.5s - 5.5s
  Fase 4 (dissolução):   5.5s - 7.0s

Dissolução/emergência:   1.5s - 2.5s
Transição de página:     0.6s - 1.0s
Hover response:          0.15s - 0.25s
Scroll reveal:           0.8s - 1.2s
  Stagger por elemento:  80ms - 150ms
  Duration total:        400ms - 700ms

Silêncio antes do efeito: 0.8s MÍNIMO (regra absoluta)
```

---

## Easing com Gravidade

```
Entrada com peso:        power2.inOut / power3.inOut
                         cubic-bezier(0.4,0,0.2,1)

Saída natural:           power2.out
                         cubic-bezier(0.4,0,1,1)

Emergência de sombras:   power3.in → power1.out

Hero/página transition:  cubic-bezier(0.76, 0, 0.24, 1)
Section enter:           cubic-bezier(0.16, 1, 0.3, 1)

Mouse follow:            lerp 0.05 - 0.08 (suave, nunca snap)

EVITAR sem razão narrativa:
  bounce, elastic, back — comunicam leveza/brincadeira
  O Dark Editorial não é leve.
```

---

## Scroll

```
ScrollTrigger (GSAP):
  start: "top 85%"     — entrada quando 85% do topo entra
  end: "top 20%"       — saída quando topo atinge 20% da viewport
  scrub: false         — snap > scrub para elementos de conteúdo
  pin: false por default — usar pin apenas em seções de storytelling

Velocidade de scroll para efeitos:
  deltaY / dt = velocidade instantânea
  Decaimento: strength *= Math.exp(-dt * speed)
  Persistência após parada: 0.3s - 0.8s

Parallax (quando narrativamente justificado):
  5-8 camadas, não 2
  Velocidades: calculadas por função de profundidade f(z) = 1/(1+z)
  O mouse move a câmera — os objetos ficam onde estão
```

---

## Partículas

```
Desktop (sem GPU dedicada — Intel Iris Xe como baseline):
  Máximo: 2000 - 5000 partículas
  Alvo: 3000 com fps gate de 60fps

Mobile:
  Máximo: 200 - 500 partículas
  Alvo: 300

Comportamento:
  Física simulada > decorativo
  Força de atração/repulsão > movimento aleatório

Cor:
  Escuridão com temperatura — nunca branco puro (#FFFFFF)
  Tom: rgba(18, 18, 24, 0.8) no luminoso
  Tom: rgba(255, 255, 255, 0.6) no dark

Tamanho:
  0.5px - 3px (variação cria profundidade)
```

---

## Shaders

```
Fragment shader:
  Atmosfera e dissolução
  Efeito grain: valor float 0.02 - 0.06
  Vignette: sutil nas bordas, não centro
  Color grading: temperatura + contraste, não filtro

Vertex shader:
  Deformação de geometria com peso
  Amplitude máxima: 0.1 - 0.3 em coordenadas normalizadas

Noise:
  Simplex noise para movimento orgânico
  Perlin noise para texturas de superfície
  Velocidade: 0.001 - 0.005 por frame (lento é melhor)

GPU Budget (Intel Iris Xe):
  Fragment: máx 4 texturas simultâneas
  Vertex: máx 65k vértices por mesh sem instancing
  Draw calls: máx 50 por frame para 60fps estável
```

---

## Performance Gates (Aprovação)

```
60fps: OBRIGATÓRIO em dispositivo médio (Intel Iris Xe)
  Se não passa: remover o efeito, não simplificar

First contentful paint: < 3s antes do preloader iniciar
TTI (Time to Interactive): < 8s incluindo preloader

Bundle WebGL: < 500KB gzipped para Three.js r128
  Usar tree-shaking: import { Scene, PerspectiveCamera } from 'three'

prefers-reduced-motion:
  OBRIGATÓRIO em todo efeito
  Fallback: versão estática ou CSS simples
  Nunca desabilitar completamente a experiência
```

---

## Changelog

| Versão | Data | Mudança |
|---|---|---|
| 1.0.0 | 2026-05-30 | Criação — parâmetros extraídos do CEO-Effects SKILL.md e DNA v2.1.0 |
