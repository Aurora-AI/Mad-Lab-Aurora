---
deprecated: true
status: deprecated
deprecated_by: OS-MADLAB-AGENTIC-PIVOT-20261016-001
superseded_by: docs/AGENTS/DOCTRINE.md
---

# Mad Lab Aurora — Manual da Agência (Constituição e Roteador) [DEPRECATED]
**Versão:** 3.0.0  
**Data:** 28 de Maio de 2026  
**Status:** 🔴 DEPRECATED (`deprecated: true`) — Substituído por `docs/AGENTS/DOCTRINE.md`, `AGENTS.md` e `GEMINI.md` (`DEC-MADLAB-AGENTIC-PIVOT-002`)  
**Localização canônica:** `MadLabAurora/docs/brand/MANUAL_DA_AGENCIA.md`  

---

> Este documento é a Constituição Criativa máxima do Mad Lab Aurora.  
> Rege a governança de direção visual e estabelece o Roteamento Central de toda a malha documental.  
> Todo ativo e subprojeto criativo responde a esta Constituição.  

---

## 1. Posicionamento e Governança Organizacional

### 1.1 O Que É o Mad Lab Aurora
O Mad Lab Aurora **não é um projeto vertical**. Ele é a **camada e o braço criativo da Aurora**, responsável pela direção de arte visual, craft de interface, motion design, experimentação em WebGL e construção de experiências de alto impacto para todo o ecossistema. 

