# Generative Cinematic Grammar

Este documento não é um repositório de prompts, mas o **motor sintático** que ensina os agentes do Mad Lab Aurora a gerar outputs visuais e cinéticos inéditos. Ele contém as regras de combinação das primitivas.

---

## 1. O Peso Visual (Visual Weight Formula)

A geração de uma cena não começa pelos elementos, mas pelo "peso" emocional desejado. Toda cena tem um `Weight Score` de 1 a 10.

*   **Weight 1-3 (Respiro, Transição, Interface Leve):**
    *   **Composição:** Espaços vazios maciços (COM-001).
    *   **Motion:** Fade-in estático simples.
    *   **Iluminação:** Clara/Off-white (LGT-003). Nenhum chiaroscuro.
    *   *Regra de Combinação:* Nunca use `Scroll-Driven Glitch` (MOT-005) ou `Orbital Drift` (MOT-001) aqui.

*   **Weight 4-7 (Tensão, Prova, Argumento Central):**
    *   **Composição:** Split Assimétrico (COM-002) ou Grid de Diagnóstico (COM-003).
    *   **Motion:** Magnetic Cursor (INT-001) + Parallax de Scroll Leve (CAM-003).
    *   **Iluminação:** Chiaroscuro sutil (LGT-001) + Grão analógico leve (ATM-001).
    *   *Regra de Combinação:* Interação restrita a componentes de conversão.

*   **Weight 8-10 (Hero, Clímax, Revelação Dramática):**
    *   **Composição:** Tipografia Oversized (COM-005) sobrepondo vídeo ou render WebGL.
    *   **Motion:** Staggered Fade-Rise (TRN-001) cruzado com Scroll-Driven Glitch (MOT-005).
    *   **Iluminação:** Fundo `#0C0C0C` (LGT-001) + Cursor Spotlight (INT-002) + Liquid Glass (ATM-002).
    *   *Regra de Combinação:* A página inteira reage (Scroll, Mouse, Inércia). Silêncio de 0.5s antes de iniciar a entrada.

---

## 2. Padrões de Intertravamento (Interlocking Patterns)

Como um idioma real, as técnicas devem intertravar-se:

*   **A Regra da Refração (Liquid Glass + Parallax):**
    Sempre que usar `Liquid Glass` (ATM-002), é *obrigatório* usar `Scroll Parallax` (CAM-003) no conteúdo atrás do vidro, e o fundo atrás do vidro deve deslocar a uma velocidade *diferente* do vidro em si. (Isso gera refração percebida).

*   **A Regra do Oposto Complementar (Tipografia + Movimento):**
    Se a tipografia for gigante e ocupar >60% da tela (`clamp()` absurdo), o movimento de entrada deve ser lento, contínuo e sem bounce. Se a tipografia for Voz 2 (técnica/pequena), o movimento pode ser mecânico, duro e estocástico (Glitch).

*   **O Eixo Frio/Quente (Atmosfera + Interação):**
    Se o fundo for Frio (Navy/Preto profundo), o `Cursor Spotlight` (INT-002) ou glow de interação deve ser um tom quente sutil (ex: laranja ambarino ou rosa coral `mix-blend-mode: color-dodge`).

---

## 3. Anti-Padrões Proibidos (Genéricos)

Seja gerando do zero ou fazendo engenharia reversa, evite:
1.  **Botões Genéricos Sem Magnetismo:** CTAs devem ser `Liquid Glass` ou possuir tracking magnético (`INT-001`).
2.  **Entrada Instantânea:** Absolutamente nada carrega instantaneamente no primeiro frame. A regra de ouro é: **Atraso base + Stagger (Delay: 0.2s * index)**.
3.  **Fundo Estéril:** Evite `#000000` puro sem grão (`ATM-001`) ou distorção radial/overlay.
4.  **Cards Comuns:** Sem bordas sólidas pesadas. Cards devem ser de vidro, recuados ou delimitados apenas por tipografia.

---

## 4. Prompting Generativo (O "Spec")

Para gerar uma cena 100% autoral baseada na gramática:

1.  *Defina o Weight:* Ex: 9 (Clímax de Hero).
2.  *Combine os Eixos:* Typo Oversized + Fundo Dark Navy + Liquid Glass Overlay.
3.  *Adicione Tensão:* Inserir Scroll-Driven Parallax + Stagger Entrance.
4.  *Gere o código ou spec estruturado usando React + Tailwind + Framer Motion.*
