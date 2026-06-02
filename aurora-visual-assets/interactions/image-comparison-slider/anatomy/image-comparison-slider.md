# ANATOMY: Image Comparison (Vanilla Slider)
`ID: interactions-image-comparison-002`

## 1. RESUMO EXECUTIVO
Uma implementação "Zero-Dep" do padrão de comparação de imagens, focada em performance bruta e simplicidade. Ao contrário da versão 001 (que usa Framer Motion), esta versão utiliza `React.useCallback` e `window event listeners` para gerenciar o estado do slider, mantendo a técnica de `clip-path: inset()` para renderização visual.

## 2. ESPECIFICAÇÕES TÉCNICAS
- **Core**: Vanilla React (Hooks).
- **Event Orchestration**:
  - `handleMove`: Calcula a porcentagem baseada no `getBoundingClientRect()` do container.
  - `Global Listeners`: O uso de um listener global no `window` para `mouseup` garante que o arrasto seja interrompido mesmo se o cursor sair da viewport ou do container.
- **Visual**:
  - Utiliza `z-index` manual para separar as camadas (Top: z-10, Handle: z-20).
  - `clip-path: inset()` idêntico ao padrão P027, garantindo consistência visual na biblioteca.

## 3. PADRÕES IDENTIFICADOS
- **P027: Dual Clip-Path Synchronization** (Consolidado).
- **P028: Global Event Capture**: Técnica de delegar eventos de finalização de gestos (Up/End) ao objeto global para evitar estados de "clique fantasma".

## 4. VEREDITO CEO-EFFECTS
> [!IMPORTANT]
> **STATUS: APROVADO**
> 
> Excelente para casos onde o bundle size é crítico ou onde se deseja controle total sobre o ciclo de re-renderização sem a sobrecarga de uma biblioteca de animação.

---

## 5. VEREDITO CEO-DESIGN
> [!IMPORTANT]
> **STATUS: APROVADO (NATIVE)**
> 
> O design do handle com SVG puro é limpo e funcional. Ideal para documentações técnicas ou interfaces administrativas que requerem leveza.

## 6. INSTRUÇÕES DE INSTALAÇÃO
1. Copiar `index.tsx` para `components/ui/image-comparison-slider.tsx`.
2. Não requer dependências externas além do React.
3. Uso:
\`\`\`tsx
<ImageComparison 
  beforeImage="..." 
  afterImage="..." 
/>
\`\`\`
