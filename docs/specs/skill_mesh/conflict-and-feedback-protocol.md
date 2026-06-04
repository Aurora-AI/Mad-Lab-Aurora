---
name: conflict-and-feedback-protocol
version: 1.0.0
status: production
---

# Skill Mesh — Protocolo de Conflito e Feedback Cruzado

> Protocolo operacional para detecção, registro e resolução de conflitos
> entre skills do ecossistema MadLab Aurora.
>
> **Referenciado por:** `qa-review` SKILL.md Fase 7

---

## 1. Quando Gerar um CrossSkillFeedback

Uma skill deve gerar um evento `cross-skill-feedback` quando detectar:

| Trigger | Tipo de Issue | Exemplo |
|---|---|---|
| Regra A contradiz Regra B | `CONTRADICTION` | CEO-Design aprova border-radius 16px; CEO-Web rejeita |
| Skill referencia algo que não existe | `MISSING_RULE` | qa-review referencia schema inexistente |
| Path físico incorreto | `PATH_ERROR` | Token Ledger com path incorreto |
| Anti-padrão reincidente | `ANTI_PATTERN` | Gradiente SaaS reaparecendo após correção |
| Scope de duas skills sobreposto | `SCOPE_OVERLAP` | CEO-Effects e CEO-Design decidindo os mesmos efeitos |
| Referência desatualizada | `OUTDATED_REFERENCE` | Skill cita DNA v1.0 quando v2.1.0 está vigente |
| Contrato de input/output violado | `CONTRACT_VIOLATION` | Discovery Specialist entregando JSON sem os 8 campos |

---

## 2. Como Gerar o Evento

### Passo 1 — Identificar o problema
O problema deve ser **concreto e evidenciável** — não especulativo.

### Passo 2 — Criar o evento JSON
Usar o schema em `docs/specs/skill_mesh/cross-skill-feedback-event.schema.json`

Campos obrigatórios:
```
event_id      → CSF-{YYYY-MM-DD}-{SEQ auto-incremental}
timestamp     → ISO 8601
source_skill  → quem detectou
target_skill  → quem precisa corrigir
issue_type    → enum do schema
severity      → CRITICO / ALTO / MEDIO / BAIXO
description   → máximo 500 chars, concreto
evidence      → path e snippet quando disponível
recommended_action → ação específica e acionável
```

### Passo 3 — Persistir o evento
```
docs/Vault/OS-Evidence/{OS_ID}/cross-skill-feedback/{event_id}.json
```

Se não houver OS ativa, usar:
```
docs/Vault/OS-Evidence/CROSS-SKILL-FEEDBACK-POOL/{YYYY-MM-DD}/{event_id}.json
```

### Passo 4 — Reportar no output do QA
Incluir no relatório de qa-review:

```
## Fase 7 — Cross-Skill Feedback
Evento gerado: {event_id}
Source: {source_skill} → Target: {target_skill}
Tipo: {issue_type} | Severidade: {severity}
Ação recomendada: {recommended_action}
```

---

## 3. Resolução de Conflitos

### Hierarquia de Autoridade para Resolução

Quando duas skills têm regras conflitantes, a resolução segue a hierarquia:

```
1. MANUAL_DA_AGENCIA.md (constituição — autoridade máxima)
2. mad-lab-aurora-dna-v2.1.0.md (DNA visual)
3. ELYSIAN_BRAND_KIT_v1.1.md (tokens e identidade)
4. designmanualposthero.md (grid e tipografia)
5. SKILL.md individual da skill de domínio primário
```

**Regra de domínio primário:**
- Questão de identidade visual → CEO-Design é autoridade
- Questão de motion/efeito → CEO-Effects é autoridade
- Questão de conversão/layout → CEO-Web é autoridade
- Questão de código/entrega → qa-review é autoridade

### Quando o conflito não tem resolução clara

1. Pausar a micro-etapa atual
2. Criar issue no Vault: `docs/Vault/Decisions/DECISION-PENDING-{YYYY-MM-DD}-{SEQ}.md`
3. Reportar ao Comandante para decisão de arquitetura
4. Não avançar sem resolução confirmada

---

## 4. Severidade e Impacto

| Severidade | Impacto | Ação Necessária |
|---|---|---|
| CRITICO | Bloqueia entrega ou causa falha em produção | Corrigir antes de qualquer avanço |
| ALTO | Degrada a qualidade operacional da skill | Corrigir na próxima sessão |
| MEDIO | Reduz a confiabilidade ou consistência | Corrigir no sprint seguinte |
| BAIXO | Melhoria de clareza ou documentação | Registrar e corrigir quando conveniente |

---

## 5. Anti-Padrões (O Que NÃO Fazer)

```
✗ Gerar eventos genéricos sem evidência concreta
✗ Gerar evento de CONTRADICTION sem verificar a hierarquia de autoridade primeiro
✗ Resolver um conflito unilateralmente sem registrar a decisão
✗ Ignorar um evento de severidade CRITICO
✗ Gerar mais de 3 eventos por sessão sem ao menos um resolution preenchido
```

---

## 6. Inventário de Eventos Ativos

*Registrar aqui eventos gerados mas ainda sem resolução:*

| Event ID | Source → Target | Tipo | Severidade | Status |
|---|---|---|---|---|
| CSF-2026-05-30-001 | qa-review → agent-reflexion-cost | PATH_ERROR | ALTO | ✅ RESOLVIDO |
| CSF-2026-05-30-002 | qa-review → agent-thread-recorder | PATH_ERROR | ALTO | ✅ RESOLVIDO |
