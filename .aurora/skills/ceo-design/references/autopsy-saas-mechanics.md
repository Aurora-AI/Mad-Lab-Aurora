# Autópsia de Engenharia: Desconstrução de Truques de UI

**Documento:** Manual de Auditoria e Reconhecimento Técnico
**Referencial:** Veto de Tendência SaaS
**Classificação:** Engenharia Reversa / Anti-Padrão
**Status:** REGISTRADO (Scope: Global)

---

## 1. Decomposição Mecânica (A Anatomia da Ilusão)

O efeito consiste em um "sanduíche" de 5 camadas que simulam interatividade através de manipulação de DOM e propriedades de renderização CSS.

### Nó 1: A Malha de Ruído (DOM/JS)
- **Mecânica:** Função JavaScript gerando strings randômicas em loop.
- **Impacto:** Cria uma textura visual dinâmica que serve de base para o ruído.

### Nó 2: O Motor de Reatividade (Event Listener)
- **Mecânica:** `mousemove` trigger.
- **Impacto:** Recalcula a string a cada movimento, criando a ilusão de "decodificação" em tempo real.

### Nó 3: A Máscara de Revelação (CSS Mask-Image)
- **Mecânica:** `radial-gradient` com opacidade variável.
- **Impacto:** Oculta a maior parte do ruído, revelando apenas a região sob o cursor.

### Nó 4: O Rastreamento de Eixo (CSS Variables)
- **Mecânica:** Passagem de coordenadas X/Y do JS para o CSS via variáveis (`--x`, `--y`).
- **Impacto:** Sincroniza a posição da máscara com o hardware do mouse.

### Nó 5: Injeção de Identidade (Mix-Blend-Mode)
- **Mecânica:** Propriedade `color` ou `overlay` em uma camada de gradiente superior.
- **Impacto:** "Pinta" os caracteres randômicos com as cores da marca.

---

## 2. Diagnóstico de Fraqueza (Veredito CEO-Design)

1. **Dependência de Ciclo de CPU:** O efeito exige repinturas constantes (repaints) que sacrificam a performance em prol da cosmética.
2. **Ausência de Caráter Estático:** Se o script for removido, o design colapsa. Reprovado no teste de permanência Draplin.
3. **Escalabilidade Nula:** Inútil para identidades físicas ou dispositivos sem hover.

## 3. Heurística de Auditoria para o Agente

Ao revisar um código ou proposta, o CEO-Design deve procurar por:
- `mix-blend-mode` usado como motor principal de legibilidade.
- `mask-image` dinâmico atrelado a `mousemove`.
- Geração de texto randômico via JS para fins ornamentais.

**Ação:** VETO IMEDIATO. Redirecionar para tipografia monumental estática.

---

## 4. Mapeamento de Grafo (JSON)

```json
{
  "agent": "ceo-design",
  "node_type": "EngenhariaReversa",
  "domain": "design_desenvolvimento",
  "core_insight": "O efeito de texto dinâmico estilo Evervault é uma construção aditiva que mascara a ausência de engenharia tipográfica real.",
  "dark_editorial_alignment": "conflita",
  "relations": [
    { "type": "AUDITA", "target": "AntiTendencia:RuidoSaaS" }
  ]
}
```
