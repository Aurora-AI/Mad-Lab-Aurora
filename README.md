# MadLabAurora

Braco criativo do ecossistema Aurora.

## Papel canonico

- concentrar propriedades web institucionais e ativos criativos
- agrupar produtos cognitivos ligados a narrativa, conteudo e distribuicao
- manter esses ativos fora da raiz do portfolio e fora da fabrica Ozzmosis

## Topologia canonica

```text
C:\Projetos\MadLabAurora\          ← path canonico
├── aurora-web/                    ← site institucional Elysian
├── AuroraCognitiveAssets/         ← factory de infoprodutos cognitivos
├── integrations/                  ← runtimes de integracao (open-design, etc)
├── .aurora/                       ← skills, domain-policy, toolbelt-consumer
├── docs/
│   ├── OS/                        ← Ordens de Servico (evidencia auditavel)
│   └── Vault/                     ← decisoes, KIs, threads append-only
├── projects/                      ← contratos e manifests de produtos
├── transfer/ready/                ← zona de transferencia para repos soberanos
└── checkouts/                     ← workspaces locais (ignorados pelo git)
    └── Elysian-Corp/              ← produto soberano: github.com/Aurora-AI/Elysian-Corp
```

## Regras

- sites institucionais e brand experiences vivem aqui
- produtos criativos podem viver aqui quando pertencem ao braco criativo
- ativos compartilhados e reutilizaveis da plataforma continuam em Ozzmosis
- agentes transversais continuam em aurora-agents
- codigo publicavel de produtos soberanos NAO pertence a este repo (ver docs/Vault/Decisions/)
