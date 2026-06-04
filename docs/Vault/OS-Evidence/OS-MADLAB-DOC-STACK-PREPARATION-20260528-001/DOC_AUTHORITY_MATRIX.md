# Matriz de Autoridade e Delimitação de Escopos

**OS ID:** `OS-MADLAB-DOC-STACK-PREPARATION-20260528-001`  
**Fase:** Diagnóstico e Alinhamento de Hierarquia  
**Status:** VALIDADO

---

## 1. Hierarquia Linear de Autoridade

Para garantir integridade arquitetural e evitar contradições operacionais entre os agentes de IA e desenvolvedores, a ordem linear de precedência documental fica estabelecida como:

1.  **`MANUAL_DA_AGENCIA.md`** (Constituição Criativa Máxima do Mad Lab)
2.  **`domain-policy.json`** (Soberania Técnica, Capabilities e Proteção contra Duplicações)
3.  **`mad-lab-aurora-dna-v2.1.0.md`** (Identidade de Tom, Escrita e Regras NLU)
4.  **`ELYSIAN_BRAND_KIT_v1.1.md`** (Diretriz Visual da Marca Mãe Elysian)
5.  **`designmanualposthero.md`** (Regras Táticas de Composição e Interface Post-Hero)
6.  **`DESIGN_LIBRARY.md`** (Biblioteca Física de Efeitos e Shaders)
7.  **Referências locais e Brand ID** (Corpus de Consulta Estática, sem poder normativo)

---

## 2. Matriz de Arbitragem por Tipo de Conflito

Quando dois ou mais documentos apresentarem diretrizes concorrentes ou divergentes sobre o mesmo elemento, o conflito será resolvido direcionando a decisão à autoridade arbitral correspondente:

| Tipo de conflito | Documento arbitral | Nível de Autoridade |
|---|---|:---:|
| **Escopo do Mad Lab** (papel do laboratório, governança criativa) | `MANUAL_DA_AGENCIA.md` | Constitucional |
| **Prioridade do Comandante Rodrigo** (critérios estéticos gerais) | `MANUAL_DA_AGENCIA.md` | Constitucional |
| **Capability / integração / Trustware técnico** (segurança, rede, Álvaro) | `domain-policy.json` | Soberania Técnica |
| **Identidade criativa / tom / NLU** (como a IA escreve e se comporta) | `mad-lab-aurora-dna-v2.1.0.md` | Identidade Sensorial |
| **Marca Elysian** (logotipo, Emerald, tipografia Söhne corporativa) | `ELYSIAN_BRAND_KIT_v1.1.md` | Identidade Visual |
| **Layout pós-hero / seções abaixo da dobra** (estrutura tática de grades) | `designmanualposthero.md` | Regras de Layout |
| **Efeitos / shaders / WebGL / motion técnico** (código GLSL, gsap loops) | `DESIGN_LIBRARY.md` | Biblioteca Técnica |
| **Inspiração visual** (efeitos de Aino, Exo Ape, Lusion, screenshots) | *Referências locais* | Sem autoridade normativa |

---

## 3. Delimitação e Separação de Escopos

### 3.1 Camada Constitucional vs. Camada Tática
*   **Regras Constitucionais (`MANUAL_DA_AGENCIA.md`, `mad-lab-aurora-dna.md`):** Regem o *porquê* das decisões, a postura narrativa, a lei de contraste dos dois mundos, o orçamento de hardware e o tom de voz da agência. Não contêm seletores CSS, comandos npm específicos ou códigos GLSL hardcoded.
*   **Regras Táticas e Bibliotecas (`designmanualposthero.md`, `DESIGN_LIBRARY.md`):** Regem o *como* da implementação. Contêm tamanhos de fontes, margens, seletores, regras de motion estritas e referências a fragmentos de código reutilizáveis. Devem obedecer estritamente à camada constitucional.

### 3.2 Identidade Corporativa Elysian vs. Flexibilidade dos Subprojetos
*   **A Marca Mãe (`ELYSIAN_BRAND_KIT_v1.1.md`):** Rege a marca mãe **Elysian** e o site institucional central. Seus tokens (off-white, fonte Söhne, acento Emerald singular) servem para garantir a unidade corporativa.
*   **Subprojetos do Mad Lab:** O Mad Lab Aurora constrói experiências e produtos para múltiplas verticais (Lex, CRM, laboratórios). Para estes subprojetos, a paleta central da Elysian e tipografia Söhne corporativa não podem ser uma prisão. Os subprojetos podem introduzir paletas de cores secundárias dedicadas de forma governada (como o Amber para o Mad Lab ou Índigo para o CRM) e tipografias e grids experimentais, desde que:
    1.  Respeitem a postura narrativa do **Dark Editorial** (luxo invisível, contraste e proporção);
    2.  Sejam documentados como exceção de escopo aprovada pelo Diretor de Design (`approved_by`).

---

## 4. Análise de Sobreposições Críticas

O inventário revelou três áreas de sobreposição que devem ser mitigadas no plano de reescrita:
1.  **Tipografia Técnica:** O `ELYSIAN_BRAND_KIT_v1.1.md` define JetBrains Mono como fonte técnica para metadados, enquanto o `designmanualposthero.md` detalha o comportamento tipográfico de Voz 2 (técnica). A Voice 2 deve herdar e seguir as parametrizações do Brand Kit, sem criar conflitos de escala.
2.  **Cores e Opacidades:** O `designmanualposthero.md` rege opacidades de fundo cinza, mas o Brand Kit possui tokens específicos JSON de opacidade de texto e superfícies. Os arquivos CSS de produção devem consumir os tokens JSON centrais do Brand Kit.
3.  **Física e WebGL:** Há duplicação da explicação de "Profundidade Impossível" e "Regra do Silêncio (0.8s)" entre o `MANUAL_DA_AGENCIA.md` e o `mad-lab-aurora-dna-v2.1.0.md`. A parte técnica da física deve ser delegada à `DESIGN_LIBRARY.md` e a regra filosófica/comportamental deve ficar exclusivamente no `MANUAL_DA_AGENCIA.md`.
