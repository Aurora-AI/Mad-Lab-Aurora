# Implementation Plan — OS-MADLAB-AGENTIC-PIVOT-20261016-001

## 1. Fontes lidas
- `C:\Users\rodri\Desktop\Eu preciso criar uma habilidade par.txt` (linhas 1–744, lido em `2026-10-16T10:10:12-03:00`).
- `C:\Projetos\Aurora\docs\AGENTS\DOCTRINE.md` (linhas 1–148, lido em `2026-10-16T10:17:27-03:00`).
- `C:\Projetos\Aurora\GEMINI.md`, `C:\Projetos\Aurora\AGENTS.md`, `C:\Projetos\Aurora\CLAUDE.md` (linhas 1–143, lidos em `2026-10-16T10:17:27-03:00`).
- `C:\Projetos\Aurora\docs\CONSTITUICAO\EMENDA_v9.1_MANUAL_AURORA.md` (linhas 1–471, lido em `2026-10-16T10:17:42-03:00`).
- `C:\Projetos\Aurora\docs\CONSTITUICAO\criterio_formal_de_aceite_de_interface.md` (linhas 1–179, lido em `2026-10-16T10:17:43-03:00`).
- `C:\Projetos\Aurora\docs\AGENTS\LAW.md` (linhas 1–250) e `C:\Projetos\Aurora\docs\AGENTS\POLICY_TRUSTWARE.md` (linhas 1–58).
- `C:\Projetos\Aurora\docs\AGENTS\registry_criteria.md` (linhas 1–123) e `C:\Projetos\Aurora\docs\specs\skill_mesh\skill.schema.json` (linhas 1–689).
- `C:\Projetos\Aurora\docs\os\PLANO-MESTRE-INFRAESTRUTURA-EMPRESA-20260801.md` (linhas 1–260) e `C:\Projetos\Aurora\docs\Vault\Business\DESENHO-AGENTES-VENDAS-RESGATE-20260811.md` (linhas 1–101).
- `C:\Projetos\Aurora\.agents\skills\auditor.skill\SKILL.md` (linhas 1–233) e `C:\Projetos\Aurora\.agents\skills\qa-review.skill\SKILL.md` (linhas 1–394).
- `C:\Projetos\Aurora\packages\tooling\scripts\doctrine.mjs` (linhas 1–109) e `C:\Projetos\Aurora\packages\tooling\scripts\check-plan-conformance.mjs` (linhas 1–240).
- `c:\Projetos\MadLabAurora\AGENTS.md` (linhas 1–185), `c:\Projetos\MadLabAurora\GEMINI.md` (linhas 1–216), `c:\Projetos\MadLabAurora\.aurora\domain-policy.json` (linhas 1–42), `c:\Projetos\MadLabAurora\.aurora\toolbelt-consumer.json` (linhas 1–24), `c:\Projetos\MadLabAurora\.agents\rules\designmanualposthero.md` (linhas 1–237), `c:\Projetos\MadLabAurora\project-manifest.json` (linhas 1–479).

## 2. Reformulação
- **Entendimento literal:** Reorganizar o repositório `c:\Projetos\MadLabAurora` para operar sob a Doutrina Operacional vigente de `C:\Projetos\Aurora` (`docs/AGENTS/DOCTRINE.md`, `EMENDA_v9.1_MANUAL_AURORA.md`, `criterio_formal_de_aceite_de_interface.md`, `skill.schema.json`) e sob a Arquitetura de Presença Web Agêntica e Outbound Pós-IA definida em `C:\Users\rodri\Desktop\Eu preciso criar uma habilidade par.txt`, mantendo todas as conexões com a fábrica Aurora/Ozzmosis e descontinuando o modelo estético anterior (Dark Theme, Dark Editorial, Mad Lab Theme, WebGL/Three.js decorativo).
- **O que isto explicitamente NÃO é (Não-escopo):** Não é deleção física de arquivos do Vault, não altera MCPs ou `.aurora/toolbelt-consumer.json`, e não reescreve o código interno dos apps antes da definição do catálogo inicial pelo Comandante.
- **Suposições declaradas:** As skills e documentos estéticos antigos recebem `deprecated: true` / `status: deprecated` conforme a regra append-only (Doutrina §5), e as novas skills já nascem com bloco `## Mesh Contract` validado contra `C:\Projetos\Aurora\docs\specs\skill_mesh\skill.schema.json`.

