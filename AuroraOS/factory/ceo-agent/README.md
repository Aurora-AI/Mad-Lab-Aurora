# CEO Agent — Domínio SOVEREIGN

**ID:** ceo-agent-v1
**Spec:** `Ozzmosis/aurora-agents/specs/ceo-agent.json`
**Namespace Vault:** `Ozzmosis/docs/Vault/Projects/CEO-SOVEREIGN/`
**Constitution:** `Ozzmosis/docs/Vault/Raw/CEO-AGENT-STRATEGIC-ALIGNMENT.md`

---

## Responsabilidades

- Monitorar integridade da fábrica (Ozzmosis + CRM + ElysianLex)
- Priorizar backlog e emitir Sovereignty Reports
- Propor decisões de `BUSINESS_GENESIS` (criação de departamentos/estrutura)
- Auditar estado operacional da empresa

## Outputs deste diretório

- `vault/` — Relatórios e análises do CEO sobre a fábrica Aurora interna

## Outputs em `AuroraOS/projects/`

- Análises e sandboxes do CEO para projetos externos ou de clientes

## Regras de Isolamento

- Acessa ElysianLex APENAS via Trustware Bridge
- Todas as ordens passam pelo AuroraRouter (gate determinístico)
- Vault de acesso restrito: `docs/Vault/Raw/` e `docs/Vault/Projects/CEO-SOVEREIGN/`
- Message bus: apenas tópicos `strategy/*`, `integrity/*`, `ops/backlog`
