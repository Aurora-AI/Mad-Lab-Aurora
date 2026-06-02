# WebGL Scroll Sync — Anatomy

**Asset ID:** webgl-scroll-sync-001
**Categoria:** effects/scroll-sync
**Origem:** externa — Lusion Ltd (Bristol, UK)
**Fonte:** github.com/lusionltd/WebGL-Scroll-Sync
**Licença:** MIT
**Stack:** Three.js + WebGL + Vanilla JS
**Ingerido em:** 2026-04-18
**OS:** OS-ANTIGRAVITY-AURORA-VISUAL-ASSETS-20260418-010

---

## Conceito

*"O canvas que acompanha a página em vez de fingir que está fixo."*

Resolve o problema estrutural de sincronizar WebGL com scroll nativo
sem scroll-jacking — usando `position: absolute` e offset compensatório
a cada rAF em vez da convenção `position: fixed`.

---

## O Problema Resolvido

Canvas `position: fixed` + scroll nativo = drift.

O scroll acontece no thread do browser. rAF acontece no thread de
rendering. Quando o scroll dispara entre dois frames, o canvas não
tem a posição nova a tempo — objetos 3D descolam dos elementos DOM.

A solução padrão da indústria era scroll-jacking. Lusion encontrou
outra saída: deixar o canvas rolar com a página fisicamente,
e compensar via transform a cada frame.

---

## Pipeline de Rendering

```
JavaScript (a cada rAF):
  1. scrollDelta → updateStrength() → exponential decay
  2. scrollOffset.set(scrollX, scrollY - padding)
  3. canvas.style.transform = translate(scrollOffset) ← P046
  4. Para cada item DOM:
     a. getBoundingClientRect() + scrollOffset → u_domXY ← P048
     b. frustum check → mesh.visible ← P052
     c. u_rands atualizado estocásticamente
  5. renderer.render()

Vertex Shader (por vertex):
  1. u_domXY - u_scrollOffset + u_domWH * 0.5 → centro em pixel space
  2. Inverter eixo Y (DOM vs WebGL)
  3. position.xy * u_domWH → escalar para tamanho DOM
  4. / u_resolution * 2 - 1 → NDC ← P049
  5. Passar UV

Fragment Shader (por pixel):
  1. hash43() → noise para glitch UVs ← P050
  2. uvOffset proporcional a u_strength
  3. 5 amostras acumuladas (motion blur)
  4. Normalizar + brighten com strength
```

---

## Padrões (P046–P052)

### P046 — Absolute Canvas Scroll Sync
Canvas `position: absolute` que rola com a página.
A cada rAF: `canvas.style.transform = translate(scrollX, scrollY)`.
Zero drift porque canvas e DOM estão no mesmo fluxo de scroll.

### P047 — Vertical Canvas Padding Buffer
`canvasHeight = viewportHeight * (1 + padding * 2)` com padding = 0.25.
Renderiza 25% extra top + bottom para absorver clipping em scroll rápido.
Custo: ~50% mais pixels no eixo vertical. Aceitável na maioria dos casos.

### P048 — Single Canvas Multi-DOM Anchoring
`getBoundingClientRect()` + `scrollOffset` = posição absoluta no documento.
Um único canvas, múltiplos elementos DOM ancorados com precisão de pixel.
Resolve o limite de contextos WebGL por página.

### P049 — DOM-to-NDC Vertex Mapping
Vertex shader converte pixel coordinates para NDC sem JavaScript de posicionamento.
PlaneGeometry genérica (1×1) se posiciona e escala sobre qualquer DOM element.
A matemática: `(pixelXY / resolution) * 2 - 1`.

### P050 — Scroll-Driven Glitch Shader
Distorção proporcional à velocidade do scroll via hash noise estocástico.
5 amostras acumuladas = motion blur direcional.
Brightness aumenta com `u_strength` — imagem clareia em scroll rápido.
Hash: Dave_Hoskins hash43 (shadertoy.com/view/4djSRW).

### P051 — Scroll Strength Decay
`strength *= Math.exp(-dt * 10)` — decaimento exponencial físico.
`strength += Math.min(targetStrength, 5)` — cap para evitar overflow.
Resultado: força sobe instantaneamente com scroll, decai naturalmente.

