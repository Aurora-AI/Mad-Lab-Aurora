# OS-MADLAB-INTEGRATION-001 — M4: Controlled Integration Candidate

**Data:** 2026-06-09  
**Status:** CONCLUÍDA  
**Build:** ✅ PASSOU  

---

## Arquivos Criados / Modificados

| Arquivo                                          | Tipo      | Ação               |
|--------------------------------------------------|-----------|--------------------|
| `ElysianCorp/astro.config.mjs`                   | Config    | Modificado         |
| `ElysianCorp/src/pages/api/chat.ts`              | Endpoint  | Criado             |
| `ElysianCorp/src/components/ui/ElysianChat.tsx`  | Island    | Criado (promovido) |

---

## astro.config.mjs — Mudanças

```js
// Adicionado:
import vercel from '@astrojs/vercel';

// output: 'static' (Astro v6 — 'hybrid' removido; comportamento híbrido é o padrão)
// adapter: vercel() — necessário para server endpoints rodarem no Vercel
output: 'static',
adapter: vercel(),
```

**Descoberta durante M4:** `output: 'hybrid'` foi removido no Astro v6.1.x.
O comportamento híbrido (SSG por padrão + endpoints server opt-in) é agora o padrão
do `output: 'static'` quando um adapter está presente. Config corrigida e documentada.

---

## /api/chat — Astro Server Endpoint

```
Arquivo: src/pages/api/chat.ts
export const prerender = false  ✅ (opt-out SSG — roda server-side)
Método aceito: POST             ✅
GET explicitamente bloqueado    ✅
GEMINI_API_KEY via import.meta.env (server-only, sem PUBLIC_) ✅
Falha sem apiKey: 500, sem vazar segredo ✅
Payload sem message: 400 ✅
JSON inválido: 400 ✅
Erro upstream: 502 ✅
```

---

## ElysianChat — Island Promovida

```
Arquivo: src/components/ui/ElysianChat.tsx
Directive recomendada: client:load
Reduced-motion guard: ✅
  - scrollIntoView: 'instant' quando prefers-reduced-motion
  - transições CSS desativadas quando prefers-reduced-motion
  - animação chatIn desativada quando prefers-reduced-motion
Chamada /api/chat: fetch POST ✅ (sem mudança de contrato)
Nenhuma referência a GEMINI_API_KEY no client ✅
```

---

## Dependências Instaladas

| Pacote           | Versão    | Motivo                              |
|------------------|-----------|-------------------------------------|
| `@astrojs/vercel`| ^10.0.8   | Adapter para server endpoints       |
| `@google/genai`  | ^2.8.0    | SDK Gemini no server endpoint       |
| `lenis`          | N/A       | NÃO instalado — uso confirmado ausente no destino |

---

## Resultado do Build

```
astro build
output: "static"
mode: "server"
adapter: @astrojs/vercel
✓ prerendered: /index.html, /halide-demo, /wave-demo
✓ server function bundled
✓ Complete in 30.03s
```

---

## Scan de Segurança — Bundle Client

```
Scan: .vercel/output/static/ + dist/client/
GEMINI_API_KEY  → AUSENTE no client bundle ✅
VITE_*          → AUSENTE no client bundle ✅
PUBLIC_GEMINI   → AUSENTE no client bundle ✅

Scan: .vercel/output/functions/ (server-side)
GEMINI_API_KEY  → presente apenas no SDK @google/genai
                  (referências literais à string do env var name — esperado)
                  VALOR da chave: nunca presente ✅
```

---

## Checklist de Aceite M4

```
[✅] build executa
[✅] astro config não força SPA
[✅] páginas continuam SSG por padrão (prerendered)
[✅] /api/chat usa export const prerender = false
[✅] /api/chat aceita apenas POST (GET → 405)
[✅] payload sem message → 400
[✅] ausência de GEMINI_API_KEY → 500 sem vazar segredo
[✅] nenhuma variável PUBLIC_GEMINI_API_KEY
[✅] nenhuma variável VITE_GEMINI_API_KEY
[✅] nenhum segredo no client bundle
[✅] React entra como island (ElysianChat via client:load)
[✅] escopo restrito aos 3 arquivos planejados
[✅] commit isolado da M4
```

---

## Restrições Preservadas

```
[✅] PR não aberto
[✅] Promotion Package não gerado ainda
[✅] Deploy produtivo não executado como conclusão da M4
[✅] Open Design não alterado
[✅] Checkout local não versionado
[✅] Nenhum fallback inseguro para API key
```

---

## Próxima Etapa

**M5 — Smoke & Runtime Certification**
