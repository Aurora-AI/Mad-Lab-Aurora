# Promotion Package — Elysian-Corp Astro Islands Integration

**OS de origem:** OS-MADLAB-INTEGRATION-001 — Astro Islands Integration Bridge  
**Data:** 2026-06-09  
**Status:** PRONTO PARA PR  
**Aprovação humana:** OBRIGATÓRIA antes de merge no repo soberano  

---

## Nome da Integração

```
elysian-corp-astro-islands-integration
```

Ponte de integração entre o candidato visual/técnico do Mad Lab Aurora e o
repositório soberano `Aurora-AI/Elysian-Corp`, executada por contrato via Promotion Package.

---

## Objetivo Visual

Integrar o componente `ElysianChat` como Astro Island no produto soberano,
preservando a identidade visual forense, a densidade tipográfica e o padrão
cinematográfico já certificados em produção em `elysian.ia.br`.

O componente deve aparecer como extensão orgânica do produto — não como widget
externo ou adição genérica.

---

## Objetivo Técnico

- Adicionar endpoint `/api/chat` como Astro server route (server-side Gemini proxy)
- Preservar `GEMINI_API_KEY` exclusivamente server-side
- Adicionar `ElysianChat` como island `client:load`
- Habilitar SSR parcial no repo soberano via `output: 'static'` + `@astrojs/vercel`
- Preservar comportamento SSG em todas as páginas existentes

---

## Arquitetura Astro Islands

```
ElysianCorp/
├── astro.config.mjs          ← output: 'static' + adapter: vercel()
├── src/
│   ├── pages/
│   │   ├── index.astro       ← SSG (prerendered — sem mudança)
│   │   └── api/
│   │       └── chat.ts       ← server endpoint (prerender=false)
│   └── components/
│       └── ui/
│           └── ElysianChat.tsx ← island client:load
└── package.json              ← +@astrojs/vercel +@google/genai
```

**Modelo de hidratação:**
- Páginas → SSG por padrão (sem mudança de comportamento)
- `/api/chat` → `prerender = false` → executa server-side em runtime
- `ElysianChat` → `client:load` → hidrata imediatamente no client

---

## Componentes Promovidos

### ElysianChat.tsx
- **Origem:** `aurora-web/src/components/ElysianChat.tsx`
- **Destino:** `ElysianCorp/src/components/ui/ElysianChat.tsx`
- **Directive:** `client:load`
- **Função:** Interface de qualificação de prospects via Oráculo Elysian
- **Trigger:** Visível após 45% de scroll da viewport (zero impacto no FCP)
- **Reduced-motion:** ✅ guard implementado (scroll instant, transitions off, chatIn off)

### Instrução de uso em index.astro

```astro
---
import ElysianChat from '../components/ui/ElysianChat';
---
<ElysianChat client:load />
```

---

## API — /api/chat

| Campo            | Valor                                     |
|------------------|-------------------------------------------|
| Endpoint         | `POST /api/chat`                          |
| Auth             | Nenhuma (server-side key auth com Gemini) |
| Método bloqueado | GET → 405                                 |
| Payload          | `{ message: string, history?: [], systemInstruction?: string }` |
| Response 200     | `{ text: string }`                        |
| Response 400     | `{ error: "message required" \| "Invalid JSON" }` |
| Response 500     | `{ error: "Service unavailable" }` (sem apiKey) |
| Response 502     | `{ error: "Upstream provider unavailable" }` (erro Gemini) |
| Segredo exposto  | NUNCA — apenas `process.env.GEMINI_API_KEY` server-side |

---

## Variáveis de Ambiente

| Variável         | Ambiente         | Tipo       | Obrigatório |
|------------------|------------------|------------|-------------|
| `GEMINI_API_KEY` | Production + Preview | Encrypted | SIM |

**Configuração:**
```
Vercel Dashboard → aurora-mycelium/elysiancorpfront
→ Settings → Environment Variables
→ Add: GEMINI_API_KEY (Encrypted, Production + Preview)
```

**Proibido:**
```
PUBLIC_GEMINI_API_KEY  → expõe ao client bundle
VITE_GEMINI_API_KEY    → Astro não usa VITE_ convention
```

---

## Dependências Adicionadas

| Pacote            | Versão    | Motivo                              |
|-------------------|-----------|-------------------------------------|
| `@astrojs/vercel` | ^10.0.8   | Adapter para server endpoints Astro |
| `@google/genai`   | ^2.8.0    | SDK Gemini no server endpoint       |

**Não adicionado:** `lenis` — uso confirmado ausente no destino.

---

## Budgets de Performance

| Métrica                    | Impacto da integração               |
|----------------------------|-------------------------------------|
| First Contentful Paint     | Zero — ElysianChat oculto até 45% scroll |
| JavaScript bundle (client) | +ElysianChat island (~8KB estimado) |
| Server cold start          | +Gemini SDK no server bundle        |
| GEMINI_API_KEY              | Nunca no client bundle              |

