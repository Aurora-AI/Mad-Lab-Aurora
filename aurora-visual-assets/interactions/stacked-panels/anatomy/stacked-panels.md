# ANATOMY: Stacked Interactive Panels
`ID: interactions-stacked-panels-001`

## 1. RESUMO EXECUTIVO
O **Stacked Interactive Panels** é um componente de exploração visual que utiliza profundidade 3D real e física de molas (`useSpring`) para reagir ao cursor. O diferencial técnico é o uso de uma função de influência Gaussiana para criar uma "onda" de escala e deslocamento que segue o mouse de forma orgânica e amortecida.

## 2. ESPECIFICAÇÕES TÉCNICAS
- **Core**: Next.js + Framer Motion.
- **Interação**: Mouse Move + Gaussian Influence Math (`Math.exp`).
- **3D Engine**: CSS `preserve-3d` + `perspective` + `translateZ`.
- **Efeitos Visuais**: `mix-blend-mode: multiply` para coloração dinâmica + noise background overlay.

## 3. PADRÕES IDENTIFICADOS
- **P012: Gaussian Proximity Wave**: Uso de funções exponenciais negativas para decaimento suave de influência baseado em distância espectral ou física.
- **P013: 3D Depth Stacking**: Técnica de posicionamento em camadas no eixo Z com perspectiva global para criar volume sem bibliotecas WebGL.

## 4. VEREDITO CEO-EFFECTS
> [!IMPORTANT]
> **STATUS: APROVADO**
> 
> A resposta tátil do componente é de altíssimo nível. A transição entre os gradientes e as imagens do Unsplash via `multiply` é uma lição de como unificar assets heterogêneos sob uma mesma direção de arte.

---

## 5. VEREDITO CEO-DESIGN
> [!IMPORTANT]
> **STATUS: APROVADO (NATIVE)**
> 
> A arquitetura de molas independentes para cada painel garante que a interação nunca pareça "travada". Alinhamento perfeito com o pilar de "Sistemas Vivos" da Aurora. O uso de `transformOrigin: bottom center` nas escalas adiciona um peso gravitacional correto à onda.

## 6. INSTRUÇÕES DE INSTALAÇÃO
1. Copiar `index.tsx` para `components/ui/stacked-panels.tsx`.
2. Certificar-se que `framer-motion` está instalado.
3. O container pai deve ter uma altura definida (ex: `h-[600px]`) e `perspective` configurada via inline style ou Tailwind.
