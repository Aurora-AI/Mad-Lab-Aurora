# Anti-Padrão: O Monólito Sci-Fi e o Laser de Cybersecurity (Filtro Negativo)

**Documento:** Diretriz de Rejeição Visual  
**Referencial:** Veto de Abstracionismo Genérico de IA  
**Classificação:** Anti-Padrão Cênico  
**Status:** BLOQUEADO (DNA Conflict)  

---

## 1. Identidade do Problema
Ao tentar materializar conceitos abstratos de segurança, confidencialidade ou perímetros invioláveis (como o "Fail-Closed Trust Boundary"), a inteligência generativa tende a recorrer ao clichê do **"Monólito de Ficção Científica"**. Este padrão consiste em blocos de metal ou pedra massiva flutuando ou assentados em ambientes escuros, cortados ao meio por frestas mecânicas perfeitas por onde escapa um feixe de luz laser (dourado, azul ou verde) sob uma atmosfera de fumaça volumétrica densa e chiaroscuro artificial extremo.

Este padrão cria uma estética de "concept art de videogame de ficção científica" ou "relicário misterioso", que é imediatamente identificável como renderização genérica de IA (Midjourney/DALL-E), colidindo com o tom forense-editorial e utilitário da ElysianCorp.

---

## 2. Heurísticas de Rejeição (Filtro do CEO-Design)

### A. O Teste do Concept Art
- **Pergunta:** Esta imagem se parece com o plano de fundo de um jogo espacial de ficção científica ou com a capa de um livro de mistério tecnológico?
- **Critério:** Se o asset se assemelha a uma pintura de reator de energia futurista ou monólito alienígena, ele deve ser **REJEITADO**.

### B. O Princípio da Redução de Pirotecnia Luminosa
- **Pergunta:** O perímetro de segurança é definido por luzes/lasers ou pela estrutura física e diagramação?
- **Critério:** O uso de raios lasers, feixes lineares de alta intensidade ou fontes de luz concentrada simulando "portais" ou "chaves de dados" virtuais é considerado artificial. **VETO**.

---

## 3. Especificação de Veto para o Agente

O CEO-Design deve reconhecer as seguintes composições e aplicar o veto imediato:
- **Feixes de Laser Lineares:** Luzes pontuais ou traçados vetoriais de luz cruzando frestas físicas para simular dados ou barreiras.
- **Monólitos Flutuantes em Névoa:** Estruturas geométricas suspensas ou envoltas em fumaça volumétrica dramática (efeito "relicário").
- **Glow Artificial nas Bordas:** Brilho digital exagerado nos limites dos blocos metálicos para forçar o contraste chiaroscuro.

---

## 4. Nó de Ingestão (JSON)

```json
{
  "agent": "ceo-design",
  "node_type": "AntiTendencia",
  "domain": "design_art_direction",
  "core_insight": "A representação de perímetros de segurança via monólitos metálicos escuros e feixes de laser que atravessam fendas em fumaça volumétrica é um clichê de geração de IA que desvia do tom editorial forense, assemelhando-se a concept art de ficção científica.",
  "dark_editorial_alignment": "conflita",
  "action": {
    "what": "Vetar representação de segurança de dados através de blocos monolíticos e feixes laser brilhantes.",
    "deadline_days": 0,
    "owner": "rodrigo"
  },
  "tags": ["anti-ai", "veto-sci-fi", "anti-pattern-monolith", "design-generico"]
}
```