## 3. O que este plano NÃO faz (Não-escopo)
- Não faz deleção (`rm`/`del`) de nenhum arquivo histórico do Vault (`docs/Vault/`) nem de diretórios existentes.
- Não faz alteração em `.aurora/toolbelt-consumer.json` nem em servidores MCP.
- Não faz refatoração do código interno dos subprojetos (`aurora-web/`, `ElysianCorp/`, `tone-lab-site/`) nesta OS de governança.

## 4. Restrições herdadas (Verbatim da OS)
- Manter integralmente as conexões com o ecossistema Aurora (`C:\Projetos\Aurora`), sistemas, agentes, skills, MCPs e `.aurora/toolbelt-consumer.json`.
- Descontinuar obrigatoriamente os modelos de design atuais, incluindo Dark Theme, Dark Editorial, Mad Lab Theme, WebGL/Three.js r128 decorativo e gates subjetivos de beleza.
- Sincronizar a Doutrina Operacional com `C:\Projetos\Aurora\docs\AGENTS\DOCTRINE.md` (incluindo Emenda v9.1, validação em duas vias `reprova`, cobertura adversarial de gates `EXIT=1`, mapeamento 1:1 plano-relatório e proibição de ficar verde por remoção).
- Implementar as skills `agentic-web-architect` e `b2b-ai-outbound-architect` com bloco `## Mesh Contract` válido contra `C:\Projetos\Aurora\docs\specs\skill_mesh\skill.schema.json`.
- Usar exclusivamente `document.modelContext` (Chrome 150+ WebMCP Declarative e Imperative APIs), sendo proibido usar a API depreciada `navigator.modelContext`.
- Exigir que toda página, seção, serviço e notícia siga a arquitetura Dual-Surface: SSR/SSG imediato, espelhamento Markdown (`Accept: text/markdown` e rotas `.md`), JSON-LD `@graph`, `/.well-known/agent-card.json` (A2A v0.3+), `/llms.txt`, Spec-Sheet Architecture, Citation-Magnet Pattern e Critério Formal de Aceite de Interface da Aurora (`criterio_formal_de_aceite_de_interface.md`).
- Respeitar estritamente a regra Vault append-only: nada é deletado nem reescrito em `docs/Vault/`, documentos e skills estéticas obsoletas recebem `deprecated: true`.
- Nunca capturar exit code com pipe (`cmd | tail`); usar redirecionamento ou execução direta verificando `EXIT=$?`.

## 5. Blast Radius Previsto

<!-- BLAST_RADIUS:INICIO -->
- Arquivos criados (7):
  - `docs/Vault/OS-Evidence/OS-MADLAB-AGENTIC-PIVOT-20261016-001/OS-MADLAB-AGENTIC-PIVOT-20261016-001.md`
  - `docs/Vault/OS-Evidence/OS-MADLAB-AGENTIC-PIVOT-20261016-001/PLAN.md`
  - `docs/Vault/Decisions/DEC-MADLAB-AGENTIC-PIVOT-002.md`
  - `docs/AGENTS/DOCTRINE.md`
  - `CLAUDE.md`
  - `.aurora/skills/agentic-web-architect/SKILL.md`
  - `.aurora/skills/b2b-ai-outbound-architect/SKILL.md`
  - `scripts/check-madlab-governance.mjs`
  - `scripts/test-madlab-governance-reprova.mjs`
