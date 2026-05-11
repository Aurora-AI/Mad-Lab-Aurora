# 🛡️ Sovereignty Report: {{report_id}}

**Data de Geração:** {{generated_at}}  
**Severidade:** {{severity}}  
**Taxa de Sucesso de Reparo (30d):** {{success_rate}}

---

## 🔍 Alertas de Recorrência Detectados

O monitor de soberania identificou padrões de falha que excederam o limite de tolerância sistêmica. Estes itens exigem atenção estrutural.

| ID do Padrão | Categoria | Ocorrências | Última Vista |
| :--- | :--- | :--- | :--- |
{{alerts_table}}

---

## 🛠️ Ações Sugeridas (CEO-Product-Owner)

Com base na análise de recorrência, as seguintes ações de endurecimento são recomendadas:

{{suggested_actions}}

---

## 🛡️ Auditoria de Integridade (Health Check)

Todos os bancos de dados operacionais foram verificados durante este ciclo de supervisão.

- **Dispatcher State:** VALIDATED (PRAGMA OK)
- **Vector Memory:** OPERATIONAL
- **Vault Partition:** SECURE

---
*Este relatório foi gerado automaticamente pelo módulo CEO-Oversight (OS-08) para garantir a governança industrial da Aurora.*
