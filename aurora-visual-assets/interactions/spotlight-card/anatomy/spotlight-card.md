# ANATOMY: Spotlight Card (Glow Hover)
`ID: interactions-spotlight-card-001`

## 1. RESUMO EXECUTIVO
O **Spotlight Card** é uma implementação sofisticada de "cursor tracking" que utiliza variáveis CSS globais e `background-attachment: fixed` para criar um efeito de iluminação que atravessa múltiplos cards de forma coordenada. A técnica utiliza máscaras complexas (`mask-composite`) para desenhar bordas iluminadas apenas na área sob o cursor.

## 2. ESPECIFICAÇÕES TÉCNICAS
- **Core**: Vanilla React + CSS Variables.
- **Spotlight Technique**:
  - `background-attachment: fixed`: Garante que o gradiente de luz permaneça fixo em relação ao viewport, permitindo que o movimento do mouse sincronize a iluminação entre diferentes cards.
  - `mask-composite: intersect`: Técnica avançada de recorte para desenhar apenas o "contorno" da borda sem preencher o conteúdo.
  - Dinamismo: O matiz (`--hue`) é calculado com base na posição percentual do cursor (`--xp`), criando mudanças sutis de cor conforme o usuário navega na página.
- **Performance**: Depende de `pointermove` no nível de documento. Recomenda-se debouncing ou throttling se o número de cards for massivo, embora o uso de variáveis CSS minimize o custo de re-renderização do React.

## 3. PADRÕES IDENTIFICADOS
- **P023: Fixed Coordinate Syncing**: Uso de coordenadas globais compartilhadas via variáveis CSS para sincronizar efeitos visuais entre múltiplos componentes independentes.
- **P024: Advanced CSS Mask Compositing**: Uso de `mask-clip` e `mask-composite` para renderizar bordas gradientes complexas com sub-pixel precision.

## 4. VEREDITO CEO-EFFECTS
> [!IMPORTANT]
> **STATUS: APROVADO**
> 
> O efeito de "luz contínua" entre cards adjacentes é um marcador clássico de design S-Tier. A integração de matiz dinâmico baseado na posição horizontal é um detalhe de polimento que eleva a percepção de interatividade.

---

## 5. VEREDITO CEO-DESIGN
> [!IMPORTANT]
> **STATUS: APROVADO (NATIVE)**
> 
> A tipografia interna deve ser mantida com contraste médio para não competir com o brilho da borda. Recomenda-se o uso de `backdrop-blur` elevado para reforçar a estética de "vidro fumê" característica da Aurora.

## 6. INSTRUÇÕES DE INSTALAÇÃO
1. Copiar `index.tsx` para `components/ui/spotlight-card.tsx`.
2. O componente utiliza variáveis CSS injetadas via tag `<style>`. Certifique-se de que o Tailwind está configurado para não purgar classes geradas dinamicamente se necessário (embora aqui as classes sejam estáticas).
3. Uso básico: `<GlowCard glowColor="purple">Conteúdo</GlowCard>`.
