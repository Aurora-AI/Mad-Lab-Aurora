# TONE LAB OS: MASTER SPECIFICATION (v3.0)

> Baseline arquitetural definitivo do Tone Lab OS.

## 1. Identidade e Propósito
O Tone Lab OS não é um "Headless CMS" nem um "blog de áudio". Ele é um **Knowledge Operating System**.
Seu propósito não é publicar conteúdo editorial, mas sim **registrar conhecimento, relacionar entidades, acompanhar estados e tomar decisões de engenharia e manufatura**.

## 2. A Fundação de Dados (Knowledge Graph)
O sistema opera através do polimorfismo em duas camadas distintas.

### Camada 1: Entity Types (O que o objeto é)
As unidades lógicas do sistema não são páginas, são "Entidades".
- `Equipment` (Físico: Guitarras, Amplificadores, Gabinetes)
- `Plugin` / `Digital` (Software, DSP)
- `Project` (Engenharia, Modificações, Construções)
- `Research` (Papers, Artigos, Teses)
- `Measurement` (Resultados de Bancada)
- `Purchase` (Leads e orçamentos)
- `Document` / `Note`

### Relacionamentos de Primeiro Nível
As entidades não existem em vácuo. Um relacionamento é mais forte que uma tag.
Ex: `Marshall Origin 50C (Equipment) -> Utilizado em -> Projeto Amp Signature Proto01 (Project)`.

---

## 3. A Arquitetura Visual (Dual-Mode UX)

A interface reflete o contraste entre descoberta e engenharia pura.

### 3.1. Marshall Store Mode (Descoberta)
**O que é:** O ponto de entrada. Um catálogo visual inspirado em e-commerces premium (como o da própria Marshall).
- **UI:** Fundo Escuro (`#050505`), grandes imagens brutais (Brutalismo Comercial).
- **Navegação:** Filtros simples no topo (ALL, GUITARS, AMPS).
- **Conteúdo dos Cards:** Apenas a fotografia do ativo e nomenclaturas essenciais. Sem ficha técnica.
- **Sensação:** "Estou explorando uma loja".

### 3.2. Tone Lab Detail Mode (Engenharia)
**O que é:** O dossiê aberto após o clique no catálogo.
- **UI:** Fundo Claro/Ethereal (`#F8F7F3`), tipografia técnica (monospace e sans limpa), tabelas de dados.
- **Header Modular:** Contém a classificação do objeto, Status (Planned/Owned) e Prioridade. Navegação em abas transversais (Architecture, Schematics, Bench Test).
- **Módulos Especializados:** O layout se adapta à Entidade. Se for um *Amp Project*, exibe topologia e válvulas. Se for *Research*, exibe links e sumarizações.
- **Sensação:** "Abri o manual técnico do projeto na bancada".

---

## 4. O Coração do OS: Ingestão de Dados (Inbox)

Para ser um "arquivo vivo alimentado constantemente", a ingestão de dados tem precedência sobre a exibição.
**Princípio Maior:** A interface nunca deve perguntar por um campo que possa ser inferido pelo contexto. O atrito de entrada deve ser zero.

### 4.1. O Pipeline Estrutural
`Capture → Structure → Relate → Validate → Render`

### 4.2. Universal Entry (Command Palette)
- **Atalho:** `Ctrl + K` ou botão Global `[ + ]`.
- **Inteligência Contextual:** Se ativada *dentro* do dossiê de um equipamento, a Palette já amarra a nova entidade ao equipamento em questão (Auto-Relate).

### 4.3. Modos de Captura
- **Quick Capture:** Inserção imediata (uma URL, um preço, um bloco de texto). Requer quase zero tipagem e cai na *Inbox* com o status `NEEDS REVIEW`.
- **Structured Create:** Um modal largo e de design limpo. Baseado na seleção do usuário, os campos mudam organicamente (Polimorfismo de Forms).

---

## 5. Renderização e Topologia Dinâmica (Signal Path)

Dentro do Dossiê, a Cadeia de Áudio (*Signal Path & Audio Flow*) atua como uma renderização do grafo de dependências do hardware.
- Em vez de um infográfico estático, o React consome o array `signalChain` do banco de dados e desenha a esteira.
- O nó do equipamento atual que o usuário está visualizando recebe destaque automático (`Under Test`).

---
*Fim da Especificação.*
