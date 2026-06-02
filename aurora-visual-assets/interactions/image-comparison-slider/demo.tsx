import { ImageComparison } from "./index";

export default function DemoOne() {
  const cityImg = "https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?auto=format&fit=crop&q=80&w=1200";
  const cityNightImg = "https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?auto=format&fit=crop&q=80&w=1200&sat=-50&brightness=-30";

  return (
    <div className="w-full min-h-screen bg-zinc-950 flex flex-col items-center justify-center p-8 font-sans">
        <div className="w-full text-center mb-12">
            <h1 className="text-4xl md:text-5xl font-bold text-white mb-4 tracking-tighter">
              Aura <span className="text-white/20">Comparison</span>
            </h1>
            <p className="text-zinc-500 max-w-md mx-auto">
              Vanilla implementation of spectral alignment for visual verification.
            </p>
        </div>
        
        <div className="max-w-5xl w-full border border-white/5 rounded-2xl overflow-hidden shadow-[0_0_50px_-12px_rgba(255,255,255,0.1)]">
          <ImageComparison
              beforeImage={cityImg}
              afterImage={cityNightImg}
              altBefore="City Day"
              altAfter="City Muted Night"
              className="aspect-video"
          />
        </div>
    </div>
  )
}
