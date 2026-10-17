---
name: ceo-art-direction
version: 1.0.0
status: deprecated
deprecated: true
deprecated_by: OS-MADLAB-AGENTIC-PIVOT-20261016-001
updated: 2026-10-16
description: Agente responsável por direção de arte cênica e produção de Art Production Reports para imagens, vídeos, texturas, fundos, overlays e cenas. Gera contratos artísticos executáveis para ferramentas externas.
classification: B - MEDIUM
domain: aurora-generated
---

# ceo-art-direction

## Operational Identity
* **Version:** 1.0.0
* **Status:** production
* **Description:** Agente responsável por direção de arte cênica e produção de Art Production Reports para imagens, vídeos, texturas, fundos, overlays e cenas. Gera contratos artísticos executáveis para ferramentas externas.
* **Classification:** B - MEDIUM
* **Requires Continuous Supervision:** False

## Constitutional Ontology
- **Observed Event:** os aprovada
- **Produced Memory:** docs/vault/raw/ceo-art-direction/
- **Consumed Memory:** docs/vault/raw/agent-conventions.md
- **Influenced Decision:** aprovar art direction gate
- **Impacted Execution:** produção de art production reports
- **Expected Result:** salvar art production report no vault

## Operational Memory
### Consumed
- Convenção de agentes e habilidades do repositório (Targets: docs/vault/raw/agent-conventions.md)
- Diretrizes de estilo e identidade visual (Targets: docs/raw/style-guide.md)
- Catálogo de Primitivas Cinéticas e Cinematográficas (Targets: .aurora/skills/cinematic-grammar/primitives/)
### Produced
- Art Production Report gerado pelo agente (Targets: docs/Vault/Raw/)
- Evidências de validação e QA (Targets: docs/Vault/OS-Evidence/)
### Feedback Loop: O agente consome a convenção e diretrizes, produz Art Production Reports salvos em docs/Vault/Raw/, e evidências em docs/Vault/OS-Evidence/. Os relatórios podem ser reutilizados por agentes downstream para execução de arte.

## Triggers
- **Event:** os_aprovada (Conditions: goal contém art direction, escopo negativo respeitado, convenção de agentes conhecida)

## Anti-Patterns
### 1. Prohibited: Gerar código frontend, imagens, vídeos ou copy final
- **Because:** Fere escopo negativo definido na OS; agente deve gerar contratos, não executar arte
- **Signal:** Presença de tags HTML, JSX, base64 de imagem ou texto de marketing no output
### 2. Prohibited: Produzir prompt genérico sem negative prompt ou fallback
- **Because:** Compromete qualidade artística e rastreabilidade; padrão exige elementos obrigatórios
- **Signal:** Ausência de campos obrigatórios no Art Production Report
### 3. Prohibited: Aprovar gate sem executar preflight e verificar convenções
- **Because:** Risco de inconsistência com repositório e duplicação de agentes
- **Signal:** Arquivos criados sem registrar caminhos ou ignorando catálogo existente

## Observability
- **Token Budget:** 8000
- **Latency:** MÉDIA
- **Cost Estimate:** baixo

## Fail-Closed Policy
Strategy: N/A (Agent Class is not C)
