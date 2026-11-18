---
name: cdp-design-system-extractor
version: 1.0.0
updated: 2026-10-19
classification: madlab-production
status: active
domain: agentic-design-system
description: |
  Arquiteto e Engenheiro de Extração de Living Design Systems em HTML via Chrome DevTools Protocol (CDP), Playwright e MCP para o Google Antigravity IDE. Extrai tokens semânticos (:root), física de animação (cubic-bezier), @keyframes, estados forçados de :hover/:focus via CDP, shaders WebGL1/WebGL2 e screenshots 2x DPI de qualquer URL de referência externa. Emite 4 artefatos canônicos versionados (design-telemetry.json, visual-shader-manifest.json, design-tokens.json e design-system.html) calibrados para Paz Cognitiva e WebMCP (document.modelContext).
---

# CDP Design System Extractor (Antigravity Edition)

> **Lei Canônica:** `docs/AGENTS/DOCTRINE.md` · `C:\Projetos\Aurora\docs\CONSTITUICAO\EMENDA_v9.1_MANUAL_AURORA.md` · `C:\Projetos\Aurora\docs\CONSTITUICAO\criterio_formal_de_aceite_de_interface.md`

Esta habilidade guia a extração determinística de tokens visuais, física de movimento e microinterações de qualquer URL de referência utilizando **Playwright + Chrome DevTools Protocol (CDP)**, consolidando o resultado em uma arquitetura multi-artefato encabeçada por um **Living Design System em HTML (`design-system.html`)** para consumo por agentes de IA no Google Antigravity IDE.

---

## 1. Quando Usar

- Extrair a engenharia visual de um site de referência (Linear, Stripe, Awwwards, Godly) via CDP.
- Capturar curvas de aceleração não-lineares (`cubic-bezier`), durações e `@keyframes` diretamente da memória do navegador.
- Medir o delta exato de microinterações (`:hover`, `:focus-visible`) forçadas no motor Blink via `CSS.forcePseudoState`.
- Interceptar código-fonte GLSL de Shaders WebGL1 e WebGL2 via hooks prévios no protótipo de contexto.
- Gerar o contrato semântico `design-tokens.json` e o preview executável `design-system.html` compatíveis com a Paz Cognitiva e o WebMCP da Aurora (`document.modelContext`).

---

## 2. A Arquitetura Canônica de 4 Artefatos + Blueprints Estruturais

O extrator separa o fato observado imutável da decisão de adaptação da Aurora, gerando quatro artefatos vinculados por um `capture_id`:

1. **`design-telemetry.json` (`cdp.telemetry.v1`):** Tokens brutos computados, `@keyframes`, curvas cubic-bezier, deltas de hover forçados via `CSS.forcePseudoState`, classificação tipográfica em 4 papéis semânticos (`typography_roles`), links de fontes e `@font-face` (`font_assets`), **Blueprints de Seções estruturais com slots (`section_blueprints`)** e filtros SVG ativos vinculados a seletores CSS (`active_svg_filters`).
2. **`visual-shader-manifest.json` (`cdp.shaders.v1`):** GLSL puro de shaders WebGL1/WebGL2 interceptados, uniforms detectados, metadados de canvas e pares de screenshots 2x DPI com transição congelada.
3. **`design-tokens.json` (`w3c.design-tokens.v1`):** Contrato semântico estruturado e limpo de cores reais da referência, tipografia por papel (`sans`, `display`, `hand`, `mono`), espaçamentos e raios.
4. **`design-system.html` (`html5.living-spec.v1`):** Living Style Guide executável com catálogo de componentes e arquétipos de layout clonados da referência, sem hardcode de paletas genéricas (`#f8fafc`), motor Vanilla JS seguro e suporte a formulários WebMCP (`:tool-form-active`).

---

## 2.1. Protocolo de Transplante de Conteúdo (Content-Over-Clone)

Todo agente desenvolvedor ou de design do Mad Lab Aurora deve aplicar rigorosamente os seguintes princípios:
1. **Banimento do Card Stacking:** Proibido estruturar páginas empilhando dezenas de `.card` genéricos e idênticos. O layout final deve respeitar os `section_blueprints` extraídos pelo CDP.
2. **Efeitos SVG e Animações Ativas:** Filtros `<filter>` ou `@keyframes` extraídos devem possuir classes CSS funcionais ativas e elementos de teste no Living Style Guide (`.ds-effect-{id}`).
3. **Tipografia por Papéis:** O texto corrido (`body`) utiliza obrigatoriamente `--ds-font-sans`. Fontes caligráficas/manuscritas (`faracohand`, `cursive`) são restritas a `--ds-font-hand` para callouts e anotações marginais. Proibido fallback para fontes genéricas de sistema sem carregar webfonts.

