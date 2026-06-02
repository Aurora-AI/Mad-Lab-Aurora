import { useRef, useLayoutEffect } from 'react';
import { useTexture } from '@react-three/drei';
import * as THREE from 'three';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useEdgePreservingMaterial } from './materials/useEdgePreservingMaterial';

gsap.registerPlugin(ScrollTrigger);

export default function PuzzleGroup() {
  const groupRef = useRef<THREE.Group>(null);
  const meshesRef = useRef<THREE.Mesh[]>([]);

  const textures = useTexture([
    '/assets/1.png',
    '/assets/2.png',
    '/assets/3.png',
    '/assets/4.png',
    '/assets/5.png',
    '/assets/puzzle-pb.png',
  ]);

  // Proporções (ajuste conforme necessário)
  const aspect = 1.0; // 1:1, altere para 16/9 se suas imagens forem widescreen
  const width = 7.5;
  const height = width / aspect;
  const thickness = 0.1;

  useLayoutEffect(() => {
    const group = groupRef.current;
    if (!group) return;

    // Estado inicial: dispersão profunda e rotações caóticas
    meshesRef.current.forEach((mesh, index) => {
      const angle = (index / (textures.length - 1)) * Math.PI * 2;
      const radius = 14;

      if (index === textures.length - 1) {
        // Imagem consolidada: começa oculta atrás do ponto focal
        mesh.position.set(0, 0, -4);
        const materials = mesh.material;
        if (Array.isArray(materials)) {
          materials.forEach((mat) => {
            if (mat) mat.opacity = 0;
          });
        } else if (materials) {
          (materials as THREE.Material).opacity = 0;
        }
        mesh.scale.setScalar(0.85);
      } else {
        // Peças soltas: distribuição em órbita elíptica com profundidade
        mesh.position.x = Math.cos(angle * 1.7) * radius * 0.9;
        mesh.position.y = Math.sin(angle * 2.3) * radius * 0.7;
        mesh.position.z = -12 + Math.sin(angle) * 6; // Z entre -18 e -6

        mesh.rotation.x = Math.random() * Math.PI;
        mesh.rotation.y = Math.random() * Math.PI;
        mesh.rotation.z = Math.random() * Math.PI;
      }
    });

    const tl = gsap.timeline({
      scrollTrigger: {
        trigger: 'body',
        start: 'top top',
        end: '+=2200',
        scrub: 1.8,
      },
    });

    // Rotação do grupo com eixo inclinado para evitar colapso planar
    tl.to(
      group.rotation,
      {
        x: 0.25, // Inclinação constante para manter visibilidade
        y: Math.PI * 2,
        z: 0.1,
        ease: 'power2.inOut',
        duration: 1,
      },
      0
    );

    // Animação individual de cada peça
    meshesRef.current.forEach((mesh, index) => {
      const isFinalPiece = index === textures.length - 1;
      const materials = mesh.material as THREE.Material[];

      if (!isFinalPiece) {
        // Convergência para o centro com Z ligeiramente negativo (passam por trás da imagem final)
        tl.to(
          mesh.position,
          {
            x: 0,
            y: 0,
            z: -0.08, // "Véu de Evento": passam por trás da peça final
            ease: 'back.out(1.8)',
            duration: 1.1,
          },
          0.1
        );

        tl.to(
          mesh.rotation,
          {
            x: 0,
            y: 0,
            z: 0,
            ease: 'power4.inOut',
            duration: 1.0,
          },
          0.1
        );

        // Desaparecimento progressivo antes da conclusão
        tl.to(
          materials,
          {
            opacity: 0,
            duration: 0.25,
            stagger: 0.01,
          },
          0.85
        );
      } else {
        // Peça final: emerge na frente e ganha opacidade
        tl.to(
          mesh.position,
          {
            z: 0.02,
            ease: 'power2.out',
            duration: 0.8,
          },
          0.4
        );

        tl.to(
          materials,
          {
            opacity: 1,
            duration: 0.3,
            stagger: 0.02,
          },
          0.85
        );

        tl.to(
          mesh.scale,
          {
            x: 1,
            y: 1,
            z: 1,
            ease: 'elastic.out(1, 0.3)',
            duration: 0.6,
          },
          0.85
        );
      }
    });

    return () => {
      tl.kill();
    };
  }, [textures.length]);

  return (
    <group ref={groupRef}>
      {textures.map((tex, i) => {
        const materialsArray = useEdgePreservingMaterial(tex);
        return (
          <mesh
            key={i}
            ref={(el) => (meshesRef.current[i] = el!)}
            material={materialsArray}
            castShadow
            receiveShadow
          >
            <boxGeometry args={[width, height, thickness]} />
          </mesh>
        );
      })}
    </group>
  );
}
