# QA-ART-DIRECTION-GATE

## Descrição do Gate
Este gate valida se a direção artística e a produção técnica de assets visuais cumprem os critérios de anti-genericidade e as restrições estéticas da marca, garantindo que o resultado final seja executável e não possua aparência de IA/SaaS clichê.

---

## Checklist de Validação
- [ ] O asset parece pertencer a um mundo visual próprio, e não a um template genérico.
- [ ] O asset possui uma função narrativa explícita vinculada à seção de destino.
- [ ] A função cognitiva está claramente declarada e justifica o asset.
- [ ] O prompt de geração principal está em inglês e é detalhado/específico.
- [ ] Existe um `negative prompt` robusto em inglês que explicitamente bloqueia estilos genéricos de render.
- [ ] Existem elementos obrigatórios claros listados para a geração.
- [ ] Existem elementos proibidos explícitos.
- [ ] Há referências estéticas/artísticas válidas sem instruir cópia literal.
- [ ] As especificações técnicas (aspect ratio, formato e peso) estão declaradas.
- [ ] O fallback (SVG, CSS ou Canvas) está definido e é funcional.
- [ ] A seção de handoff cobre instruções para `ceo-design`, `ceo-effects` e `ceo-web`.

---

## Sinais Bloqueantes (Anti-AI & Anti-Generic)
Se qualquer um dos itens abaixo for detectado, o asset deve ser **REPROVADO AUTOMATICAMENTE**:
- [ ] Presença de robô humanoide genérico ou figuras stock corporativas.
- [ ] Presença de cérebro digital brilhante, rede de sinapses genérica ou ícones Lucide crus.
- [ ] Fundo preto absoluto chapado sem ruído, matéria ou textura.
- [ ] Uso de neon cyberpunk ou hologramas azuis genéricos de ficção científica.
- [ ] Layout ou prompt que poderia servir para qualquer SaaS de tecnologia convencional.

---

## Rubrica de Pontuação
- **5.0 — Excelente:** Direção artística única, totalmente integrada à narrativa, com prompt em inglês extremamente descritivo, negative prompt completo, fallback robusto e handoff claro para todos os CEOs.
- **4.0 — Bom (Threshold Mínimo):** Direção utilizável com pequenas lacunas documentais não bloqueantes (ex: handoff pouco detalhado em um dos CEOs, mas com prompt e fallback válidos).
- **3.0 — Regular:** Direção parcialmente útil, mas ainda contendo descrições ligeiramente genéricas ou falta de especificação em luz/câmera.
- **2.0 — Insuficiente:** Asset meramente decorativo, sem função cognitiva clara ou com prompt fraco.
- **1.0 — Ruim:** Prompt genérico que evoca estética de IA tradicional (ex: "glowing brain background").
- **0.0 — Inaceitável:** Violação direta das proibições estéticas e estruturais (presença de robôs, cérebros brilhantes, etc.).

---

## Processo de Reprovação
Se o score for inferior a **4.0**, a direção artística deve ser devolvida ao emissor com o log detalhado das violações encontradas.
