# GEMINI.md — Instruções Operacionais (Gemini / Antigravity Context)

> Instruções específicas para o agente Gemini/Antigravity ao atuar no Mad Lab Aurora.
> Leia este arquivo e o `AGENTS.md` antes de qualquer ação.

---

## 1. Contexto do Domínio

O **Mad Lab Aurora** é o braço criativo da Aurora — responsável por direção de arte,
motion design, WebGL e craft de interface para todo o ecossistema.

**Posição na hierarquia:**
- Consome capacidades da fábrica **Ozzmosis** (read-only, via Toolbelt Registry)
- Fornece ativos visuais e padrões estéticos para os produtos verticais (ElysianLex, CRM)
- Não é um produto — é uma **camada de infraestrutura criativa**

**Autoridade máxima:** `docs/brand/MANUAL_DA_AGENCIA.md` v3.0.0

---

## 2. Quick Commands (Subprojetos)

### aurora-web (Site institucional)
```bash
cd aurora-web
npm run dev          # Dev server (porta 3001)
npm run build        # Build de produção
npm run preview      # Preview do build
```

### ElysianCorp (Produto)
```bash
cd ElysianCorp
# Verificar README.md local para comandos específicos
```

### Skill Evolution System (scaffolding — NÃO usar em produção ainda)
```bash
cd aurora-agents/skill-evolution-system
python run_ses_landing_page.py   # Teste de pipeline (output genérico)
```

---

## 3. Topologia do Repositório

| Diretório | Papel |
|---|---|
| `.aurora/skills/` | 15 skills locais do domínio criativo |
| `.agents/rules/` | Regras always_on (designmanualposthero.md) |
| `aurora-web/` | Site institucional Aurora (Vite + TS) |
| `aurora-agents/` | Skill Evolution System (scaffolding) |
| `aurora-visual-assets/` | Componentes, shaders e interações canônicas |
| `docs/brand/` | DNA, Manual da Agência, Brand Kit Elysian |
| `docs/Vault/` | Memória local: KIs, OS-Evidence, Threads, Decisions |
| `integrations/open-design/` | 138 sistemas de design catalogados |
| `ElysianCorp/` | Produto derivado sob governança do MadLab |
| `Referências/` | Materiais de referência visual e inspiração |
| `conductor/` | Integração com Ozzmosis Conductor |

---

## 4. Pilha Documental (Roteador Central)

```text
MANUAL_DA_AGENCIA.md (Constituição)
          │
  ┌───────┼───────────────────────┐
  ▼       ▼                       ▼
domain-  ELYSIAN_BRAND_KIT_v1.1  designmanualposthero.md
policy   (Identidade / Logo)      (Grid / Tipografia / Motion)
  │
  ▼
DESIGN_LIBRARY.md
(Shaders / WebGL / P046-P052)
```

**Regra de conflito:** Em caso de divergência entre documentos,
a hierarquia acima determina qual prevalece (superior tem prioridade).
Ver `docs/Vault/OS-Evidence/OS-MADLAB-DOC-STACK-PREPARATION-20260528-001/DOC_CONFLICT_RULES.md`

---

## 5. Sistema Agêntico — Inventário

### Skills S-Tier (prontas para produção)
- `ceo-design`, `ceo-effects`, `ceo-web`, `ceo-copy` — leia os arquivos locais em `.aurora/skills/`
- `qa-review` — Gate obrigatório ao finalizar qualquer entrega
- `.agents/rules/designmanualposthero.md` — Always-on, impacto sistêmico

### Skills A-Tier (funcionais, sem `references/` completas ainda)
- `agent-reflexion-cost`, `agent-thread-recorder` — funcionais, path do Ledger já corrigido
- `taste-design`, `design-md` — funcionais para geração de DESIGN.md
- `ceo-marketing`, `ceo-product-owner`, `ceo-business-partner` — sem arquivos locais de referência

### Skills B-Tier (funcionais mas subdesenvolvidas)
- `ceo-critique-theater`, `ceo-discovery-specialist` — wrappers de 22 linhas
- `engenheiro-reverso` — 34 linhas, sem template de output completo

### Scaffolding (NÃO usar como produção)
- `aurora-agents/skill-evolution-system/` — pipeline existe mas output é genérico

---

## 6. Padrão de Motion e Stack

```
Three.js     → r128 (FIXO — não atualizar sem OS aprovada)
             → NÃO usar THREE.CapsuleGeometry (disponível apenas r142+)
             → Alternativas: CylinderGeometry, SphereGeometry

R3F          → React Three Fiber com useFrame, useThree, Canvas

GSAP         → + ScrollTrigger (scroll animado)
             → + Timeline (sequências complexas)
             → + Ticker (sync com R3F)

GLSL         → Fragment shader: atmosfera, dissolução, cor
             → Vertex shader: deformação de geometria com peso
             → Noise: perlin/simplex para movimento orgânico

PROIBIDO     → CUDA, nvidia-*, torch, WebGPU (sem OS)
             → prefers-reduced-motion fallback: OBRIGATÓRIO em todo efeito
```

---

