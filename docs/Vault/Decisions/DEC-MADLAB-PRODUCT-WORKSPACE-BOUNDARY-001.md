# DEC-MADLAB-PRODUCT-WORKSPACE-BOUNDARY-001

**Data:** 2026-06-09  
**Status:** APROVADA  
**Autoridade:** Rodrigo Cesar Winhaski  
**Contexto:** OS-MADLAB-REPO-AND-AGENT-MESH-AUDIT-001 → M6 → abertura OS-MADLAB-REPO-HARDENING-001

---

## Decisão

O Mad Lab Aurora pode hospedar workspaces operacionais de produtos criativos — como Elysian-Corp —
para aproveitar agentes, skills, gates, Vault e ferramentas locais.

Porém, o código-fonte publicável desses produtos **não pertence ao repositório MadLabAurora**.

Cada produto mantém seu repositório soberano próprio, e toda transferência ocorre por contrato de promoção.

---

## Topologia Canônica

```
MadLabAurora/                     ← foundry / ambiente de construção
├── checkouts/
│   └── Elysian-Corp/             ← workspace operacional local (ignorado pelo git)
├── projects/
│   └── elysian-corp/             ← contratos, decisões, manifests (rastreado)
├── transfer/
│   └── ready/
│       └── elysian-corp/         ← pacotes prontos para promoção (rastreado como .gitkeep)
└── docs/Vault/
```

```
Aurora-AI/Elysian-Corp            ← SSOT do produto publicado
https://github.com/Aurora-AI/Elysian-Corp.git
```

---

## Regras Derivadas

| Regra | Descrição |
|---|---|
| R1 — Soberania do produto | Elysian-Corp é repo soberano. MadLabAurora não versiona código do produto. |
| R2 — Checkout permitido | `checkouts/Elysian-Corp/` pode existir localmente para trabalho operacional. Ignorado pelo git. |
| R3 — Promoção por contrato | Toda transferência de artefato para o repo soberano ocorre via promotion package + PR. Nenhuma cópia informal vira integração. |
| R4 — MadLab como foundry | MadLab fornece: agentes, skills, vault, gates, QA. Não retém: código publicável, assets definitivos de produto. |
| R5 — Sem submodule implícito | `ElysianCorp/` atual não deve ser tratado como submodule sem `.gitmodules` formal. Reclassificar como checkout local ou formalizar corretamente. |
| R6 — Transfer zone | `transfer/ready/elysian-corp/` é o ponto de saída oficial. Artefato só deixa o Mad Lab por este caminho. |

---

## O que esta decisão NÃO é

- Não proíbe desenvolvimento de produtos dentro do Mad Lab
- Não exige que todos os repos sejam externos
- Não desfaz o trabalho já feito (BUILD-001 etc.) — recontextualiza onde ele vive

---

## Frase Canônica

> O Mad Lab pode hospedar o trabalho.  
> Mas não sequestra a verdade do produto.

---

## Produtos cobertos por esta decisão

| Produto | Repo soberano | Workspace no Mad Lab |
|---|---|---|
| Elysian-Corp | https://github.com/Aurora-AI/Elysian-Corp.git | `checkouts/Elysian-Corp/` |
