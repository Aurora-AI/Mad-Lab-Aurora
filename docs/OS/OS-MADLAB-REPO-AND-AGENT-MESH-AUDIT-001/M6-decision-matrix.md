# M6 — Decision Matrix

**OS:** OS-MADLAB-REPO-AND-AGENT-MESH-AUDIT-001  
**Date:** 2026-06-09  
**Synthesizes:** M1 (direct) + M2 + M3 + M4 + M5 (agents)

---

## Repo State (Evidence-Based)

| Assertion (prior audit) | Verdict | Evidence |
|---|---|---|
| "14 agentes" | INCORRECT — é 15 | git ls-files .aurora/skills/ |
| "11 certificados" | CORRECT | skill-registry.json + SKILL.md frontmatter |
| "4 scaffolding com refs faltando" | PARTIALLY CORRECT | ceo-business-partner tem 9/9 — os outros têm 4/7 |
| "ElysianCorp submodule" | INCORRECT — não é submodule | git submodule status: fatal (sem .gitmodules) |
| "checkouts como lixo" | NÃO DECIDIR | ignorado pelo .gitignore — fora do escopo do repo |
| "Build-001 pronto para migrar" | NÃO CONFIRMADO | não existe no repo canônico rastreado |
| "Conductor bloqueia skill.created" | NÃO PROVADO | nenhum runtime encontrado para essa claim |
| "Malha integrada e funcionando" | PARCIAL | contratos existem; bridge é CONTRACTUAL_ONLY |
| "aurora-web é projeto ativo" | PROVEN | package.json rastreado, vercel.json válido, dist presente |
| "AuroraCognitiveAssets é ativo" | PROVEN | Python runtime CLI com integração Infoproduct Factory |

---

## M6 Decision Matrix

### KEEP — sem ação necessária

| Item | Evidência |
|---|---|
| `.aurora/skills/` (11 certified) | SKILL.md + references rastreados, skill-registry.json ativo |
| `aurora-web/` | RUNTIME_PROVEN, Vercel configurado, 6 rotas funcionais |
| `AuroraCognitiveAssets/` | RUNTIME_PROVEN, Python CLI ativo |
| `aurora-visual-assets/` | 106 arquivos rastreados, referenciado por projetos via alias |
| `docs/Vault/` | Token Ledger, OS-Evidence, Decisions — tudo rastreado |
| `integrations/` (717 arquivos) | Catálogo Open-Design, usado pelo ceo-critique-theater |
| `conductor/` | Static PoC válido — 3 arquivos rastreados |
| `qa-review/feedback_loop.py` | EXECUTABLE — runtime real, memory.json ativo v1.0.4 |

### FIX_REQUIRED — correção antes da próxima OS

| Item | Problema | Ação |
|---|---|---|
| `README.md` | `C:\Aurora\MadLabAurora` (path errado) | Atualizar para `C:\Projetos\MadLabAurora` + expandir topologia |
| `ElysianCorp` git tracking | Tracked como 1 arquivo sem `.gitmodules` | Decidir: formalizar submodule com `.gitmodules` OU remover `ElysianCorp/.git` e rastrear como diretório normal |
| `aurora-web/src/components/ElysianChat.tsx` | `VITE_GEMINI_API_KEY` exposta no browser (P1) | Implementar backend proxy antes de produção |
| `AuroraCognitiveAssets/` | Sem `requirements.txt` rastreado (P1) | Criar e commitar requirements.txt |
| `evolution-delta.md` | Referenciado por 7 skills — não rastreado em nenhuma | Criar o arquivo em cada `references/` ou criar um canônico compartilhado |

### PROMOTE_TO_CERTIFICATION — ação na malha agêntica

| Skill | Status atual | O que falta | Ação |
|---|---|---|---|
| `ceo-business-partner` | scaffolding/draft | Nada — 9/9 refs presentes | Rodar SES → deve atingir certified |
| `ceo-copy` | scaffolding/draft | `copy-dna.md`, `icp-language.md`, `evolution-delta.md` | Criar os 3 arquivos + rodar SES |
| `ceo-marketing` | scaffolding/draft | `positioning-algorithm.md`, `sales-playbook.md`, `evolution-delta.md` | Criar os 3 arquivos + rodar SES |
| `ceo-product-owner` | scaffolding/draft | `martell-protocol.md`, `product-pain-ontology.md`, `evolution-delta.md` | Criar os 3 arquivos + rodar SES |

### NOT_CONFIRMED — não decidir ainda

| Item | Razão |
|---|---|
| BUILD-001 migration | Existe em `C:\Projetos\Aurora\MadLabAurora\factory\` (outro repo) — não rastreado no canônico. Aguarda OS-MADLAB-REPO-HARDENING-001 |
| `checkouts/` cleanup | Ignorado pelo .gitignore — fora do escopo desta auditoria de repo |
| Bridge runtime implementation | CONTRACTUAL_ONLY é o estado correto por agora — implementar quando Ozzmosis bridge for necessário operacionalmente |

---

## OS Status Registry Atualizado

| OS | Status |
|---|---|
| OS-019R | CONCLUÍDA |
| OS-MADLAB-BUILD-001 | FECHADA — REVIEWABLE_CANDIDATE |
| OS-MADLAB-REPO-TOPOLOGY-AUDIT-001 | CONCLUÍDA |
| OS-MADLAB-REPO-AND-AGENT-MESH-AUDIT-001 | CONCLUÍDA (este documento) |
| OS-MADLAB-REPO-HARDENING-001 | PRÓXIMA — migração BUILD-001, fix ElysianCorp git, README |
| OS-MADLAB-INTEGRATION-001 | CONGELADA |

---

## Frase Canônica

> O repo tem constituição, runtime provado, e malha agêntica com 11/15 skills certificadas.  
> Os 4 problemas restantes são cirúrgicos: um path drift no README, uma chave de API exposta,  
> um tracking de git inconsistente no ElysianCorp, e 3 skills que precisam de arquivos de conhecimento.  
> Nenhum deles bloqueia o laboratório — todos bloqueiam o produto.
