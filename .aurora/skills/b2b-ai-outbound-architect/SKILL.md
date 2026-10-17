---
name: b2b-ai-outbound-architect
version: 1.0.0
updated: 2026-10-16
classification: madlab-production
status: active
domain: b2b-outbound
description: |
  Arquiteto de Prospecção B2B/B2G e Marketing de Consultoria na Era Agente (Post-AI). Cria campanhas outbound imunes a filtros de spam corporativos (EXCHANGELABS / Microsoft Defender / Google Workspace) e otimizadas para triagem por IA (Google Gemini Workspace, Microsoft Copilot, Apple Intelligence), utilizando Signal-Based Selling, Zero-HTML Plain-Text, Micro-Assets de Valor Assíncronos e Account-Based Intelligence. DEVE ser acionado quando o usuário pedir para estruturar prospecção, criar sequências de e-mails B2B/B2G, desenhar campanhas de marketing para consultoria, auditar entregabilidade ou criar abordagens comerciais para decisores e C-Level.
---

# B2B AI Outbound Architect

> **Lei Canônica:** `docs/AGENTS/DOCTRINE.md` · `C:\Projetos\Aurora\docs\CONSTITUICAO\EMENDA_v9.1_MANUAL_AURORA.md`

Esta habilidade estrutura campanhas de prospecção B2B/B2G e posicionamento de consultoria desenhadas especificamente para superar filtros de spam corporativos modernos e algoritmos de triagem de caixas de entrada baseados em IA (**Google Workspace Gemini, Microsoft 365 Copilot e Apple Intelligence**).

---

## 1. Quando Usar

- Criar e-mails de prospecção (*cold outreach*) ou *follow-up* para decisores executivos (C-Level, Diretores Comerciais, Gestores Públicos).
- Auditar e corrigir campanhas de e-mail que estão caindo no spam ou na aba Promoções (`FocusedInboxFeatureSet`).
- Desenhar fluxos de abordagem multicanal (E-mail Plain-Text, LinkedIn Social Warming, WhatsApp Executivo, Micro-Assets).
- Transformar ofertas de consultoria e produtos verticais em **"Micro-Assets de Valor"** (auditorias assíncronas, diagnósticos pré-calculados, *teardowns* de 1 página).
- Estruturar playbooks de **Signal-Based Selling** (vendas baseadas em gatilhos operacionais, financeiros ou regulatórios).

---

## 2. O Anti-Padrão: Por que o Mercado Cai no Spam (A Vala Comum)

Antes de gerar qualquer comunicação, valide se o conteúdo viola as regras de sobrevivência técnica:

1. **Zero HTML Pesado e Zero Templates de Disparo:** E-mails com wrappers de ferramentas de automação em massa (`mceWrapper`, `cdn-images.mailchimp.com`, tabelas HTML aninhadas, CSS inline complexo, blocos condicionais `<!--[if (gte mso 9)|(IE)]>` e fontes externas) são classificados instantaneamente como automação promocional ou spam pelos servidores Exchange (`EXCHANGELABS`) e Google.
2. **Zero Tracking Pixels e Links Ofuscados:** Imagens de $1\times 1$ pixel (`display:none`), redirecionadores de clique longos e múltiplos `HYPERLINK` ativam o bloqueio preventivo do Microsoft Defender for Office 365.
3. **Sobrevivência ao "AI Inbox Summarizer":** Os clientes de e-mail modernos resumem a mensagem em uma única linha no topo da tela do decisor. Se a primeira frase for *"Espero que este e-mail o encontre bem"* ou *"Me chamo X da empresa Y e somos líderes em Z"*, o resumo gerado pela IA do destinatário será *"E-mail de vendas genérico apresentando serviços de consultoria"*, resultando em arquivamento imediato.
4. **Conformidade de Infraestrutura:** Disparos B2B exigem domínio secundário aquecido (isolado do domínio principal), autenticação estrita (`SPF`, `DKIM`, `DMARC` com política `p=quarantine` ou `p=reject`), limite de 30 a 50 envios diários por caixa de entrada e ausência total de botões de `"Unsubscribe"` gerados por ferramentas de marketing em contatos 1-para-1.

