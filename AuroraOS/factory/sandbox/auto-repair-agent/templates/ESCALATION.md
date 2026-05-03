# ESCALATION — {{task_id}}

**OS:** {{os_id}}
**Tentativas:** {{total_attempts}}/{{max_attempts}}
**Modo sandbox:** {{sandbox_mode}}
**Timestamp:** {{timestamp}}

## Evidência de Falha
{{last_stderr}}

## Hipóteses Testadas
{{#each attempts}}
### Tentativa {{attempt_number}} — {{status}}
- Hipótese: {{hypothesis}}
- Duração: {{duration_seconds}}s
- Output: {{stdout}}
{{/each}}

## Ação Requerida
Revisão humana necessária. O auto-repair-agent esgotou todas as hipóteses disponíveis.
