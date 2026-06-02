import React from 'react';

export const FounderDensity: React.FC = () => {
  return (
    <section className="relative w-full py-32 bg-stone border-t border-ink/5 overflow-hidden">
      <div className="container mx-auto px-8 md:px-20">
        <div className="flex flex-col md:flex-row items-center gap-20">
            {/* Portrait Column */}
            <div className="w-full md:w-1/2 relative">
                <div className="aspect-4/5 bg-ink/5 grayscale contrast-125 overflow-hidden border border-ink/10 relative group">
                    <img 
                        src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=1974&auto=format&fit=crop" 
                        alt="Founder Portrait"
                        className="w-full h-full object-cover transition-transform duration-[2s] group-hover:scale-105"
                    />
                    <div className="absolute inset-0 bg-ink/10 mix-blend-multiply" />
                    
                    {/* Floating Info */}
                    <div className="absolute bottom-6 left-6 p-4 bg-parchment/90 backdrop-blur border border-ink/5">
                         <span className="font-mono text-[9px] text-ink uppercase tracking-[0.3em]">
                            Rodrigo B. // Founder & Architect
                         </span>
                    </div>
                </div>
                
                {/* Decorative Elements */}
                <div className="absolute -top-10 -right-10 font-mono text-[120px] text-ink/3 select-none pointer-events-none">
                    05
                </div>
            </div>

            {/* Manifesto Column */}
            <div className="flex-1">
                <span className="font-mono text-[10px] text-aureate tracking-[0.4em] mb-8 block uppercase">
                    05 // FOUNDER DENSITY
                </span>
                <blockquote className="space-y-12">
                    <p className="font-display text-4xl md:text-5xl text-ink leading-[1.2]">
                        "O maior risco da IA não é a inteligência superior, mas a <span className="italic font-light">alucinação inferior</span> governando decisões críticas."
                    </p>
                    <footer className="pt-8 border-t border-ink/10">
                        <p className="font-editorial text-xl text-ink/80 leading-relaxed mb-8">
                            Nós não construímos chatbots. Nós construímos sistemas de evidência. A Aurora nasceu da necessidade de um mundo onde o determinismo não é opcional, mas o alicerce de toda soberania.
                        </p>
                        <div className="flex items-center gap-4">
                            <div className="w-12 h-px bg-aureate" />
                            <span className="font-mono text-[11px] text-ink uppercase tracking-widest">
                                R.B. // Aurora Intelligence
                            </span>
                        </div>
                    </footer>
                </blockquote>
            </div>
        </div>
      </div>
    </section>
  );
};

export default FounderDensity;
