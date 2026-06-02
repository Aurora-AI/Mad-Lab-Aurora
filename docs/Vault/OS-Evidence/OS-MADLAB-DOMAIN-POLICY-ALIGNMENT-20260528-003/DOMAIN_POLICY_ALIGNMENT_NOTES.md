# Notas de Alinhamento — domain-policy.json

**OS ID:** `OS-MADLAB-DOMAIN-POLICY-ALIGNMENT-20260528-003`  
**Data:** 28 de Maio de 2026  
**Status:** IMPLEMENTADO  

---

## 1. Resumo das Alterações no JSON

O arquivo `C:/Projetos/MadLabAurora/.aurora/domain-policy.json` foi modificado para alinhar suas regras técnicas de governança local com a nova Constituição `MANUAL_DA_AGENCIA.md` v3.0.0.

### Principais Modificações:
1. **Rastreabilidade e Versão:**
   - Elevada a versão técnica da política (`policy_version`) de `1.0.0` para `1.1.0`.
   - Adicionada referência constitucional (`constitution_ref`) apontando para `docs/brand/MANUAL_DA_AGENCIA.md`.
   - Vinculada a versão da constituição consumida (`constitution_version`) como `3.0.0`.
2. **Referência aos Gates de Qualidade:**
   - Inserido o objeto `quality_gates_ref` sob a chave `governance`, mapeando os IDs e âncoras exatos da Constituição correspondentes a cada um dos gates de conformidade:
     - `design` -> `docs/brand/MANUAL_DA_AGENCIA.md#51-o-gate-de-design-ceo-design`
     - `effects` -> `docs/brand/MANUAL_DA_AGENCIA.md#52-o-gate-de-efeitos-ceo-effects`
     - `web` -> `docs/brand/MANUAL_DA_AGENCIA.md#53-o-gate-de-arquitetura-espacial-ceo-web`
     - `copy` -> `docs/brand/MANUAL_DA_AGENCIA.md#54-o-gate-de-escrita-ceo-copy`
3. **Novas Ações Proibidas (Prohibited Actions):**
   - Adicionada a restrição `"bypass_visual_quality_gates"` para proibir qualquer promoção de código ou design sem a checagem formal dos gates.
   - Adicionada a restrição `"auto_promote_knowledge_to_global_vault"` para blindar o fluxo de promoção de KIs locais contra autopromoções sem curadoria de sanitização.

### Parâmetros Preservados:
- `domain`: `"madlab"` (identificador único local).
- `boundary`: `"creative-arm"` (limitação de fronteira criativa).
- `can_consume`: Lista de capacidades lidas da fábrica preservada.
- `local_only`: Lista de ferramentas e processos locais preservada.
- `global_promotion_path`: Mantido o fluxo sequencial manual e `auto_promotion: false` inalterado.

---

## 2. Diff de Alteração Técnica

```diff
 {
   "domain": "madlab",
   "policy_name": "Mad Lab Domain Sovereignty Policy",
-  "version": "1.0.0",
+  "policy_version": "1.1.0",
+  "constitution_ref": "docs/brand/MANUAL_DA_AGENCIA.md",
+  "constitution_version": "3.0.0",
   "governance": {
     "boundary": "creative-arm",
+    "quality_gates_ref": {
+      "design": "docs/brand/MANUAL_DA_AGENCIA.md#51-o-gate-de-design-ceo-design",
+      "effects": "docs/brand/MANUAL_DA_AGENCIA.md#52-o-gate-de-efeitos-ceo-effects",
+      "web": "docs/brand/MANUAL_DA_AGENCIA.md#53-o-gate-de-arquitetura-espacial-ceo-web",
+      "copy": "docs/brand/MANUAL_DA_AGENCIA.md#54-o-gate-de-escrita-ceo-copy"
+    },
     "can_consume": [
       "observability.get_trace_summary",
       "observability.osqa.list_qa_artifacts_by_os",
       "alvaro-contracts",
       "reflexion-code-triaging"
     ],
     "prohibited_actions": [
       "create_local_mcp_gateway",
       "replicate_alvaro_runtime",
       "duplicate_global_qdrant_instance",
-      "execute_autonomous_production_self_healing"
+      "execute_autonomous_production_self_healing",
+      "bypass_visual_quality_gates",
+      "auto_promote_knowledge_to_global_vault"
     ],
     "local_only": [
       "madlab.design_system_lint",
       "madlab.visual_performance_harness",
       "madlab.hydration_integrity_check",
       "madlab.motion_regression_check",
       "candidate_knowledge_indicators_local"
     ],
     "global_promotion_path": {
       "process": "candidate_ki -> bibliotecario_sanitization -> qa_review_gate -> manual_approval -> global_vault_promotion",
       "auto_promotion": false
     }
   }
 }
```
