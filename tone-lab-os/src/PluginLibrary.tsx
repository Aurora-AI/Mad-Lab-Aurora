import { Search } from "lucide-react";

export function PluginLibrary() {
  const plugins = [
    { name: "FabFilter Pro-Q 3", type: "EQ / Dynamic EQ", status: "Installed", rating: "★★★★★", usage: "Mix / Corrective" },
    { name: "Neural DSP Nolly", type: "Amp Suite", status: "Installed", rating: "★★★★☆", usage: "Metal / Tracking" },
    { name: "Valhalla VintageVerb", type: "Reverb", status: "Installed", rating: "★★★★★", usage: "Creative / Space" },
    { name: "Soundtoys Decapitator", type: "Saturation", status: "Wishlist", rating: "-", usage: "Character" },
    { name: "Oeksound Soothe2", type: "Dynamic Resonance", status: "Installed", rating: "★★★★★", usage: "Harshness reduction" }
  ];

  return (
    <div className="min-h-screen bg-ethereal text-charcoal p-12">
      <header className="mb-12 max-w-7xl mx-auto flex justify-between items-end border-b border-gray-300 pb-8">
        <div>
          <h1 className="text-5xl font-bold uppercase tracking-tight text-black mb-2">Plugin Library</h1>
          <p className="text-gray-500 text-sm font-mono uppercase tracking-widest">Digital Processing Registry</p>
        </div>
        <div className="flex gap-4">
          <div className="relative">
            <Search size={14} className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" />
            <input 
              type="text" 
              placeholder="SEARCH LIBRARY..." 
              className="bg-white/50 backdrop-blur-md border border-gray-300 text-black pl-12 pr-4 py-3 w-72 focus:outline-none focus:border-black transition-colors uppercase text-xs font-mono"
            />
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto">
        <div className="flex gap-6 text-xs font-mono uppercase tracking-widest text-gray-500 mb-8">
          <span className="text-black font-bold cursor-pointer border-b-2 border-black pb-1">ALL</span>
          <span className="hover:text-black cursor-pointer">EQ</span>
          <span className="hover:text-black cursor-pointer">COMPRESSOR</span>
          <span className="hover:text-black cursor-pointer">AMP</span>
          <span className="hover:text-black cursor-pointer">CAB</span>
          <span className="hover:text-black cursor-pointer">DELAY</span>
          <span className="hover:text-black cursor-pointer">REVERB</span>
        </div>

        <div className="bg-white/60 backdrop-blur-2xl border border-white rounded-[24px] shadow-[0_8px_32px_rgba(0,0,0,0.04)] overflow-hidden">
          <div className="grid grid-cols-12 gap-4 text-[10px] font-mono text-gray-400 uppercase tracking-widest border-b border-gray-200 px-8 py-6 bg-white/40">
            <div className="col-span-3">Plugin Name</div>
            <div className="col-span-3">Category / Type</div>
            <div className="col-span-2">Status</div>
            <div className="col-span-2">Primary Usage</div>
            <div className="col-span-2">Rating</div>
          </div>

          <div className="flex flex-col">
            {plugins.map((pl, i) => (
              <div key={i} className="grid grid-cols-12 gap-4 items-center px-8 py-5 border-b border-gray-100 last:border-0 hover:bg-white/80 cursor-pointer transition-colors text-sm">
                <div className="col-span-3 font-sans font-bold text-black uppercase tracking-tight">{pl.name}</div>
                <div className="col-span-3 text-gray-600">{pl.type}</div>
                <div className="col-span-2 flex items-center gap-2 font-mono text-xs">
                  <span className={`w-2 h-2 rounded-full ${pl.status === 'Installed' ? 'bg-black' : 'bg-gray-300'}`}></span>
                  {pl.status}
                </div>
                <div className="col-span-2 text-gray-600">{pl.usage}</div>
                <div className="col-span-2 text-black tracking-widest">{pl.rating}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
