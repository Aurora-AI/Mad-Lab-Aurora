'use client';

import { Canvas, extend, useFrame, useThree } from '@react-three/fiber';
import { useAspect, useTexture, Html } from '@react-three/drei';
import { useMemo, useRef, useState, useEffect } from 'react';
import * as THREE from 'three/webgpu';
import { bloom } from 'three/examples/jsm/tsl/display/BloomNode.js';
import { Mesh } from 'three';
import { ArrowUpRight, Cpu, Globe, MousePointer2, Scan } from "lucide-react";

import {
  abs,
  blendScreen,
  float,
  mod,
  mx_cell_noise_float,
  oneMinus,
  smoothstep,
  texture,
  uniform,
  uv,
  vec2,
  vec3,
  pass,
} from 'three/tsl';

// Unsplash assets for a premium, dark futuristic look
const TEXTUREMAP = "https://images.unsplash.com/photo-1635776062127-d379bfcba9f8?q=80&w=2070&auto=format&fit=crop";
const DEPTHMAP = "https://images.unsplash.com/photo-1550684848-fac1c5b4e853?q=80&w=2070&auto=format&fit=crop";

class ScannerMaterial extends THREE.NodeMaterial {
  map: THREE.Texture | null = null;
  depthMap: THREE.Texture | null = null;
  timeNode = uniform(0);

  constructor() {
    super();
    this.transparent = true;
  }

  setup() {
    const progress = mod(this.timeNode.mul(0.3), 1.2).sub(0.1);
    
    const vUv = uv();
    // In TSL, texture nodes are created via texture(map, uv)
    const texColor = texture(this.map!, vUv);
    const depthColor = texture(this.depthMap!, vUv);
    
    // Scan line effect
    const scanLine = smoothstep(progress, progress.add(0.005), vUv.y).mul(
      oneMinus(smoothstep(progress.add(0.005), progress.add(0.01), vUv.y))
    );
    
    const scanTrail = smoothstep(progress.sub(0.15), progress, vUv.y).mul(
      oneMinus(smoothstep(progress, progress.add(0.01), vUv.y))
    );

    const noise = mx_cell_noise_float(vUv.mul(20).add(this.timeNode.mul(0.1)));
    
    // Fix grid logic: step is step(edge, value)
    const gridXY = abs(mod(vUv.mul(40), 1.0).sub(0.5));
    const gridX = smoothstep(0.015, 0.02, gridXY.x);
    const gridY = smoothstep(0.015, 0.02, gridXY.y);
    const gridSignal = oneMinus(gridX.mul(gridY)).mul(scanTrail).mul(0.15);

    const finalColor = texColor.rgb
      .mul(0.4)
      .add(vec3(0.0, 0.8, 1.0).mul(scanLine.mul(2.0)))
      .add(vec3(0.0, 0.4, 0.6).mul(scanTrail.mul(noise)))
      .add(vec3(0.0, 0.6, 1.0).mul(gridSignal));

    const alpha = float(1.0).sub(depthColor.r.mul(0.8));

    return finalColor.mul(alpha);
  }
}

