# AuroraOS — Sistema Operacional da Empresa de Um Homem Só

**Status:** ATIVO
**Owner:** CEO Agent (ceo-agent-v1) + Comandante (Rodrigo)
**Governança:** Manual de Construção Aurora v9.0 §3.5

---

## Conceito

AuroraOS é o diretório raiz de toda a malha cognitiva autônoma da empresa.
Não é código de produto — é a camada operacional que orquestra a fábrica e os projetos.

O CEO Agent opera exclusivamente dentro deste diretório (e seu namespace no Vault).
Outputs do CEO, análises, sandboxes e relatórios estratégicos nunca são criados na raiz do portfólio.

---

## Estrutura

```
AuroraOS/
├── factory/                 # FRENTE 1 — Uso interno da fábrica Aurora
│   ├── ceo-agent/           # CEO Agent: constitution, vault, decisões internas
│   │   └── vault/           # Outputs e relatórios do CEO sobre a fábrica
│   ├── agents/              # Agentes validados para uso interno Aurora
│   └── workflows/           # Workflows internos aprovados e em produção
│
└── projects/                # FRENTE 2 — Projetos externos / clientes
    └── [project-slug]/      # Sandbox isolado por projeto
                             # Ex: Audit_Sandbox_2026/ = análises do CEO para projetos externos
```

---

## Regras

- **R1 — CEO não cria na raiz**: Todo output do CEO Agent vai para `factory/ceo-agent/vault/` (fábrica) ou `projects/[slug]/` (projetos externos).
- **R2 — factory/ é validado**: Nada vai para `factory/` sem ter sido testado e aprovado via OS formal.
- **R3 — projects/ é isolado**: Cada projeto externo tem seu diretório independente. Dados de projetos não contaminam a fábrica.
- **R4 — Trustware Bridge obrigatório**: AuroraOS não acessa ElysianLex diretamente. Toda comunicação entre domínios passa pelo AuroraRouter.
- **R5 — Nenhum código de produto aqui**: Código vive em `Ozzmosis/`, `CRM/`, `ElysianLex/`. AuroraOS é operacional, não de produto.
