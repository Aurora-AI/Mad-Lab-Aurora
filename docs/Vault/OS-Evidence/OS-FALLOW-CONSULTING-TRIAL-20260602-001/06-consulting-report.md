# Consulting Report — Fallow External Trial

## Escopo

Auditoria read-only do repositório C:\Projetos\MadLabAurora usando Fallow via npx, sem instalação permanente, sem aplicação de correções e sem criação de configuração nova.

## Versão do Fallow

fallow 2.86.0

## Comandos executados

- fallow --version
- fallow --format json
- fallow audit --format json --quiet
- fallow dead-code --format json
- fallow dupes --format json
- fallow health --score --hotspots --targets --format json
- fallow fix --dry-run --no-create-config --format json

## Garantias operacionais

- fix --yes não executado
- fix --force não executado
- package.json não alterado
- lockfiles não alterados
- código não alterado
- CI não alterado
- Toolbelt não alterado
- MCP não criado
- .fallowrc.json não criado

## Resumo executivo

O Fallow executou com sucesso via npx e produziu saídas JSON parseáveis nos comandos principais. O resultado mais útil veio de `full`, `dead-code`, `dupes`, `health` e `fix-preview`. O único comando realmente bloqueado foi `audit`, que depende de base branch e de um repositório git detectável; como o workspace não expõe `.git` na raiz, esse fluxo ficou indisponível.

O retrato técnico geral do código é de dívida estrutural real, com muitos arquivos órfãos, imports não resolvidos, duplicação relevante e health score mediano. O que o Fallow encontrou aqui não parece ruído puro: há problemas concretos, mas a ferramenta também sofre limitação clara de ambiente neste workspace.

## Resultado por comando

| Comando | Exit Code | JSON Parseável | Resultado | Observação |
|---|---:|---|---|---|
| fallow full | 0 | sim | útil | 289 issues totais; 203 unused files; 49 unresolved imports. |
| audit | 2 | sim | tool gap | Falhou por falta de base branch e ausência de git no workspace. |
| dead-code | 1 | sim | útil com ruído | 289 issues totais; principalmente unused files. |
| dupes | 0 | sim | alto valor | Clone groups concretos; issue_count_hint 41 no resumo sanitizado. |
| health | 0 | sim | útil | Score 60.9, grade C, duplication 20.2%. |
| fix-preview | 0 | sim | preview somente | 29 propostas de fix, sem mutação. |

## Achados consolidados

### 1. Duplicação concreta

O `dupes` encontrou clone groups reais entre implementações de `ForensicOpening` em:

- ElysianCorp/elysian-motion/src/ForensicOpening.tsx
- ElysianCorp/src/components/motion/ForensicOpening.tsx

Os blocos duplicados são grandes o suficiente para justificar extração de trecho comum ou parametrização. Isso é um achado de valor alto porque reduz manutenção e risco de divergência entre duas implementações muito parecidas.

### 2. Arquivos órfãos e código morto

O `dead-code` apontou 289 issues totais, com destaque para:

- 203 unused files
- 34 unused exports
- 3 unused types
- 49 unresolved imports

Esse perfil sugere uma base com muito código desconectado, módulos não referenciados e possivelmente ativos antigos ainda preservados por precaução. Parte desse material pode ser intencional, mas o volume é alto o bastante para justificar triagem manual.

### 3. Health estrutural mediano

O `health` produziu:

- score 60.9
- grade C
- duplication 20.2%
- dead_file_pct 47.7%
- dead_export_pct 15.1%
- average_maintainability 80.6
- severity_critical_count 28
- severity_high_count 37
- severity_moderate_count 56

O sinal principal aqui não é só a nota, mas a combinação de duplicação alta, taxa grande de arquivos mortos e múltiplas ocorrências de severidade alta/critica. Isso é útil para priorização, mas ainda não substitui análise humana de contexto.

### 4. Preview de fix sem mutação

O `fix --dry-run --no-create-config` gerou 29 propostas de correção, concentradas em remoção de exports aparentemente não usados. Exemplos observados no preview:

- ScrambleBackground
- ScramblePortrait
- GlowCard
- BlackBoxRevealed
- telemetry
- IndustrialGrid

Esse preview é útil como mapa de oportunidades, mas não deve ser tratado como ordem de limpeza automática. Alguns exports podem ser usados indiretamente, por tooling ou por consumo fora do grafo estático do analisador.

## Erros e limitações

### Erros de execução

- `audit` retornou exit code 2 com JSON de erro indicando impossibilidade de detectar base branch.
- `dead-code` retornou exit code 1, mas com JSON parseável e resultados válidos; nesse caso o exit code funciona como verdict de auditoria, não como crash.
- Os comandos de saúde e preview não falharam, mas emitiram warning sobre `node_modules` ausente e hotspot analysis pulado.

### Limitações do ambiente

- O workspace não expõe `.git` na raiz, então a parte diff-based do Fallow não consegue operar plenamente.
- O warning sobre `node_modules directory not found` indica que a análise pode estar menos precisa do que seria com dependências instaladas localmente.
- `health` informou `hotspot analysis skipped: no git repository found at project root`, o que reduz a utilidade do foco em hotspots.

### Ruído e falso positivo prováveis

- Scripts utilitários e harnesses aparecem como dead files, mas podem ser intencionais e merecer WONTFIX em vez de remoção.
- O preview de fix mostra muitos `remove_export`, mas isso não prova que a limpeza seja segura sem checar consumo dinâmico ou composição indireta.

## Apontamentos importantes

1. O Fallow é forte em triagem estrutural ampla, especialmente duplicação e inventário de código morto.
2. O Fallow é fraco neste workspace para auditoria de changeset porque o repo não está disponível como git para o fluxo esperado.
3. O preview de fix é informativo, mas não deve ser promovido a ação automática.
4. A qualidade da evidência é suficiente para consultoria externa, não para gate oficial read-only neste ambiente.

## Avaliação

### Precisão

Boa para duplicação e triagem estrutural. Média para dead-code, porque mistura órfãos reais com utilitários que precisam de contexto humano.

### Utilidade

Alta para priorização de dívida técnica e revisão de monorepo JS/TS.

### Segurança operacional

Boa. O trial permaneceu read-only e o fix foi somente preview.

### Aderência à Aurora

Moderada a boa para o ecossistema JS/TS, mas ainda insuficiente para ingestão como gate oficial neste workspace sem resolver a dependência de git/base branch.

## Próximos passos

1. Manter o Fallow como consultor externo read-only.
2. Reexecutar o trial em um workspace com `.git` real, ou a partir de um checkout completo do repo, para validar o fluxo `audit`.
3. Triar os 203 unused files e os 49 unresolved imports com donos de módulo antes de qualquer remoção.
4. Extrair ou consolidar os blocos duplicados de `ForensicOpening`.
5. Tratar o preview de 29 fixes como backlog de revisão, não como ordem de mudança.
6. Só considerar ingestão futura se a ferramenta mantiver JSON estável e comportamento consistente em ambiente git completo.

## Conclusão técnica

Fallow é útil como auditor externo read-only e entregou achados reais, mas ainda não está pronto para ser gate oficial no MadLabAurora neste ambiente. O ganho principal é em diagnóstico e priorização; o principal bloqueio é a dependência de git/base branch para uma parte importante do fluxo.