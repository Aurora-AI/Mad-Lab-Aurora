# Human Classification — Fallow Consulting Trial

## Critérios

- TP — True Positive: achado real e corrigível.
- FP — False Positive: achado incorreto.
- WONTFIX: achado real, mas intencional.
- OUT_OF_SCOPE: fora do escopo do trial.
- TOOL_GAP: limitação da ferramenta ou incompatibilidade com o workspace.
- HIGH_VALUE: achado que evitaria bug, dívida técnica ou acoplamento relevante.

## Amostra classificada

| ID | Comando | Arquivo/Área | Tipo | Classificação | Justificativa | Ação Recomendada |
|---|---|---|---|---|---|---|
| 1 | audit | repo-wide | config/dependency | TOOL_GAP | O comando depende de base branch e o workspace não expõe `.git`, então a auditoria de changeset não consegue operar aqui. | Registrar como limitação de ambiente. |
| 2 | full | repo-wide | observability | TOOL_GAP | O próprio Fallow reportou hotspot analysis skipped porque não encontrou repositório git. | Usar em repo com git se a base branch for necessária. |
| 3 | dead-code | ElysianCorp/docs/brand/Elysian Design System/colors_and_type.css | unused file | TP | O arquivo foi apontado como não utilizado e parece um artefato órfão real. | Revisar se pode ser removido. |
| 4 | dead-code | ElysianCorp/elysian-motion/src/Composition.tsx | unused file | TP | Mesmo padrão de órfão estático, com sugestão clara de deleção ou suppress. | Confirmar uso em runtime e limpar se não houver. |
| 5 | dead-code | ElysianCorp/scripts/hydration-integrity-check.js | utility script | WONTFIX | É plausivelmente um script de suporte/checagem manual; a análise estática não consegue provar ausência de uso. | Manter até revisão do fluxo de scripts. |
| 6 | dead-code | ElysianCorp/scripts/motion-regression-check.js | utility script | WONTFIX | Mesma categoria de harness/checagem auxiliar. | Manter sob revisão manual. |
| 7 | dead-code | ElysianCorp/scripts/visual-performance-harness.js | utility script | WONTFIX | Ferramenta auxiliar de performance, potencialmente intencional fora do runtime principal. | Manter sob revisão manual. |
| 8 | dupes | ElysianCorp/elysian-motion/src/ForensicOpening.tsx + ElysianCorp/src/components/motion/ForensicOpening.tsx | duplication | TP | Clone group real, com trecho de 31 linhas e sugestão objetiva de extração. | Consolidar o trecho compartilhado. |
| 9 | dupes | ElysianCorp/elysian-motion/src/ForensicOpening.tsx + ElysianCorp/src/components/motion/ForensicOpening.tsx | duplication | TP | Segundo clone group real, com trecho de 15 linhas. | Consolidar ou parametrizar. |
| 10 | health | repo-wide | maintainability | HIGH_VALUE | Health score C, duplication 20.2% e 289 issues totais indicam dívida técnica mensurável. | Usar como triagem e priorização, não como gate oficial. |

## Métricas manuais

- Total de achados analisados: 10
- True positives: 4
- False positives: 0
- WONTFIX: 3
- OUT_OF_SCOPE: 0
- TOOL_GAP: 2
- HIGH_VALUE: 1
- Taxa aproximada de sinal útil: 50%
- Taxa aproximada de ruído/limitação: 50%

## Observações

O trial mostra boa utilidade em análise ampla e duplicação, mas a auditoria de changeset ficou bloqueada pela ausência de git no workspace.