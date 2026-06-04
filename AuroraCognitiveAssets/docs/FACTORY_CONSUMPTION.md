# Factory Consumption

## Papel deste repositorio

`AuroraCognitiveAssets` e um `product` consumidor. Ele nao e source of truth de governanca e nao e source of truth da fabrica.

## Capacidade consumida

- sistema governado: `infoproduct-factory`
- pacote formal previsto: `@aurora/infoproduct-factory-contracts`
- servico runtime ativo: `@aurora/infoproduct-factory-service`
- fonte executavel do ativo: `Ozzmosis`
- fonte de governanca: `Aurora`

## Regra de integracao

Este produto so pode consumir a Infoproduct Factory por:

- pacote versionado
- API/servico tipado

Fica proibido:

- importar arquivos de `Ozzmosis` por path local
- copiar contratos da fabrica para dentro deste repositorio como verdade primaria
- transformar este produto em ownership tecnico da capacidade

## Estado atual

O manifesto do produto declara o contrato compartilhado e o servico tipado da fabrica.

Para `AuroraCognitiveAssets`, a integracao operacional ativa e via API tipada, porque a superficie atual do produto e Python-oriented e nao um workspace Node consumidor do pacote TS.

Integracoes futuras podem continuar usando o pacote compartilhado apenas como contrato canonico de referencia, mas o runtime deste produto deve permanecer desacoplado por HTTP/API enquanto esta topologia for mantida.

## Superficie de consumo atual

O cliente Python deste produto consome os endpoints tipados da fabrica para:

- `health`
- `intake`
- `GET /pipeline/runs/:runId`
- `research`
- `architecture`
- `review`
- `distribution`

Os endpoints genericos `validate` e `advance` permanecem disponiveis apenas como utilitarios auxiliares. O fluxo operacional principal do produto deve preferir os endpoints explicitos por estagio.

## Autenticacao

Quando o servico da fabrica estiver protegido, este produto deve enviar bearer token via variavel de ambiente:

- `INFOPRODUCT_FACTORY_TOKEN`
- `INFOPRODUCT_FACTORY_TOKEN_FILE`

`health` pode permanecer publico para observabilidade basica, mas os endpoints de pipeline devem ser tratados como superficie autenticada.

Para operacao local, prefira `INFOPRODUCT_FACTORY_TOKEN_FILE` apontando para um arquivo nao-versionado com o valor do token.

## Escopos minimos

Para o fluxo operacional atual deste produto, o token provisionado precisa carregar:

- `pipeline:read`
- `pipeline:write`

Tokens apenas de leitura podem consultar execucoes e validacoes, mas nao devem iniciar ou avancar pipeline.

## Identidade de consumidor

Quando a fabrica operar com binding por consumidor, este produto deve enviar:

- `X-Aurora-Consumer: AuroraCognitiveAssets`

No cliente Python, isso deve ser resolvido por:

- `INFOPRODUCT_FACTORY_CONSUMER_ID=AuroraCognitiveAssets`

## Identidade de ambiente

Quando a fabrica operar com binding por ambiente, este produto deve enviar:

- `X-Aurora-Environment: dev`

No cliente Python, isso deve ser resolvido por:

- `INFOPRODUCT_FACTORY_ENVIRONMENT=dev`

## Auditoria de acesso

As operacoes autenticadas deste produto contra a fabrica devem produzir trilha de auditoria persistida por `runId`, com:

- `principal`
- `consumer`
- `environment`
- `scope`
- `action`
- `occurredAt`

Para este consumidor, o comportamento esperado minimo e:

- `pipeline:intake` auditado na escrita inicial
- `pipeline:get_run` auditado em leituras autenticadas de execucao

## Estado macro da integracao

A macro etapa de endurecimento e operacionalizacao da integracao foi concluida.

Estado esperado para este produto:

- consumo do pipeline completo por API tipada
- autenticacao por bearer token com escopos
- binding por consumidor e ambiente
- auditoria persistida com `principal`, `keyId`, `consumer`, `environment`, `scope` e `action`
- ciclo de credenciais gerido pela fabrica com planner e cutover no lado `Ozzmosis`
- manutencao preventiva de credenciais avaliada pela fabrica por policy de ambiente e janela de expiracao

Este repositorio continua apenas como consumidor operacional. O lifecycle das credenciais e a politica primaria de acesso permanecem fora deste produto.
