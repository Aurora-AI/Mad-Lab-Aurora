# ANATOMY: Davincho Parallax Hero
`ID: heroes-davincho-001`

## 1. RESUMO EXECUTIVO
O **Davincho Hero** é um componente de impacto visual imediato que utiliza o scroll para orquestrar profundidade. Através de `framer-motion`, a imagem de fundo se move em uma velocidade diferente do conteúdo textual, enquanto a tipografia utiliza `mix-blend-difference` para garantir legibilidade editorial e contraste dinâmico sobre imagens em escala de cinza.

## 2. ESPECIFICAÇÕES TÉCNICAS
- **Core**: Next.js + Framer Motion (`motion/react`).
- **Interação**: `useScroll` + `useTransform` (Scroll-Driven Parallax).
- **Estilo**: `clip-path` (curtain masking) + `mix-blend-difference`.
- **Animações**: 
  - Transformação dinâmica do eixo Y baseada no progresso do scroll do container.
  - Otimização de renderização via aceleração de hardware (GPU transforms).

## 3. PADRÕES IDENTIFICADOS
- **P010: Scroll-Driven Transform Parallax**: Técnica de desacoplamento de camadas visuais para criar percepção de 3D simulado via scroll.
- **P011: Typography Mix-Blend Difference**: Uso de `mix-blend-difference` em tipografia branca sobre backgrounds variados para criar o "Aurora High-Contrast Editorial Look".

## 4. VEREDITO CEO-EFFECTS
> [!IMPORTANT]
> **STATUS: APROVADO**
> 
> A "calma" do parallax é o que o torna premium. Evitamos movimentos frenéticos para focar no "Statement" editorial. A combinação de `mix-blend-difference` com imagens em escala de cinza define perfeitamente a sobriedade Dark Editorial.

---

## 5. VEREDITO CEO-DESIGN
> [!IMPORTANT]
> **STATUS: APROVADO (NATIVE)**
> 
> **ESTADO NATIVE**: Este é o primeiro ativo ingerido sob supervisão nativa. A estrutura segue rigorosamente os princípios de hierarquia e stress estrutural da Aurora. O uso de `z-index` e `clip-path` demonstra uma arquitetura de camadas limpa e performante.

## 6. INSTRUÇÕES DE INSTALAÇÃO
1. Instalar dependências: `npm install framer-motion`.
2. Copiar `index.tsx` para `components/ui/hero-davincho.tsx`.
3. Ajustar o `clip-path` se o componente for usado dentro de layouts com wraps específicos.
