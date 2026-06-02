# OS Evidence Trace — OS-MADLAB-02
**OS ID:** `OS-MADLAB-VISUAL-QUALITY-GATES-20260527-002`  
**Fase:** Micro-Etapa 1 — Manifest & Domain Policy Semantic Gate  
**Data:** 27 de Maio de 2026  
**Status:** CONCLUÍDO (Aprovado por Testes Semânticos)  

---

## 1. Escopo Executado

O objetivo da Micro-Etapa 1 foi estender o validador de governança para uma análise **semântica** das políticas de domínio e manifestos de consumo do Mad Lab, garantindo a conformidade total e a blindagem contra duplicações.

As seguintes verificações semânticas foram implementadas em [validate-configs.ps1](file:///C:/Projetos/MadLabAurora/scripts/validate-configs.ps1) e testadas com sucesso:

1. **Resolução Semântica do `extends`:**
   * O script agora obtém o diretório absoluto do subprojeto (pai da pasta `.aurora`) e resolve o caminho relativo de `extends` a partir dali. 
   * Confirma se o caminho final resolvido é exatamente `C:\Projetos\MadLabAurora\.aurora\domain-policy.json`.
   * **Bloqueio de Auto-referência:** Falha se o caminho resolvido apontar para o próprio arquivo de configuração do subprojeto.
2. **Checagem de Capabilities do Toolbelt:**
   * Valida que `observability.get_trace_summary` e `observability.osqa.list_qa_artifacts_by_os` são configurados obrigatoriamente como `read-only` e `required: true`.
   * Valida que `topology-impact-analyzer` está definido como `required: false` (opcional) com status `"planned_or_contract_only"`.
   * Confirma que `on_unavailable` aponta para `FACTORY_TOOL_UNAVAILABLE`.
3. **Garantias de Não-Duplicação de Soberania:**
   * O script varre o workspace de forma ativa em busca de caminhos proibidos (ex: `ElysianCorp\alvaro-core`, `ElysianCorp\qdrant`), garantindo a ausência de runtime do Álvaro ou bancos de dados paralelos e acusando violação imediata caso existam.
4. **Verificação de Regras Root:**
   * Garante que `domain` é `'madlab'`, que a política de domínio raiz contém as ações proibidas e que a promoção automática global de KIs está desativada (`"auto_promotion": false`).

---

## 2. Evidência de Execução do Gate

O script de integridade semântica foi executado e concluiu com êxito:
```powershell
powershell -File C:\Projetos\MadLabAurora\scripts\validate-configs.ps1
```

**Output dos Logs:**
```text
[SEMANTIC-GATE] Iniciando validação semântica de governança e soberania...
✅ [ROOT-POLICY] Política de domínio raiz íntegra.
✅ [TOOLBELT-CONSUMER] Manifesto de consumo do Toolbelt íntegro.
✅ [SUBPROJECT-POLICY] Validação de herança OK para: C:\Projetos\MadLabAurora\ElysianCorp\.aurora\domain-policy.json
✅ [SUBPROJECT-POLICY] Validação de herança OK para: C:\Projetos\MadLabAurora\aurora-web\.aurora\domain-policy.json
✅ [SUBPROJECT-POLICY] Validação de herança OK para: C:\Projetos\MadLabAurora\AuroraCognitiveAssets\.aurora\domain-policy.json
✅ [SEMANTIC-GATE] Sucesso! Todas as regras de herança, não-duplicação e soberania do domínio madlab foram validadas.
```

Não existem pendências ou inconformidades técnicas na Micro-Etapa 1.
