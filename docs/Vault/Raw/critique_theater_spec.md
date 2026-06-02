# CRITIQUE THEATER: ESPECIFICAÇÃO (AURORA SSOT)

Este documento formaliza o sistema de auditoria estética de 5 dimensões utilizado no MadLab Aurora para garantir que nenhum design "genérico" chegue à produção.

## 1. As 5 Dimensões de Auditoria

### A. Philosophy Consistency (Consistência Filosófica)
*   **Pergunta**: O artefato segue uma direção clara (Monocle, WIRED, Kinfolk) ou é uma colcha de retalhos?
*   **Check**: Vocabulário de design (chrome, spacing, accent) consistente em todas as páginas.

### B. Visual Hierarchy (Hierarquia Visual)
*   **Pergunta**: Um estranho sabe o que ler em 1º, 2º e 3º lugar sem esforço?
*   **Check**: Contraste de escala tipográfica, uso correto de pesos e fluxos de leitura (Z-Pattern / L-Pattern).

### C. Detail Execution (Execução de Detalhes)
*   **Pergunta**: Existe polimento nos "últimos 10%" (alinhamento, leading, kerning, grids)?
*   **Check**: Alinhamento de colunas em grids complexos, ausência de órfãos tipográficos, proporção de imagens.

### D. Functionality (Funcionalidade)
*   **Pergunta**: O design funciona para o uso pretendido (navegação, legibilidade, interações)?
*   **Check**: CTAs visíveis, acessibilidade de contraste, navegação por teclado/touch, legibilidade à distância.

### E. Innovation (Inovação)
*   **Pergunta**: O design empurra o limite ou é apenas o "mediano seguro"?
*   **Check**: Presença de um elemento inesperado (layout, motion, tipografia) que serve à tese central.

## 2. Escala de Pontuação (0-10)

| Range | Status | Descrição |
|-------|--------|-----------|
| **0–4** | *Broken* | Falha crítica; tape and string. Reconstrução necessária. |
| **5–6** | *Functional* | Competente, mas genérico ou com inconsistências visíveis. |
| **7–8** | *Strong* | Polido, profissional e com hierarquia clara. Padrão Aurora. |
| **9–10** | *Exceptional* | Grau de revista (Magazine-grade); inovação e execução perfeitas. |

## 3. Lógica de Feedback (Keep / Fix / Quick-wins)
Toda auditoria deve resultar em:
*   **Keep**: Elementos que estão funcionando e não devem ser tocados.
*   **Fix**: Problemas P0/P1 que são visualmente custosos e exigem tempo.
*   **Quick-wins**: Ajustes de 5-15 minutos com alto impacto (ex: trocar flex por grid).

## 4. O Radar Chart
A visualização oficial da auditoria é um gráfico de radar (SVG inline) que permite identificar instantaneamente quais eixos estão fracos. A "silhueta" da auditoria é a marca registrada da qualidade Aurora.
