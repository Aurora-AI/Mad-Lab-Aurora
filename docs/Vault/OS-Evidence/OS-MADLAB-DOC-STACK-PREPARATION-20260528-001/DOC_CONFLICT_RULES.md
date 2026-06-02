# Regras de Resolução de Conflitos Documentais

**OS ID:** `OS-MADLAB-DOC-STACK-PREPARATION-20260528-001`  
**Fase:** Governança de Conflitos e Inconsistências  
**Status:** VALIDADO

---

## 1. O Teste Absoluto do Mad Lab Aurora

Toda decisão de design, layout, tipografia ou motion deve se submeter, em última instância, à regra estética absoluta do laboratório:

> **"Nada que saia do Mad Lab Aurora pode parecer site feito por IA."**

### 1.1 O que constitui "Cara de IA" (Sinais de Alerta Bloqueantes):
1.  **Estruturas Monótonas:** Layouts perfeitamente simétricos (Headline + Subtítulo + Parágrafo + Botão centralizado) sem quebras de eixo.
2.  **Genericidade de Fontes:** Uso de fontes do sistema sem intenção editorial (ex: Arial, Inter como fonte display).
3.  **Clichês SaaS:** Cards com bordas arredondadas exageradas (>12px) e sombras pesadas para simular profundidade.
4.  **Cores Artificiais:** Gradientes roxo/azul ou policromia excessiva.
5.  **Animações sem Peso:** Elementos que flutuam em parallax de apenas duas camadas ou aplicam *fade-in* simples idêntico a todos os elementos em scroll.
6.  **Decorativos de Clichê:** Emojis ou ícones flat lineares que não comunicam rigor ou dados de verdade.

---

## 2. Protocolo Lógico de Resolução de Conflitos

Em caso de divergência ou ambiguidade entre regras da pilha documental, o agente/desenvolvedor deve executar o seguinte algoritmo de resolução de 4 passos:

```text
INÍCIO
  │
  ├─► [PASSO 1] O conflito envolve segurança, capabilities de rede,
  │             Trustware técnico ou integrações com o Conector Álvaro/Fábrica?
  │             YES ──► Aplica-se domain-policy.json (Soberania Técnica) e encerra.
  │             NO
  │
  ├─► [PASSO 2] O conflito afeta a postura do laboratório, orçamento de hardware (60fps)
  │             ou prioridades do Comandante?
  │             YES ──► Aplica-se MANUAL_DA_AGENCIA.md (Constitucional) e encerra.
  │             NO
  │
  ├─► [PASSO 3] Consulte a Matriz de Arbitragem (DOC_AUTHORITY_MATRIX.md).
  │             O conflito cai sob o escopo específico de um documento arbitral?
  │             YES ──► Aplica-se o documento arbitral correspondente e encerra.
  │             NO
  │
  └─► [PASSO 4] Aplica-se a regra de precedência linear direta (1 a 6) e encerra.
FIM
```

---

## 3. Diretriz para Referências Externas e Corporais

*   **Não Importação de Ruído:** O código-fonte de sites de referências (`Aino`, `Exo Ape`, `Lusion`) ou capturas de tela do `Brand ID` nunca devem ser copiados diretamente para o repositório ativo de produção.
*   **Papel de Consulta:** Referências de terceiros servem apenas para responder à pergunta: *"Que física de movimento eles usaram para passar essa sensação?"*
*   **Tradução para o DNA:** A técnica da referência deve ser decodificada e traduzida para os tokens visuais e de cores da Elysian antes de ser reescrita no repositório.
