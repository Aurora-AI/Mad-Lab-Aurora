# Evolution Delta — Próxima Ingestão de Motion

**Versão:** 1.0.0  
**Skill:** ceo-effects, ceo-design, ceo-web  
**Status:** 🟡 Living Document — atualizar após cada OS concluída  

> Este documento captura os deltas de aprendizado que ainda não foram ingeridos na memória global.
> Quando um item for ingerido via pipeline KI, mover para `docs/Vault/KIs/approved/` e marcar aqui como `deprecated: true`.

---

## Pending Ingestion (KI Candidates)

### KI-CANDIDATE-001 — Regra do Silêncio Operacional
**Origem:** CEO-Effects + Mad Lab DNA v2.1.0  
**Aprendizado:** Todo ativo Aurora-native requer 0.8s de estado de repouso antes de qualquer animação. Isso não é delay técnico — é a física narrativa que dá peso ao que vem depois.  
**Status:** Candidato para `docs/Vault/KIs/candidates/`  
**Prioridade:** Alta

### KI-CANDIDATE-002 — Dark Editorial é Postura, não Paleta
**Origem:** Mad Lab DNA v2.1.0  
**Aprendizado:** Fundo #000000 não é Dark Editorial. Dark Editorial é a postura narrativa onde cada elemento tem densidade de intenção equivalente a uma editorial Vogue — independente da cor de fundo.  
**Status:** Candidato  
**Prioridade:** Alta

### KI-CANDIDATE-003 — Parallax de 2 Camadas = Commodity
**Origem:** CEO-Effects SKILL.md  
**Aprendizado:** Parallax de 2 camadas em velocidades diferentes é a versão commodity da profundidade. A profundidade real tem 5-8 camadas com velocidades calculadas por função de profundidade f(z) = 1/(1+z), com o mouse movendo a câmera, não os objetos.  
**Status:** Candidato  
**Prioridade:** Média

### KI-CANDIDATE-004 — Three.js r128 como Versão Fixa
**Origem:** Stack canônico do CEO-Effects  
**Aprendizado:** O MadLab Aurora usa Three.js r128 como versão fixa. THREE.CapsuleGeometry foi introduzida em r142. Alternativas: CylinderGeometry, SphereGeometry. Qualquer atualização de versão requer OS formal.  
**Status:** Candidato  
**Prioridade:** Alta (segurança operacional)

### KI-CANDIDATE-005 — Anti-Padrão: Layout Centralizado como Default
**Origem:** designmanualposthero.md  
**Aprendizado:** Headline + subtítulo + parágrafo + botão em coluna central sem quebra de eixo é o padrão de blog 2019. PROIBIDO por default no MadLab Aurora. Alternativas aprovadas: Split Assimétrico 40/60, Pinned Statement, Grid de Diagnóstico, Manifesto Horizontal, Composição Ancorada em Dados.  
**Status:** Candidato  
**Prioridade:** Alta

---

## Delta de Design (Aprendizados Visuais Recentes)

### DELTA-001 — Elysian Brand Kit v1.1 em Produção
**Data:** 2026-04-24  
**Mudança:** Brand Kit atualizado para v1.1.0 com arquitetura do hero dual-phase, tokens JSON completos e sistema de imagem com técnicas de double exposure aprovadas.  
**Impacto nas skills:** CEO-Design deve usar ELYSIAN_BRAND_KIT_v1.1.md como referência de logo e tokens.

### DELTA-002 — Acento Mad Lab: Âmbar #D97706
**Data:** 2026-04-24  
**Mudança:** A cor de vertical do Mad Lab Aurora é Âmbar (#D97706). Aparece apenas como label técnico `STRATEGY: MAD LAB AURORA` — nunca como cor de UI principal no site institucional Elysian.  
**Impacto:** CEO-Design e CEO-Effects devem usar esta cor apenas nesse contexto específico.

### DELTA-003 — Open Design Library: 138 sistemas catalogados
**Data:** 2026-05-27  
**Mudança:** A integração Open Design tem 138 sistemas de design em `integrations/open-design/catalog_design_systems.json`. O CEO-Critique-Theater e o CEO-Discovery-Specialist têm acesso a este catálogo inteiro — não apenas aos 5 sistemas primários.  
**Impacto:** Discovery e Critique devem referenciar o catalog JSON, não hardcodar sistemas.

---

## Como Usar Este Documento

1. **Quando detectar um aprendizado novo:** adicionar em "Pending Ingestion"
2. **Quando uma OS gerar um anti-padrão:** adicionar em "Delta de Design"
3. **Quando um KI for aprovado e ingerido:** marcar o item com `deprecated: true` e registrar path do KI em `docs/Vault/KIs/approved/`
4. **Atualização deste arquivo:** append-only. Nunca deletar entradas históricas.