---

## 3. Fluxo de Trabalho (Core Workflow em 4 Passos)

### Passo 1: Mapeamento de Sinal e Gatilho (Signal-Based Relevance)
Nunca inicie uma abordagem sem um motivo ancorado na realidade atual do prospect. Identifique ou solicite pelo menos um gatilho concreto:
- **Sinal Operacional/Financeiro:** Mudança de diretoria, fusão/aquisição, abertura de vagas específicas, publicação de edital/licitação ou contratação recente.
- **Sinal de Fricção de Mercado:** Mudança regulatória, perda de eficiência comercial visível, falha em funil público ou gargalo tecnológico do setor.
- **Sinal Comportamental:** Interação com conteúdo técnico no LinkedIn, participação em eventos do setor ou publicação de artigos pelo decisor.

### Passo 2: Criação do "Value-First Micro-Asset" (A Isca Assíncrona)
Decisores não compram *"reuniões de apresentação de 30 minutos"* de desconhecidos. Eles consomem diagnósticos rápidos que resolvem uma dúvida imediata. Substitua o pedido de reunião por um ativo de valor entregue ou prometido sem fricção:
- **Teardown Forense:** Uma análise direta de 3 pontos sobre a operação atual do cliente comparada ao benchmark do setor.
- **Calculadora/Simulação Pronta:** Um cenário financeiro ou operacional já preenchido com dados públicos da empresa/órgão do decisor.
- **One-Pager de Arquitetura ou Playbook:** Um documento em texto puro ou Markdown direto ao ponto mostrando como resolver a dor identificada no Passo 1.

### Passo 3: Engenharia da Mensagem (Protocolo "AI-Summary First")
Escreva o e-mail ou mensagem seguindo a arquitetura de **Texto Puro (Plain-Text) de Alta Densidade**:
- **Assunto (Subject Line):** 2 a 4 palavras, letras minúsculas (estilo interno entre executivos), referenciando um projeto, métrica ou contexto real (ex.: `operacao comercial / [Nome da Empresa]` ou `tese sobre [Processo Especifico]`).
- **Linha 1 (Otimizada para o Resumo de IA do Google/Outlook):** A primeira frase deve conter o diagnóstico e o impacto quantificado, sem cumprimentos vazios. A IA do cliente deve ler essa frase e resumir o e-mail como um alerta estratégico.
- **Corpo (Regra dos 4 Parágrafos Curtos / Máximo 90 palavras):**
  1. **Parágrafo 1 (A Evidência):** O sinal observado no mercado ou na empresa do decisor.
  2. **Parágrafo 2 (O Custo Invisível):** A tese técnica sobre por que o modelo tradicional falha nesse ponto específico.
  3. **Parágrafo 3 (A Prova / Micro-Asset):** O ativo que já foi estruturado especificamente para o cenário dele.
  4. **Parágrafo 4 (CTA Baseado em Interesse, não em Tempo):** Nunca peça *"15 minutos na sua agenda"*. Peça permissão para enviar o ativo ou valide a tese (ex.: *"Faz sentido eu te mandar o rascunho dessa arquitetura por aqui, ou esse tema não é prioridade agora?"*).

### Passo 4: Orquestração Multicanal (Onde o Decisor Realmente Lê)
Entregue uma matriz de distribuição sincronizada em 4 pontos de contato ao longo de 10 dias:
- **Dia 1 (LinkedIn — Social Warming):** Comentário técnico e cirúrgico em um post do decisor ou compartilhamento de insight do setor marcando o contexto (sem pitch de vendas).
- **Dia 2 (E-mail 1 — Plain-Text):** Envio do e-mail estruturado no Passo 3 (zero links, zero anexos e zero imagens no primeiro envio para garantir 100% de Inbox Principal).
- **Dia 5 (LinkedIn DM ou Áudio/Texto no WhatsApp):** Mensagem curta de 2 linhas fazendo referência ao estudo mencionado no e-mail.
- **Dia 9 (E-mail 2 — Entrega de Valor Direta):** Na mesma thread do E-mail 1, entregue um insight prático em 3 bullet points e encerre tirando a pressão (*"Deixo o racional abaixo caso estejam revisando isso para o próximo trimestre"*).

