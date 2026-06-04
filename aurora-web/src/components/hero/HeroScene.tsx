import { Canvas } from '@react-three/fiber';
import { EffectComposer, DepthOfField, Vignette, Noise } from '@react-three/postprocessing';
import { Suspense, useEffect } from 'react';
import { useThree, useFrame } from '@react-three/fiber';
import PuzzleGroup from './PuzzleGroup';
import { telemetry } from '../../lib/arc/telemetry';

function StageMonitor() {
  const { gl } = useThree();
  
  useFrame((state) => {
    const fps = Math.round(1 / state.clock.getDelta());
    
    telemetry.update({
      fps: isFinite(fps) ? fps : 60,
      drawCalls: gl.info.render.calls,
      triangles: gl.info.render.triangles,
      memory: (gl.info.memory as any).geometries || 0
    });
  });

  return null;
}

export default function HeroScene() {
  return (
    <div 
      id="hero-scene-root"
      className="w-full h-screen bg-void relative overflow-hidden flex flex-col items-center justify-center"
      style={{ minHeight: '100vh', height: '100vh' }}
    >
      <Canvas
        camera={{ position: [0, 0, 12], fov: 45 }}
        gl={{ antialias: true, alpha: false, stencil: false }}
        shadows
      >
        <color attach="background" args={['#000000']} />

        {/* Cinematic Luxury Lighting */}
        <ambientLight intensity={0.2} />
        <directionalLight
          position={[5, 10, 5]}
          intensity={2.5}
          castShadow
          shadow-mapSize-width={2048}
          shadow-mapSize-height={2048}
          shadow-bias={-0.0001}
        />
        <pointLight position={[-10, -5, 5]} intensity={1.5} color="#ffffff" />
        <spotLight 
          position={[0, 20, 10]} 
          angle={0.15} 
          penumbra={1} 
          intensity={3} 
          castShadow 
        />

        <Suspense fallback={null}>
          <StageMonitor />
          <PuzzleGroup />
        </Suspense>

        <EffectComposer enableNormalPass={false}>
          <DepthOfField
            focusDistance={0}
            focalLength={0.1}
            bokehScale={5}
          />
          <Noise opacity={0.02} />
          <Vignette darkness={0.6} offset={0.1} />
        </EffectComposer>
      </Canvas>

      {/* Overlay: Luxury Typography (The "MIRA" touch) */}
      <div className="hero-fixed-overlay">
        <h1 className="hero-title-mira">
          <span className="block animate-reveal-up">AURORA</span>
        </h1>
        
        <div 
          className="mt-6 overflow-hidden flex items-center gap-4 text-ghost uppercase tracking-widest text-[0.7rem]"
          style={{ fontFamily: 'var(--font-body)' }}
        >
          <span className="w-12 h-[1px] bg-ghost/30 block" />
          <span className="animate-reveal-up" style={{ animationDelay: '0.4s' }}>
            Luxury Digital Experiences
          </span>
          <span className="w-12 h-[1px] bg-ghost/30 block" />
        </div>
      </div>

      {/* Luxury Border Frame */}
      <div className="hero-frame" />
    </div>
  );
}
