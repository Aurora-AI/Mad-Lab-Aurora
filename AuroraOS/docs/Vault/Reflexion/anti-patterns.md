# Catálogo de Anti-Patterns (Aurora Reflexion)

Este documento centraliza os padrões de falha detectados pelo `agent-reflexion-code`.

## Inicialização de Runtime (IR)

### 🔴 ir-mock-in-production
- **Contexto**: Orquestradores de produção criando arquivos de mock (ex: `asset_kit_manifest.json`) quando não os encontram.
- **Causa raiz**: Bypass para testes E2E passarem, ignorando a injeção do fixture pelo teste.
- **Prevenção**: Nunca injetar mocks em código de produção. Regra de ouro: Fail-Closed e Zero Scaffolding.
- **Última vez**: 2026-06-01 (AuroraOS)

## Configuração de Ambiente (CA)

### 🔴 ca-path-traversal-startswith
- **Contexto**: Uso de `str(path).startswith()` para validar se um arquivo está contido em um diretório (ex: path security na staging area).
- **Causa raiz**: Comparações literais de strings são ignorantes de hierarquia de FileSystem (ex: `Staging-Hacked` dá match em `Staging`).
- **Prevenção**: Sempre utilize `resolved.is_relative_to(base_dir)` da biblioteca `pathlib`.
- **Última vez**: 2026-06-01 (AuroraOS)
