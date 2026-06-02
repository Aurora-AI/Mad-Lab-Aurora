# Plano de Atualização da Pilha Documental

**OS ID:** `OS-MADLAB-DOC-STACK-PREPARATION-20260528-001`  
**Fase:** Planejamento Sequencial de Reescrita  
**Status:** VALIDADO

---

## 1. Cronograma e Ordem Recomendada de Atualização

Para garantir que a reescrita documental ocorra de forma segura, sem criar contradições ou inconsistências internas, a reescrita canônica deve obedecer à seguinte ordem sequencial (um documento de cada vez):

```text
FASE 1: MANUAL_DA_AGENCIA.md  (Constituição Central)
  │
  ▼
FASE 2: domain-policy.json  (Alinhamento de Capabilites)
  │
  ▼
FASE 3: mad-lab-aurora-dna-v2.1.0.md  (Purificação do Manifesto de NLU)
  │
  ▼
FASE 4: designmanualposthero.md  (Alinhamento Tático de Tipografia/Grids)
  │
  ▼
FASE 5: DESIGN_LIBRARY.md  (Versionamento e Indexação Física de Shaders)
```

### Detalhamento das Etapas:

1.  **Etapa 1 — `MANUAL_DA_AGENCIA.md` (Próxima OS: `OS-MADLAB-MANUAL-DA-AGENCIA-REWRITE-20260528-002`)**
    *   *Objetivo:* Consolidar-se como a única constituição e roteador central da pilha. Ele estabelecerá os limites, regras de dois mundos e a física visual, apontando para os sub-documentos para regras táticas (Post-Hero) ou especificações de marca (Brand Kit).
2.  **Etapa 2 — `domain-policy.json`**
    *   *Objetivo:* Limpar e alinhar a governança de capabilities locais e remover redundâncias sobre termos comerciais das verticais.
3.  **Etapa 3 — `mad-lab-aurora-dna-v2.1.0.md`**
    *   *Objetivo:* Eliminar as repetições históricas (Sabbath, referências Exo Ape/Lusion) e purificá-lo como a "Bula Sensorial" de tom e escrita para agentes de IA (regras cognitivas NLU).
4.  **Etapa 4 — `designmanualposthero.md`**
    *   *Objetivo:* Reconciliar o uso da tipografia Display de serifa editorial com a fonte Söhne sans-serif do Brand Kit da Elysian, criando regras de convivência claras nas seções de produtos verticais.
5.  **Etapa 5 — `DESIGN_LIBRARY.md`**
    *   *Objetivo:* Organizar o inventário técnico de shaders de WebGL, cursores e transições, vinculando os códigos físicos existentes em `aurora-visual-assets/` aos seus respectivos registros de "Anatomy WebGL" e hashes.

---

## 2. Invariantes e Aprendizados a Preservar

As futuras reescritas estão proibidas de atenuar, remover ou afrouxar os seguintes aprendizados acumulados da Aurora:

1.  **A Lei dos Dois Mundos:** O mundo luminoso (off-white, ar, Da Vinci) e o mundo dark (preto profundo, tensão da máquina) operam com igual peso. Nenhum é "modo de fallback" ou "identidade secundária".
2.  **A Conquista Narrativa do Dark:** O preto nunca deve ser usado como atalho ou template genérico. A tensão do escuro é conquistada pela jornada na página, e necessita de justificativa no brief.
3.  **A Regra do Silêncio:** O estado de repouso obrigatório de 0.8s antes de qualquer transição ou animação de elemento visual.
4.  **Orçamento de Performance:** O target inflexível de 60fps em dispositivos móveis medianos.
5.  **A Regra Mnemônica Anti-IA:** O bloqueio absoluto de elementos simétricos centralizados, gradientes SaaS e border-radius de produto de baixo custo.
