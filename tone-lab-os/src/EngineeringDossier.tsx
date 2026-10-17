import { Zap, ShieldAlert } from "lucide-react";

export function EngineeringDossier() {
  return (
    <div className="min-h-screen bg-ethereal text-charcoal p-12">
      <header className="mb-12 max-w-5xl mx-auto">
        <div className="flex gap-4 items-center mb-4">
          <span className="bg-black text-white px-3 py-1 text-[10px] font-mono uppercase tracking-widest">Project Amp-001</span>
          <span className="text-gray-500 text-xs font-mono uppercase tracking-widest">v1.1 Revision</span>
        </div>
        <h1 className="text-5xl font-bold font-sans uppercase tracking-tighter text-black mb-4">
          Amplificador Signature
        </h1>
        <p className="text-xl text-gray-700 max-w-3xl leading-relaxed">
          Protótipo 01 — Plataforma valvulada modular de baixa potência. 
          Especificação de conceito, arquitetura, modificações, upgrades, gates de validação e roadmap de industrialização.
        </p>
      </header>

      <main className="max-w-5xl mx-auto grid grid-cols-12 gap-8">
        <aside className="col-span-3">
          <nav className="flex flex-col gap-1 text-sm font-bold uppercase tracking-widest text-gray-400">
            <a href="#" className="text-black py-2 border-l-2 border-black pl-4">Specification</a>
            <a href="#" className="hover:text-black py-2 pl-4 transition-colors">Schematic</a>
            <a href="#" className="hover:text-black py-2 pl-4 transition-colors">Signal Path</a>
            <a href="#" className="hover:text-black py-2 pl-4 transition-colors">Power Supply</a>
            <a href="#" className="hover:text-black py-2 pl-4 transition-colors">BOM</a>
            <a href="#" className="hover:text-black py-2 pl-4 transition-colors">Test Points</a>
            <a href="#" className="hover:text-black py-2 pl-4 transition-colors">Measurements</a>
            <a href="#" className="text-red-600 py-2 pl-4 flex items-center gap-2"><ShieldAlert size={14}/> Safety</a>
            <a href="#" className="hover:text-black py-2 pl-4 transition-colors">Build Log</a>
          </nav>
        </aside>

        <section className="col-span-9">
          <div className="bg-white/60 backdrop-blur-2xl border border-white rounded-[24px] p-12 shadow-[0_8px_32px_rgba(0,0,0,0.04)] mb-8">
            <h2 className="text-sm font-mono uppercase tracking-widest text-gray-500 mb-6 flex items-center gap-2">
              <Zap size={16} /> Central Principle
            </h2>
            <p className="text-2xl font-serif text-black leading-tight mb-8">
              "Projetar comportamentos, não copiar circuitos. Toda modificação tonal deve partir de um fenômeno musical definido, ser reproduzida externamente e medida, depois traduzida para circuito próprio."
            </p>

            <h2 className="text-sm font-mono uppercase tracking-widest text-gray-500 mb-6 mt-12">
              Engineering Decisions
            </h2>
            
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="py-4 text-xs font-bold uppercase tracking-widest text-black">Decision Node</th>
                  <th className="py-4 text-xs font-bold uppercase tracking-widest text-black">State / Parameter</th>
                </tr>
              </thead>
              <tbody className="text-sm">
                <tr className="border-b border-gray-100">
                  <td className="py-4 font-bold text-black">Baseline Técnico</td>
                  <td className="py-4 text-gray-600">JCM800 Micro — preferência por EF80 push-pull</td>
                </tr>
                <tr className="border-b border-gray-100">
                  <td className="py-4 font-bold text-black">Potência</td>
                  <td className="py-4 text-gray-600">Baixa potência / uso de estúdio (Transformador dependente)</td>
                </tr>
                <tr className="border-b border-gray-100">
                  <td className="py-4 font-bold text-black">Construção V0</td>
                  <td className="py-4 text-gray-600">Turret/eyelet board (Não iniciar por PCB industrial)</td>
                </tr>
                <tr className="border-b border-gray-100">
                  <td className="py-4 font-bold text-black">Chassis</td>
                  <td className="py-4 text-gray-600">Formato físico de head 50/100 W (Superdimensionado)</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>
      </main>
    </div>
  );
}
