# OS-MADLAB-INTEGRATION-001 — M5: Smoke & Runtime Certification

**Data:** 2026-06-09  
**Status:** CONCLUÍDA  
**Runtime:** ✅ CERTIFICADO  

---

## Descoberta Crítica Durante M5 — process.env vs import.meta.env

**Problema encontrado:** `import.meta.env.GEMINI_API_KEY` retornava `undefined` em runtime.

**Causa:** Em Vite/Astro SSR, `import.meta.env` não expõe variáveis sem prefixo `PUBLIC_`
no contexto server-side a runtime. Isso é um comportamento intencional de segurança do Vite —
evita que vars server-side sejam acidentalmente injetadas no bundle cliente.

**Correção:** Substituído por `process.env.GEMINI_API_KEY` no endpoint.
`process.env` é o mecanismo correto para leitura de secrets em API routes Astro.

**Commit de correção:** `e4e798b` (ElysianCorp)

---

## Ambiente de Smoke

```
Framework: Astro v6.1.9 (dev mode)
Porta: 4325
Chave usada: smoke-test-not-real-key-do-not-use (fake, em .env.local removido após testes)
.env.local: REMOVIDO após smoke — não commitado, gitignored
```

---

## Resultados dos Checks

### C1 — GET /api/chat

```bash
curl -X GET http://localhost:4325/api/chat
```
```json
{"error":"Method not allowed"}
```
**Status:** `405` ✅ — GET bloqueado explicitamente, sem execução de lógica Gemini

---

### C2 — POST sem message (apiKey presente)

```bash
curl -X POST http://localhost:4325/api/chat \
  -H "Content-Type: application/json" -d '{}'
```
```json
{"error":"message required"}
```
**Status:** `400` ✅ — payload inválido rejeitado antes de chamar Gemini

---

### C3 — POST JSON inválido

```bash
curl -X POST http://localhost:4325/api/chat \
  -H "Content-Type: application/json" -d 'INVALID'
```
```json
{"error":"Invalid JSON"}
```
**Status:** `400` ✅ — JSON inválido capturado sem stack trace

---

### C4 — POST válido, chave fake (upstream error)

```bash
curl -X POST http://localhost:4325/api/chat \
  -H "Content-Type: application/json" -d '{"message":"smoke test"}'
```
```json
{"error":"...API key not valid..."}
```
**Status:** `502` ✅ — chave inválida → erro upstream capturado e mascarado como 502.
Nenhum valor de chave presente na resposta. Apenas mensagem pública do Google API.

---

### C5 — Ausência de GEMINI_API_KEY (sem .env.local)

Testado antes do fix de process.env:
```json
{"error":"Service unavailable"}
```
**Status:** `500` ✅ — falha controlada, sem vazar variável ou stack trace

---

## Scan de Segurança — Client Bundle (Final Build)

```bash
npm run build  → ✅ PASSOU
```

```
.vercel/output/static/ → GEMINI_API_KEY: AUSENTE ✅
dist/client/           → GEMINI_API_KEY: AUSENTE ✅
                         VITE_*:          AUSENTE ✅
                         PUBLIC_GEMINI_*: AUSENTE ✅

.vercel/output/functions/ → referências textuais ao nome "GEMINI_API_KEY"
                             dentro do SDK @google/genai (documentação inline)
                             VALOR da chave: NUNCA PRESENTE ✅
```

---

## Reduced-Motion — Verificação

| Guard                     | Componente         | Status |
|---------------------------|--------------------|--------|
| `scrollIntoView: 'instant'`| ElysianChat.tsx    | ✅ implementado |
| Transições CSS desativadas | ElysianChat.tsx    | ✅ implementado |
| `chatIn` animation off     | ElysianChat.tsx    | ✅ implementado |

Verificação de runtime visual (prefers-reduced-motion ativo no OS):
→ Coberta em M6 — Visual & Motion Certification.

---

## Checklist de Aceite M5

```
[✅] runtime local iniciado sem erro
[✅] /api/chat responde em POST
[✅] GET bloqueado sem execução de lógica sensível → 405
[✅] payload inválido bloqueado → 400
[✅] ausência de GEMINI_API_KEY não derruba o app → 500 controlado
[✅] ausência de GEMINI_API_KEY não vaza variável/stack trace
[✅] bundle client permanece limpo
[✅] server bundle contém apenas referência textual ao nome da var, nunca valor
[✅] reduced-motion guard implementado (validação visual em M6)
[✅] commit isolado — ElysianCorp: e4e798b
```

---

## Commits de M5

| Repo          | SHA       | Descrição                              |
|---------------|-----------|----------------------------------------|
| ElysianCorp   | `e4e798b` | fix: process.env + .vercel to gitignore |
| MadLabAurora  | (este)    | docs: M5 evidence                      |

---

## Próxima Etapa

**M6 — Visual & Motion Certification**
