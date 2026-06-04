# ANATOMY: Plasma Grid Shader (Bare-Metal WebGL)
`ID: backgrounds-plasma-grid-001`

## 1. RESUMO EXECUTIVO
Um background cinético de alta performance que utiliza WebGL puro para renderizar uma malha de "plasma" e "grid" dinâmico. Ao contrário das implementações que usam Three.js, esta versão interage diretamente com o contexto WebGL do browser, minimizando o overhead de abstração e garantindo renderização em 60fps constantes mesmo em dispositivos com hardware limitado.

## 2. ESPECIFICAÇÕES TÉCNICAS
- **WebGL Lifecycle**: Gerencia manualmente a compilação de shaders (`loadShader`), linkagem de programas (`initShaderProgram`) e o loop de renderização via `requestAnimationFrame`.
- **Coordinate Mapping**: Utiliza um sistema de coordenadas normalizado (`-1.0` a `1.0`) para cobrir todo o viewport e escala esses valores no Fragment Shader para criar o efeito de "grid infinito".
- **Shader Logic (P032)**:
  - Warp: Usa funções pseudo-aleatórias trigonométricas para distorcer as coordenadas UV.
  - Plasma: Renderiza 16 camadas de linhas (`linesPerGroup`) sincronizadas com o tempo (`iTime`).

## 3. PADRÕES IDENTIFICADOS
- **P031: Bare-Metal WebGL Integration**: Integração de baixo nível com o contexto WebGL sem bibliotecas de animação externas.
- **P032: Normalized Coordinate Warp**: Técnica de distorção de UVs baseada em tempo e posição para simular fluidez orgânica.

## 4. VEREDITO CEO-EFFECTS
> [!IMPORTANT]
> **STATUS: APROVADO**
> 
> O visual "Cyber-Grid" é um pilar do design Dark Editorial. A ausência de dependências externas torna este ativo extremamente valioso para aplicações que priorizam tempos de carregamento mínimos (LCP).

---

## 5. VEREDITO CEO-DESIGN
> [!IMPORTANT]
> **STATUS: APROVADO (NATIVE)**
> 
> Perfeito para seções Hero ou backgrounds globais. O controle de fading horizontal/vertical no shader evita bordas duras e facilita a leitura de conteúdo sobreposto.

## 6. INSTRUÇÕES DE INSTALAÇÃO
1. Copiar `index.tsx` para `components/ui/shader-background.tsx`.
2. Não requer dependências externas.
3. Uso:
\`\`\`tsx
<div className="relative w-full h-screen">
  <ShaderBackground className="absolute inset-0 -z-10" />
  <main>Conteúdo</main>
</div>
\`\`\`
