"use client"

import { Canvas } from "@react-three/fiber"
import { ShaderPlane, EnergyRing } from "./index"
import { Suspense } from "react"

export default function PaperShadersDemo() {
  return (
    <div className="w-full h-screen bg-black">
      <Canvas camera={{ position: [0, 0, 3], fov: 45 }}>
        <Suspense fallback={null}>
          <ambientLight intensity={0.5} />
          
          {/* Main Spectral Plane */}
          <ShaderPlane 
            position={[0, 0, 0]} 
            color1="#000000" 
            color2="#333333" 
          />
          
          {/* Outer Energy Orbitals */}
          <EnergyRing radius={1.2} color="#ffffff" position={[0, 0, 0.1]} />
          <EnergyRing radius={1.5} color="#444444" position={[0, 0, -0.1]} />
          
          {/* Background Aura */}
          <ShaderPlane 
            position={[0, 0, -1]} 
            color1="#1a1a1a" 
            color2="#000000" 
          />
        </Suspense>
      </Canvas>
      
      {/* Editorial Overlay */}
      <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none p-8">
        <div className="max-w-2xl w-full text-center">
          <h1 className="text-6xl font-bold text-white tracking-tighter mb-4 mix-blend-difference">
            SHADER <span className="text-white/20">FABRIC</span>
          </h1>
          <p className="text-zinc-500 font-mono text-xs uppercase tracking-[0.2em]">
            P029: Procedural Noise / P030: Vertex Deformation
          </p>
        </div>
      </div>

      <div className="absolute bottom-12 left-12 font-mono text-[10px] text-white/20 uppercase tracking-widest">
        Render Engine: WebGL 2.0 / R3F
      </div>
    </div>
  )
}
