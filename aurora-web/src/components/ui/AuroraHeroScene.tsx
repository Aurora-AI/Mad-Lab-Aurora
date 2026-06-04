'use client';

import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import { Points, PointMaterial, Float, Text } from '@react-three/drei';
import * as THREE from 'three';

interface AuroraHeroSceneProps {
  progress: number; // 0 to 1
}

const GoldenScramble = ({ progress }: { progress: number }) => {
  const pointsRef = useRef<THREE.Points>(null);
  
  const particlesCount = 1200; // Densidade aumentada
  const positions = useMemo(() => {
    const pos = new Float32Array(particlesCount * 3);
    for (let i = 0; i < particlesCount; i++) {
        pos[i * 3] = (Math.random() - 0.5) * 25; 
        pos[i * 3 + 1] = (Math.random() - 0.5) * 25;
        pos[i * 3 + 2] = (Math.random() - 0.5) * 15;
    }
    return pos;
  }, [particlesCount]);

  useFrame((state) => {
    if (!pointsRef.current) return;
    const time = state.clock.getElapsedTime();
    pointsRef.current.rotation.z = time * 0.03;
    
    const material = pointsRef.current.material as THREE.PointsMaterial;
    // Fade out suave baseado no progresso
    material.opacity = Math.max(0, 0.6 - progress * 0.8); 
  });

  return (
    <Points ref={pointsRef} positions={positions} stride={3} frustumCulled={false}>
      <PointMaterial
        transparent
        color="#C5A059" // Aureate Weight
        size={0.08}
        sizeAttenuation={true}
        depthWrite={false}
        blending={THREE.AdditiveBlending}
      />
    </Points>
  );
};

const PuzzlePiece = ({ index, progress }: { index: number; progress: number }) => {
  const meshRef = useRef<THREE.Mesh>(null);
  
  const initialPos = useMemo(() => [
    (Math.random() - 0.5) * 15,
    (Math.random() - 0.5) * 15,
    (Math.random() - 0.5) * 8
  ], []);

  const finalPos = [
    (index % 3) * 1.6 - 1.6,
    Math.floor(index / 3) * 1.6 - 1.6,
    0
  ];

  useFrame(() => {
    if (!meshRef.current) return;
    
    // Curva de Gravidade Real: Ease-out pronunciado (Hermite ou Power 3)
    const gravityProgress = Math.min(1, Math.pow(progress, 2.5));

    meshRef.current.position.x = THREE.MathUtils.lerp(initialPos[0], finalPos[0], gravityProgress);
    meshRef.current.position.y = THREE.MathUtils.lerp(initialPos[1], finalPos[1], gravityProgress);
    meshRef.current.position.z = THREE.MathUtils.lerp(initialPos[2], finalPos[2], gravityProgress);
    
    meshRef.current.rotation.x = THREE.MathUtils.lerp(index * 2, 0, gravityProgress);
    meshRef.current.rotation.y = THREE.MathUtils.lerp(index, 0, gravityProgress);
    
    const mat = meshRef.current.material as THREE.MeshStandardMaterial;
    // Brilho remanescente da "herança"
    mat.emissiveIntensity = Math.max(0, (1 - gravityProgress) * 0.1);
  });

  return (
    <mesh ref={meshRef}>
      <boxGeometry args={[1.5, 1.5, 0.05]} />
      <meshStandardMaterial
        color="#F4F1EA" // Parchment Memory
        metalness={0.2}
        roughness={0.8} // Mais material, menos plástico
        emissive="#C5A059"
        emissiveIntensity={0.1}
      />
    </mesh>
  );
};

export const AuroraHeroScene: React.FC<AuroraHeroSceneProps> = ({ progress }) => {
  const pieces = Array.from({ length: 9 });

  return (
    <>
      <ambientLight intensity={0.4} />
      <pointLight position={[10, 10, 10]} intensity={1.5} color="#F4F1EA" />
      <pointLight position={[-10, -10, 10]} intensity={0.8} color="#C5A059" />
      <spotLight position={[0, 0, 15]} intensity={2} angle={0.3} penumbra={1} castShadow />

      <GoldenScramble progress={progress} />
      
      <group position={[0, 0, -1]}>
        {pieces.map((_, i) => (
          <PuzzlePiece key={i} index={i} progress={progress} />
        ))}
      </group>

      <Float speed={1.5} rotationIntensity={0.05} floatIntensity={0.1}>
        <Text
          anchorX="center"
          anchorY="middle"
          fontSize={1.4}
          color="#F4F1EA"
          position={[0, 0, 1]}
          fillOpacity={Math.max(0, (progress - 0.75) * 4)}
          material-toneMapped={false}
          letterSpacing={0.4}
          font="/fonts/EditorialNew-Italic.woff" // Placeholder for Voz Monumental
        >
          AURORA
        </Text>
      </Float>
    </>
  );
};
