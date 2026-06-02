# ANATOMY: Paper Shaders (Vertex & Fragment GLSL)
`ID: backgrounds-paper-shaders-001`

## 1. RESUMO EXECUTIVO
O **Paper Shaders** é um sistema de renderização 3D de baixo nível que utiliza WebGL (via R3F) para criar superfícies dinâmicas e fluidas. Através de shaders customizados, o componente deforma uma geometria de plano em tempo real e aplica padrões de ruído procedimental para simular energia ou fluxos orgânicos.

## 2. ESPECIFICAÇÕES TÉCNICAS
- **Vertex Shader (P030)**: Manipula a posição dos vértices no domínio do tempo e espaço, criando uma "ondulação" matemática que não depende de animações de transformação CSS.
- **Fragment Shader (P029)**: Calcula a cor de cada pixel baseado em uma função de ruído (Seno/Cosseno composta), permitindo gradientes complexos que evoluem sem repetição óbvia.
- **Side Buffer**: Usa `side: THREE.DoubleSide` para garantir que a geometria deformada seja visível de qualquer ângulo, essencial para planos que se dobram.

## 3. PADRÕES IDENTIFICADOS
- **P029: Custom GLSL Shader Material**: Injeção de lógica matemática pura para renderização de pixels.
- **P030: Geometry Deformation**: Manipulação direta de `attr.position` no vertex shader para criar movimento físico.

## 4. VEREDITO CEO-EFFECTS
> [!IMPORTANT]
> **STATUS: APROVADO**
> 
> O efeito de deformação é sutil o suficiente para não distrair, mas complexo o suficiente para transmitir alta tecnologia. A performance é superior ao uso de SVGs complexos para o mesmo efeito visual.

---

## 5. VEREDITO CEO-DESIGN
> [!IMPORTANT]
> **STATUS: APROVADO (NATIVE)**
> 
> Integrado perfeitamente ao DNA Aurora. Recomenda-se o uso de `color1` em tons escuros e `color2` com baixa saturação para manter o contraste Editorial.

## 6. INSTRUÇÕES DE INSTALAÇÃO
1. Copiar `index.tsx` para `components/ui/paper-shaders.tsx`.
2. Instalar dependências: `npm install three @react-three/fiber`.
3. Requer um `<Canvas>` wrapper para renderizar.
\`\`\`tsx
<Canvas>
  <ShaderPlane color1="#111" color2="#333" />
</Canvas>
\`\`\`
