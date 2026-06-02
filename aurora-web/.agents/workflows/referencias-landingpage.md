---
description: Referências para a criação da Landing page Elysian
---


### 1. Design Tokens (Fundação Visual)

**A. Paleta de Cores (High-Key & Contraste)**
A estrutura de cores foca-se na eliminação de tons intermediários que possam comprometer a clareza, apostando num contraste extremo e sofisticado:
* **Fundo/Superfície Principal:** Branco Absoluto (`#FFFFFF`). Utilizado para garantir uma interface imaculada, maximizando a luz e evitando qualquer perceção de "ecrã sujo".
* **Elementos Primários e Texto:** Preto Piano (`#000000`). Aplicado em tipografia principal, bordas e ícones de interface para um contraste nítido e direto.
* **Cores de Destaque (Acentos Digitais):** * Ciano/Aqua (`#00FFEF`): Para indicadores de estado ativo, animações de interface (canvas/WebGL) e microinterações.
    * Vermelho (`#FF0000`): Para chamadas de atenção críticas ou pontos de foco secundários.

**B. Tipografia**
* **Família Principal:** LayGrotesk.
* **Hierarquia:**
    * *Display / Títulos (H1, H2):* Pesos maiores (Semibold), com entrelinha reduzida (110%) para blocos de texto coesos.
    * *Subtítulos (H3, H4):* Regular ou Medium, atuando como ponte entre os títulos de grande escala e o texto de apoio.
    * *Corpo do Texto (Body):* Regular, com entrelinha generosa (150%) para leitura fluida sobre o fundo Branco Absoluto.
    * *Micro-cópia / Legendas:* Letras maiúsculas, tamanho reduzido, com rastreio (tracking) aumentado para elegância e respiro.

**C. Espaçamento e Grid**
* **Sistema de Grid:** 12 colunas fluidas para desktop, reduzindo para 4 em mobile.
* **Escala de Espaçamento:** Baseada em múltiplos de 8px e 10px.
    * Uso de variáveis globais de macro-espaçamento (ex: `space-desktop: 50`, `space-mobile: 50`) para manter um respiro consistente entre secções (sections) e evitar o encapsulamento excessivo de componentes.

### 2. Componentes UI (Biblioteca Principal)

**A. Botões (Calls to Action)**
* **Primário:** Fundo em Preto Piano, texto em Branco Absoluto. Sem cantos arredondados (ou raio mínimo de 2px), conferindo um aspeto editorial e rigoroso.
* **Secundário (Outline):** Fundo transparente, borda de 1px em Preto Piano, texto em Preto Piano.
* **Hover States:** Inversão de cores rápida ou transição de preenchimento direcional utilizando o Ciano/Aqua como detalhe subtil.

**B. Navegação (Header & Menu)**
* **Header:** Fixo, fundo Branco Absoluto ou totalmente transparente, fundindo-se com a página. Logotipo à esquerda, itens de menu minimalistas à direita.
* **Menu Modal (Hambúrguer):** Ícone composto por linhas vetoriais simples em Preto Piano. Ao abrir, o modal ocupa todo o ecrã com fundo Branco Absoluto, tipografia em escala Display para os links e navegação simplificada.

**C. Ícones e Grafismos**
* **Estilo:** Minimalista, construído através de SVG inline. Linhas de espessura de 1px a 1.5px.
* **Padrões:** Uso de setas finas alongadas e matrizes de pequenos pontos geométricos para acompanhar a leitura ou indicar direções e processos tecnológicos.

### 3. Movimento e Interação (Comportamento)

* **Revelação na Rolagem (Scroll Reveal):** Máscaras que revelam os títulos e parágrafos de baixo para cima à medida que entram na janela de visualização (viewport).
* **Transições de Estado:** Mudanças de opacidade suaves (fade) para evitar saltos abruptos.
* **Sobreposições (Overlays):** Utilização cuidadosa de desfoque (blur) ou opacidade em modais para não perder a relação com a camada base da interface, mas mantendo a leitura impecável.

