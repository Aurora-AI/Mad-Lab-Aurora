# Motion Grammar Summary — OS-019R
**Gerado em:** 2026-06-08 22:35:31
**Fonte:** M4 Runtime Extraction (Playwright + IO Spy)
**Confiança:** Alta para estrutura / Média para timing curves (JS-driven não escaneável)

---

## Princípio de Motion

A Exo Ape usa motion como **campo físico**, não como decoração. Toda a página é um
ambiente de camadas compostas que respondem ao input do usuário com latência mínima.

---

## IntersectionObserver — CONFIRMADO

```
Instâncias: 1
Eventos capturados: 21
Uso primário: revelar elementos + acionar video play() via JS callback
Mecanismo: window.IntersectionObserver wrapper confirmado por spy injection
```

---

## Padrões de Motion

### MP-MOT-001: Viewport Reveal
**Trigger:** IntersectionObserver threshold
**Efeito:** elemento entra na viewport — dispara opacity/transform de entrada
**Timing:** 0.5s ease (único timing confirmado em M4)
**Reduced motion:** static — sem animação de entrada

### MP-MOT-002: Nav Theme Transition
**Trigger:** mudança de seção / scroll
**Efeito:** nav alterna entre .is-light e .is-dark
**Timing:** 0.5s ease
**Reduced motion:** não especificado

### MP-MOT-003: Menu Overlay Open/Close
**Trigger:** click .menu-button (z:14)
**Efeito:** nav overlay aparece/desaparece
**Timing:** 0.5s ease estimado
**Reduced motion:** não especificado

### MP-MOT-004: Editorial Media Loop
**Trigger:** IO threshold — play() via JS
**Efeito:** vídeo começa loop silencioso
**Timing:** —
**Reduced motion:** poster apenas


---

## GPU Architecture

```
will-change: transform
Elementos na referência: 68
Mad Lab budget:
  low:    5 layers
  medium: 12 layers
  high:   20 layers
  reduced_motion: 0 layers
```

**Regra crítica**: remover `will-change` após animação.

---

## CSS Transitions confirmadas

| Duration | Timing | Property |
|---|---|---|
| 0.5s | ease | opacity |

**Nota**: A maioria do motion é JS-driven (rAF, IO). CSS transitions detectadas são o
mínimo — o sistema visual real usa JavaScript para a maior parte dos comportamentos.

---

## H1 Transform em Repouso

```
matrix(1, 0, 0, 1, -20, 0) = translateX(-20px)
```

Indica entrada de H1 com offset inicial de -20px → 0 ao revelar.
Este é o estado congelado no meio da animação de reveal.

---

## Reduced Motion — Contrato Mad Lab

```
Regra: useReducedMotion() fail-closed (herdada da OS-019 M0)
CSS detectado na referência: Não detectado — possível CSS-in-JS
Mad Lab: OBRIGATÓRIO implementar mesmo que a referência não implemente
```

Implementação mínima obrigatória:
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Arquivos de referência

```
motion_grammar.json             — primitivos e roles
scroll_behavior.json            — snapshots de scroll
timing_curves.json              — curvas confirmadas
media_runtime_behavior.json     — autoplay analysis
motion_pattern_map.json         — padrões com timing
gpu_layer_strategy.json         — budget por qualidade
reduced_motion_observations.json — CSS analysis
```
