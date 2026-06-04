# ANATOMY: Cinematic Motion Footer (Volvox)
`ID: interactions-motion-footer-001`

## 1. RESUMO EXECUTIVO
O **Cinematic Motion Footer** transforma o encerramento da página em um momento de revelação cinematográfica. Utilizando a técnica de `Curtain Reveal` (revelação por cortina) via GSAP ScrollTrigger, o rodapé parece estar sempre lá, mas só é descoberto quando o conteúdo principal "sobe" para fora do viewport.

## 2. ESPECIFICAÇÕES TÉCNICAS
- **Core**: React + GSAP + ScrollTrigger.
- **Interação**: `MagneticButton` (Inércia rítmica).
- **Estilo**: Inline CSS (Standard shadcn tokens) + OKLCH color mixing.
- **Efeitos**: 
  - `Aurora Breathe`: Radial gradient animado.
  - `Metallic Text Glow`: Efeito de stroke e brilho metálico.
  - `Diagonal Marquee`: Movimento contínuo em -2 graus.

## 3. PADRÕES IDENTIFICADOS
- **P006: GSAP Curtain Reveal**: Uso de `clip-path` e `fixed positioning` para criar a ilusão de profundidade vertical.
- **P007: Magnetic Interaction Primitive**: Lógica de atração baseada no cursor para elementos de UI.

## 4. VEREDITO CEO-EFFECTS
> [!IMPORTANT]
> **STATUS: APROVADO**
> 
> A física aplicada ao `MagneticButton` é impecável — a transição entre a atração e o retorno elástico (`elastic.out`) cria uma satisfação táctil rara na web. O uso do `Marquee` diagonal quebra a rigidez horizontal do layout, injetando uma "energia residual" de movimento. O silêncio é preservado pela baixa opacidade dos elementos de fundo (grid 3% foreground).

---

## 5. VEREDITO CEO-DESIGN
> [!IMPORTANT]
> **STATUS: RESISTENTE**
> 
> Estruturalmente, o componente é uma fortaleza. A abstração do `MagneticButton` como um componente interno prova maturidade arquitetural. A hierarquia visual é clara: o texto gigante "SOBERS" serve como âncora visual, enquanto as "Glass Pills" organizam a navegação.
> 
> **Nota de Stress**: O componente não quebra em viewports pequenos devido ao switch de layout do `Bottom Bar` (md:flex-row). O alinhamento com o DNA Dark Editorial é de 100%.

## 6. INSTRUÇÕES DE INSTALAÇÃO
1. Copiar `index.tsx` para `components/ui/motion-footer.tsx`.
2. Adicionar `gsap` ao `package.json`.
3. Adicionar configuração de fonte `Plus Jakarta Sans`.
