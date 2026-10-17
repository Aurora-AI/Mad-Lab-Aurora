# Tone Lab OS — publicação e QA
Data: 05/10/2026. Veredito: APROVADO COM RESSALVAS para a migração operacional inicial.
Site privado: https://tone-lab-os.winhaski.chatgpt.site
Fonte isolada: C:\Projetos\MadLabAurora\tone-lab-site. Protótipo preservado.
Commit publicado: dc7eab5b6324e4fcbc0054384d6cf7cbae19be89
Deployment: appgdep_6ac40eb4e35c8191b75840ced69b6b07 — succeeded.
Versão: appgprj_6ac3e362caf88191ab03672283f12c4a~appgver_e87aab4a058081918e36d44c7771816d

## Matriz de critérios
| Critério | Estado | Evidência |
|---|---|---|
| Fundação persistente | feito | D1 entities/relations/history; R2 privado; migrations aplicadas; revisão otimista e conflitos 409 |
| Store → Dossier e captura contextual | feito | UI real, rotas publicadas, dark Store e Dossier off-white; filtro, busca, formulário contextual |
| Research → Inbox → Promote → Related | feito | RES-2026-c042aff3-2764-4dd5-a5e8-ebe1378ac257, revisão 5; percurso UI com D1 hospedado; registro promovido reaparece no navegador direto publicado |
| Schematic → revision → Project History | feito | DOC-2026-8356139e-bad6-46bc-937f-2da572660993, PDF MOCK, QA-01 → QA-02, snapshots e histórico em Signature |
| Purchase → Dossier | feito | PUR-2026-4e883a4f-4606-4930-b51b-dceed6e0bd7e, fornecedor e preço MOCK identificados na UI |
| Recuperação dos testes | feito | PDF e compra MOCK arquivados, não apagados; histórico preservado |
| Acervo local | feito | Seis DOCX importados como documentos brutos, hashes e origem; não promovidos automaticamente a fatos técnicos |
| Integração Drive | não feito | Referências e sincronização Drive pendentes; importação local não prova sincronização |
| QA visual | parcial | Desktop e viewport 390×844 inspecionados; auditoria completa de teclado, contraste, zoom 200% e leitores de tela pendente |
| Viewer engenharia | parcial | Upload R2, iframe PDF, acesso original, zoom e revisões verificados; pan de imagem/fullscreen e fidelidade visual PDF não integralmente auditados |
| Expansão M5 | não feito | Fase futura, fora da migração inicial |

Os três percursos de escrita foram exercitados na UI real em um shell local de QA ligado ao D1/R2 privado hospedado. O acesso autenticado direto ao site foi posteriormente confirmado no navegador; a versão final carregou Knowledge e Store, incluindo Research promovido e ownership corrigido. Isso não equivale a repetir todos os percursos de escrita no navegador direto.

Validação adicional: TypeScript e build Vinext passaram. O teste de integração SQLite executa as migrations e a API real: baseline, promoção, revisão/snapshot, compras, conflito otimista, transição inválida, bloqueio MOCK e preço inválido — PASS. Esse teste não substitui D1 nem navegador.

Origem: Origin 50C permanece NOT_OWNED / PLANNED; Ampero OWNED / ACTIVE conforme diretriz. Epiphone e Aria ficam OWNERSHIP TO VERIFY. Signature é projeto com placeholder, sem fotografia falsa Marshall. Não há medidas de bancada ou telemetria conectada; imagens de referência têm direitos a confirmar. Nenhuma automação recorrente foi criada.

## Falhas e reparos
Workerd local foi bloqueado pelo Windows Application Control: proteção preservada. Verificação visual usou shell Vite da UI real com persistência hospedada. Helpers oficiais de build/pacote precisaram de shims locais ignorados para npm/Git Bash no Windows. Credencial de publicação expirada foi renovada para o mesmo projeto. Confirmação nativa de arquivamento travou o navegador; removida para ação reversível com restauração. Dados MOCK foram arquivados via API privada.

## Limites e continuidade
Não alterar a audiência privada sem instrução. Documentos brutos precisam de revisão humana e fontes por parâmetro. Completar o mapeamento Drive, QA de acessibilidade e viewer antes de alegar cobertura integral da Master Specification. Gateway de observabilidade indisponível nesta sessão; somente evidência local e Sites. Nenhum resultado de observabilidade foi simulado.
