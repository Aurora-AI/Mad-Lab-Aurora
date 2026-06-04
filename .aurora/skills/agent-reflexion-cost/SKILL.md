# Agent Reflexion Cost

**Status:** ✅ Produção  
**Versão:** 1.0.0  
**Criada por:** OS-ANTIGRAVITY-AURORA-VAULT-20260418-006  
**Função:** Rastreamento automático de custo por OS/step ao final de cada execução

---

## Identidade

Você é o guardião do Token Ledger da Aurora. Toda vez que uma OS é concluída,
você captura custo e tokens por step e persiste no Vault.

Você não julga a qualidade do trabalho. Você registra o custo com precisão.

---

## Quando Ativar

Esta skill é ativada **automaticamente ao final de toda OS concluída**.
O trigger é a presença da frase "OS concluída" ou "gate verificado" seguida
de um evidence file sendo gerado.

Também pode ser chamada explicitamente: `/reflexion-cost [OS_ID]`

---

## Protocolo de Execução

### Passo 1 — Coletar dados da OS

Para cada step da OS concluída, estimar ou coletar:
- Nome e número do step
- Agente executor
- Modelo usado
- Tokens de entrada (estimativa pelo tamanho do prompt + contexto)
- Tokens de saída (contagem real do output gerado)
- Duração em ms (se disponível)

### Passo 2 — Calcular custo estimado

Tabela de preços de referência (atualizar quando mudar):

| Modelo | Input (por 1M tokens) | Output (por 1M tokens) |
|---|---|---|
| claude-sonnet-4-6 | $3.00 | $15.00 |
| claude-haiku-4-5 | $0.25 | $1.25 |
| gemini-2.0-flash | $0.10 | $0.40 |
| gemini-1.5-pro | $1.25 | $5.00 |

**Fator BR:** multiplicar custo USD por 7.0 (5.0 taxa base * 1.4 majoração fiscal) para estimar BRL.

### Passo 3 — Gerar entry JSON

Para cada step, gerar entry conforme schema:
```
C:\Projetos\MadLabAurora\docs\Vault\Token-Ledger\_schema\entry.schema.json
```

Salvar em:
```
C:\Projetos\MadLabAurora\docs\Vault\Token-Ledger\{YYYY-MM-DD}\{OS_ID}-step-{N}.json
```

### Passo 4 — Atualizar aggregation mensal

Ler o arquivo `_monthly\{YYYY-MM}.json` e atualizar:
- `total_tokens` (somar novos)
- `total_cost_usd` (somar novos)
- `total_cost_brl` (recalcular)
- `by_agent` (atualizar agente executor)
- `by_os` (adicionar nova OS)
- `top_cost_steps` (reordenar top 5)
- `optimization_notes` (adicionar se step custou >2x a média)

### Passo 5 — Verificar alertas de budget

```env
BUDGET_ANTIGRAVITY=250  (USD/mês)
BUDGET_CLAUDECODE=150
BUDGET_CODEX=100
```

Se agente atingiu >80% do budget: adicionar `budget_alert: true` no monthly.
Se agente atingiu 100%: reportar ao Comandante antes de próxima execução.

---

## Semantic Triggers

### Keywords (tool_search)
- "token ledger", "custo da OS", "quanto custou", "cost tracking"
- "reflexion-cost", "budget alert", "tokens gastos"
- "aggregation mensal", "monthly summary"

### Context Patterns
- OS concluída (gate executado, evidence file gerado)
- Pergunta sobre custo de uma OS específica
- Revisão de budget mensal

### Negations (não disparar quando)
- OS ainda em execução
- Pergunta técnica sem relação com custo

### Agent Affinity
- Requerida por: nenhuma (skill terminal)
- Compatível com: agent-reflexion-code (ambas rodam ao fim de OS)
- Incompatível com: nenhuma

### Observability
- Custo estimado por invocação: BAIXO (<0.001 USD)
- Token budget recomendado: 2000 tokens
- Latência típica: RÁPIDA <5s
