# ANATOMY: Neon Button (Glimmer Edge)
`ID: borders-neon-button-001`

## 1. RESUMO EXECUTIVO
O **Neon Button** é um componente de interface que utiliza o padrão de "Glimmer Edge" para criar uma percepção de profundidade e brilho neon sem o uso de propriedades pesadas como `box-shadow` com grandes raios de difusão. A técnica baseia-se em camadas finas (1px) de gradientes posicionadas nas bordas superior e inferior, que são ativadas em estados de hover.

## 2. ESPECIFICAÇÕES TÉCNICAS
- **Core**: Tailwind CSS + CVA (Class Variance Authority).
- **Glimmer Technique**:
  - Camadas `absolute inset-x-0 h-px`.
  - Gradiente `bg-gradient-to-r from-transparent via-blue-500 to-transparent`.
- **Performance**: Extremamente leve. Utiliza apenas propriedades de renderização rápida (opacidade, transformações simples).
- **Consistência**: Implementado com `rounded-full` para se alinhar ao padrão de botões premium da Aurora.

## 3. PADRÕES IDENTIFICADOS
- **P022: Gradient Border Glimmer**: Uso de linhas de 1px com gradientes centralizados para simular brilho localizado em arestas de componentes (Edge Glow).

## 4. VEREDITO CEO-EFFECTS
> [!IMPORTANT]
> **STATUS: APROVADO**
> 
> O efeito é sutil e elegante. O fato de o brilho superior aparecer apenas no hover enquanto o inferior permanece como uma base de luz constante (baixa opacidade) cria uma hierarquia tátil excelente.

---

## 5. VEREDITO CEO-DESIGN
> [!IMPORTANT]
> **STATUS: APROVADO (NATIVE)**
> 
> Compatível 100% com o DNA Dark Editorial. Recomenda-se o uso com a variante `default` (bg-blue-500/5) para manter a transparência e sofisticação. A variante `solid` deve ser reservada apenas para CTAs primários de alta conversão.

## 6. INSTRUÇÕES DE INSTALAÇÃO
1. Copiar `index.tsx` para `components/ui/neon-button.tsx`.
2. Instalar `class-variance-authority`.
3. Certifique-se de que o utilitário `cn` (Tailwind Merge + Clsx) está disponível no seu projeto.
