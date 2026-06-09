# OS-MADLAB-INTEGRATION-001 — M3: Astro Islands Integration Plan

**Data:** 2026-06-09  
**Status:** PLANO — aguardando aprovação antes de implementação  

---

## Emenda Nominal — Correção Arquitetural

| Campo               | Valor anterior              | Valor corrigido                       |
|---------------------|-----------------------------|---------------------------------------|
| Nome técnico da OS  | Next.js Integration Bridge  | **Astro Islands Integration Bridge**  |
| Framework destino   | Next.js (assumido)          | **Astro v6.1.9 + React Islands**      |

**M1 e M2 preservadas.** Lineage intacta. Apenas o nome técnico da travessia é corrigido.

> A travessia não é Next.js.  
> A travessia é Astro Islands.  
> React entra como organismo hidratado, não como SPA soberano.

---

## Contexto Arquitetural

### Origem
```
C:\Projetos\MadLabAurora\aurora-web\
Framework: Vite + React SPA
Entry: src/main.tsx → App.tsx
Routing: react-router-dom (client-side)
Bundle: SPA completo no client
```

### Destino
```
C:\Projetos\MadLabAurora\ElysianCorp\
Framework: Astro v6.1.9 + @astrojs/react
Output: static (implícito — sem adapter configurado)
Entry: src/pages/index.astro
Routing: Astro file-based (SSG por padrão)
Hydration: client:* directives por island
```

---

## Decisão Arquitetural Crítica — output mode & adapter

### Problema
O destino está em **modo estático puro** (sem `output` declarado no `astro.config.mjs`,
sem adapter configurado). Para `/api/chat` funcionar como server endpoint em runtime,
o projeto precisa de:

1. `output: 'hybrid'` no `astro.config.mjs` (estático por padrão, endpoints podem optar por server)
2. Adapter `@astrojs/vercel` instalado

Sem isso, um endpoint com `export const prerender = false` **falha no build**.

### Decisão: output hybrid + @astrojs/vercel

```js
// astro.config.mjs — mudança planejada
import vercel from '@astrojs/vercel';

export default defineConfig({
  output: 'hybrid',          // páginas estáticas + endpoints server-side
  adapter: vercel(),
  integrations: [react()],
  // ... resto preservado
});
```

**Justificativa:** `hybrid` preserva o comportamento SSG atual de todas as páginas
(sem regressão) e habilita apenas os endpoints que optarem por `prerender = false`.

---

## Componentes — Classificação por Client Directive

### Componentes candidatos vindos da origem

| Componente              | Directive recomendada | Justificativa                                      |
|-------------------------|----------------------|----------------------------------------------------|
| `ElysianChat.tsx`       | `client:load`        | UI interativa — deve estar pronta ao carregar       |
| `Preloader.tsx`         | `client:load`        | Roda na entrada da página, precisa de JS imediato  |
| `SovereignHeroWebGL.tsx`| `client:load`        | WebGL — requer instância Three.js no client        |
| `ScrollDriver.tsx`      | `client:load`        | Controla scroll global — inicialização imediata    |
| `useScrollProgress`     | N/A (hook)           | Integrar nos componentes que já usam no destino    |

### Padrão de islands já em uso no destino (referência)

| Componente              | Directive atual      |
|-------------------------|----------------------|
| `MagneticCursor`        | `client:load`        |
| `Header`                | `client:load`        |
| `GazeForensicHero`      | `client:load`        |
| `IntegrityGap`          | `client:visible`     |
| `ControlFailure`        | `client:visible`     |
| `TrustwareReality`      | `client:visible`     |
| `MotionViewer`          | `client:only="react"`|

---

## Estratégia: /api/chat no Astro

### Arquivo alvo
```
ElysianCorp/src/pages/api/chat.ts
```

### Estrutura planejada
```ts
// src/pages/api/chat.ts
export const prerender = false;  // ← opt-out de SSG — roda server-side

import type { APIRoute } from 'astro';

export const POST: APIRoute = async ({ request }) => {
  const apiKey = import.meta.env.GEMINI_API_KEY;
  if (!apiKey) {
    return new Response(JSON.stringify({ error: 'Service unavailable' }), { status: 500 });
  }

  const body = await request.json().catch(() => null);
  if (!body?.message) {
    return new Response(JSON.stringify({ error: 'message required' }), { status: 400 });
  }

  const { GoogleGenAI } = await import('@google/genai');
  const ai = new GoogleGenAI({ apiKey });
  const chat = ai.chats.create({
    model: 'gemini-2.0-flash',
    config: { systemInstruction: body.systemInstruction },
    history: body.history ?? [],
  });

  const response = await chat.sendMessage({ message: body.message });
  return new Response(JSON.stringify({ text: response.text }), { status: 200 });
};
```