## 7. Paleta e Tipografia (Dark Editorial)

```
Escuridão com temperatura:
  #0D0D0D, #111110, #1A1A17 — nunca #000000 puro em seções

Off-white com memória:
  #F4F2ED, #F8F7F3 — nunca #FFFFFF puro exceto em precisão técnica

Dourado com peso:
  Tom de iluminura medieval — nunca amarelo puro

Acento profundo:
  1 única cor de acento por projeto — nunca dois

PROIBIDO:
  Gradiente SaaS (roxo→azul→verde)
  Gradiente de texto
  Mais de 3 cores + branco + cinza simultâneos
```

```
Voz 1 / Display (headline):
  Serif editorial pesado (Didone, Modern, Transitional)
  Tamanho: 52-120px | Nunca Inter, Roboto, Arial

Voz 2 / Técnica (labels, metadados):
  Monospace ou sans geométrico, CAPSLOCK, tracking 0.3-0.5em
  Tamanho: 8-12px | Nunca em corpo corrido

Voz 3 / Editorial (corpo):
  Serif clássico (Garamond, Caslon) ou sans refinado
  Tamanho: 16-20px | Nunca CAPSLOCK
```

---

## 8. Regras de OS e Micro-Etapas

1. **Tarefas de risco Médio/Alto/Crítico** exigem OS formal
2. OS em micro-etapas — nunca monolítica
3. Cada micro-etapa: executar → gate → `qa-review` → **PARAR**
4. Aguardar confirmação de sucesso sem ressalvas antes de avançar
5. Falha no gate: corrigir na etapa atual, não avançar
6. Evidence file em `docs/Vault/OS-Evidence/OS-MADLAB-{DOMÍNIO}-{DATA}-{SEQ}/`
7. `agent-reflexion-cost` ao concluir OS
8. `agent-thread-recorder` ao concluir sessão com decisões

---

## 9. Descoberta Física de Contratos (Anti-Alucinação)

> **INVARIANTE:** Antes de qualquer OS ou plano de implementação,
> executar varredura física para verificar contratos, schemas e paths reais.
> **PROIBIDO** documentar utilitários ou contratos que não existam fisicamente.

Para verificar se um arquivo existe antes de referenciar:
```powershell
Test-Path "C:\Projetos\MadLabAurora\.aurora\skills\ceo-design\references\founder-dna.md"
```

---

## 10. Armadilhas Conhecidas

| # | Armadilha | Impacto | Mitigação |
|---|---|---|---|
| 1 | `references/` nas skills não existem fisicamente | Skill opera sem contexto real do DNA do fundador | Sprint 1: criados como parte da remediação |
| 2 | Path do Token Ledger estava incorreto (`C:\Projetos\Aurora\MadLabAurora\`) | Escrita falharia silenciosamente | Corrigido no Sprint 1 |
| 3 | SES gera output idêntico para qualquer skill | Não usar SES como validação real | Declarado como scaffolding |
| 4 | `vault_manifest.json` sem entradas reais | Bibliotecário não rastreado | Pipeline de KI pendente |
| 5 | `catalog_design_systems.json` tem 138 sistemas | Discovery Specialist funciona, mas skill tem 22 linhas apenas | Sprint 2 expandirá a skill |
| 6 | Three.js versão — r128 fixado | `CapsuleGeometry` não existe em r128 | Nunca usar sem verificar changelog |
| 7 | `cross-skill-feedback-event.schema.json` não existe | Fase 7 do qa-review não pode ser executada | Sprint 2: criar schemas |

---

## 11. Observabilidade da Fábrica (Read-Only)

O Mad Lab pode consumir (quando disponível):
- `observability.get_trace_summary` — resumo de traces
- `observability.osqa.list_qa_artifacts_by_os` — artefatos QA por OS

**Se o gateway não estiver disponível:** registrar indisponibilidade como
`FACTORY_TOOL_UNAVAILABLE` e prosseguir com evidência local.
**Nunca simular resultado de observabilidade.**

---

## 12. Referências Essenciais

| Documento | Localização |
|---|---|
| Constituição Criativa | `docs/brand/MANUAL_DA_AGENCIA.md` |
| DNA Visual Dark Editorial | `docs/brand/mad-lab-aurora-dna-v2.1.0.md` |
| Brand Kit Elysian | `docs/brand/ELYSIAN_BRAND_KIT_v1.1.md` |
| Post-Hero Design Manual | `.agents/rules/designmanualposthero.md` |
| Biblioteca de Padrões WebGL | `docs/Vault/DESIGN_LIBRARY.md` |
| Design Library Completa | `docs/Vault/DesignLibrary/` |
| Soberania de Domínio | `.aurora/domain-policy.json` |
| Toolbelt Consumer | `.aurora/toolbelt-consumer.json` |
| Decisão Mesh Agentivo | `docs/Vault/Decisions/DEC-MADLAB-AGENTIC-MESH-001.md` |
| Dívida Visual | `.aurora/design-debt-baseline.json` |
| Catálogo Open-Design (138) | `integrations/open-design/catalog_design_systems.json` |
