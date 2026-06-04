# ANATOMY: Particle Text Effect
`ID: interactions-particle-text-001`

## 1. RESUMO EXECUTIVO
O **Particle Text Effect** é uma experiência interativa de alta fidelidade que transmuta texto estático em um sistema dinâmico de milhares de partículas físicas. O componente utiliza amostragem de pixels de um canvas off-screen para mapear a tipografia e aplica vetores de força (steering behavior) para orquestrar o movimento fluido entre palavras.

## 2. ESPECIFICAÇÕES TÉCNICAS
- **Core**: Vanilla Canvas 2D + Physics Engine customizada.
- **Pixel Sampling**: Uso de `getImageData` em um canvas auxiliar para extrair coordenadas de texto branco sobre fundo preto.
- **Steering Behaviors**: 
  - `Arrive`: Partículas desaceleram ao chegar no alvo (`proximityMult`).
  - `Steer`: Aplicação de força limitada (`maxForce`) para evitar jitter e garantir fluidez.
- **Color Transition**: Interpolação ponderada (`colorWeight`) entre cores de origem e destino durante a transição de palavras.
- **Interação**: 
  - `Right-Click Destruction`: Partículas dentro de um raio de 50px do mouse são marcadas como `killed` e repelidas para fora do canvas.

## 3. PADRÕES IDENTIFICADOS
- **P020: Text-to-Canvas Pixel Mapping**: Técnica de renderizar texto em buffer invisível para gerar destinos de partículas baseados em densidade de pixels.
- **P021: Physics-Based Particle Steering**: Uso de conceitos de Craig Reynolds (Velocity, Acceleration, Steering) para criar movimentos que parecem ter massa e inércia.

## 4. VEREDITO CEO-EFFECTS
> [!IMPORTANT]
> **STATUS: APROVADO**
> 
> A destruição física do texto via mouse é o ponto alto. Transforma o conteúdo em algo tangível. Para Aurora, este efeito deve ser usado com tipografia pesada (Serif Display ou Sans Bold) para maximizar o impacto visual das partículas.

---

## 5. VEREDITO CEO-DESIGN
> [!IMPORTANT]
> **STATUS: APROVADO (NATIVE)**
> 
> Este componente valida o poder da amostragem estocástica. Ao embaralhar os índices de coordenadas (`coordsIndexes`), evitamos que o texto "nasça" de forma linear, criando uma sensação de formação de nuvem. Perfeito para transições de mensagens fundamentais da marca.

## 6. INSTRUÇÕES DE INSTALAÇÃO
1. Copiar `index.tsx` para `components/ui/particle-text.tsx`.
2. O componente é autocontido e não possui dependências externas além do React.
3. Personalize `words` prop para injetar as mensagens da Aurora.
