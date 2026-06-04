# ANATOMY: Stack Feature Section (Staggered Orbital Rotation)
`ID: sections-stack-feature-001`

## 1. RESUMO EXECUTIVO
A **Stack Feature Section** é um componente de apresentação de "tech stack" que utiliza um layout de órbita concêntrica. A técnica chave é o deslocamento do centro das órbitas para fora do viewport visível (`translate-x-[50%]`), criando uma percepção de curvatura massiva. O componente utiliza animações CSS síncronas para manter os ícones em pé enquanto as órbitas giram.

## 2. ESPECIFICAÇÕES TÉCNICAS
- **Core**: React + CSS Keyframes.
- **Orbital Technique**:
  - Trigonometria Dinâmica: Posicionamento de elementos filhos via `cos()` e `sin()` aplicados a passos de ângulo uniformes.
  - Counter-Rotation: Uso de uma animação inversa (`spin-reverse`) nos ícones individuais para anular a rotação da órbita pai, mantendo os logotipos legíveis (orientação vertical constante).
  - Staggered Speeds: Cada nível de órbita possui uma duração de animação diferente (`12s`, `18s`, `24s`), eliminando a percepção de padrão rígido e criando um movimento orgânico pseudo-caótico.
- **Performance**: Extremamente eficiente, pois utiliza apenas transformações de rotação (`rotate`) que são aceleradas por hardware.

## 3. PADRÕES IDENTIFICADOS
- **P026: Multi-Orbit Geometric Rotation**: Uso de múltiplas camadas de rotação concêntrica com compensação de orientação (counter-rotation) para exibição de bibliotecas de ícones ou parceiros.

## 4. VEREDITO CEO-EFFECTS
> [!IMPORTANT]
> **STATUS: APROVADO**
> 
> A escolha de órbitas tracejadas (`border-dotted`) e o corte lateral criam uma sensação de "sala de controle" ou monitoramento sistêmico. A compensação de rotação nos ícones é o detalhe que separa uma implementação amadora de uma premium.

---

## 5. VEREDITO CEO-DESIGN
> [!IMPORTANT]
> **STATUS: APROVADO (NATIVE)**
> 
> Compatível com o padrão de seções de apresentação Aurora. Recomenda-se remover o `border-gray-200` externo e usar um `shadow-2xl` interno ou apenas o background preto absoluto para um visual mais integrado ao Dark Editorial.

## 6. INSTRUÇÕES DE INSTALAÇÃO
1. Copiar `index.tsx` para `components/ui/stack-feature-section.tsx`.
2. Instalar as dependências de ícones: `npm install react-icons`.
3. Certifique-se de ter o componente `Button` da shadcn configurado.
4. Uso: `<FeatureSection />`.