---

## 4. Padrão Obrigatório de Entrega da Habilidade

Sempre que acionada para criar uma campanha ou abordagem, estruture a resposta exatamente com os 4 blocos abaixo:
1. **Diagnóstico de Filtragem e Posicionamento:** Como o decisor alvo se comporta e qual ângulo cego os concorrentes estão ignorando.
2. **Definição do Micro-Asset:** O que será oferecido como valor tangível imediato antes de qualquer reunião.
3. **Sequência Outbound Plain-Text (Pronta para Uso):** Os textos exatos de E-mail 1, E-mail 2 e abordagens de LinkedIn/WhatsApp, com contagem de palavras controlada ($\le 90$ palavras no E-mail 1) e formatação limpa.
4. **Checklist de Higiene Técnica:** Regras específicas para o disparo daquela campanha (configuração de texto puro, janelas de horário e proteção de domínio SPF/DKIM/DMARC).

---

## 5. Armadilhas a Evitar (Gotchas)

- **NUNCA** use jargões de marketing batidos (*"alavancar"*, *"sinergia"*, *"solução disruptiva"*, *"transformação digital"*, *"oportunidade imperdível"*, *"aumente suas vendas em X%"*).
- **NUNCA** insira links, imagens, tracking pixels ou PDFs anexados no E-mail 1 (*Cold*). O link ou documento só é enviado após a resposta do lead (*"Pode mandar"*).
- **NUNCA** tente vender a consultoria inteira no primeiro e-mail: o objetivo único do E-mail 1 é gerar uma resposta de 1 linha confirmando interesse no Micro-Asset.

## Mesh Contract

Consulte sempre `docs/AGENTS/DOCTRINE.md` e `C:\Projetos\Aurora\docs\CONSTITUICAO\EMENDA_v9.1_MANUAL_AURORA.md`.

