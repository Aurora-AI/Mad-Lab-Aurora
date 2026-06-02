# Aurora Cognitive Assets — Content Engine P01 🚀
**Unidade de Processamento de Dados e Cognição — Versão 0.1**

---

## 📍 Visão Geral
Este módulo em Python é o motor de processamento do projeto **Aurora Cognitive Assets**. Ele é responsável por:
1. Ler arquivos brutos em `docs/Vault/`.
2. Aplicar as Skills de Orquestração (`skills/`).
3. Interfacear com os Agentes Locais (`agents/`).

---

## 🛠️ Roadmap de Desenvolvimento
- [ ] [P01] Script de Ingestão: Conversão de `.md` bruto para estrutura de capítulos.
- [ ] [P02] Auditoria Comportamental: Script de validação OQS Automático.
- [ ] [P03] Exportador Multifomato: PDF, Notion, LinkedIn Post.

---

## ⚙️ Configuração Inicial
```python
# Placeholder para inicialização do motor de processamento
import os

VAULT_PATH = "../../docs/Vault/"
SKILLS_PATH = "../../skills/"

def process_extractions():
    print("Iniciando varredura no Vault...")
    # Lógica de orquestração via agentes em breve
    pass
```

## Integração com a Infoproduct Factory

Este produto consome a fabrica por API tipada.

- Service: `@aurora/infoproduct-factory-service`
- Base URL: `INFOPRODUCT_FACTORY_BASE_URL`
- Token opcional: `INFOPRODUCT_FACTORY_TOKEN`

Cliente local:

- `apps/content-engine/client/infoproduct_factory_client.py`
- `apps/content-engine/client/run_infoproduct_pipeline.py`
- `apps/content-engine/client/refinement_pipeline.py`
- `apps/content-engine/client/run_refinement_pipeline.py`

Exemplo:

```bash
python apps/content-engine/client/run_infoproduct_pipeline.py --brief brief.json
```

## Pipe de Refinamento no App

O `content-engine` agora possui uma superficie propria para executar o pipe de refinamento do consumidor e produzir duas saidas:

- resultado tecnico completo do run
- resumo legivel para avaliacao humana

Entrypoint:

```bash
python apps/content-engine/client/run_refinement_pipeline.py \
  --payload-dir docs/Vault/OS-Evidence/apo-real-brief-test \
  --output-dir docs/Vault/OS-Evidence/apo-real-brief-test \
  --print-summary
```

Saidas esperadas no `output-dir`:

- `refinement-result.json`
- `final-run-record.json`
- `refinement-summary.md`
