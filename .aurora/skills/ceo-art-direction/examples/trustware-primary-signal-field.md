# Art Production Report — Trustware Primary Signal Field

## 1. Resumo executivo
Este asset representa o perímetro de segurança lógica e governança da Elysian. Utiliza um fundo escuro texturizado com alta densidade física (grão analógico) e elementos geométricos em cores primárias puras (vermelho, azul e amarelo) que indicam estados de bloqueio, passagem e validação de dados. A estética evita qualquer representação literal ou futurista de IA, focando no rigor de um diagrama mecânico forense.

## 2. Local de uso
- **Página:** Home / ElysianCorp Portal
- **Seção/Elemento:** Fundo da Câmara 02 (Governance / Method)

## 3. Função narrativa
Representar a rigidez do método `fail-closed` da Elysian. As formas e cores indicam os caminhos que os dados percorrem e onde são retidos ou aprovados sob regras determinísticas (perímetro selado).

## 4. Função cognitiva
Ajudar o usuário a processar o conceito de segurança através da materialidade. O contraste dramático e os limites físicos na imagem reduzem a carga cognitiva de entender o que é "contenção lógica", tornando o conceito quase palpável.

## 5. Descrição artística do asset
Uma superfície áspera de papel ou pedra preta fosca, coberta de grão fino e marcas de abrasão realistas. No centro, linhas finas e precisas desenham um diagrama retangular incompleto (o perímetro). Três sinais luminosos discretos mas de alta saturação física aparecem em interseções geométricas:
- Um sinal vermelho circular opaco que bloqueia uma linha diagonal.
- Um sinal azul cobalto retangular que valida o alinhamento de um bloco de dados.
- Um sinal amarelo ocre que representa o estado de transição ou simulação.

## 6. Composição
- **Disposição:** Assimétrica, pesando no terço central esquerdo, com linhas de fuga que se dissolvem no canto superior direito.
- **Ponto Focal:** O círculo vermelho de bloqueio (sinal primário de contenção).

## 7. Câmera / lente / enquadramento
- **Lente:** 50mm macro.
- **Enquadramento:** Forensic, visão superior com leve inclinação (perspectiva de 5 graus), profundidade de campo rasa que desfoca as extremidades do diagrama.

## 8. Luz
- **Estilo:** Chiaroscuro de alto contraste.
- **Direção:** Luz rasante lateral (esquerda para direita) para evidenciar a rugosidade física do fundo fosco.

## 9. Cor
- **Paleta:** Fundo carvão (#0C0C0D), cinza grafite, acentos em vermelho primário puro (#E63946), azul cobalto (#1D3557) e amarelo ocre (#F1FAEE / #E9C46A).
- **Cor Dominante:** Preto carvão.

## 10. Materiais e textura
- **Materiais:** Papel de algodão de alta gramatura, fibra mineral prensada, tinta acrílica espessa sobre a superfície.
- **Textura:** Rugosidade tátil, grão analógico denso, arranhões de agulha metálica.

## 11. Elementos obrigatórios
- Fundo carvão texturizado com grão analógico visível.
- Perímetro geométrico fino e translúcido.
- Três sinais luminosos físicos em cores primárias (vermelho, azul, amarelo).
- Linhas finas de medição e coordenadas de calibração que parecem entalhadas na matéria.

## 12. Elementos proibidos
- Robôs, androides ou representações humanas.
- Qualquer forma de cérebro brilhante ou rede neural brilhante.
- Hologramas flutuantes tridimensionais azuis.
- Texturas limpas ou gradientes digitais roxos/azuis.
- Texto renderizado na imagem ou logos corporativos artificiais.

## 13. Referências artísticas
- Fotografia forense industrial de meados do século XX.
- Diagramas de engenharia da Bauhaus.
- Trabalho de texturas físicas do Exo Ape (site de referência).

## 14. Prompt universal para geração
`Forensic macro photography of a physical textured matte dark charcoal paper surface, heavy organic paper grain, tiny scratches, a minimalistic technical diagram engraved into the surface, fine linear geometric lines, three distinct primary color marks: a thick cadmium red acrylic paint drop, a small ultramarine blue geometric line, and a cobalt yellow ochre spot. Chiaroscuro lighting, sharp side-light casting shadows, shallow depth of field, 50mm lens, high-contrast, tactile detail --ar 16:9`

## 15. Negative prompt
`3d, render, CGI, digital art, shiny, corporate, glossy, vector, flat, blue hologram, glowing neural network, cyber brain, generic neon, robot, cyborg, futuristic HUD, neon cyberpunk, plain black background, stock photo, simulated texture`

## 16. Variações solicitadas
- **Variação 1:** Foco macro apenas no sinal vermelho primário (Aspect Ratio 1:1 para mobile).
- **Variação 2:** Diagrama expandido com linhas amarelas ocupando mais espaço horizontal (Aspect Ratio 21:9).

## 17. Especificações técnicas
- **Aspect Ratio:** 16:9
- **Peso Alvo (KB):** Máximo 180kb (após compressão WebP/AVIF com WebGL/CSS filter overlay de noise).

## 18. Fallback
- **Tipo:** CSS + SVG Inline
- **Valor:** SVG com fundo `#0C0C0D` com SVG inline renderizando as linhas de perímetro em cinza opaco e os círculos de sinal primários com filtros CSS de blur.

## 19. Riscos de produção
- **Baixo Contraste:** O diagrama pode dificultar a leitura do texto flutuante. Solução: Aplicar um overlay CSS de gradiente preto suave no lado esquerdo onde o texto é posicionado.

## 20. Critérios de aceite
- [ ] O grão de fundo é perceptível mesmo em telas de baixa resolução.
- [ ] As cores primárias são saturadas e não parecem gradientes fluorescentes digitais.
- [ ] A profundidade de campo mantém o texto de handoff legível sem brigar com os elementos da cena.

## 21. Handoff para Design / Effects / Web
- **Design:** O `ceo-design` deve alinhar o layout da câmara de forma que a tipografia Didone fique perfeitamente legível na metade esquerda, livre do ponto focal do asset (que fica no terço direito).
- **Effects:** O `ceo-effects` deve aplicar um overlay CSS de ruído estático em loop (noise grain) sobre o elemento para dar a sensação de que o grão do papel se move sutilmente em repouso.
- **Web:** O `ceo-web` deve implementar o fallback SVG integrado diretamente no código do componente para garantir pontuação de performance no lighthouse mesmo em redes lentas.