export function FuturisticHeroContent() {
  const meshRef = useRef<Mesh>(null);
  const { size } = useThree();
  const scale = useAspect(size.width, size.height, 1);
  const textures = useTexture({
    map: TEXTUREMAP,
    depthMap: DEPTHMAP,
  });

  const material = useMemo(() => {
    const mat = new ScannerMaterial();
    mat.map = textures.map;
    mat.depthMap = textures.depthMap;
    return mat;
  }, [textures]);

  const [mouse, setMouse] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setMouse({
        x: (e.clientX / window.innerWidth - 0.5) * 2,
        y: (e.clientY / window.innerHeight - 0.5) * 2,
      });
    };
    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.position.x = THREE.MathUtils.lerp(meshRef.current.position.x, mouse.x * 0.2, 0.05);
      meshRef.current.position.y = THREE.MathUtils.lerp(meshRef.current.position.y, -mouse.y * 0.2, 0.05);
      meshRef.current.rotation.y = THREE.MathUtils.lerp(meshRef.current.rotation.y, mouse.x * 0.1, 0.05);
      meshRef.current.rotation.x = THREE.MathUtils.lerp(meshRef.current.rotation.x, -mouse.y * 0.1, 0.05);
      material.timeNode.value = state.clock.getElapsedTime();
    }
  });

  return (
    <group>
      <mesh ref={meshRef} scale={[scale[0] * 1.5, scale[1] * 1.5, 1]}>
        <planeGeometry args={[1, 1, 64, 64]} />
        <primitive object={material} attach="material" />
      </mesh>

      <Html fullscreen portal={undefined}>
        <div style={{ pointerEvents: 'none', position: 'fixed', inset: 0, width: '100vw', height: '100vh', color: 'white' }}>
          
          {/* Top Left: System Core */}
          <div style={{ position: 'absolute', top: '4rem', left: '4rem', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
             <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
               <div style={{ display: 'flex', height: '2.5rem', width: '2.5rem', alignItems: 'center', justifyContent: 'center', borderRadius: '50%', background: 'rgba(59, 130, 246, 0.2)', boxShadow: '0 0 15px rgba(59, 130, 246, 0.3)', border: '1px solid rgba(59, 130, 246, 0.4)' }}>
                 <Cpu className="h-5 w-5 text-blue-400" />
               </div>
               <div style={{ display: 'flex', flexDirection: 'column' }}>
                 <span style={{ fontSize: '9px', textTransform: 'uppercase', letterSpacing: '0.3em', color: 'rgba(96, 165, 250, 0.6)', fontWeight: 600 }}>System Core</span>
                 <span style={{ fontFamily: 'monospace', fontSize: '13px', fontWeight: 'bold', color: 'rgba(255, 255, 255, 0.9)', textTransform: 'uppercase', letterSpacing: '-0.02em' }}>Aurora-λ Online</span>
               </div>
             </div>
          </div>

          {/* Center: Main Content */}
          <div style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '2.5rem', textAlign: 'center', maxWidth: '100%' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem' }}>
              <span style={{ height: '1px', width: '4rem', background: 'linear-gradient(to right, transparent, rgba(59, 130, 246, 0.5))' }} />
              <span style={{ fontFamily: 'monospace', fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.4em', color: '#60a5fa' }}>Pioneering Digital Sovereignty</span>
              <span style={{ height: '1px', width: '4rem', background: 'linear-gradient(to left, transparent, rgba(59, 130, 246, 0.5))' }} />
            </div>

            <h1 style={{ fontSize: 'clamp(4rem, 12vw, 9rem)', fontWeight: 900, letterSpacing: '-0.05em', lineHeight: 0.9, margin: 0 }}>
              MIRA <span style={{ color: 'transparent', WebkitTextFillColor: 'transparent', backgroundImage: 'linear-gradient(to bottom, white, rgba(255,255,255,0.1))', backgroundClip: 'text', WebkitBackgroundClip: 'text', textTransform: 'uppercase' }}>Intelligence</span>
            </h1>

            <p style={{ maxWidth: '40rem', fontSize: 'clamp(1rem, 2vw, 1.25rem)', color: 'rgba(255,255,255,0.5)', lineHeight: 1.6, fontWeight: 300, letterSpacing: '0.05em', margin: 0, padding: '0 2rem' }}>
              Architecting the next epoch of enterprise synthesis. Where raw logic meets cinematic performance.
            </p>

            <div style={{ display: 'flex', flexWrap: 'wrap', alignItems: 'center', justifyContent: 'center', gap: '1.5rem', paddingTop: '1.5rem' }}>
              <button style={{ pointerEvents: 'auto', position: 'relative', overflow: 'hidden', borderRadius: '9999px', background: 'white', padding: '1.25rem 2.5rem', fontSize: '0.875rem', fontWeight: 'bold', color: 'black', border: 'none', cursor: 'pointer', transition: 'transform 0.2s', boxShadow: '0 10px 30px rgba(255,255,255,0.2)' }}>
                <span style={{ position: 'relative', zIndex: 10, display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                  Initialize Protocol <ArrowUpRight className="h-4 w-4" />
                </span>
              </button>
              <button style={{ pointerEvents: 'auto', borderRadius: '9999px', border: '1px solid rgba(255,255,255,0.1)', background: 'rgba(255,255,255,0.03)', padding: '1.25rem 2.5rem', fontSize: '0.875rem', fontWeight: 'bold', color: 'white', backdropFilter: 'blur(20px)', transition: 'all 0.3s', cursor: 'pointer' }}>
                 View Manifesto
              </button>
            </div>
          </div>

          {/* Bottom Right: Status Info */}
          <div style={{ position: 'absolute', right: '4rem', bottom: '4rem', display: 'flex', alignItems: 'center', gap: '2rem', fontFamily: 'monospace', fontSize: '10px', textTransform: 'uppercase', letterSpacing: '0.2em', color: 'rgba(255,255,255,0.4)' }}>
             <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
               <Scan className="h-4 w-4 text-white/50" />
               <span>Biometric Encrypted</span>
             </div>
             <div style={{ height: '4px', width: '4px', borderRadius: '50%', background: 'rgba(59, 130, 246, 0.5)', boxShadow: '0 0 8px rgba(59, 130, 246, 0.8)' }} />
             <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
               <Globe className="h-4 w-4 text-white/50" />
               <span>Global Synthesis Node</span>
             </div>
          </div>
        </div>
      </Html>
    </group>
  );
}

export function HeroFuturistic() {
  return (
    <div id="hero-futuristic" style={{ position: 'relative', height: '100vh', width: '100vw', minHeight: '100vh', overflow: 'hidden', background: '#000' }}>
      <Canvas
        gl={{
          antialias: true,
          alpha: true,
        }}
        camera={{ position: [0, 0, 5], fov: 45 }}
        style={{ height: '100vh', width: '100vw', background: '#000' }}
      >
        <color attach="background" args={['#000']} />
        <ambientLight intensity={0.5} />
        <FuturisticHeroContent />
      </Canvas>
      
      {/* Dynamic scanline overlay */}
      <div style={{ pointerEvents: 'none', position: 'absolute', inset: 0, background: 'linear-gradient(rgba(18,16,16,0) 50%, rgba(0,0,0,0.25) 50%), linear-gradient(90deg, rgba(255,0,0,0.06), rgba(0,255,0,0.02), rgba(0,0,10,0.06))', backgroundSize: '100% 2px, 3px 100%', opacity: 0.2 }} />
      
      {/* Radial vignette */}
      <div style={{ pointerEvents: 'none', position: 'absolute', inset: 0, background: 'radial-gradient(circle at center, transparent 0%, black 100%)', opacity: 0.6 }} />
    </div>
  );
}
