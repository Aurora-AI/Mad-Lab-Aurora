import React from 'react';

export const TheGateway: React.FC = () => {
  return (
    <section className="relative w-full py-40 bg-parchment border-t border-ink/5 overflow-hidden" id="cta">
      <div className="container mx-auto px-8 text-center relative z-10">
        <span className="font-mono text-[10px] text-aureate tracking-[0.4em] mb-12 block uppercase">
            06 // THE GATEWAY
        </span>
        
        <h2 className="font-display text-6xl md:text-8xl text-ink leading-none mb-16 max-w-4xl mx-auto">
            A soberania não se pede, <br />
            <span className="italic font-light">se executa.</span>
        </h2>
        
        <div className="flex flex-col items-center gap-12">
            <p className="font-editorial text-xl text-ink/60 max-w-xl mx-auto leading-relaxed">
                Inicie o protocolo de credenciamento e garanta o acesso à infraestrutura de inteligência determinística da Aurora.
            </p>
            
            <button className="group relative overflow-hidden bg-ink text-parchment px-16 py-6 font-mono text-[12px] uppercase tracking-[0.3em] transition-transform active:scale-95">
                <span className="relative z-10">Certificar Ativo Digital</span>
                <div className="absolute inset-0 bg-aureate transform translate-y-full transition-transform group-hover:translate-y-0 duration-500 ease-in-out" />
            </button>
            
            <div className="flex items-center gap-6 mt-8">
                 <span className="font-mono text-[9px] text-ink/30 uppercase tracking-widest">Protocol: 0xCRED_01</span>
                 <div className="w-1 h-1 rounded-full bg-aureate" />
                 <span className="font-mono text-[9px] text-ink/30 uppercase tracking-widest">Status: Ready_for_Ingestion</span>
            </div>
        </div>
      </div>

      {/* Decorative Axis Break */}
      <div className="absolute top-1/2 left-[10%] w-[80%] h-px bg-ink/5 -rotate-12 pointer-events-none opacity-40" />
      <div className="absolute top-1/2 left-[10%] w-[80%] h-px bg-ink/5 rotate-6 pointer-events-none opacity-40" />
      
      {/* Background Symbol */}
      <div className="absolute -bottom-20 -left-20 font-mono text-[30vw] text-ink/2 select-none pointer-events-none">
        Ω
      </div>
    </section>
  );
};

export default TheGateway;
