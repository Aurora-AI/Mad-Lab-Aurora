# ANATOMY: Falling Pattern (Infinite Gradient Rain)
`ID: backgrounds-falling-pattern-001`

## 1. RESUMO EXECUTIVO
O **Falling Pattern** é um componente de fundo cinético que simula uma "chuva" de elementos geométricos usando uma combinação massiva de `radial-gradient` empilhados. A animação é realizada via `background-position`, deslocando as coordenadas de início para coordenadas de fim de longa distância em um loop infinito, criando a ilusão de fluxo constante.

## 2. ESPECIFICAÇÕES TÉCNICAS
- **Core**: React + Framer Motion.
- **Kinetic Technique**:
  - `background-position` Animation: Diferente de transformar um elemento no eixo Y, o componente anima a posição das texturas de fundo. Isso permite que um único elemento `div` contenha dezenas de camadas de gradiente animadas simultaneamente.
  - Dot Matrix Overlay: Um overlay absoluto com `backdrop-filter` e um gradiente radial repetitivo cria uma matriz de pontos que "fragmenta" o fundo, gerando um efeito de profundidade digital / estética "grid".
- **Performance**: Executado via Framer Motion. Como anima propriedades de fundo (`background-position`), pode haver carga na GPU se o número de gradientes for excessivo em telas de altíssima resolução. Recomenda-se manter o `duration` alto para evitar "stuttering".

## 3. PADRÕES IDENTIFICADOS
- **P025: Infinite Coordinate Sliding**: Animação de `background-position` entre duas strings de coordenadas massivas para simular movimento infinito de texturas procedurais.

## 4. VEREDITO CEO-EFFECTS
> [!IMPORTANT]
> **STATUS: APROVADO**
> 
> A técnica de usar `radial-gradient` para desenhar "traços" de luz que caem é extremamente eficiente em termos de assets (zero imagens externas). O overlay de matriz de pontos é o que "vende" o efeito como algo editorial e tecnológico.

---

## 5. VEREDITO CEO-DESIGN
> [!IMPORTANT]
> **STATUS: APROVADO (NATIVE)**
> 
> A paleta padrão deve ser mantida em `var(--primary)` com baixa opacidade para não distrair do conteúdo principal. Perfeito para seções hero com pouco texto ou dashboards que precisam de "vida" sistêmica lenta e constante.

## 6. INSTRUÇÕES DE INSTALAÇÃO
1. Copiar `index.tsx` para `components/ui/falling-pattern.tsx`.
2. Certifique-se de que o Framer Motion está instalado.
3. Uso básico: `<FallingPattern color="rgba(59, 130, 246, 0.5)" />`.
