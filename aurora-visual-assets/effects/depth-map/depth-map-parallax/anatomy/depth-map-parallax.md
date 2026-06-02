# Anatomia Técnica — P001 — Depth Map Parallax

## 1. Definição do Ativo
- **ID:** `depth-map-parallax-001`
- **Categoria:** `effects/depth-map`
- **Padrão:** P001 (Profundidade Volumétrica Baseada em Mapa)
- **Tech Stack:** Three.js WebGPU (TSL)

## 2. Anatomia de Sincronização (Fase 2)
Este ativo foi projetado para operar em conjunto com o **P046 (Scroll Sync)**.

### O Pipeline de "Profundidade Impossível":
1. **DOM Sync (P046):** O `AbsoluteCanvas` mantém o container WebGL perfeitamente ancorado à seção da página, sem *drift*.
2. **Depth Displacement (P001):** O material desloca a textura conforme o scrollY ou a posição do mouse, usando o mapa de profundidade como guia de escala.
3. **Resultado:** A imagem parece possuir volume real que habita o espaço entre os elementos de texto do DOM.

## 3. Implementação TSL (Core)
A lógica fundamental reside no deslocamento de UVs:
```typescript
const depthNode = texture(depthMap, uv()).r;
const displacement = uMouse.mul(depthNode).mul(uIntensity);
const displacedUv = uv().add(displacement);
return texture(map, displacedUv);
```

## 4. Parâmetros Canônicos
- `uMouse`: `vec2` representando a posição normalizada do ponteiro (-1 a 1).
- `uIntensity`: `float` calibrando a força do efeito. Default Aurora: `0.05`.

## 5. Requisitos de Ativos
- **Map:** Textura RGB (4K recomendado para heróis).
- **DepthMap:** Textura Greyscale (Normalizada, onde Branco = Front e Preto = Back).
