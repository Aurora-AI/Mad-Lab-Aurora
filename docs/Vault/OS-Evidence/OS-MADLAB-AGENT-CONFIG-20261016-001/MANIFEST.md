---
os: OS-MADLAB-AGENT-CONFIG-20261016-001
created: 2026-10-16T09:25:25-03:00
purpose: Backup das configurações de agente anteriores à reescrita do zero de AGENTS.md e GEMINI.md
policy: append-only — nenhum arquivo deste diretório é deletado ou reescrito
decision: deleção real recusada pelo humano em 2026-10-16T09:32; originais preservados com deprecated: true
---

# Backup — Configurações de agente (pré-reescrita)

Os arquivos em `backup-originais/` são cópias byte a byte dos originais.
O status de descontinuação fica registrado **aqui**, e não dentro das cópias, para não invalidar os hashes.

| Arquivo (backup) | Origem | SHA-256 | deprecated | superseded_by |
|---|---|---|---|---|
| `AGENTS.md` | `/AGENTS.md` | `9DBAC0DE2C105F3D5921267F48C163ACD1DAC05C94A8DE7F1A57AA24BEB86BA2` | true | nova versão de `/AGENTS.md` (pendente — autor humano) |
| `GEMINI.md` | `/GEMINI.md` | `2F999FF555EAABF8AFD7FF98C4452793BA8C37BDEB455FD5D4816E2E3809D419` | true | nova versão de `/GEMINI.md` (pendente — autor humano) |
| `skills.json` | `/.agents/skills.json` | `4753B7E7AE8F08C1FEA272E985AC5D6B1E3D63D0DDBA234C042D18BAEF05DF12` | false | — (fora do escopo atual; aguardando decisão) |
| `designmanualposthero.md` | `/.agents/rules/designmanualposthero.md` | `FBA6BB97F70949D0495DF6CDE4DE45CC4F9F913B6DA2F5D7D5B55DD7925C4BD4` | false | — (fora do escopo atual; aguardando decisão) |

## Verificação

```powershell
Get-ChildItem backup-originais | ForEach-Object { "$($_.Name) $((Get-FileHash $_.FullName).Hash)" }
```

## Pendências registradas

1. Contradição de direção visual: Dark Editorial (AGENTS/GEMINI/post-hero) × Mad Lab Theme (skill `ceo-design`). Deve ser resolvida na nova versão escrita pelo humano.
2. Escopo do "padrão novo": se inclui `.agents/rules/`, `.agents/skills.json` e `.aurora/*.json`. Não decidido.
