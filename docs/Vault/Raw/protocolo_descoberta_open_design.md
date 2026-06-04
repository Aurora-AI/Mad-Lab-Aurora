# PROTOCOLO DE DESCOBERTA: OPEN-DESIGN (AURORA SSOT)

Este documento define o padrão de ouro para o "Turn-1 Discovery" dentro do ecossistema MadLab Aurora, baseado na lógica industrial do `open-design`.

## 1. As 8 Dimensões de Decisão
Antes de gerar qualquer layout, o agente deve resolver estas 8 dimensões ortogonais.

| # | Dimensão | Chave | Descrição |
|---|-----------|-----|-----------|
| 1 | Color Palette | `palette` | Define o esquema de cores base (Background, Surface, Text). |
| 2 | Accent Color | `accent` | A cor de destaque para CTAs e elementos interativos. |
| 3 | Body Typography | `typography` | Fonte principal para leitura de corpo de texto. |
| 4 | Display Typography | `display` | Fonte de impacto para headlines e displays. |
| 5 | Layout Model | `layout` | Estrutura de grid (Single-column, Two-column, Asymmetric). |
| 6 | Mood | `mood` | O tom emocional (Minimal, Playful, Brutalist, Editorial). |
| 7 | Density | `density` | Espaçamento e "respiro" (Compact, Balanced, Spacious). |
| 8 | Constraints | `exclude` | Elementos proibidos (Gradients, Animations, Stock Photos). |

## 2. Protocolo de Questionário (8 Grupos)
O agente deve coletar informações nestes grupos sequenciais para preencher o `inputs.json`.

1. **Identidade de Marca**: Nome, Mark (glifo único como Ø, ▲, ★), Tagline e Descrição.
2. **Metadados Operacionais**: Licença, Versão, Ano, URL primária e E-mail de contato.
3. **Navegação**: Até 5 links principais com badges opcionais de contagem.
4. **Hero & Prova**: Headline (MixedText: sans+italic+dot), Lead, CTAs e métricas iniciais (stats).
5. **Manifesto & Proposta**: Texto de manifesto e 4 cards de "Capabilities".
6. **Produto & Metodologia**: 5 cards de "Labs" (pills de filtro) e 4 passos de "Method".
7. **Social Proof**: 2 cards de "Selected Work" e 1 Testemunho central com glifos de parceiros.
8. **Fechamento**: CTA final, 4 colunas de links de rodapé e o "Mega Kicker".

## 3. Mapeamento de Linguagem Natural (Conversão I-Lang)

| Frase do Usuário | Dimensão | Valor Sugerido |
|------------------|-----------|----------------|
| "Dark mode", "Preto e branco" | palette | `monochrome_dark` |
| "Minimalista", "Limpo" | mood | `professional_minimal` |
| "Editorial", "Revista" | mood | `editorial` |
| "Espaçoso", "Muito respiro" | density | `spacious` |
| "Sem animações", "Estático" | exclude | `animations` |
| "Grid assimétrico" | layout | `asymmetric` |

## 4. Resolução de Tokens Padrão (Fallback)
Se o usuário não especificar, aplique o conjunto neutro:
* `palette=light_clean`
* `accent=electric_blue`
* `typography=inter`
* `display=same_as_body`
* `layout=single_column`
* `mood=professional_minimal`
* `density=balanced`
* `exclude=none`
