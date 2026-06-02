# Decision — Fallow Consulting Trial

## Decisão

MANTER COMO CONSULTOR EXTERNO

## Justificativa

O Fallow entregou saída parseável e achados úteis, especialmente em `dupes`, `health` e `dead-code`, mas a parte de auditoria de changeset ficou bloqueada pela ausência de `.git`/base branch no workspace. Isso impede tratá-lo como gate oficial read-only neste ambiente.

## Evidência usada

- 03-json-validation.txt
- 05-human-classification.md
- 06-consulting-report.md

## Restrições se ingerido

- Somente read-only/dry-run.
- Sem fix --yes.
- Sem MCP cru.
- Sem auto-cura autônoma.
- Sem CI gate até nova OS.
- Sem alteração de código sem approval.

## Próxima OS, se aplicável

OS-AURORA-ALVARO-TOOLBELT-FALLOW-GATE-20260602-001