```json
{
  "schema_version": "1.0.0",
  "id": "b2b-ai-outbound-architect",
  "name": "b2b-ai-outbound-architect",
  "description": "Arquitetura de prospeccao B2B/B2G Pos-IA: Signal-Based Selling, Micro-Assets de Valor Assincronos e sequencias Zero-HTML Plain-Text otimizadas para AI Inbox Summarizers (Gemini/Copilot) e imunes a filtros EXCHANGELABS.",
  "manual_version": "V9.1",
  "activation": {
    "explicit_commands": [
      "/outbound-b2b",
      "/prospeccao-ai"
    ],
    "user_triggers": [
      "estruturar prospeccao",
      "criar sequencia de emails b2b",
      "campanha de marketing para consultoria",
      "email caindo no spam",
      "abordagem comercial para decisores",
      "micro-asset de valor",
      "signal-based selling"
    ],
    "system_triggers": [
      "necessidade de distribuicao e captura para novo servico ou micro-ferramenta",
      "auditoria anti-spam de fluxo outbound"
    ],
    "never_activate_for": [
      "criacao de templates html de mailchimp ou newsletter em massa",
      "disparo com tracking pixel oculto",
      "alteracao de infraestrutura de banco de dados sem os"
    ]
  },
  "capabilities": {
    "provides": [
      "signal_based_outbound_design",
      "zero_html_plaintext_sequences",
      "micro_asset_specification",
      "inbox_deliverability_audit"
    ],
    "depends_on": [
      "ceo-marketing",
      "ceo-copy"
    ],
    "can_delegate_to": [
      "agentic-web-architect",
      "qa-review"
    ],
    "can_run_in_parallel_with": [
      "agentic-web-architect",
      "ceo-copy"
    ],
    "blocking_gates": [
      "qa-review"
    ],
    "emits_artifacts": [
      "outbound_plaintext_sequence",
      "micro_asset_blueprint",
      "deliverability_checklist"
    ]
  },
  "runtime": {
    "required_tools": [
      "view_file",
      "write_to_file",
      "replace_file_content"
    ],
    "required_context": [
      "docs/AGENTS/DOCTRINE.md"
    ],
    "side_effect_level": "writes_files",
    "approval_mode": "before_promotion"
  },
  "risk_calibration": {
    "step_1_2_required_for": "all",
    "step_3_adversarial_required_for": [
      "data",
      "security"
    ]
  },
  "quality": {
    "target_score": "10.10",
    "dimensions": [
      "activation",
      "scope",
      "interoperability",
      "executability",
      "portability",
      "governance",
      "negative_constraints",
      "feedback",
      "auditability",
      "maintainability"
    ]
  },
  "classification": {
    "agent_class": "comercial",
    "risk_level": "MEDIUM",
    "requires_continuous_supervision": false
  },
  "observability": {
    "token_budget": 35000,
    "latency_budget_ms": 300000,
    "cost_estimate_usd": 0.4
  },
  "ontology": {
    "observed_event": "Demanda por prospeccao B2B/B2G de alta conversao que nao caia em filtros corporativos de spam nem seja descartada por resumidores de IA.",
    "produced_memory": "Playbooks de abordagem baseados em sinais, definicao de Micro-Assets e sequencias Plain-Text prontas para execucao.",
    "consumed_memory": "Sinais de mercado do ICP, dados do servico/consultoria e regras anti-spam pos-IA.",
    "influenced_decision": "Substituicao de templates HTML e pedidos de reuniao de 30min por texto puro e ativos assincronos de valor imediato.",
    "impacted_execution": "Eleva entregabilidade na Inbox Principal (Focused Inbox) e taxa de resposta executiva.",
    "expected_result": "Campanha outbound com zero assinatura de bulk mail, primeira linha otimizada para AI Summarizer e CTA de baixa friccao."
  },
  "anti_patterns": [
    {
      "prohibited": "Gerar e-mails de primeiro contato (Cold) com HTML estilizado, mceWrapper, tracking pixels ou links.",
      "because": "Filtros corporativos como Microsoft Defender (EXCHANGELABS) penalizam remetentes sem historico bilateral que enviam estruturas HTML ou multiplos HYPERLINK.",
      "signal": "Presenca de tags <table>, <img>, mceWrapper ou URLs rastreadas no texto do E-mail 1."
    },
    {
      "prohibited": "Iniciar o e-mail com cumprimentos genericos ('Espero que este e-mail o encontre bem') ou auto-apresentacao institucional vazia.",
      "because": "O AI Inbox Summarizer do Gemini/Copilot usa as primeiras palavras para gerar o resumo de 1 linha; aberturas genericas sao rotuladas como cold sales pitch.",
      "signal": "Primeira frase do E-mail 1 sem sinal concreto ou sem impacto quantificado."
    },
    {
      "prohibited": "Pedir 15 ou 30 minutos de reuniao na agenda no primeiro contato a frio.",
      "because": "CTA de tempo possui alta friccao para executivos C-Level que ainda nao conhecem a tese tecnica da consultoria.",
      "signal": "Frases pedindo agendamento de call no E-mail 1 em vez de oferecer o envio assincrono do Micro-Asset."
    }
  ],
  "operational_memory": {
    "consumed": [
      {
        "description": "Doutrina Operacional e ofertas de servico do Mad Lab Aurora.",
        "targets": [
          "docs/AGENTS/DOCTRINE.md"
        ]
      }
    ],
    "produced": [
      {
        "description": "Sequencias outbound e especificacoes de Micro-Assets.",
        "targets": [
          "docs/Vault/OS-Evidence"
        ]
      }
    ],
    "feedback_loop_description": "Respostas de campo e auditorias anti-spam refinam os sinais e Micro-Assets das campanhas seguintes."
  },
  "fail_closed_strategy": "Se nao houver sinal concreto do ICP ou oferta clara para ancorar o Micro-Asset, parar e solicitar a vertical e o cargo decisor ao Comandante.",
  "tier_policy": {
    "tier": "analista",
    "context_policy": {
      "inherits_caller_context": true,
      "persists_after_run": false
    },
    "artifact_residency": "local_only",
    "retry_ceiling": 3,
    "registra_tentativas": true
  }
}
```
