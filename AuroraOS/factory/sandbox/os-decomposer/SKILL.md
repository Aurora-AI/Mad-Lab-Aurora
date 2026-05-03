# Skill: os-decomposer
---
id: os-decomposer
name: OS Decomposer
description: Decomposes complex Operating Orders (OS) into a DAG of atomic micro-tasks.
activation:
  mode: delegated
  activated_by: ["product-integrity-engineer", "master-skill"]
  semantic_triggers: ["@os-decompose", "/decompose-os"]
capabilities:
  provides: ["os_decomposition", "dependency_graph"]
  depends_on: []
  can_delegate_to: ["auto-repair-agent"]
  emits_artifacts: ["decomposed_os.json"]
---

## Overview
A OS Decomposer é responsável por atomizar tarefas complexas para garantir que o `repair_loop` opere em passos pequenos, testáveis e de baixo risco.

## Usage
Acione esta skill enviando o caminho de uma OS em Markdown.
Exemplo: `/decompose-os path/to/OS-004.md`

## Rules
1. Cada micro-tarefa deve ser executável em ≤ 120 segundos.
2. Cada micro-tarefa deve ter um teste de aceitação determinístico.
3. Mudanças de código acima de 50 linhas forçam a subdivisão da tarefa.
