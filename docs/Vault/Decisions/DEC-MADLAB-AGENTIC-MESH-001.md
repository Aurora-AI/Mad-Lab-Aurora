# DEC-MADLAB-AGENTIC-MESH-001
**Título:** Mad Lab Aurora como consumidor governado da malha agentiva Aurora/Ozzmosis  
**Status:** Aprovado  
**Data:** 27 de Maio de 2026  

---

## Decisão

O **Mad Lab Aurora** consumirá as capacidades da fábrica **Ozzmosis** — especificamente Observabilidade Agentiva (read-only), Toolbelt Registry, Reflexion, Bibliotecário/Vault, QA e análise topológica quando disponível — atuando como uma vertical criativa governada. 

O Mad Lab está estritamente proibido de:
* Recriar ou instanciar cópias do runtime do Álvaro localmente;
* Criar um Gateway MCP de observabilidade ou escrita próprio;
* Instanciar uma base Qdrant ou Vault global paralela sem Ordem de Serviço formal;
* Executar auto-repair ou self-healing autônomo diretamente em produção.

O domínio do Mad Lab terá seus próprios gates locais e específicos para qualidade estética, performance de renderização, consistência de hidratação e estabilidade de animação, gravando evidências e submetendo candidatos a KIs de forma supervisionada.

---

## Critério de Sucesso

Um subprojeto do Mad Lab (ex: `ElysianCorp`) deve ser capaz de:
1. Executar preflights visuais locais;
2. Consultar capacidades disponíveis na fábrica via Toolbelt Registry;
3. Emitir e registrar o evento `FACTORY_TOOL_UNAVAILABLE` quando um serviço esperado estiver indisponível;
4. Registrar evidências locais no Vault do Mad Lab;
5. Propor KIs ou anti-padrões candidatos sem poluir de forma automática a memória global da fábrica.
