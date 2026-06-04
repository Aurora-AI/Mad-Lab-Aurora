"use client"

import { ShaderAnimation } from "./index"

export default function ShaderLinesDemo() {
  return (
    <div className="relative w-full h-[650px] bg-black overflow-hidden rounded-xl border border-white/5 flex items-center justify-center">
      {/* Background layer */}
      <div className="absolute inset-0 z-0">
        <ShaderAnimation />
      </div>
      
      {/* Content Layer */}
      <div className="relative z-10 flex flex-col items-center gap-6 px-12 text-center">
        <div className="space-y-2">
          <h2 className="text-zinc-500 font-mono text-[10px] uppercase tracking-[0.4em]">
            Visual Protocol 033 / 034
          </h2>
          <h1 className="text-7xl md:text-8xl font-bold text-white tracking-tighter leading-none italic uppercase">
            Shader<br />
            <span className="text-white/20">Lines</span>
          </h1>
        </div>
        
        <p className="max-w-md text-zinc-400 text-sm font-medium leading-relaxed tracking-tight">
          A procedural energy flow rendered through a pixelated mosaic grid. 
          Driven by high-precision GLSL uniforms.
        </p>

        <button className="px-6 py-2 bg-white text-black text-[10px] font-bold uppercase tracking-widest rounded-full hover:bg-zinc-200 transition-colors">
          Initialize Sequence
        </button>
      </div>

      {/* Aesthetic Overlays */}
      <div className="absolute inset-0 pointer-events-none bg-[radial-gradient(circle_at_center,transparent_0%,black_100%)] opacity-40 z-20" />
      <div className="absolute inset-0 pointer-events-none bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-[0.03] contrast-150 brightness-150 z-30" />
    </div>
  )
}
