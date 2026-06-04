# ANATOMY: Background Paths
`ID: backgrounds-paths-001`

## 1. RESUMO EXECUTIVO
O **Background Paths** é um componente de ambientação que utiliza 36 caminhos SVG animados para criar um fluxo visual hipnótico e tecnológico. O componente combina animações de `pathOffset` com tipografia staggering (efeito spring letra-a-letra), resultando em uma experiência de Hero Section imersiva e de alta percepção de valor.

## 2. ESPECIFICAÇÕES TÉCNICAS
- **Core**: Next.js + Framer Motion.
- **Background**: SVG dinâmico gerado via loop matemático (36 caminhos).
- **Animações**: 
  - `pathLength` e `pathOffset` para o fluxo dos caminhos.
  - `spring` staggered para a entrada da tipografia.
- **Estilo**: `bg-clip-text` com gradientes neutros + Glassmorphism no CTA.

## 3. PADRÕES IDENTIFICADOS
- **P014: Dynamic SVG Flow**: Técnica de animar o deslocamento de um caminho SVG (`pathOffset`) em loop infinito para simular fluxo de energia ou dados.
- **P015: Spring-Staggered Typography**: Orquestração de caracteres individuais com física de mola para criar entradas de texto não-lineares e fluidas.

## 4. VEREDITO CEO-EFFECTS
> [!IMPORTANT]
> **STATUS: APROVADO**
> 
> O movimento linear e lento dos paths no fundo cria a "vibe" certa — sofisticada e constante. A randomização na duração de cada path (`20s + random`) evita o reconhecimento de padrões repetitivos, mantendo o fundo orgânico.

---

## 5. VEREDITO CEO-DESIGN
> [!IMPORTANT]
> **STATUS: APROVADO (NATIVE)**
> 
> Design estruturalmente resiliente. A escala do SVG se adapta bem ao viewport via `viewBox`. A tipografia em `bg-clip-text` reforça o pilar de "DesignEditorial" da Aurora, mantendo legibilidade mesmo sobre os paths em movimento.

## 6. INSTRUÇÕES DE INSTALAÇÃO
1. Copiar `index.tsx` para `components/ui/background-paths.tsx`.
2. Certificar-se que `framer-motion`, `@radix-ui/react-slot` e `class-variance-authority` estão instalados.
3. O componente é ideal para ser usado como base de `Hero Sections` ou `Landing Pages` imersivas.
