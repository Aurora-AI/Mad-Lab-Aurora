"use client"

import VaporizeTextCycle, { Tag } from "./index"

export default function VapourTextDemo() {
  return (
    <div className="relative w-full h-screen bg-black overflow-hidden flex flex-col items-center justify-center p-12">
      {/* Background Ambience */}
      <div className="absolute inset-0 z-0 bg-[radial-gradient(circle_at_center,rgba(20,20,20,1)_0%,black_100%)]" />
      
      {/* Editorial Header */}
      <div className="absolute top-12 left-12 z-10 space-y-1">
        <p className="text-[10px] font-mono text-zinc-500 uppercase tracking-[0.5em] leading-none">
          Aurora Cinematic Type
        </p>
        <p className="text-[10px] font-mono text-white/20 uppercase tracking-[0.5em] leading-none">
          Archive v1.19.0
        </p>
      </div>

      {/* Main Kinetic Typography Component */}
      <div className="relative z-10 w-full max-w-5xl h-[300px] flex items-center justify-center">
        <VaporizeTextCycle
          texts={["AURORA", "EDITORIAL", "KINETIC"]}
          font={{
            fontFamily: "Inter, sans-serif",
            fontSize: "120px",
            fontWeight: 800
          }}
          color="rgb(255, 255, 255)"
          spread={8}
          density={6}
          animation={{
            vaporizeDuration: 2.5,
            fadeInDuration: 1.5,
            waitDuration: 1.0
          }}
          direction="left-to-right"
          alignment="center"
          tag={Tag.H1}
        />
      </div>

      {/* Dynamic Caption Overlay */}
      <div className="relative z-10 mt-24 max-w-sm text-center">
        <p className="text-zinc-500 text-[11px] font-medium leading-relaxed tracking-tight uppercase">
          Dissolving the boundaries between substance and void. 
          A procedural vaporization of digital intent.
        </p>
      </div>

      {/* Aesthetic Overlays */}
      <div className="absolute inset-0 pointer-events-none bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-[0.02] contrast-150 z-20" />
      <div className="absolute inset-0 pointer-events-none border border-white/5 m-8 z-30" />
    </div>
  )
}