### P052 — Frustum Culling Manual
`mesh.visible = item.y < canvasBottom && item.y + item.height > canvasTop`
Meshes fora do viewport têm `visible = false` — zero custo de render.
Crítico para páginas longas com muitos elementos WebGL.

---

## Performance Budget

| Métrica | Valor |
|---|---|
| Drawcalls | 1 por elemento visível |
| Geometria | PlaneGeometry 1×1 compartilhada |
| Fragment samples | 5 por pixel (motion blur) |
| Canvas overhead | ~50% extra pixels (padding) |
| GPU frame time estimado | 2–4ms mid-range |
| Otimização | Frustum culling manual (P052) |

---

## Fallback Chain

| Ambiente | Comportamento |
|---|---|
| WebGL disponível | Experiência completa com glitch shader |
| WebGL indisponível | `<noscript>` com `<img>` estático |
| Reduce motion | ⚠️ Não implementado — adicionar antes de produção |

---

## Limitações Conhecidas

1. **Sem `prefers-reduced-motion`** — o glitch shader ativa em scroll
   rápido independente da preferência do usuário. Adicionar check antes
   de qualquer uso em produção.

2. **5 samples no fragment shader** — monitorar frame budget em
   dispositivos mobile low-end. Reduzir `NUM_SAMPLES` para 3 se necessário.

3. **Padding buffer fixo em 25%** — pode ser insuficiente em scroll
   muito rápido em telas longas. Configurável via `padding` em `onResize()`.

4. **Sem React/framework wrapper** — vanilla JS puro. Para uso em
   aurora-web (React 19), criar wrapper que inicializa/destrói no
   ciclo de vida do componente.

---

## Como Usar na Aurora

### Uso básico (vanilla)
```javascript
// 1. HTML: canvas dentro de wrapper
// <div id="wrapper"> <canvas id="canvas"></canvas> <div class="image">...</div> </div>

// 2. CSS obrigatório:
// #wrapper { position: relative }
// #canvas { position: absolute; z-index: -1 }  ← NÃO fixed

// 3. Instanciar e iniciar
import { init } from '@aurora-visual/webgl-scroll-sync'
requestAnimationFrame(init)  // aguardar um frame para CSS estar pronto
```

### Combinação recomendada para profundidade impossível
```javascript
// Substituir img.frag por shader de depth map (ver P001)
// Manter toda a arquitetura de canvas sync (P046–P049)
// Resultado: profundidade WebGL ancorada a elementos DOM com scroll nativo
```

---

## VEREDITO CEO-EFFECTS

**APROVADO COM RESSALVAS**

Intenção articulável: *"Imagens que habitam o DOM como matéria física —
e revelam seu peso quando você rola rápido."*

O glitch shader (P050) é feedback físico real — não decoração.
A distorção proporcional à velocidade comunica que você está
literalmente rasgando o espaço ao rolar.

Ressalva 1: `prefers-reduced-motion` ausente — obrigatório antes de produção.
Ressalva 2: 5 fragment samples — monitorar em mobile low-end.

---

## VEREDITO CEO-DESIGN

**APROVADO — infraestrutura**

Ativo sem identidade visual própria. É cola técnica que habilita
outros ativos a habitarem o DOM com precisão.

O Teste 7 (DNA Mad Lab Aurora) se aplica aos ativos que usam
este sistema como base — não ao sistema em si.

CSS do demo original (identidade Lusion) foi removido na ingestão.

---

## Relevância Estratégica para Aurora

Este ativo resolve o elo que faltava na Fase 2.

A biblioteca tinha P001–P005 (depth map, WebGPU) e P006–P045
(GSAP, scroll narrativo). Nenhum resolvia:
*"Como ancorar um efeito WebGL a um elemento DOM específico
com scroll nativo, sem drift e sem scroll-jacking?"*

P046–P052 respondem isso.

Com esta base, qualquer efeito de profundidade impossível da biblioteca
pode ser ancorado a qualquer elemento DOM — hero, card, seção, título —
com precisão de pixel, scroll nativo, e zero jank.

**É a cola entre a profundidade impossível e o DOM.**