- Arquivos atualizados (17):
  - `AGENTS.md`
  - `GEMINI.md`
  - `.aurora/domain-policy.json`
  - `.agents/rules/designmanualposthero.md`
  - `project-manifest.json`
  - `.aurora/skills/qa-review/SKILL.md`
  - `.aurora/skills/ceo-web/SKILL.md`
  - `.aurora/skills/ceo-copy/SKILL.md`
  - `.aurora/skills/ceo-design/SKILL.md` (marcação `deprecated: true`)
  - `.aurora/skills/ceo-effects/SKILL.md` (marcação `deprecated: true`)
  - `.aurora/skills/ceo-3d/SKILL.md` (marcação `deprecated: true`)
  - `.aurora/skills/ceo-art-direction/SKILL.md` (marcação `deprecated: true`)
  - `.aurora/skills/cinematic-grammar/SKILL.md` (marcação `deprecated: true`)
  - `.aurora/skills/taste-design/SKILL.md` (marcação `deprecated: true`)
  - `.aurora/skills/design-md/SKILL.md` (marcação `deprecated: true`)
  - `.aurora/skills/ceo-critique-theater/SKILL.md` (marcação `deprecated: true`)
  - `docs/brand/MANUAL_DA_AGENCIA.md` (marcação `deprecated: true`)
  - `docs/brand/mad-lab-aurora-dna-v2.1.0.md` (marcação `deprecated: true`)
- Artefatos de fechamento (4):
  - `docs/Vault/OS-Evidence/OS-MADLAB-AGENTIC-PIVOT-20261016-001/EVIDENCE_FINAL.md`
  - `docs/Vault/OS-Evidence/OS-MADLAB-AGENTIC-PIVOT-20261016-001/QA_REPORT.md`
  - `docs/Vault/Token-Ledger/2026-10-16/OS-MADLAB-AGENTIC-PIVOT-20261016-001.json`
  - `docs/Vault/Threads/2026-10-16/agentic-pivot-reorganization.md`
<!-- BLAST_RADIUS:FIM -->

## 6. Micro-Etapas (com Gate e Condição de Falha)

### ME-0 — Conformidade do plano (10 min)
- **Ação:** Executar `check-plan-conformance.mjs` de `C:\Projetos\Aurora\packages\tooling\scripts\check-plan-conformance.mjs` contra a OS e este plano.
- **Gate:** `EXIT=0`, `ausentes=0`, `fracas=0`, `secoes-ausentes=0`, `blast-radius-ausente=false`.
- **Condição de falha:** Se falhar, bloqueia imediatamente o início da ME-1 e exige correção do `PLAN.md`.

### ME-1 — Decisão Arquitetural e Doutrina Unificada (`DOCTRINE.md`, `AGENTS.md`, `GEMINI.md`, `CLAUDE.md`) (15 min)
- **Ação:** Criar `docs/Vault/Decisions/DEC-MADLAB-AGENTIC-PIVOT-002.md` e `docs/AGENTS/DOCTRINE.md`, e sincronizar `AGENTS.md`, `GEMINI.md` e `CLAUDE.md` na raiz do `MadLabAurora` unindo a Doutrina Operacional de `C:\Projetos\Aurora\docs\AGENTS\DOCTRINE.md` (Emenda v9.1) e a governança de Produção Web Agêntica.
- **Gate:** Existência dos 5 arquivos via `Test-Path` e verificação de que o bloco `<!-- DOCTRINE:START --> ... <!-- DOCTRINE:END -->` é idêntico nos 4 arquivos de doutrina (`EXIT=0`).
- **Condição de falha:** Se falhar, bloqueia o avanço para a ME-2 e corrige a divergência na etapa.

### ME-2 — Criação e Validação de Contrato das Skills `agentic-web-architect` e `b2b-ai-outbound-architect` (15 min)
- **Ação:** Criar `.aurora/skills/agentic-web-architect/SKILL.md` e `.aurora/skills/b2b-ai-outbound-architect/SKILL.md` com instruções completas e bloco `## Mesh Contract` compatível com `C:\Projetos\Aurora\docs\specs\skill_mesh\skill.schema.json`.
- **Gate:** Validação via script Python/jsonschema contra `C:\Projetos\Aurora\docs\specs\skill_mesh\skill.schema.json` retornando `EXIT=0`.
- **Condição de falha:** Se falhar, bloqueia o avanço para a ME-3 e corrige o contrato JSON das skills.

