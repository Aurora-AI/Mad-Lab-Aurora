# Build Constraints — OS-019R / Mad Lab Theme
**Gerado em:** 2026-06-08 22:35:31
**promotion_allowed:** false

---

## 1. GPU / Performance

### Budget de layers

| Qualidade | Max will-change layers | Parallax | Video Autoplay |
|---|---|---|---|
| low | 5 | False | False |
| medium | 12 | sutil | intersection_only |
| high | 20 | True | intersection_only |
| reduced_motion | 0 | False | False |

### Regras obrigatórias

- `will-change: transform` apenas nos elementos que serão animados no frame seguinte
- Remover `will-change` após animação via JS (`el.style.willChange = 'auto'`)
- Não usar `will-change: all`
- Testar em dispositivos de médio desempenho (não apenas high-end)
- `transform` (não `top/left`) para todas as animações de posição

---

## 2. Vídeo / Mídia

- **autoplay HTML**: `false` — nunca usar atributo `autoplay` diretamente
- **Mecanismo correto**: `IntersectionObserver` com threshold ≈ 0.3 → `video.play()`
- **Sempre**: `muted=true`, `loop=true`, `preload="none"` até threshold
- **Poster**: obrigatório como placeholder antes da carga
- **Máximo simultâneo**: 3 vídeos em playback simultâneo na viewport
- **Reduced motion**: `poster` estático apenas — não chamar `play()`
- **A11y**: vídeos sem narração dispensam track. Com narração: track obrigatório

---

## 3. Tipografia

- **Fonte primária**: **PROIBIDA** TWKLausanne (proprietária da Exo Ape)
  - Usar substituto aprovado com equivalência de contraste óptico
  - Fallback stack: `Helvetica Neue, Helvetica, Arial, sans-serif`
- **Times New Roman**: NOT_CANONICAL — nunca declarar em `font-family`
- **H1 desktop**: 250px, letter-spacing -11.5px (ratio -0.046), weight 400
- **H1 mobile**: 62.4px, letter-spacing -1.56px (ratio -0.025), weight 400
- **Fórmula de tracking**: `letter-spacing = font-size × tracking_ratio`
  - Desktop (> 768px): ratio = -0.046
  - Mobile (< 640px): ratio = -0.025
  - Abaixo de 40px: ratio = 0 a -0.01
- **line-height display**: `font-size × 0.904`
- **Não usar bold** em escala monumental (weight 400 é o padrão da referência)

---

## 4. Cores

- Paleta near-monocromática: `#0d0e13` (escuro) + `#ffffff` (branco)
- Escala de opacidade: sufixos -02/-04/-06/-08
- `#e0ccbb` (bege editorial) — **apenas texto grande** (> 18px bold). Falha WCAG em body
- `#e4e0db` (light grey) — decorativo apenas, nunca texto
- Modo escuro: `--color-story #070707` para seções editoriais escuras
- Nunca adicionar cor saturada sem revisar o sistema completo

---

## 5. Z-Index

| Camada | Z-Index | Uso |
|---|---|---|
| Base interativo | 1 | elementos clicáveis padrão |
| Conteúdo elevado | 2 | cards, hover states |
| Navegação | 9 | nav fixa |
| Menu trigger | 14 | botão de menu (acima da nav) |
| Overlay / Modal | 20 | overlays de tela cheia |

- Máximo de 5 camadas declaradas
- Nunca declarar z-index > 20 sem justificativa de modal/overlay crítico

---

## 6. Responsive

- Desktop breakpoint principal: 1440px
- Mobile breakpoint: 390px
- H1 escala 4:1 entre desktop e mobile (250px → 62.4px)
- Nav height máxima: ~64px–80px
- Variação de layout deve ser testada em: 390, 768, 1024, 1440

---

## 7. Acessibilidade

- `useReducedMotion()` fail-closed — **contrato herdado da OS-019 M0**
  - Se `prefers-reduced-motion: reduce` → static poster, sem transforms animados
- `will-change` deve ser removido antes de animação em modo reduzido
- Imagens: `alt` obrigatório em todas as imagens de conteúdo
- Vídeos com narração: `<track>` obrigatório
- Focus states de teclado: obrigatórios (não testados na referência — implementar conforme WCAG 2.4.7)

---

## 8. Limites de similaridade visual

- Composição de hero: diferente da referência (texto diferente + mídia diferente)
- Grid de portfolio: proporções de cards distintas da grade da Exo Ape
- Footer: cor escura é permitida; grid e copy devem ser distintos
- Logo/marca: identidade exclusiva do Mad Lab Aurora

---

## 9. Código proibido nesta OS

```
SynthesizedPage.client.tsx
rendered_screenshot.png (como candidato)
promotion_metadata.json
PromotionApprovalRecord
Human Review Package
```

> Estes artefatos pertencem a OS futura de construção, não à OS-019R.
