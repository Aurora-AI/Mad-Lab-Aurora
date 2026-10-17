# ceo-art-direction (Agente de Direção de Arte Cênica)

Este agente preenche a lacuna entre a curadoria visual (`agente-awwwards`) e o desenvolvimento de componentes/layouts (`ceo-design`, `ceo-effects`, `ceo-web`).

Ele cria contratos de produção artística para assets externos (imagens, vídeos, texturas, fundos, overlays), garantindo conformidade com o Manual da Agência v3.0.0 e erradicando qualquer sinal de IA genérica.

## Estrutura de Diretórios
```
.aurora/skills/ceo-art-direction/
├── agent.md
├── system-prompt.md
├── README.md
├── contracts/
│   ├── art_direction_brief.schema.json
│   ├── art_production_report.schema.json
│   ├── scene_card.schema.json
│   └── visual_world_bible.schema.json
├── templates/
│   ├── art-production-report.md
│   ├── scene-card.md
│   └── visual-world-bible.md
├── gates/
│   └── qa-art-direction-gate.md
├── examples/
│   └── trustware-primary-signal-field.md
└── evals/
    ├── golden_inputs/
    └── golden_outputs/
```
