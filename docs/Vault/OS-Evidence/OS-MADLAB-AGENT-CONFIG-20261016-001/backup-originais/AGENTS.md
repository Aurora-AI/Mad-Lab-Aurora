# AGENTS.md — Mad Lab Aurora

> Guia operacional compacto para sessões de agente neste repositório.
> Leia este arquivo e o `GEMINI.md` antes de qualquer outra ação.

---

## Identidade e Posição no Ecossistema

O **Mad Lab Aurora** é o **braço criativo da Aurora** — não um projeto vertical.
É a camada de direção de arte, craft de interface, motion design e experimentação WebGL
para todo o ecossistema (ElysianLex, CRM, SilentOperator, etc.).

```text
           ELYSIAN (Marca Mãe)
                │
         MAD LAB AURORA  ◄── Você está aqui
          ┌────┴────┐
  Projetos Verticais  Ozzmosis (Fábrica)
  (Lex / CRM / etc)  (Conductor / Libs)
```

**Autoridade máxima criativa:** `docs/brand/MANUAL_DA_AGENCIA.md` (v3.0.0)  
**DNA Visual:** `docs/brand/mad-lab-aurora-dna-v2.1.0.md`

---

## Regras de Fronteira (OBRIGATÓRIAS)

- **Proibido** recriar ou instanciar cópias do runtime do Álvaro localmente
- **Proibido** criar MCP Gateway de observabilidade próprio
- **Proibido** instanciar Qdrant ou Vault global paralelo sem OS formal
- **Proibido** executar auto-repair autônomo em produção
- **Proibido** promover KIs automaticamente para a memória global da fábrica
- Consumo da fábrica Ozzmosis: **exclusivamente via Toolbelt Registry** (`toolbelt-consumer.json`)
- Toda ausência de serviço de fábrica gera evento `FACTORY_TOOL_UNAVAILABLE` com fallback explícito

---

## Constituição Criativa — Regra Estética Absoluta

> **"Nada que saia do Mad Lab Aurora pode parecer site feito por IA."**

Os 6 sinais de alerta a eliminar ativamente:
1. Simetria linear crua sem quebra de eixo
2. Tipografias de sistema como Voz Display (Inter, Roboto, Arial)
3. Gradientes neon SaaS (roxo→azul→verde)
4. Border-radius e sombras clichês de templates comerciais
5. Motion decorativo sem gravidade (bounce, elastic sem razão)
6. Background #000000 como substituto de Dark Editorial real

**Dark Editorial é postura narrativa — não paleta, não dark mode.**

---

## Os 4 Gates de Qualidade (Não Negociáveis)

Nenhum design ou interface entra em produção sem passar pelos quatro:

| Gate | Agente | Pergunta Central |
|---|---|---|
| Design | `ceo-design` | "Esta estrutura sobrevive ao colapso físico?" |
| Efeitos | `ceo-effects` | "Este efeito tem intenção articulável?" |
| Arquitetura | `ceo-web` | "Este espaço foi construído com disciplina?" |
| Escrita | `ceo-copy` | "Cada palavra aqui tem peso de sentença?" |

---

## Skills Locais Disponíveis (`.aurora/skills/`)

| Skill | Domínio | Acionamento |
|---|---|---|
| `ceo-design` | Sistemas visuais, identidade, DNA | Identidade, tipografia, paleta, stress estrutural |
| `ceo-effects` | Motion, WebGL, GSAP, shaders | Animação, preloader, parallax, Three.js |
| `ceo-web` | Conversão, layout, presença digital | Site, landing page, hero, CTA, prova social |
| `ceo-copy` | Densidade verbal, tom | Copy, headline, manifesto, escrita de seção |
| `ceo-marketing` | Canal, distribuição | Canal de venda, funil, ICP, oferta |
| `ceo-product-owner` | Produto, backlog | Features, prioridade, dor de mercado |
| `ceo-business-partner` | Estratégia competitiva | Posicionamento, decisão estratégica |
| `ceo-critique-theater` | Auditoria multi-dimensão | Revisão de interface contra sistema Open-Design |
| `ceo-discovery-specialist` | Extração de briefing | Turn-1 discovery, conversão para I-Lang |
| `qa-review` | Gate de qualidade | Ao finalizar qualquer código, produto ou OS |
| `agent-reflexion-cost` | Token Ledger | Ao concluir OS — registra custo e tokens |
| `agent-thread-recorder` | Memória de sessão | Ao concluir sessão com OSes ou decisões |
| `taste-design` | Design System (DESIGN.md) | Geração de sistemas visuais para Stitch |
| `design-md` | Síntese de design | Análise de projetos Stitch |
| `engenheiro-reverso` | Reverse engineering | Sistemas legados, extração de ontologia |

