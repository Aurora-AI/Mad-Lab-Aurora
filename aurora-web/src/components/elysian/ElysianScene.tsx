import React, { useRef, useMemo, useState } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { Text, PerspectiveCamera, Center } from '@react-three/drei';
import * as THREE from 'three';

const CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+[]{}<>/\\|';
const KEYWORDS = ['ELYSIAN', 'TRUSTWARE'];

// Componente para uma instancia individual de dado (para prototipagem rápida, depois converter para InstancedMesh se peso for alto)
// No entanto, para "estabilizar" em palavras com kerning Vogue, usaremos textos individuais para os grupos de palavras
// e uma massa de instâncias para o ruído de fundo.

const FloatingDataField = ({ count = 1000 }) => {
  const meshRef = useRef<THREE.InstancedMesh>(null);
  const { mouse, viewport } = useThree();
  
  const particles = useMemo(() => {
    const temp = [];
    for (let i = 0; i < count; i++) {
      const x = (Math.random() - 0.5) * 15;
      const y = (Math.random() - 0.5) * 10;
      const z = (Math.random() - 0.5) * 20 - 5;
      temp.push({ x, y, z, speed: 0.05 + Math.random() * 0.1 });
    }
    return temp;
  }, [count]);

  const dummy = useMemo(() => new THREE.Object3D(), []);

  useFrame((state) => {
    if (!meshRef.current) return;
    
    particles.forEach((p, i) => {
      // Movimento sutil de suspensão
      const time = state.clock.getElapsedTime();
      const parallaxX = mouse.x * 0.5;
      const parallaxY = mouse.y * 0.5;
      
      dummy.position.set(
        p.x + Math.sin(time * p.speed + i) * 0.1 + parallaxX * (p.z * 0.05),
        p.y + Math.cos(time * p.speed + i) * 0.1 + parallaxY * (p.z * 0.05),
        p.z
      );
      
      dummy.rotation.set(0, 0, time * 0.1);
      dummy.updateMatrix();
      meshRef.current!.setMatrixAt(i, dummy.matrix);
    });
    
    meshRef.current.instanceMatrix.needsUpdate = true;
  });

  if (!particles.length) return null;

  return (
    <instancedMesh ref={meshRef} args={[undefined, undefined, count]}>
      <planeGeometry args={[0.05, 0.05]} />
      <meshBasicMaterial color="#1A1A1A" transparent opacity={0.12} />
    </instancedMesh>
  );
};

const WordAnchor = ({ text, position, active = false }: { text: string, position: [number, number, number], active?: boolean }) => {
  const textRef = useRef<any>(null);
  const [scrambledText, setScrambledText] = useState(text);

  useFrame((state) => {
    if (!active) {
      // Efeito scramble quando não está ativo/estabilizado
      if (state.clock.elapsedTime % 0.1 < 0.02) {
        const next = text.split('').map(() => CHARS[Math.floor(Math.random() * CHARS.length)]).join('');
        setScrambledText(next);
      }
    } else {
      setScrambledText(text);
    }
    
    if (textRef.current) {
      // Flutuação sutil
      textRef.current.position.y = position[1] + Math.sin(state.clock.elapsedTime * 0.5) * 0.05;
    }
  });

  return (
    <Text
      ref={textRef}
      position={position}
      fontSize={0.5}
      color="#1A1A1A"
      letterSpacing={-0.05}
      maxWidth={10}
      textAlign="center"
    >
      {scrambledText}
    </Text>
  );
};

export const ElysianScene: React.FC<{ scrollProgress: number }> = ({ scrollProgress }) => {
  return (
    <div className="absolute inset-0 w-full h-full pointer-events-none">
      <Canvas gl={{ alpha: true }} dpr={[1, 2]}>
        <PerspectiveCamera makeDefault position={[0, 0, 8]} fov={35} />
        <ambientLight intensity={1} />
        
        <FloatingDataField count={1500} />
        
        <Center position={[0, 0, 0]}>
          <WordAnchor 
            text="ELYSIAN" 
            position={[0, 1.2, -2]} 
            active={scrollProgress > 0.2} 
          />
          <WordAnchor 
            text="TRUSTWARE" 
            position={[0, -1.2, -5]} 
            active={scrollProgress > 0.5} 
          />
        </Center>

        <fog attach="fog" args={['#FCF9F2', 4, 18]} />
      </Canvas>
    </div>
  );
};
