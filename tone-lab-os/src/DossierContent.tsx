export function DossierContent({ item }: { item: any }) {
  return (
    <div>
      {/* Minimal Borderless Navigation */}
      <header className="w-full max-w-7xl mx-auto px-8 sm:px-12 lg:px-16 pt-10 pb-6 flex items-center justify-between">
        <div className="flex items-center gap-10">
          <a className="text-sm font-semibold tracking-tight text-neutral-900 flex items-center gap-2.5" href="#">
            <span className="w-2 h-2 rounded-full bg-neutral-900"></span>
            Tone Lab
          </a>
          <nav className="hidden md:flex items-center gap-8 text-xs font-medium text-neutral-500 tracking-wide">
            <a className="hover:text-neutral-900 transition-colors" href="#">Architecture</a>
            <a className="text-neutral-900 font-semibold" href="#">Schematics</a>
            <a className="hover:text-neutral-900 transition-colors" href="#">Signal Chain</a>
            <a className="hover:text-neutral-900 transition-colors" href="#">Telemetry</a>
            <a className="hover:text-neutral-900 transition-colors" href="#">Bench Test</a>
          </nav>
        </div>
        <div className="flex items-center gap-6">
          <span className="hidden sm:inline-flex items-center gap-1.5 text-xs font-medium text-neutral-500">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
            Calibrated
          </span>
          <button className="inline-flex items-center gap-2 text-xs font-medium text-neutral-900 hover:text-neutral-500 transition-colors">
            <span className="material-symbols-outlined text-[16px]">file_download</span>
            Export Spec
          </button>
          <div className="hidden sm:flex items-center gap-3 text-neutral-400 hover:text-neutral-900 transition-colors">
            <button className="hover:text-neutral-900" title="Terminal"><span className="material-symbols-outlined text-[18px]">terminal</span></button>
            <button className="hover:text-neutral-900" title="Settings"><span className="material-symbols-outlined text-[18px]">settings_input_component</span></button>
          </div>
        </div>
      </header>

      {/* Main Editorial Canvas */}
      <main className="flex-grow w-full max-w-7xl mx-auto px-8 sm:px-12 lg:px-16 py-12 lg:py-20 space-y-28 lg:space-y-36">
        {/* Section 1 & 2: Asymmetric Editorial Hero */}
        <section className="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-20 items-center">
          {/* Left Editorial Column */}
          <div className="lg:col-span-7 space-y-8">
            <div className="space-y-4">
              <div className="flex items-center gap-3 text-xs tracking-wider uppercase font-medium text-neutral-500">
                <span>{item.category}</span>
                <span className="text-neutral-300">/</span>
                <span className="text-neutral-900 font-semibold">{item.subCategory}</span>
              </div>
              <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-neutral-900 leading-[1.06]">
                {item.name}
              </h1>
              <p className="text-base sm:text-lg text-neutral-500 font-normal tracking-tight">
                {item.dossier.subtitle}
              </p>
            </div>

            {/* Flowing Editorial Narrative */}
            <div className="space-y-5 text-neutral-500 text-[15px] sm:text-base leading-relaxed max-w-xl font-normal">
              <p>{item.dossier.description}</p>
              <p className="text-neutral-400 text-sm leading-relaxed">{item.dossier.role}</p>
            </div>

            {/* Understated Minimal Action Links */}
            <div className="pt-2 flex flex-wrap items-center gap-4">
              <button className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-neutral-900 text-white text-xs font-medium tracking-wide hover:bg-neutral-800 transition-colors">
                <span className="material-symbols-outlined text-[15px]">picture_as_pdf</span>
                Export Dossier PDF
              </button>
              <button className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-neutral-200/70 text-neutral-900 text-xs font-medium tracking-wide hover:bg-neutral-300 transition-colors">
                <span className="material-symbols-outlined text-[15px]">edit_note</span>
                Edit Specification
              </button>
              <button className="inline-flex items-center gap-1.5 px-3 py-2 text-neutral-500 hover:text-neutral-900 text-xs font-medium transition-colors">
                Bench Telemetry
                <span className="material-symbols-outlined text-[15px]">arrow_outward</span>
              </button>
            </div>
            
            {/* Subtle Physical Details Row */}
            <div className="pt-6 flex items-center gap-8 text-xs text-neutral-500 font-normal">
              <div>
                <span className="text-neutral-400 block text-[11px] mb-0.5">Priority</span>
                <span className="text-neutral-900 font-medium">{item.priority}</span>
              </div>
              <div>
                <span className="text-neutral-400 block text-[11px] mb-0.5">Status</span>
                <span className="text-neutral-900 font-medium">{item.status}</span>
              </div>
            </div>
          </div>

          {/* Right Column: Floating Product Showcase */}
          <div className="lg:col-span-5 flex justify-center items-center">
            <div className="w-full relative group">
              <div className="aspect-[4/3] rounded-3xl bg-neutral-900/95 flex items-center justify-center p-8 sm:p-12 overflow-hidden shadow-2xl shadow-neutral-900/10">
                <img 
                  className="max-h-full max-w-full object-contain filter contrast-105 transition-transform duration-700 ease-out group-hover:scale-105" 
                  alt={item.name} 
                  src={item.image} 
                />
              </div>
              <p className="mt-3 text-right text-[11px] text-neutral-400 tracking-wide">
                Unit Ref: {item.dossier.refId}
              </p>
            </div>
          </div>
        </section>

        {/* Dynamic Signal Path Architecture */}
        {item.dossier.signalChain && item.dossier.signalChain.length > 0 && (
          <section className="space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-baseline justify-between gap-2">
              <h2 className="text-xs uppercase tracking-widest font-semibold text-neutral-500">
                Signal Path &amp; Audio Flow
              </h2>
              <span className="text-xs text-neutral-400 font-normal">
                Analog Serial Pass • 1MΩ Input / 16Ω Load
              </span>
            </div>

            <div className="overflow-x-auto pb-4 pt-1 -mx-4 px-4 sm:mx-0 sm:px-0">
              <div className="flex items-center min-w-[max-content] justify-between gap-2.5">
                {item.dossier.signalChain.map((node: any, index: number) => (
                  <div key={index} className="flex items-center gap-2.5">
                    {/* Node Card */}
                    <div className={`w-44 ${node.isActive ? 'bg-white border-2 border-neutral-900 shadow-md' : 'bg-white border border-neutral-200/80 shadow-sm transition hover:shadow-md'} rounded-xl p-3.5 relative`}>
                      {node.isActive && (
                        <div className="absolute -top-2.5 right-3 px-2 py-0.5 rounded-full bg-neutral-900 text-white text-[9px] font-semibold tracking-wider uppercase flex items-center gap-1 shadow-sm">
                          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                          Under Test
                        </div>
                      )}
                      
                      <div className={`aspect-square w-full rounded-lg ${node.isActive ? 'bg-neutral-900' : 'bg-neutral-100'} overflow-hidden mb-3 flex items-center justify-center p-2`}>
                        <img alt={node.label} className={`max-h-full max-w-full object-cover rounded-md ${node.isActive ? 'filter contrast-105 object-contain' : ''}`} src={node.image} />
                      </div>
                      
                      <div className="space-y-1">
                        <span className={`text-[10px] tracking-wider uppercase font-semibold ${node.isActive ? 'text-neutral-900' : 'text-neutral-400'} block`}>{node.stage}</span>
                        <h3 className={`text-sm ${node.isActive ? 'font-bold' : 'font-semibold'} text-neutral-900 leading-snug truncate`}>{node.label}</h3>
                        <p className={`text-[11px] ${node.isActive ? 'text-neutral-600 font-medium' : 'text-neutral-500'} leading-tight line-clamp-2`}>{node.desc}</p>
                      </div>
                    </div>

                    {/* Arrow Connector (skip for last item) */}
                    {index < item.dossier.signalChain.length - 1 && (
                      <div className="flex-shrink-0 text-neutral-300 px-1">
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth="1.75" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3"></path>
                        </svg>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </section>
        )}

        {/* Section 4: Anchored Specifications Surface Container */}
        <section>
          <div className="bg-white border border-[#EAEAEA] rounded-2xl p-8 sm:p-10 shadow-[0_12px_36px_rgba(0,0,0,0.035)] space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-baseline justify-between gap-2 pb-2">
              <div className="space-y-1">
                <h2 className="text-xs uppercase tracking-widest font-semibold text-neutral-500">
                  Technical Specifications &amp; Calibration
                </h2>
                <p className="text-xs text-neutral-400">Analog laboratory verification benchmark profile</p>
              </div>
              <span className="inline-flex items-center gap-1.5 text-xs text-neutral-500 font-medium bg-neutral-50 border border-neutral-200/60 px-3 py-1 rounded-full">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                Calibrated under 230V 50Hz mains
              </span>
            </div>
            
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead>
                  <tr className="text-[11px] uppercase tracking-wider text-neutral-400 border-b border-neutral-100">
                    <th className="py-3 pr-8 font-medium w-1/4">Parameter</th>
                    <th className="py-3 pr-8 font-medium w-2/5">Specification</th>
                    <th className="py-3 pr-8 font-medium w-1/5">Reference Source</th>
                    <th className="py-3 font-medium text-right w-auto">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-neutral-100 font-normal">
                  {item.dossier.specs.map((spec: any, index: number) => (
                    <tr key={index} className="hover:bg-neutral-50/60 transition-colors">
                      <td className="py-4 pr-8 font-medium text-neutral-900">{spec.parameter}</td>
                      <td className="py-4 pr-8 text-neutral-800">{spec.value}</td>
                      <td className="py-4 pr-8 text-neutral-500">{spec.source}</td>
                      <td className="py-4 text-right">
                        {spec.status === "VERIFIED" ? (
                          <span className="inline-flex items-center gap-1 text-xs text-emerald-700 font-medium">
                            <span className="material-symbols-outlined text-[14px]">check_circle</span>
                            Verified
                          </span>
                        ) : (
                          <span className="inline-flex items-center gap-1 text-xs text-amber-700 font-medium bg-amber-50 px-2 py-0.5 rounded">
                            <span className="w-1.5 h-1.5 rounded-full bg-amber-500"></span>
                            Pending
                          </span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </section>
      </main>

      {/* Clean Editorial Footer */}
      <footer className="w-full max-w-7xl mx-auto px-8 sm:px-12 lg:px-16 pt-16 pb-12 mt-12 flex flex-col sm:flex-row items-baseline justify-between gap-6 text-xs text-neutral-400 font-normal">
        <div className="flex items-center gap-2 text-neutral-500">
          <span className="w-1.5 h-1.5 rounded-full bg-neutral-400"></span>
          <span>Tone Lab OS • Engineering Dossier</span>
        </div>
        <div className="flex flex-wrap items-center gap-6 text-neutral-500">
          <a className="hover:text-neutral-900 transition-colors" href="#">System Logs</a>
          <a className="hover:text-neutral-900 transition-colors" href="#">Calibration Protocol</a>
          <a className="hover:text-neutral-900 transition-colors" href="#">Hardware I/O</a>
          <a className="hover:text-neutral-900 transition-colors" href="#">Signal Integrity</a>
        </div>
      </footer>
    </div>
  );
}
