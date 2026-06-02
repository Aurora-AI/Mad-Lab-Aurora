# Modelo de Ingestão de Aprendizados do Vault

**OS ID:** `OS-MADLAB-DOC-STACK-PREPARATION-20260528-001`  
**Fase:** Governança de Conhecimento e Assimilação de Falhas  
**Status:** VALIDADO

---

## 1. O Fluxo de Custódia do Conhecimento (Pipeline Local)

Para garantir que os erros e as inovações visuais do Mad Lab Aurora sejam assimilados na memória ativa do laboratório de forma segura, estabelece-se o fluxo de custódia estruturado em 5 fases:

```text
DETECÇÃO (Falha/Inovação)
  │
  ▼
CATALOGAÇÃO (Registro do incidente em docs/Vault/Raw/)
  │
  ▼
TRIAGEM E CLASSIFICAÇÃO (Erros, Anti-padrões ou Candidatos a Padrões)
  │
  ▼
PROMOÇÃO GVERNADA (Validação de design e aprovação do Comandante)
  │
  ▼
SANINIZAÇÃO E MANIFESTO (Bibliotecário assina e atualiza vault_manifest.json)
```

---

## 2. Classificação de Aprendizados e Ativos

Todo aprendizado capturado no laboratório deve ser enquadrado em uma das três categorias formais:

### 2.1 Padrões de Erro Técnico (Leaks / Regressões)
*   **Definição:** Código funcional que apresenta riscos operacionais, loops infinitos, vazamentos de memória na GPU ou falta de cleanup.
*   **Exemplos catalogados:**
    *   *GSAP em useFrame:* Instanciação repetida de Tweens GSAP no laço de frames.
    *   *Texture/Material Leaks:* Criação de texturas e materiais Three.js via `useMemo` sem chamada a `.dispose()` no unmount.
    *   *Counter loops:* Declaração de `requestAnimationFrame` sem `cancelAnimationFrame` em cleanup do React.
*   **Tratamento:** Registro imediato em `docs/Vault/KIs/candidates/` como vacina de código.

### 2.2 Anti-Padrões Visuais (Sinais de "Cara de IA")
*   **Definição:** Elementos de UI, tipografia ou layouts que falham no teste de anti-genericidade e degradam a postura Dark Editorial.
*   **Exemplos catalogados:**
    *   *Layout Bloco Central:* Título + descrição + botão alinhados na coluna central sem assimetria.
    *   *Over-rounding:* Border-radius elevados (>12px) aplicados a cartões e interfaces corporativas de alto valor.
    *   *Policromia:* Excesso de tons fluorescentes ou uso de gradientes roxo-azul padrão SaaS.
*   **Tratamento:** Inclusão no checklist proibitivo de linter estático e documentação no `designmanualposthero.md`.

### 2.3 Candidatos a Padrão (Inovações Estéticas)
*   **Definição:** Efeitos visuais experimentais ou shaders customizados criados no Mad Lab que foram aprovados nos testes estéticos de S-Tier e merecem catalogação.
*   **Exemplo:** O Shader de scanline reativo com profundidade de campo desenvolvido em `hero-futuristic.tsx`.
*   **Tratamento:** Encaminhamento para a `DESIGN_LIBRARY.md` e promoção para o diretório de ativos aprovados da fábrica.

---

## 3. Regras de Custódia e Não-Exclusão (Append-Only)

1.  **Regra do Registro Histórico:** Documentos no Vault nunca são deletados ou limpos para "limpar o histórico". Eles são marcados com a tag `deprecated: true` nos metadados, preservando a linhagem e a cadeia de custódia.
2.  **Saneamento de Dados Sensíveis:** Nenhuma chave de API, dado pessoal (PII) ou credencial corporativa pode ingressar nas pastas de `Raw` ou `KIs`. Os arquivos passam por processo de sanitização estrita antes da gravação física.
3.  **Atualização de Manifesto:** Toda inserção de conhecimento ou nova vacina no diretório local de KIs deve atualizar o arquivo `vault_manifest.json` para que as IDEs e agentes saibam onde buscar contextos preventivos.