### ME-3 — Atualização de `qa-review`, `ceo-web`, `ceo-copy` e Depreciação Formal do Legado Estético (15 min)
- **Ação:** Atualizar `qa-review`, `ceo-web` e `ceo-copy` para o padrão v9.1 + Dual-Surface + `criterio_formal_de_aceite_de_interface.md`; marcar `deprecated: true` / `status: deprecated` nas 8 skills estéticas e nos 2 documentos principais de `docs/brand/`; atualizar `.agents/rules/designmanualposthero.md`, `.aurora/domain-policy.json` e `project-manifest.json`.
- **Gate:** Parse válido de `.aurora/domain-policy.json` e `project-manifest.json` (`ConvertFrom-Json`) e checagem de presença de `deprecated: true` nos 10 arquivos descontinuados (`EXIT=0`).
- **Condição de falha:** Se falhar, bloqueia o avanço para a ME-4 e corrige o arquivo inválido.

### ME-4 — Gate Determinístico de Governança Local + Teste Adversarial (`reprova`) e Fechamento da OS (15 min)
- **Ação:** Criar `scripts/check-madlab-governance.mjs` e `scripts/test-madlab-governance-reprova.mjs`, executar ambos e registrar `EVIDENCE_FINAL.md`, `QA_REPORT.md`, Token Ledger e Thread.
- **Gate:** `node scripts/check-madlab-governance.mjs` → `EXIT=0` e `node scripts/test-madlab-governance-reprova.mjs` → `EXIT=0`.
- **Condição de falha:** Se falhar, bloqueia o fechamento da OS até que a suíte de sabotagem passe sem erros.

## 7. Rollback por Etapa
- **ME-0:** Ajustar `PLAN.md` antes de tocar arquivos do repositório.
- **ME-1:** `git checkout -- AGENTS.md GEMINI.md` e reversão dos novos arquivos `CLAUDE.md`, `docs/AGENTS/DOCTRINE.md` e `docs/Vault/Decisions/DEC-MADLAB-AGENTIC-PIVOT-002.md`.
- **ME-2:** Reversão de `.aurora/skills/agentic-web-architect/SKILL.md` e `.aurora/skills/b2b-ai-outbound-architect/SKILL.md`.
- **ME-3:** `git checkout -- .aurora/skills/ .agents/rules/designmanualposthero.md .aurora/domain-policy.json project-manifest.json docs/brand/`.
- **ME-4:** Reversão de `scripts/check-madlab-governance.mjs` e `scripts/test-madlab-governance-reprova.mjs`.

## 8. Critério de Aceite
1. `node "C:\Projetos\Aurora\packages\tooling\scripts\check-plan-conformance.mjs" --os "c:\Projetos\MadLabAurora\docs\Vault\OS-Evidence\OS-MADLAB-AGENTIC-PIVOT-20261016-001\OS-MADLAB-AGENTIC-PIVOT-20261016-001.md" --plan "c:\Projetos\MadLabAurora\docs\Vault\OS-Evidence\OS-MADLAB-AGENTIC-PIVOT-20261016-001\PLAN.md"` → `EXIT=0`.
2. `node "c:\Projetos\MadLabAurora\scripts\check-madlab-governance.mjs"` → `EXIT=0`.
3. `node "c:\Projetos\MadLabAurora\scripts\test-madlab-governance-reprova.mjs"` → `EXIT=0`.
4. `git diff .aurora/toolbelt-consumer.json` → vazio (`EXIT=0`).

## 9. Destino da Evidência
- `c:\Projetos\MadLabAurora\docs\Vault\OS-Evidence\OS-MADLAB-AGENTIC-PIVOT-20261016-001\`
