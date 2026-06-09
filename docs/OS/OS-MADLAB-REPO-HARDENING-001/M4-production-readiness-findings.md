# OS-MADLAB-REPO-HARDENING-001 — M4: Production Readiness Findings

**Data:** 2026-06-09  
**Etapa:** M4 de 6  
**Status:** REGISTRADO  
**Evidência base:** OS-MADLAB-REPO-AND-AGENT-MESH-AUDIT-001 (git ls-files ground truth)

---

## Sumário Executivo

Quatro findings de produção identificados durante OS-MADLAB-REPO-AND-AGENT-MESH-AUDIT-001.
Dois são bloqueadores hard (P0/P1 de segurança e governança), dois são P1 de consistência.

| ID | Severidade | Título | Status |
|---|---|---|---|
| PRF-001 | P0 | Client-side LLM key exposure — ElysianChat | ABERTO |
| PRF-002 | P1 | ElysianCorp git tracking anomaly | ABERTO |
| PRF-003 | P1 | README DOC_PATH_DRIFT | ABERTO |
| PRF-004 | P1 | evolution-delta.md não rastreado (7 skills afetadas) | ABERTO |

---

## PRF-001 — Client-side LLM Key Exposure

**Severidade:** P0 (segurança)  
**Arquivo:** `aurora-web/src/components/ElysianChat.tsx:66-67`  
**Evidência:**
```typescript
const genAI = new GoogleGenerativeAI(import.meta.env.VITE_GEMINI_API_KEY);
```

**Problema:** `VITE_` prefixed env vars são embutidas no bundle Vite em build-time e ficam visíveis no JavaScript público. A chave Gemini API pode ser extraída do bundle por qualquer visitante.

**Resolução exigida:**
- Criar endpoint backend `/api/ai/chat` que injete a chave server-side
- ElysianChat passa para fetch contra o proxy, sem acesso direto à API Gemini
- VITE_GEMINI_API_KEY removida do `.env` público; renomear para `GEMINI_API_KEY` (sem prefixo VITE_)

**Gate:** Nenhuma build de produção de aurora-web pode ser publicada antes desta correção.

---

## PRF-002 — ElysianCorp Git Tracking Anomaly

**Severidade:** P1 (governança estrutural)  
**Path:** `ElysianCorp/` (raiz do repo)  
**Evidência:**
```
git submodule status → fatal: no submodule mapping found in .gitmodules for path 'ElysianCorp'
git status → modified: ElysianCorp (modified content, untracked content)
```

**Problema:** `ElysianCorp/` contém `.git/` próprio mas não há `.gitmodules` no MadLabAurora. Git rastreia como um gitlink orphan (1 entrada de árvore), tornando-o perpetuamente "dirty" sem submodule configurado.

**Decisão aplicável:** DEC-MADLAB-PRODUCT-WORKSPACE-BOUNDARY-001 — R5: "sem submodule implícito".

**Resolução exigida (duas opções mutuamente exclusivas):**

*Opção A — Formalizar como checkout local (RECOMENDADA):*
```bash
git rm --cached ElysianCorp
echo "ElysianCorp/" >> .gitignore
git commit -m "chore(boundary): remove ElysianCorp gitlink, add to .gitignore"
```
ElysianCorp continua como workspace local operacional conforme R2.

*Opção B — Formalizar como submodule:*
```bash
git submodule add https://github.com/Aurora-AI/Elysian-Corp.git ElysianCorp
git commit -m "chore(boundary): formalize ElysianCorp as proper submodule"
```
Só válido se equipe decidir rastrear referência de commit explicitamente no MadLab.

**Gate:** Resolve o dirty-state perpétuo que polui git status.

---

## PRF-003 — README DOC_PATH_DRIFT

**Severidade:** P1 (documentação)  
**Arquivo:** `README.md:14`  
**Evidência:**
```markdown
# Path: C:\Aurora\MadLabAurora    ← INCORRETO
```
**Correto:** `C:\Projetos\MadLabAurora`

**Contexto:** Caminho antigo do período em que o repo vivia em `C:\Aurora\`. Mudança ocorreu antes do audit, ref permaneceu.

**Resolução exigida:**
- Atualizar linha 14 com path canônico
- Expandir seção de topologia para incluir: canonical path, checkouts/, transfer/, projects/, docs/OS/, docs/Vault/

**Gate:** Nenhum onboarding doc pode referenciar path obsoleto.

---

## PRF-004 — evolution-delta.md Não Rastreado

**Severidade:** P1 (governança de skills)  
**Arquivo esperado:** `.aurora/skills/evolution-delta.md` (ou equivalente)  
**Evidência:**
```
git ls-files .aurora/skills/ | grep evolution-delta → (nenhum resultado)
```

**Problema:** 7 skills referenciam `evolution-delta.md` em seus `SKILL.md` como fonte de verdade para decisões de evolução. O arquivo não existe no repo rastreado — skills referenciam um fantasma.

**Skills afetadas (confirmadas por grep em SKILL.md):**
- ceo-business-partner
- scaffolding-skill (+ 5+ variantes referenciadas)

**Resolução exigida:**
- Criar `evolution-delta.md` canônico com schema mínimo: `skill_id`, `version`, `delta_type`, `rationale`
- Rastrear em `.aurora/` ou definir caminho exato e atualizar todas as referências nas skills
- Após criação, executar SES completo para ceo-business-partner (9/9 refs presentes → pronto para certificação)

**Gate:** Nenhuma skill pode ser certificada enquanto referenciar arquivo inexistente.

---

## Decisões de Priorização

```
PRF-001 → Resolver ANTES de qualquer build/deploy de aurora-web
PRF-002 → Resolver ANTES do próximo commit em main (dirty state permanente)
PRF-003 → Resolver nesta OS (baixo custo, alta clareza)
PRF-004 → Resolver antes de certificar qualquer skill que referencie evolution-delta
```

---

## Próxima Etapa

**M5 — Accessibility Certification**  
Targets: `Preloader.tsx`, `useScrollProgress`, conductor GSAP — gaps de `prefers-reduced-motion`.
