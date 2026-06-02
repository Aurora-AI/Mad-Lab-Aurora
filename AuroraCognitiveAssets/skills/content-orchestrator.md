# Skill: Content Orchestrator (ACA-001) 🏗️
**Versão 1.0 — Projeto: Aurora Cognitive Assets — Março 2026**

---

## 📍 Finalidade
Esta skill automatiza a estruturação de ativos de conhecimento de longo formato (Livros, Manuais, Playbooks) a partir de extrações cognitivas brutas. Ela garante que a hierarquia de informação siga o padrão **APO (Arquitetura de Performance Orquestrada)**.

---

## ⚙️ Capacidades

1. **Mapping de Tese**: Identificar a tese central em uma transcrição bruta.
2. **Clusterização de Pilares**: Agrupar insights relacionados em capítulos lógicos.
3. **Detecção de Ghost Notes**: Sinalizar pontos onde o especialista "encurtou" a explicação e precisa de mais profundidade.
4. **Geração de Sumário Canônico**: Criar a estrutura de capítulos pronta para escrita.

---

## 🛠️ Protocolo de Uso (Para o Redator Sênior)

### Passo 1: Ingestão
Leia o arquivo de extração em `docs/Vault/`.

### Passo 2: Extração de Padrões
Execute a análise de frequência de termos e conceitos-chave. Identifique os "Axiomas do Mestre".

### Passo 3: Montagem do Esqueleto
Gere um documento `.md` com a seguinte estrutura:
- **Título**
- **Tese Central**
- **Capítulos (H2)**
- **Ações Imediatas (Bottom-line)**

---

## 🛡️ Guardrails

- Não invente conceitos. Se não houver clareza no Vault, peça "Extração de Profundidade".
- Mantenha o equilíbrio 70% Conhecimento Prático / 30% Teoria Estruturante.
- Cada capítulo deve terminar com um "Checklist de Integridade".
