# ANATOMY: Entropy (Order vs Chaos)
`ID: backgrounds-entropy-001`

## 1. RESUMO EXECUTIVO
O **Entropy** é um simulador visual de partículas baseado em Canvas que explora a dualidade entre ordem e caos. Metade do sistema opera em um grid estruturado (Ordem), enquanto a outra metade se move de forma estocástica (Caos). Quando partículas de caos se aproximam da zona de ordem, elas exercem influência física, desestruturando temporariamente o grid.

## 2. ESPECIFICAÇÕES TÉCNICAS
- **Core**: Canvas 2D API para alta performance.
- **DPR Scaling**: Suporte nativo para telas Retina/High-DPI.
- **Física de Partículas**:
  - `Order Particles`: Possuem "home coordinates" (`originalX/Y`) e tentam retornar a elas via interpolação linear (`0.05`).
  - `Chaos Particles`: Movimento browniano com limites de colisão no eixo central e bordas.
  - `Influence`: Cálculo de força baseado em proximidade (`Math.hypot`).
- **Networking**: Desenho de linhas de conexão entre vizinhos em um raio de 50px.

## 3. PADRÕES IDENTIFICADOS
- **P016: Entropy Particle Physics**: Lógica de comportamento dual onde um estado (caos) "infecta" e modifica o estado vizinho (ordem) via transferência de momentum/influência.
- **P017: Canvas Proximity Networking**: Algoritmo de busca de vizinhos otimizado (rodando a cada 30 frames) para renderizar redes neurais ou estruturas de dados vivas.

## 4. VEREDITO CEO-EFFECTS
> [!IMPORTANT]
> **STATUS: APROVADO**
> 
> A tensão visual no "desgaste" da ordem pela entropia é uma mimese perfeita de processos naturais e digitais. O uso de `alpha` dinâmico baseado na influência preserva a estética Dark Editorial sem excesso de brilho.

---

## 5. VEREDITO CEO-DESIGN
> [!IMPORTANT]
> **STATUS: APROVADO (NATIVE)**
> 
> Altamente resiliente e modular. A decisão de usar Canvas em vez de SVG para >600 partículas garante 60fps constantes mesmo em dispositivos mobile. O alinhamento matemático (grid 25x25) permite que o componente seja usado como placeholder de "loading inteligente" ou fundo de dashboards.

## 6. INSTRUÇÕES DE INSTALAÇÃO
1. Copiar `index.tsx` para `components/ui/entropy.tsx`.
2. O componente aceita `size` (padrão 400px) e `className`.
3. Ideal para fundos de seções de "Tecnologia", "Análise" ou "Governança".
