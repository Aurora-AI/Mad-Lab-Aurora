# ANATOMY: Creative Team Marquee (Cnippet)
`ID: interactions-team-marquee-001`

## 1. RESUMO EXECUTIVO
A **Creative Team Section** utiliza um Marquee infinito para exibir membros da equipe, transformando uma seção estática em um fluxo contínuo de rostos e cargos. O efeito de transição grayscale-to-color no hover incentiva a exploração individual sem sobrecarregar o usuário.

## 2. ESPECIFICAÇÕES TÉCNICAS
- **Core**: Next.js + Tailwind (CSS Keyframes).
- **Interação**: `Marquee` (Infinite loop) + CSS Hover (Grayscale filter).
- **Estilo**: Tailwind utility classes + SVG Background paths.
- **Animações**: 
  - `marquee`: Deslocamento horizontal infinito.
  - `marquee-vertical`: Suporte para variantes verticais.

## 3. PADRÕES IDENTIFICADOS
- **P008: Seamless Card Marquee**: Técnica de duplicação de itens para criar loops infinitos sem interrupções visuais.
- **P009: SVG Masked Decorators**: Uso de paths SVG orgânicos com `clip-path` para quebrar a geometria retilínea de grids web.

## 4. VEREDITO CEO-EFFECTS
> [!IMPORTANT]
> **STATUS: APROVADO**
> 
> A intenção social é clara e bem executada. O marquee em velocidade controlada (`40s`) transmite atividade constante sem causar distração ou náusea. A transição de cor no hover é suave e serve como um feedback tátil visual de "conheça-me".

---

## 5. VEREDITO CEO-DESIGN
> [!IMPORTANT]
> **STATUS: RESISTENTE**
> 
> **MILSTONE**: Este ativo finaliza o corpus inicial de 3 ativos. O status do agente foi elevado para **NATIVE**.
> 
> Estruturalmente, o uso de `Image` do Next.js garante performance de carregamento (WebP/Lazy). A profundidade é dada pelos degradês laterais que escondem a entrada e saída dos cards, limpando a carga cognitiva. Alinhamento 100% com o padrão Dark Editorial (especialmente em modo dark).

## 6. INSTRUÇÕES DE INSTALAÇÃO
1. Copiar `index.tsx` para `components/ui/team-section.tsx`.
2. Adicionar os `@keyframes marquee` ao `index.css` global.
3. Instalar `lucide-react` para os ícones decorativos.
