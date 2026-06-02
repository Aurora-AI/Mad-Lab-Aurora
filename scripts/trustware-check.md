# Checklist Automatizado — Trustware & Production First

Este script/checklist deve ser rodado (mentalmente ou via CI) antes de qualquer promoção.

## 1. Integridade Física
- [ ] Estrutura de diretórios segue o padrão `vault/patterns/pattern-XXX-name/`?
- [ ] Todos os arquivos obrigatórios (9) estão presentes?
- [ ] Nenhuma dependência externa (npm, CDN) não auditada?

## 2. Produção (Budgets)
- [ ] FPS alvo declarado (60 Desktop / 30 Mobile)?
- [ ] Degradação automática prevista em `feature_flags`?
- [ ] Fallback estático funcional e semanticamente equivalente?
- [ ] Reduced Motion respeitado (desliga movimento, mantém função)?

## 3. Cognição (Trustware)
- [ ] **Neutralidade**: O padrão evita induzir emoção ou urgência não solicitada?
- [ ] **Proporcionalidade**: O tempo de execução é proporcional à complexidade da informação?
- [ ] **Anti-Narrativa**: Easings dramáticos foram removidos?
- [ ] **Honestidade**: O padrão esconde algo enquanto carrega/transita? (Loading screens disfarçadas são proibidas).

## 4. Governança
- [ ] `promotion.md` contém cláusulas de rejeição claras?
- [ ] Há limites de uso explícitos (Contextos Proibidos)?
- [ ] O padrão possui um "kill switch" (flag `enabled`)?

## Resultado
- **PASS**: Todas as respostas são "Sim" ou conformes.
- **FAIL**: Qualquer violação bloqueia a promoção.
