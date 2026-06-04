# Manual do Usuário: Aurora Cognitive Assets (ACA) 🧠
**S.S.O.T. Operacional — Versão 1.0 — Abril 2026**

---

## 📍 1. Propósito do Repositório
O **Aurora Cognitive Assets (ACA)** é a unidade consumidora da Fábrica Ozzmosis especializada em **extração e tratamento de conhecimento**. Ele atua como o "shell" (concha) que armazena material bruto e gerencia a produção de ativos digitais (E-books, Scripts, Playbooks) com o DNA do Fundador.

---

## ⚙️ 2. Arquitetura de Operação
O projeto funciona em um modelo de **Cadeia Logística de Conhecimento**:

1.  **Entrada (Vault)**: O material bruto (transcrições, áudios, teses) é depositado em `docs/Vault/`.
2.  **Processamento (Content Engine)**: Utiliza-se o Client Python para enviar o briefing para a `infoproduct-factory-service` da Ozzmosis.
3.  **Refinamento (Agentes & Skills)**: As skills do projeto (em `skills/`) orientam os agentes (Scribe, Closer, Navigator) na lapidação do conteúdo.
4.  **Saída (OS-Evidence)**: Todo resultado finalizado é persistido com seu registro de auditoria (OQS) em `docs/OS-Evidence/`.

---

## 🛠️ 3. Como Operar (Comandos)

O coração técnico do repositório está em `apps/content-engine/client/`.

### A. Preparar o Briefing
Crie um arquivo `brief.json` seguindo o modelo em `docs/Vault/OS-Evidence/OS-001/brief.json`.

### B. Iniciar a Produção (Pipeline)
Para enviar um briefing para a fábrica:
```bash
python apps/content-engine/client/run_infoproduct_pipeline.py --brief docs/Vault/OS-Evidence/OS-XXX/brief.json
```

### C. Executar Refinamento Automático
Para consolidar os resultados da fábrica e gerar o sumário legível:
```bash
python apps/content-engine/client/run_refinement_pipeline.py \
  --payload-dir docs/Vault/OS-Evidence/OS-XXX \
  --output-dir docs/Vault/OS-Evidence/OS-XXX \
  --print-summary
```

---

## 🛡️ 4. Governança e Qualidade (OQS)
Nenhum ativo pode sair do ACA sem o selo de auditoria.
Use as skills correspondentes para validar:
- **`behavioral-sales-audit.md`**: Validação de gatilhos Kahneman.
- **`content-orchestrator.md`**: Validação de estrutura APO.
- **`market-arbitrage.md`**: Validação de oportunidade de tráfego.

---

## ⚠️ 5. Observações Importantes
- **Dependência**: Este repositório requer que a `infoproduct-factory-service` esteja rodando (geralmente em `localhost:4310`).
- **Simulação Manual**: Em ambientes onde a fábrica está inacessível, o operador pode (e deve) utilizar as skills manualmente para gerar os artefatos de evidência.
