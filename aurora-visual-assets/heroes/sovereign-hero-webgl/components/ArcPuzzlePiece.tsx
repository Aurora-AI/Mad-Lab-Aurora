import React, { useMemo, useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { useGLTF } from '@react-three/drei';
import * as THREE from 'three';
import gsap from 'gsap';

// Vertex Shader: Implementação do Pivot-based Displacement
const vertexShader = `
  attribute vec3 aCentroid;
  attribute float aRandomFactor;
  
  uniform float uProgress;
  uniform float uTime;

  varying vec2 vUv;
  varying vec3 vNormal;
  varying vec3 vCentroid;

  // Função auxiliar para rotação via quaternions/eixos
  mat4 rotationMatrix(vec3 axis, float angle) {
    axis = normalize(axis);
    float s = sin(angle);
    float c = cos(angle);
    float oc = 1.0 - c;
    return mat4(oc * axis.x * axis.x + c,           oc * axis.x * axis.y - axis.z * s,  oc * axis.z * axis.x + axis.y * s,  0.0,
                oc * axis.x * axis.y + axis.z * s,  oc * axis.y * axis.y + c,           oc * axis.y * axis.z - axis.x * s,  0.0,
                oc * axis.z * axis.x - axis.y * s,  oc * axis.y * axis.z + axis.x * s,  oc * axis.z * axis.z + c,           0.0,
                0.0,                                0.0,                                0.0,                                1.0);
  }

  void main() {
    vUv = uv;
    vNormal = normal;
    vCentroid = aCentroid;

    // 1. Centralizar o fragmento no próprio pivô (aCentroid)
    vec3 localPos = position - aCentroid;

    // 2. Calcular Rotação Individual (Inércia)
    float angle = uProgress * 6.28 * (1.0 + aRandomFactor);
    vec3 rotationAxis = normalize(vec3(aRandomFactor, 1.0 - aRandomFactor, aRandomFactor * 0.5));
    vec4 rotatedPos = rotationMatrix(rotationAxis, angle) * vec4(localPos, 1.0);

    // 3. Deslocamento (Explosão + Gravidade + Drift)
    // uProgress = 0 (peça montada), uProgress = 1 (peça explodida)
    
    // Y-Bias: Efeito de Peso/Gravidade
    float weight = uProgress * 1.5 * (1.0 + aRandomFactor * 0.5);
    
    // Drift Atmosférico: Micro-oscilação quando parado
    // Usamos aCentroid como semente para que cada peça respire em um tempo diferente
    vec3 drift = vec3(
      sin(uTime * 0.5 + aCentroid.x) * 0.05,
      cos(uTime * 0.3 + aCentroid.y) * 0.05,
      sin(uTime * 0.7 + aCentroid.z) * 0.05
    ) * uProgress;

    vec3 displacement = (aCentroid * (1.0 + uProgress * 2.5 * aRandomFactor)) + drift;
    displacement.y -= weight; // Aplicação da Gravidade

    // 4. Posição Final
    vec3 finalPos = rotatedPos.xyz + displacement;

    gl_Position = projectionMatrix * modelViewMatrix * vec4(finalPos, 1.0);
  }
`;

// Fragment Shader: Ouro Incandescente e Arcos Elétricos HDR com Flicker Coerente
const fragmentShader = `
  varying vec2 vUv;
  varying vec3 vNormal;
  varying vec3 vCentroid;
  
  uniform float uProgress;
  uniform float uTime;
  uniform vec3 uMouse3D;

  // Simplex Noise 1D/2D Otimizado para GPU
  vec3 permute(vec3 x) { return mod(((x*34.0)+1.0)*x, 289.0); }
  float snoise(vec2 v){
    const vec4 C = vec4(0.211324865405187, 0.366025403784439, -0.577350269189626, 0.024390243902439);
    vec2 i  = floor(v + dot(v, C.yy) );
    vec2 x0 = v -   i + dot(i, C.xx);
    vec2 i1;
    i1 = (x0.x > x0.y) ? vec2(1.0, 0.0) : vec2(0.0, 1.0);
    vec4 x12 = x0.xyxy + C.xxzz;
    x12.xy -= i1;
    i = mod(i, 289.0);
    vec3 p = permute( permute( i.y + vec3(0.0, i1.y, 1.0 )) + i.x + vec3(0.0, i1.x, 1.0 ));
    vec3 m = max(0.5 - vec3(dot(x0,x0), dot(x12.xy,x12.xy), dot(x12.zw,x12.zw)), 0.0);
    m = m*m ;
    m = m*m ;
    vec3 x = 2.0 * fract(p * C.www) - 1.0;
    vec3 h = abs(x) - 0.5;
    vec3 ox = floor(x + 0.5);
    vec3 a0 = x - ox;
    m *= 1.79284291400159 - 0.85373472095314 * ( a0*a0 + h*h );
    vec3 g;
    g.x  = a0.x  * x0.x  + h.x  * x0.y;
    g.yz = a0.yz * x12.xz + h.yz * x12.yw;
    return 130.0 * dot(m, g);
  }

  void main() {
    // 1. Base Metal Escupido (Iluminação Lambertiana Simples)
    vec3 lightDir = normalize(vec3(5.0, 5.0, 5.0));
    float diff = max(dot(vNormal, lightDir), 0.0);
    vec3 baseColor = vec3(0.01) + vec3(0.02) * diff; 
    
    // 2. Flicker Coerente (Simplex)
    float noiseVal = snoise(vec2(uTime * 1.8, 0.0));
    float flicker = smoothstep(0.75, 0.98, noiseVal);
    
    // 3. Trilhas de Circuito (Emissivas)
    vec2 grid = fract(vUv * 20.0);
    float line = smoothstep(0.015, 0.0, abs(grid.x - 0.5) * abs(grid.y - 0.5));
    
    // 3. Arcos Elétricos Reativos (Whip Design)
    float distToMouse = length(uMouse3D - vCentroid);
    float arcIntensity = 0.0;
    
    // Raio de ativação da tensão cognitiva
    if(distToMouse < 2.0) {
      // Cálculo do arco tipo "Chicote": oscilação aumenta com T (distância)
      float t = clamp(distToMouse / 2.0, 0.0, 1.0);
      float whip = snoise(vec2(uTime * 10.0, t * 5.0)) * t * t * 0.4;
      
      float arcLine = smoothstep(0.08, 0.0, abs(vUv.x - 0.5 + whip)); 
      arcIntensity = arcLine * flicker * (2.0 - t);
    }

    // 4. Mapeamento Térmico HDR
    float thermalInput = (line * uProgress + arcIntensity) * 15.0 * flicker;
    vec3 glow = vec3(1.0, 0.25, 0.0) * thermalInput * 0.2 + // Orange
                vec3(1.0, 0.65, 0.05) * thermalInput * 0.5 + // Gold
                vec3(1.0, 1.0, 1.0) * thermalInput * 1.5;   // Surgical White
    
    gl_FragColor = vec4(baseColor + glow, 1.0);
  }
`;

interface ArcPuzzlePieceProps {
  url: string;
  progress: number; // 0 a 1
}

const ArcPuzzlePiece: React.FC<ArcPuzzlePieceProps> = ({ url, progress }) => {
  const meshRef = useRef<THREE.Mesh>(null!);
  
  // No mundo real, usaríamos C:\Aurora\MadLabAurora\aurora-web\public\assets\models\puzzle.glb
  // Mas para o build, carregamos o recurso passado.
  const { nodes } = useGLTF(url);
  
  // Preparação da Geometria Unificada
  const unifiedGeometry = useMemo(() => {
    // Aqui assumimos que o GLB já vem pré-processado com os atributos aCentroid
    // Caso contrário, implementaríamos a lógica de cálculo estático aqui.
    if (nodes.Scene) {
      // Lógica de busca e merge se necessário
      return (nodes.PuzzleMesh as THREE.Mesh).geometry;
    }
    return new THREE.BufferGeometry();
  }, [nodes]);

  const uniforms = useMemo(() => ({
    uProgress: { value: progress },
    uTime: { value: 0 },
    uMouse3D: { value: new THREE.Vector3() }
  }), []);

  useFrame((state) => {
    uniforms.uTime.value = state.clock.getElapsedTime();
    
    // Raycasting Simples para Projetar Mouse 2D -> 3D
    const { raycaster, mouse, camera } = state;
    raycaster.setFromCamera(mouse, camera);
    
    // Projetamos o mouse para um plano imaginário na frente das peças
    const targetPos = new THREE.Vector3();
    raycaster.ray.at(3.5, targetPos); 
    uniforms.uMouse3D.value.copy(targetPos);

    // Suavização GSAP para o uniform
    gsap.to(uniforms.uProgress, {
      value: progress,
      duration: 0.8,
      ease: "power2.out",
      overwrite: true
    });
  });

  return (
    <mesh ref={meshRef} geometry={unifiedGeometry}>
      <shaderMaterial
        vertexShader={vertexShader}
        fragmentShader={fragmentShader}
        uniforms={uniforms}
        transparent
      />
    </mesh>
  );
};

export default ArcPuzzlePiece;