Sua função é fornecer ativos visuais, consultoria de interface e padrões estéticos para os múltiplos projetos verticais localizados abaixo de sua governança (como o [Elysian Lex](file:///C:/Projetos/MadLabAurora/ElysianCorp/) no jurídico e o CRM / Silent Operator no comercial).

### 1.2 O Mapa de Relações
```text
                  ┌───────────────────────────────┐
                  │            ELYSIAN            │  ◄── Marca Mãe Corporativa
                  └───────────────┬───────────────┘
                                  │
                  ┌───────────────▼───────────────┐
                  │        MAD LAB AURORA         │  ◄── Camada e Braço Criativo
                  └──────┬────────────────┬───────┘
                         │                │
       ┌─────────────────▼───┐        ┌───▼─────────────────┐
       │   PROJETOS VERTICAIS │        │      OZZMOSIS       │
       │  (Elysian Lex / CRM) │        │ (Fábrica / Conductor)│
       └─────────────────────┘        └─────────────────────┘
```

*   **Elysian (Marca Mãe):** Define o núcleo corporativo e as diretrizes estratégicas de identidade geral (Brand Kit).
*   **Projetos Verticais (Lex/CRM):** Consomem os ativos estéticos e regras geradas pelo Mad Lab, adaptando-os a seus escopos de negócios específicos.
*   **Ozzmosis (Fábrica):** Fonte de libraries, infraestrutura de dados e conectores de backend (`Conductor`). O Mad Lab integra-se à fábrica sob regras rígidas de não-duplicação e soberania do Alvaro.

---

## 2. A Regra Estética Absoluta

Nada que seja concebido, desenhado ou implementado pelo Mad Lab Aurora pode parecer produto gerado de forma genérica por IAs. O critério definidor de aceitação visual é:

> **"Nada que saia do Mad Lab Aurora pode parecer site feito por IA."**

O laboratório de craft digital deve ativamente combater e eliminar os 6 sinais de alerta de genericidade (simetria linear crua, tipografias padrão de sistema como Voz Display, gradientes neon SaaS, border-radius e sombras clichês de templates comerciais, e motion decorativo sem gravidade).

---

## 3. O Alinhamento da Física Visual (Progressivo)

A profundidade impossível (Z-axis real e luz calculada em GPU) e a quebra das leis da física continuam sendo a **linha de chegada criativa (ambição máxima) do laboratório**, e não uma obrigação inicial para páginas de descompressão ou landing pages simples.

*   **Páginas Simples / Descompressão:** Foco na proporção áurea, tipografia monumental limpa e espaço negativo respirável (mundo luminoso), operando de forma leve.
*   **Sistemas Complexos / Imersivos:** Adoção de WebGPU/WebGL avançado e física com massa real à medida que a densidade narrativa do produto exige a tensão do mundo dark. O conhecimento adquirido nos layouts mais simples deve acumular-se de forma a alavancar a construção dos sistemas complexos.

---

## 4. Roteador Central da Pilha Documental

Para manter a integridade visual sem redundâncias ou duplicações em código-fonte, a pilha documental do Mad Lab Aurora é descentralizada e roteada a partir desta Constituição conforme as regras de conflito estabelecidas em [DOC_CONFLICT_RULES.md](file:///C:/Projetos/MadLabAurora/docs/Vault/OS-Evidence/OS-MADLAB-DOC-STACK-PREPARATION-20260528-001/DOC_CONFLICT_RULES.md):

```text
                                MANUAL_DA_AGENCIA.md
                                (Constituição Central)
                                          │
        ┌───────────────────┬─────────────┴─────────────┬──────────────────┐
        ▼                   ▼                           ▼                  ▼
domain-policy.json   ELYSIAN_BRAND_KIT_v1.1.md   designmanualposthero.md  DESIGN_LIBRARY.md
(Soberania Técnica)  (Identidade e Logo)         (Layouts e Vozes)        (Efeitos e Shaders)
```

1.  **Soberania Técnica e Capabilites:** Regidas exclusivamente pelo [domain-policy.json](file:///C:/Projetos/MadLabAurora/.aurora/domain-policy.json).
2.  **Identidade Visual Elysian, Logo e Emerald:** Regidos exclusivamente pelo [ELYSIAN_BRAND_KIT_v1.1.md](file:///C:/Projetos/MadLabAurora/docs/brand/ELYSIAN_BRAND_KIT_v1.1.md).
3.  **Matriz de Grid, Tipografia Post-Hero (Vozes) e Animações:** Regidas exclusivamente pelo [designmanualposthero.md](file:///C:/Projetos/MadLabAurora/.agents/rules/designmanualposthero.md).
4.  **Cortes de Código de Shaders, Texturas e Efeitos WebGL:** Regidos exclusivamente pelo catálogo técnico da [DESIGN_LIBRARY.md](file:///C:/Projetos/MadLabAurora/docs/Vault/DESIGN_LIBRARY.md).
5.  **Dívida Visual e Desvios Estéticos Congelados:** Controlados pelo arquivo governado [.aurora/design-debt-baseline.json](file:///C:/Projetos/MadLabAurora/.aurora/design-debt-baseline.json).

---

## 5. Os Gates de Qualidade e Governança Criativa

Nenhum design ou interface é promovido para a malha ativa de produção sem passar pelos quatro gates de conformidade:

### 5.1 O Gate de Design (CEO-Design)
*   *Filtro:* Stress estrutural e fidelidade ao DNA visual.
*   *Validação:* Garante a proporção áurea, legibilidade editorial, espaço de descompressão e o teste de "Dark Editorial como Postura".
*   *Critério de Rejeição:* Uso de sombras flutuantes sem intenção, gradientes policromáticos ou fontes sem autoridade tipográfica.

### 5.2 O Gate de Efeitos (CEO-Effects)
*   *Filtro:* Intenção narrativa e física visual real.
*   *Validação:* Garante a regra operacional de silêncio (0.8 segundos de repouso antes do motion), a gravidade física nas desacelerações e a performance estável de 60fps em dispositivos medianos.
*   *Critério de Rejeição:* Efeitos de animação decorativos genéricos (*bounces* elásticos, loadings estáticos) ou que causem queda de frames (jank).

### 5.3 O Gate de Arquitetura Espacial (CEO-Web)
*   *Filtro:* Disciplina de grid e escala.
*   *Validação:* Garante o uso de splits verticais assimétricos, um único elemento dominante por seção e a leitura em Z ou L.

### 5.4 O Gate de Escrita (CEO-Copy)
*   *Filtro:* Densidade verbal e tom.
*   *Validação:* Garante a economia de palavras, o subtexto editorial de luxo invisível e o uso de metadados técnicos como textura visual.

---

## 6. Assimilação de Erros e Aprendizados

Toda falha técnica (como o vazamento de Tweens GSAP na `useFrame` ou leaks de materiais Three.js na GPU) e anti-padrão de design detectados durante os testes e revisões locais devem ser catalogados e assimilados de forma determinística no Vault local.

O fluxo de processamento e vacinação do repositório deve obrigatoriamente seguir os parâmetros de append-only definidos no modelo operacional [VAULT_LEARNING_MODEL.md](file:///C:/Projetos/MadLabAurora/docs/Vault/OS-Evidence/OS-MADLAB-DOC-STACK-PREPARATION-20260528-001/VAULT_LEARNING_MODEL.md), proibindo a exclusão histórica de logs de incidentes.