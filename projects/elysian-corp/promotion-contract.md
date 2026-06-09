# Elysian-Corp — Promotion Contract

**Versão:** 0.1.0-draft  
**Data:** 2026-06-09  
**Decisão base:** DEC-MADLAB-PRODUCT-WORKSPACE-BOUNDARY-001

---

## O que constitui um promotion package válido

Para que artefatos do Mad Lab sejam promovidos ao repo soberano `Aurora-AI/Elysian-Corp`,
o package deve conter:

| Item | Obrigatório | Descrição |
|---|---|---|
| `promotion-manifest.json` | ✅ | Inventário de artefatos, versões, hashes |
| `PromotionApprovalRecord.md` | ✅ | Assinado pelo owner (Rodrigo Cesar Winhaski) |
| Artefatos de build (tokens, componentes, motion hooks) | ✅ | Copiados de `docs/OS/OS-MADLAB-BUILD-001/` |
| QA gate report | ✅ | qa-review aprovado (APPROVED ou APPROVED WITH CAVEATS) |
| Open items resolvidos | ✅ | Logo, assets, copy, focus states, device tests |
| `anti-clone-verification.json` | ✅ | 7/7 PASS confirmado |

## Condições herdadas do BUILD-001

```
[ ] Copy Trustware — "Zero tolerância a dívida técnica" (princípio, não estado)
[ ] Stats lastreados — "84 Gates de QA" verificados
[ ] Assets proprietários — placeholders substituídos ou decisão explícita
[ ] Logo definitivo — decision registrada
[ ] Keyboard focus states — testados visualmente
[ ] Copy final — aprovação criativa explícita
[ ] Testes em dispositivo real — iOS, Android, desktop older
[ ] Integração Next.js validada — OS-MADLAB-INTEGRATION-001
```

## O que NÃO constitui promoção

- Cópia manual de arquivos sem manifest
- PR direto no repo soberano sem PromotionApprovalRecord
- "Está pronto, só falta testar" — gates são obrigatórios
- Subir código do workspace local (`checkouts/Elysian-Corp/`) sem passar pela transfer zone

## Transfer zone

```
transfer/ready/elysian-corp/
```

Nenhum artefato parte do Mad Lab sem passar por este ponto.