---

## 3. Modelo de Segurança Anti-SSRF e Sanitização

1. **Esquemas Permitidos:** Apenas `http://` e `https://`. Esquemas `file:`, `javascript:`, `data:` são rejeitados de imediato.
2. **Bloqueio Anti-SSRF em 2 Níveis:**
   - **URL Primária:** Checagem de DNS e bloqueio estrito de faixas privadas IPv4 (`127.0.0.0/8`, `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `169.254.0.0/16`) e IPv6 (`::1`, `fc00::/7`, `fe80::/10`).
   - **Sub-recursos:** Guarda `page.route("**/*")` intercepta e aborta requisições secundárias para redes internas.
   - **Service Workers:** Inicializados com `service_workers="block"`, impedindo desvios do roteador.
3. **Zero Injeção de Scripts Externos:** Nenhum script executável de terceiros é copiado para o `design-system.html`. O artefato gerado contém unicamente o motor Vanilla JS interno e padronizado do compilador.

---

## 4. Precedência Constitucional da Doutrina Aurora

Em caso de divergência entre a referência externa e as normas da Aurora, prevalece obrigatoriamente a hierarquia:
$$\text{Doutrina e Emenda v9.1} \;\longrightarrow\; \text{Paz Cognitiva (Aceite de Interface)} \;\longrightarrow\; \text{Regras de Governança} \;\longrightarrow\; \text{Design System Aprovado} \;\longrightarrow\; \text{Implementação}$$

No modo padrão `aurora-agentic`, cores e fundos escuros de alta tensão visual são traduzidos para superfícies funcionais de alta legibilidade (WCAG AA/AAA, orientação $\le 3\text{s}$, zero scroll-jacking). O modo `raw-fidelity` pode ser gerado opcionalmente como `design-system-raw.html` estritamente para estudo técnico.

---

## 5. Como Invocar no Google Antigravity IDE

O servidor FastMCP expõe 3 ferramentas registradas no `mcp_config.json`:

```python
# 1. Extração de telemetria bruta via CDP
extract_cdp_design_telemetry(url="https://referencia.com", output_path="design-telemetry.json")

# 2. Captura de Shaders GLSL e pares 2x DPI
capture_webgl_and_component_states(url="https://referencia.com", output_dir=".antigravity/visual-captures")

# 3. Compilação do Living Design System e Tokens
compile_living_design_system_html(
    telemetry_path="design-telemetry.json",
    visual_manifest_path=".antigravity/visual-captures/visual-shader-manifest.json",
    output_html_path="design-system.html",
    output_tokens_path="design-tokens.json"
)
```

---

## Mesh Contract

```json
{
  "schema_version": "1.0.0",
  "id": "cdp-design-system-extractor",
  "name": "cdp-design-system-extractor",
  "description": "Arquiteto e Engenheiro de Extração de Living Design Systems em HTML via Chrome DevTools Protocol (CDP), Playwright e MCP para o Google Antigravity IDE. Extrai tokens semânticos (:root), física de animação (cubic-bezier), @keyframes, estados forçados de :hover/:focus via CDP, shaders WebGL1/WebGL2 e screenshots 2x DPI de qualquer URL de referência externa. Emite 4 artefatos canônicos versionados (design-telemetry.json, visual-shader-manifest.json, design-tokens.json e design-system.html) calibrados para Paz Cognitiva e WebMCP (document.modelContext).",
  "manual_version": "V9.1",
  "activation": {
    "explicit_commands": [
      "/cdp-extract",
      "/design-system-html",
      "/extract-style"
    ],
    "user_triggers": [
      "extrair design system de uma url",
      "puxar tokens e efeitos de um site",
      "criar living design system em html",
      "fazer engenharia reversa visual com cdp",
      "capturar shaders e hover via devtools"
    ],
    "system_triggers": [
      "URL_REFERENCE_RECEIVED_FOR_DESIGN_SYSTEM",
      "LIVING_STYLE_GUIDE_REQUESTED"
    ],
    "never_activate_for": [
      "decisoes de copy de vendas sem referencia visual",
      "estrategia competitiva b2b sem extracao tecnica"
    ]
  },
  "capabilities": {
    "core": [
      "cdp_cssom_token_extraction",
      "cdp_forced_pseudo_states_measurement",
      "webgl_glsl_shader_interception",
      "high_dpi_component_screenshot_pairing",
      "living_design_system_html_compilation"
    ],
    "optional": [
      "raw_fidelity_comparison_export",
      "svg_filter_extraction"
    ]
  },
  "runtime": {
    "primary_language": "python",
    "dependencies": [
      "mcp==1.27.2",
      "playwright==1.63.0"
    ],
    "entrypoint": "tools/mcp-design-extractor/server.py",
    "execution_mode": "mcp_stdio_daemon"
  },
  "risk_calibration": {
    "blast_radius": "tools/mcp-design-extractor e artefatos gerados no workspace",
    "reversibility": "HIGH",
    "safety_guards": [
      "anti_ssrf_primary_and_subresource_validation",
      "private_network_access_blocked",
      "external_script_injection_prohibited",
      "service_workers_blocked"
    ]
  },
  "quality": {
    "gates": [
      "mcp_handshake_stdio_verified",
      "functional_fixture_test_passed",
      "reprova_adversarial_suite_passed"
    ],
    "metrics": [
      "ssim_visual_fidelity_tolerance",
      "wcag_aa_contrast_conformance",
      "wcag_reduced_motion_compliance"
    ]
  },
  "classification": {
    "agent_class": "producao",
    "risk_level": "LOW",
    "requires_continuous_supervision": false
  },
  "observability": {
    "token_budget": 20000,
    "latency_budget_ms": 60000,
    "cost_estimate_usd": 0.05
  },
  "ontology": {
    "observed_event": "Necessidade de extrair e codificar tokens visuais, física de animação e microinterações de um site de referência para consumo no Antigravity IDE.",
    "produced_memory": "design-telemetry.json, visual-shader-manifest.json, design-tokens.json e design-system.html.",
    "consumed_memory": "Doutrina Aurora, Critério Formal de Aceite de Interface e URL de referência fornecida pelo usuário.",
    "influenced_decision": "Elimina alucinações de estilo e CSS arbitrário ao construir novos componentes e páginas.",
    "impacted_execution": "Fornece Fonte Visual Executável baseada no motor Blink para os agentes geradores de código.",
    "expected_result": "Design System em HTML 100% funcional, auditável, seguro e alinhado com a Paz Cognitiva e WebMCP."
  },
  "anti_patterns": [
    {
      "prohibited": "Copiar scripts JavaScript ou event handlers arbitrários do site de referência para o design-system.html.",
      "because": "Scripts externos não confiáveis introduzem vetores de XSS e execução não auditada no workspace.",
      "signal": "Presença de tags script externas ou inline listeners copiados da referência."
    },
    {
      "prohibited": "Permitir requisições para IPs privados ou loopback (SSRF) fora do ambiente de teste controlado.",
      "because": "Um atacante pode usar o Chromium headless para sondar portas internas ou serviços de nuvem.",
      "signal": "URL de destino resolvendo para faixas RFC 1918 ou 127.0.0.0/8 sem variável de teste."
    },
    {
      "prohibited": "Sobrepor as regras de Paz Cognitiva da Aurora adotando temas escuros agressivos ou WebGL decorativo em produção.",
      "because": "A Doutrina Aurora proíbe que estilos externos quebrem a orientação em <=3s ou a legibilidade WCAG AA/AAA.",
      "signal": "design-system.html em modo de produção forçando dark theme sem aprovação explícita."
    }
  ],
  "operational_memory": {
    "consumed": [
      {
        "description": "Doutrina e critérios de interface do Mad Lab Aurora.",
        "targets": [
          "docs/AGENTS/DOCTRINE.md",
          ".agents/rules/designmanualposthero.md"
        ]
      }
    ],
    "produced": [
      {
        "description": "Manifestos de extração e living design systems.",
        "targets": [
          "design-telemetry.json",
          "design-tokens.json",
          "design-system.html"
        ]
      }
    ],
    "feedback_loop_description": "Falhas em testes de handshake ou violações de segurança alimentam a suíte test_reprova.py."
  },
  "fail_closed_strategy": "Se a URL de referência for inacessível, privada ou violar o filtro anti-SSRF, abortar a execução imediatamente e reportar SecurityViolationError.",
  "tier_policy": {
    "tier": "horizontal",
    "context_policy": {
      "inherits_caller_context": true,
      "persists_after_run": false
    },
    "artifact_residency": "repo",
    "retry_ceiling": 3,
    "registra_tentativas": true
  }
}
```