---

## Fallback Mobile

```tsx
// ElysianChat.tsx — largura adaptativa
width: 'min(400px, calc(100vw - 4rem))'
```

O painel de chat se adapta a viewports estreitas via CSS `min()`.
Em mobile, ocupa `100vw - 4rem` máximo — não quebra layout.

---

## Reduced-Motion Contract

| Comportamento                  | Normal          | prefers-reduced-motion |
|-------------------------------|-----------------|------------------------|
| Scroll para nova mensagem      | `smooth`        | `instant`              |
| Transição do botão toggle      | `0.4s ease`     | `none`                 |
| Animação de abertura do painel | `chatIn 0.4s`   | `none`                 |
| Transição do botão enviar      | `0.3s ease`     | `none`                 |

Guard implementado via `window.matchMedia('(prefers-reduced-motion: reduce)')`.

---

## Riscos e Limitações

| Risco                                      | Severidade | Status       |
|--------------------------------------------|------------|--------------|
| GEMINI_API_KEY exposta ao client           | P0         | ✅ Mitigado  |
| Gitlink/submodule orphan no Mad Lab        | P0         | ✅ Mitigado  |
| Código soberano versionado no Mad Lab      | P0         | ✅ Mitigado  |
| 502 vaza mensagem upstream (R-001)         | P1         | ✅ Corrigido |
| Reduced-motion em componentes preexistentes| P2         | ⚠️ Backlog  |
| Screenshot mobile não capturado (R-003)    | P2         | ⚠️ Backlog  |
| lenis ausente no destino                   | P2         | ✅ Verificado — não necessário |

---

## Backlog Controlado

```
BL-001 [R-002] — Auditar reduced-motion em componentes preexistentes do ElysianCorp
BL-002 [R-003] — Capturar screenshot mobile em viewport 375px antes de release final
```

Estes itens não bloqueiam o PR do pacote de integração.
Devem ser abertos como issues no repo soberano após merge.

---

## Rollback Plan

```
[ ] Rollback = reverter commit no branch do PR (não merge direto em main)
[ ] Reverter: git revert <commit-sha>
[ ] Não requer mudança de config Vercel se GEMINI_API_KEY for mantida
[ ] Se GEMINI_API_KEY removida: endpoint retorna 500 controlado (sem crash)
[ ] Mad Lab Aurora não é afetado por rollback no repo soberano
[ ] Registrar motivo no evidence OS-MADLAB-INTEGRATION-001 antes de fechar como BLOQUEADA
```

---

## Checklist Trustware

```
[✅] Segredo nunca exposto ao client
[✅] Endpoint valida método, payload e chave antes de chamar upstream
[✅] Erro upstream normalizado — nunca vaza stack trace ou mensagem interna
[✅] Componente promovido tem reduced-motion guard
[✅] Boundary de produto soberano preservada (nenhum código soberano no Mad Lab)
[✅] Promotion Package documenta rollback
[✅] Aprovação humana obrigatória antes de merge
[✅] Build certificado em dois ambientes (local + produção Vercel)
[✅] Runtime smoke certificado (M5)
[✅] Visual certificado em produção (M6)
[⚠️] BL-001 e BL-002 abertos como backlog — não bloqueantes
```

---

## Instrução de PR para o Repo Soberano

### 1. Branch

```bash
cd ElysianCorp
git checkout -b feat/astro-islands-integration
```

### 2. Commits incluídos

```
a42bc7d  feat(integration): M4 — Astro Islands controlled integration candidate
e4e798b  fix(api): use process.env + .vercel to gitignore
dfb4879  fix(api): R-001 — normalize 502 error surface
```

### 3. Diff esperado

```
+ astro.config.mjs          — output: 'static' + adapter: vercel()
+ src/pages/api/chat.ts     — Gemini proxy server endpoint
+ src/components/ui/ElysianChat.tsx — island client:load
+ package.json              — @astrojs/vercel, @google/genai
```

### 4. Pré-merge obrigatório

```
[ ] GEMINI_API_KEY configurada no Vercel do elysiancorpfront (Production + Preview)
[ ] Build passa no PR preview deployment
[ ] /api/chat responde via POST no preview deployment
[ ] Aprovação humana registrada
```

### 5. Pós-merge

```
[ ] Abrir BL-001 como issue: reduced-motion em componentes preexistentes
[ ] Abrir BL-002 como issue: screenshot mobile 375px
[ ] Registrar merge SHA no evidence OS-MADLAB-INTEGRATION-001
```

---

## Veredito

```
PRONTO PARA PR
Aguardando aprovação humana para abertura do PR no repo soberano.
```
