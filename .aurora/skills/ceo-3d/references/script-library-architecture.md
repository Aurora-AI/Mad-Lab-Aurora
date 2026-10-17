# Script Library Architecture

O inchaço do Vault principal da Aurora é estritamente proibido. Scripts 3D utilitários gerados pelo `ceo-3d` NÃO devem ir para `docs/Vault/`.

Eles devem residir em:
`aurora-visual-assets/blender_scripts/`

## Taxonomia e Nomenclatura

Os scripts devem ser organizados em subpastas lógicas, geradas sob demanda pelo agente:

```text
aurora-visual-assets/blender_scripts/
├── architecture/       (Salas, paredes, plantas, pisos)
│   ├── arch_sala_4x4_base.py
│   └── arch_janela_param.py
├── primitives/         (Componentes visuais abstratos, DNA visual)
│   ├── prim_dark_sphere.py
│   └── prim_glass_box.py
└── environments/       (Cenários completos e complexos)
    └── env_hero_bg_scene.py
```

## Reaproveitamento (Reuse)
Antes de gerar um script 3D do zero, o `ceo-3d` ou o Orquestrador pode varrer esta pasta buscando arquivos com sufixos semelhantes, lendo-os, e ajustando as variáveis no topo do arquivo.

## Estrutura Interna do Script
Todo script salvo nesta biblioteca deve conter no topo:
1. `__docstring__` descrevendo o que o modelo faz.
2. Bloco de variáveis configuráveis (parâmetros de entrada, ex: `width`, `height`, `material_color`).
3. Execução.