**Diferença vs origem:** usa `APIRoute` do Astro em vez de `VercelRequest/VercelResponse`.
Semanticamente idêntico. `GEMINI_API_KEY` lida via `import.meta.env` (server-side em Astro
com SSR/hybrid — não exposta ao client por não ter prefixo `PUBLIC_`).

---

## Estratégia: GEMINI_API_KEY no ElysianCorp

```
Ação necessária (fora do código):
1. Acessar: https://vercel.com/aurora-mycelium/elysiancorpfront/settings/environment-variables
2. Adicionar: GEMINI_API_KEY (Encrypted, Production + Preview)
3. NÃO usar prefixo PUBLIC_ (exporia ao client)
4. NÃO usar prefixo VITE_ (não existe em Astro)
```

> Em Astro, variáveis sem prefixo `PUBLIC_` são server-only.
> `import.meta.env.GEMINI_API_KEY` no servidor = seguro.
> `import.meta.env.PUBLIC_GEMINI_API_KEY` no client = exposto — PROIBIDO.

---

## Dependências a Adicionar no Destino

| Pacote              | Motivo                                    | Onde instalar         |
|---------------------|-------------------------------------------|-----------------------|
| `@astrojs/vercel`   | Adapter para output hybrid + server routes| ElysianCorp           |
| `@google/genai`     | SDK Gemini para /api/chat                 | ElysianCorp           |
| `lenis`             | Smooth scroll (presente na origem)        | ElysianCorp — avaliar |

### Comando planejado (não executado ainda)
```bash
cd ElysianCorp
npm install @astrojs/vercel @google/genai
```

`lenis`: verificar se `GazeForensicHero` ou outro componente ativo no destino já usa
scroll nativo / GSAP ScrollSmoother antes de instalar.

---

## Estratégia: Reduced-Motion

| Componente            | Status na origem          | Plano no destino                        |
|-----------------------|---------------------------|-----------------------------------------|
| `Preloader.tsx`       | `useReducedMotion()` ✅   | Preservar ao promover como island       |
| `useScrollProgress`   | media query guard ✅      | Preservar ao integrar hook              |
| Islands do destino    | Verificar individualmente | Adicionar guard onde ausente em M4      |

**Regra:** nenhum componente promovido perde o reduced-motion guard.

---

## Estratégia: Assets

```
Verificar antes de mover:
- aurora-web/public/hero_bg.png → ElysianCorp/public/
- aurora-web/public/fonts/      → ElysianCorp/public/fonts/
- Paths em CSS/TSX atualizados para /assets/ ou /public/ do destino
```

---

## Rollback Plan

```
[ ] Qualquer mudança ocorre em branch isolado no ElysianCorp
[ ] Nunca em main diretamente
[ ] Rollback = reverter commit no branch candidato
[ ] Promotion Package invalidado se rollback necessário
[ ] Motivo registrado em evidence antes de fechar OS como BLOQUEADA
[ ] Mad Lab nunca é afetado por rollback no soberano
```

---

## O Que Este Plano NÃO Autoriza

```
[ ] Nenhuma instalação de dependência ainda
[ ] Nenhuma alteração em astro.config.mjs ainda
[ ] Nenhuma criação de src/pages/api/chat.ts ainda
[ ] Nenhuma cópia de componente ainda
[ ] Nenhum deploy ainda
[ ] Nenhuma configuração de env var no Vercel ainda
```

**Toda implementação começa apenas após aprovação deste plano.**

---

## Checklist de Aceite M3

```
[✅] OS renomeada conceitualmente para Astro Islands Integration Bridge
[✅] task.md será atualizado sem apagar histórico
[✅] plano declara que destino NÃO é Next.js
[✅] /api/chat planejado como Astro server endpoint (src/pages/api/chat.ts)
[✅] verificação de adapter/output Astro incluída — output: hybrid + @astrojs/vercel
[✅] GEMINI_API_KEY planejada no Vercel do ElysianCorp (sem PUBLIC_ prefix)
[✅] VITE_ prefix proibido no destino (Astro não usa VITE_ convention)
[✅] islands classificadas por client:load / client:visible / client:only
[✅] dependências faltantes listadas antes de instalação
[✅] rollback plan definido
[✅] nenhuma alteração técnica executada
```

---

## Próxima Etapa

**M4 — Controlled Integration Candidate** — autorizado apenas após aprovação deste plano.
