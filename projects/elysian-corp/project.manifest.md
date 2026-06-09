# Elysian-Corp — Project Manifest

**Produto:** Elysian-Corp  
**Repo soberano:** https://github.com/Aurora-AI/Elysian-Corp.git  
**Workspace local:** `checkouts/Elysian-Corp/` (ignorado pelo git do Mad Lab)  
**Data de registro:** 2026-06-09  
**Decisão de fronteira:** DEC-MADLAB-PRODUCT-WORKSPACE-BOUNDARY-001

---

## Papel no Mad Lab

Elysian-Corp é um produto criativo incubado no Mad Lab Aurora.
O Mad Lab fornece o ambiente de construção — agentes, skills, vault, QA gates.
O produto mantém seu SSOT próprio no repo soberano.

## Artefatos sob custódia do Mad Lab

| Artefato | Localização | Status |
|---|---|---|
| OS-MADLAB-BUILD-001 (tema visual) | `C:\Projetos\Aurora\MadLabAurora\factory\` → migrar para `docs/OS/` | PENDENTE MIGRAÇÃO |
| Promotion package BUILD-001 | Aguarda OS-MADLAB-REPO-HARDENING-001 | PENDENTE |
| Token system (`03-theme-tokens.ts`) | Idem | PENDENTE |
| Motion hooks (3 hooks) | Idem | PENDENTE |
| 7 componentes TSX | Idem | PENDENTE |

## Status atual

```
candidate_status:   VISUAL_CANDIDATE_APPROVED_WITH_CONDITIONS
promotion_allowed:  false
next_gate:          OS-MADLAB-REPO-HARDENING-001 → migration
after_hardening:    OS-MADLAB-INTEGRATION-001 (congelada)
```

## Caminho de promoção

```
Mad Lab (foundry)
  └── transfer/ready/elysian-corp/   ← promotion package montado aqui
        └── PR → Aurora-AI/Elysian-Corp (repo soberano)
```
