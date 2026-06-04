# ANATOMY: Image Comparison (Clip-Path Slider)
`ID: interactions-image-comparison-001`

## 1. RESUMO EXECUTIVO
O **Image Comparison** é um componente interativo que permite comparar dois estados de uma imagem (ex: Antes/Depois, Dark/Light) usando um slider horizontal. A técnica central utiliza `clip-path: inset()` sincronizado via `MotionValue` do Framer Motion, garantindo que as duas imagens permaneçam perfeitamente alinhadas enquanto suas áreas visíveis são recortadas dinamicamente.

## 2. ESPECIFICAÇÕES TÉCNICAS
- **Core**: React + Motion (Framer Motion).
- **Clipping Technique**:
  - `inset(0 0 0 value%)`: Recorta a imagem da esquerda para a direita.
  - `inset(0 100-value% 0 0)`: Recorta a imagem da direita para a esquerda.
  - Sincronização: Ambas as imagens e o slider compartilham o mesmo `motionSliderPosition` via React Context, eliminando qualquer lag entre o movimento do cursor e o recorte visual.
- **Physics**: O uso de `useSpring` permite suavizar o movimento do slider se desejado, embora o padrão seja linear (`duration: 0`) para resposta imediata.

## 3. PADRÕES IDENTIFICADOS
- **P027: Dual Clip-Path Synchronization**: Uso de um único valor de estado para controlar dois recortes complementares (`clip-path`) em sobreposição perfeita.

## 4. VEREDITO CEO-EFFECTS
> [!IMPORTANT]
> **STATUS: APROVADO**
> 
> A implementação via `clip-path` é superior tecnicamente a abordagens baseadas em largura (`width: 0% to 100%`), pois evita problemas de redimensionamento da imagem interna. A resposta tátil é excelente.

---

## 5. VEREDITO CEO-DESIGN
> [!IMPORTANT]
> **STATUS: APROVADO (NATIVE)**
> 
> Compatível com o DNA Aurora para demonstração de "Before/After" de produtos. Recomenda-se o uso de uma borda sutil no slider central e um `backdrop-blur` no handle para reforçar o visual premium.

## 6. INSTRUÇÕES DE INSTALAÇÃO
1. Copiar `index.tsx` para `components/ui/image-comparison.tsx`.
2. Instalar a dependência: `npm install motion`.
3. Uso básico:
\`\`\`tsx
<ImageComparison>
  <ImageComparisonImage src="..." alt="..." position="left" />
  <ImageComparisonImage src="..." alt="..." position="right" />
  <ImageComparisonSlider className="bg-white" />
</ImageComparison>
\`\`\`
