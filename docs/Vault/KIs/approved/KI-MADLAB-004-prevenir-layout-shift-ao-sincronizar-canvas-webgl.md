---
title: "Prevenir layout shift ao sincronizar Canvas WebGL"
domain: "webgl-effects"
evidence_type: "Relatório de performance na OS-MADLAB-VISUAL-QUALITY-GATES"
applicable_to: ["ceo-effects", "taste-design", "site-builder"]
ki_id: "KI-MADLAB-004"
approved_at: "2026-05-30"
approved_by: "antigravity-ki-pipeline"
status: "approved"
---

# KI-MADLAB-004 — Prevenir layout shift ao sincronizar Canvas WebGL

## O Aprendizado
O Canvas WebGL deve ser inicializado com `alpha: true` e tamanho de container CSS fixo antes do primeiro frame de renderização ser desenhado para evitar layout shift e flickering visíveis.

## Por Que Isso É Um KI
Muitos geradores de código criam o Canvas sem dimensões explícitas no HTML inicial, calculando o tamanho via JavaScript após o carregamento. Isso gera um shift de layout que degrada a experiência Dark Editorial.

## Aplicação Prática
```css
/* Container com tamanho fixo garantido na renderização inicial */
.webgl-container {
  width: 100vw;
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
  overflow: hidden;
  background-color: #0b0b0b;
}
```

```javascript
// Renderer inicializado com opções de suavização e fundo transparente
const renderer = new THREE.WebGLRenderer({
  canvas: document.querySelector('#webgl-canvas'),
  alpha: true,
  antialias: true,
  powerPreference: "high-performance"
});
```

## Evidência de Origem
- `docs/Vault/OS-Evidence/OS-MADLAB-VISUAL-QUALITY-GATES-20260527-002.md`
- Benchmark de carregamento no preloader da Caixa Preta AI