---

## Regra do Post-Hero (Always On)

O arquivo `.agents/rules/designmanualposthero.md` com `trigger: always_on` está sempre ativo.
Consulte-o antes de qualquer decisão de layout de seção pós-hero.

---

## Vault Local

```text
docs/Vault/
├── Raw/          — Documentos brutos ingeridos
├── Processed/    — Pós-sanitização do Bibliotecário
├── KIs/
│   ├── approved/ — KIs aprovados (fluxo: candidate → aprovação manual → aqui)
│   └── candidates/ — Candidatos aguardando revisão
├── OS-Evidence/  — Evidências de OSes executadas
├── Threads/      — Sessões estruturadas pelo agent-thread-recorder
├── Token-Ledger/ — Custo por OS/step registrado pelo agent-reflexion-cost
├── Decisions/    — Decisões arquiteturais (formato DEC-MADLAB-*.md)
└── DesignLibrary/ — Padrões WebGL e shaders
```

**Regra Vault:** append-only. Documentos obsoletos recebem `deprecated: true`.
Nunca deletar evidências históricas.

---

## Protocolo de OS (Ordens de Serviço)

Para tarefas de risco Médio, Alto ou Crítico:
1. OS formal em `docs/Vault/OS-Evidence/OS-MADLAB-{DOMÍNIO}-{DATA}-{SEQ}/`
2. Execução em micro-etapas com gates determinísticos
3. Evidence file ao concluir cada etapa
4. `qa-review` obrigatório ao final
5. `agent-reflexion-cost` para registrar custo
6. `agent-thread-recorder` para registrar decisões da sessão

Nunca executar múltiplas micro-etapas em lote.
Aguardar confirmação explícita de sucesso antes de avançar.

---

## Anti-Padrões Operacionais (Armadilhas Conhecidas)

1. **References físicas:** Skills referenciam `references/` que precisam existir. Verificar antes de acionar.
2. **Path do Token Ledger:** Path correto é `C:\Projetos\MadLabAurora\docs\Vault\Token-Ledger\`
3. **SES:** O `aurora-agents/skill-evolution-system/` existe como scaffolding — não está operacional para uso em produção ainda.
4. **KI pipeline:** Candidatos vão para `docs/Vault/KIs/candidates/` — promoção para `approved/` requer revisão manual.
5. **creative-area-manifest.json:** Pode estar desatualizado; não usá-lo como fonte de verdade de ativos.
6. **Stack WebGL:** Fixado em Three.js r128. Não usar `THREE.CapsuleGeometry` (introduzida em r142). Proibido CUDA, nvidia-*, torch.

---

## Stack Técnico Canônico

```
aurora-web/     → Vite + TypeScript (porta 3001 em dev)
ElysianCorp/    → Projeto de produto (verificar README local)
Three.js        → r128 (FIXO — não atualizar sem OS)
React Three Fiber → R3F com useFrame, useThree
GSAP            → + ScrollTrigger + Timeline
GLSL            → Fragment + Vertex shaders para efeitos profundos
CSS             → Fallback + prefers-reduced-motion OBRIGATÓRIO
```

---

## Referências Rápidas

| Documento | Função |
|---|---|
| `docs/brand/MANUAL_DA_AGENCIA.md` | Constituição criativa (autoridade máxima) |
| `docs/brand/mad-lab-aurora-dna-v2.1.0.md` | DNA Dark Editorial completo |
| `docs/brand/ELYSIAN_BRAND_KIT_v1.1.md` | Identidade Elysian, logo, Emerald |
| `.agents/rules/designmanualposthero.md` | Grid, tipografia, layouts, motion (always_on) |
| `docs/Vault/DESIGN_LIBRARY.md` | Padrões WebGL P046-P052 |
| `.aurora/domain-policy.json` | Soberania técnica e capacidades permitidas |
| `.aurora/toolbelt-consumer.json` | Capacidades da fábrica Ozzmosis consumidas |
| `docs/Vault/Decisions/DEC-MADLAB-AGENTIC-MESH-001.md` | Decisão de integração com Ozzmosis |
