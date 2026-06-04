import React, { useState, useMemo, useRef, useCallback } from 'react';
import { Link } from 'react-router-dom';

export default function GovernancePage() {
  // Action Gate state: 'AWAITING' | 'COMMITTED' | 'REJECTED'
  const [status, setStatus] = useState<'AWAITING' | 'COMMITTED' | 'REJECTED'>('AWAITING');
  
  // Interactive Data states
  const [entityName, setEntityName] = useState('Grupo Aurora Holding');
  const [entityType, setEntityType] = useState('Economic Group');
  const [contextualEvidence, setContextualEvidence] = useState(
    '...solicitamos a abertura cadastral imediata dos dados operacionais da Grupo Aurora Holding para consolidação das carteiras comerciais de Curitiba...'
  );
  
  // Per-field inline editing state
  const [editingField, setEditingField] = useState<'entityName' | 'entityType' | 'evidence' | null>(null);
  const [draftEntityName, setDraftEntityName] = useState(entityName);
  const [draftEntityType, setDraftEntityType] = useState(entityType);
  const [draftEvidence, setDraftEvidence] = useState(contextualEvidence);

  const commitField = useCallback((field: 'entityName' | 'entityType' | 'evidence') => {
    if (field === 'entityName') setEntityName(draftEntityName);
    if (field === 'entityType') setEntityType(draftEntityType);
    if (field === 'evidence') setContextualEvidence(draftEvidence);
    setEditingField(null);
  }, [draftEntityName, draftEntityType, draftEvidence]);

  const startEditing = useCallback((field: 'entityName' | 'entityType' | 'evidence') => {
    if (status !== 'AWAITING') return;
    if (field === 'entityName') setDraftEntityName(entityName);
    if (field === 'entityType') setDraftEntityType(entityType);
    if (field === 'evidence') setDraftEvidence(contextualEvidence);
    setEditingField(field);
  }, [status, entityName, entityType, contextualEvidence]);

  // Conversational state
  const [chatInput, setChatInput] = useState('');
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  
  // Calculate dynamic validation hash based on entity properties
  const dynamicHash = useMemo(() => {
    const str = `${entityName}-${entityType}-${contextualEvidence}`;
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      hash = (hash << 5) - hash + str.charCodeAt(i);
      hash = hash & hash;
    }
    const hex = Math.abs(hash).toString(16).padStart(8, '0');
    return `${hex}f3d4e7b99c43d2110ea09848fac30f3c2b189b8823dfc7c66432fa88390b${hex.slice(0, 2)}`;
  }, [entityName, entityType, contextualEvidence]);

  // Auditor stamps
  const [reviewedBy, setReviewedBy] = useState('');
  const [reviewedAt, setReviewedAt] = useState('');

  // Actions
  const handleCommit = () => {
    if (status !== 'AWAITING') return;
    if (editingField) commitField(editingField);
    setStatus('COMMITTED');
    setReviewedBy('Rodrigo W. (Protocol Level 4)');
    setReviewedAt(new Date().toISOString().replace('T', ' ').slice(0, 19) + ' UTC');
  };

  const handleReject = () => {
    if (status !== 'AWAITING') return;
    setEditingField(null);
    setStatus('REJECTED');
    setReviewedBy('Rodrigo W. (Protocol Level 4)');
    setReviewedAt(new Date().toISOString().replace('T', ' ').slice(0, 19) + ' UTC');
  };

  // Dynamic scaling and boundaries for Bottom Chat Bar
  const textDensity = useMemo(() => {
    const lineCount = chatInput.split('\n').length;
    if (chatInput.length > 240 || lineCount >= 3) {
      return 'long';
    } else if (chatInput.length > 80) {
      return 'medium';
    }
    return 'short';
  }, [chatInput]);

  const chatBarRadiusClass = useMemo(() => {
    if (textDensity === 'long') return 'rounded-[20px]';
    if (textDensity === 'medium') return 'rounded-[28px]';
    return 'rounded-[999px]';
  }, [textDensity]);

  const inputStyle = useMemo(() => {
    if (textDensity === 'long') {
      return {
        fontSize: 'clamp(13px, 1.8vw, 16px)',
        lineHeight: '1.42',
      };
    } else if (textDensity === 'medium') {
      return {
        fontSize: 'clamp(14px, 2vw, 18px)',
        lineHeight: '1.38',
      };
    } else {
      return {
        fontSize: 'clamp(15px, 2.2vw, 20px)',
        lineHeight: '1.35',
      };
    }
  }, [textDensity]);

  const textareaRef = React.useRef<HTMLTextAreaElement>(null);
  const chatBarRef = React.useRef<HTMLDivElement>(null);
  const [chatBarHeight, setChatBarHeight] = useState(88);

  React.useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      const newHeight = Math.min(textareaRef.current.scrollHeight, window.innerHeight * 0.35);
      textareaRef.current.style.height = `${newHeight}px`;
    }
  }, [chatInput]);

  React.useEffect(() => {
    const handleResize = () => {
      if (chatBarRef.current) {
        setChatBarHeight(chatBarRef.current.offsetHeight);
      }
    };
    window.addEventListener('resize', handleResize);
    handleResize(); // Initial measurement
    return () => window.removeEventListener('resize', handleResize);
  }, [chatInput]);

  return (
    <div 
      className="min-h-dvh text-ag-text antialiased flex overflow-hidden ag-background relative w-full h-screen font-ag-display"
    >
      {/* Background Volumetric Field (Ambient Drift, CSS-Only) */}
      <div className="absolute inset-0 z-0 overflow-hidden pointer-events-none">
        <div className="absolute top-[10%] right-[15%] w-[600px] h-[600px] bg-slate-200/20 rounded-full blur-[150px] bg-volumetric-1"></div>
        <div className="absolute bottom-[15%] left-[20%] w-[500px] h-[500px] bg-amber-100/10 rounded-full blur-[120px] bg-volumetric-2"></div>
      </div>

      {/* Mobile Sidebar Toggle Button */}
      <button 
        onClick={() => setIsSidebarOpen(!isSidebarOpen)}
        className="md:hidden fixed top-5 left-5 z-50 w-10 h-10 rounded-full bg-white/80 backdrop-blur border border-ag-outline flex items-center justify-center shadow-sm"
      >
        <span className="material-symbols-outlined text-[20px] text-ag-text">
          {isSidebarOpen ? 'close' : 'menu'}
        </span>
      </button>

      {/* Backdrop overlay for mobile sidebar */}
      {isSidebarOpen && (
        <div 
          className="md:hidden fixed inset-0 bg-black/10 backdrop-blur-xs z-35"
          onClick={() => setIsSidebarOpen(false)}
        />
      )}

      {/* Left Action Rail (fixed, expansion by overlay, never pushes content, keyboard focus equivalent to hover) */}
      <nav className={`
        fixed top-0 bottom-0 left-0 h-screen z-40 flex flex-col py-8 px-4 overflow-hidden group transition-all duration-300 ease-in-out
        bg-white/80 backdrop-blur-md border-r border-ag-outline
        ${isSidebarOpen ? 'translate-x-0 w-64' : '-translate-x-full md:translate-x-0 w-20 md:hover:w-64 md:focus-within:w-64'}
      `}>
        {/* User Profile */}
        <div className="flex items-center gap-3 mb-8 px-2 shrink-0">
          <div className="w-10 h-10 rounded-full border border-ag-outline bg-slate-100 flex items-center justify-center font-bold text-ag-text shrink-0">
            RC
          </div>
          <div className={`whitespace-nowrap transition-opacity duration-200 ${isSidebarOpen ? 'opacity-100' : 'opacity-0 group-hover:opacity-100 group-focus-within:opacity-100'}`}>
            <div className="font-semibold text-sm text-ag-text">Rodrigo W.</div>
            <div className="text-[10px] text-ag-text-muted font-bold uppercase tracking-wider font-ag-code">Level 4</div>
          </div>
        </div>
        
        {/* Navigation Items */}
        <div className="flex-1 flex flex-col gap-1 w-full">
          {[
            { to: '/lex', icon: 'psychology', label: 'Intelligence' },
            { to: '/governance', icon: 'verified_user', label: 'Governance', active: true },
            { to: '/crm', icon: 'smart_toy', label: 'Agents' },
            { to: '/arsenal', icon: 'layers', label: 'Arsenal' },
            { to: '/', icon: 'home', label: 'Sovereign Portal' }
          ].map((item) => (
            <Link
              key={item.label}
              className={`flex items-center gap-4 px-3 py-2.5 rounded-md transition-all text-ag-text-muted hover:bg-ag-grey-10
                ${item.active ? 'bg-ag-grey-20 text-ag-text font-semibold' : 'font-medium'}
              `}
              to={item.to}
              onClick={() => setIsSidebarOpen(false)}
            >
              <span className="material-symbols-outlined text-[20px] shrink-0" style={item.active ? { fontVariationSettings: "'FILL' 1" } : undefined}>
                {item.icon}
              </span>
              <span className={`text-xs tracking-wide whitespace-nowrap pt-0.5 transition-opacity duration-200 ${isSidebarOpen ? 'opacity-100' : 'opacity-0 group-hover:opacity-100 group-focus-within:opacity-100'}`}>
                {item.label}
              </span>
            </Link>
          ))}
        </div>

        {/* Sidebar Footer node status */}
        <div className="mt-auto border-t border-ag-outline pt-4 flex flex-col gap-1 shrink-0 w-full">
          <div className="flex items-center gap-3 px-3 py-2 text-xs font-ag-code text-ag-text-muted">
            <span className="w-2 h-2 rounded-full bg-emerald-500 shrink-0"></span>
            <span className={`transition-opacity duration-200 ${isSidebarOpen ? 'opacity-100' : 'opacity-0 group-hover:opacity-100 group-focus-within:opacity-100'} whitespace-nowrap`}>
              SLM Node: Local
            </span>
          </div>
        </div>
      </nav>

      {/* Main Grid Canvas (with dynamic bottom padding and offset sidebar clearance) */}
      <main 
        className="flex-1 pl-0 md:pl-20 relative z-20 flex flex-col h-screen overflow-y-auto px-[72px] pt-[120px]"
        style={{ paddingBottom: `calc(${chatBarHeight}px + env(safe-area-inset-bottom))` }}
      >
        
        {/* Monospace Path Tracker */}
        <div className="text-[10px] font-ag-code tracking-[0.3em] text-ag-text-muted/40 uppercase mb-ag-xl">
          WRITE INTENT
        </div>

        {/* Asymmetric 12-Column Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-(--ag-space-xl) lg:gap-(--ag-space-2xl) max-w-[1400px] w-full mx-auto my-auto py-(--ag-space-lg) animate-reveal-up">
          
          {/* Left Column: Human Narrative Dominates (Span 7) */}
          <section className="lg:col-span-7 flex flex-col justify-center space-y-(--ag-space-lg) lg:space-y-(--ag-space-xl) lg:pr-6 pr-4">
            
            {/* Context/Path Header */}
            <div className="space-y-4">
              <span className="text-ag-text-muted/30 block font-ag-code text-[9px] uppercase tracking-[0.3em]">
                REF // OS-CRM-TWENTY-CONTROLLED-WRITE-BOUNDARY-APPROVAL-RECORDS-20260529-009
              </span>
              <h1 
                className={`font-ag-display transition-all duration-700 ${
                  status === 'COMMITTED'
                    ? 'text-ag-text'
                    : status === 'REJECTED'
                    ? 'text-ag-text-muted/40'
                    : 'text-ag-text italic'
                }`}
                style={{
                  fontSize: "clamp(72px, 7.4vw, 107px)",
                  lineHeight: "1.0",
                  letterSpacing: "-0.02em",
                  fontWeight: status === 'COMMITTED' ? 600 : status === 'REJECTED' ? 300 : 450,
                  fontVariationSettings: status === 'COMMITTED'
                    ? '"wdth" 100, "opsz" 144'
                    : status === 'REJECTED'
                    ? '"wdth" 85, "opsz" 144'
                    : '"wdth" 100, "opsz" 144',
                }}
              >
                {status === 'REJECTED' ? (
                  <>
                    <span className="line-through decoration-red-400/60 decoration-2">Create</span>{' '}
                    <span className="line-through decoration-red-400/60 decoration-2">{entityType}</span>{' for '}
                    <span className="line-through decoration-red-400/60 decoration-2">{entityName}</span>
                  </>
                ) : status === 'COMMITTED' ? (
                  <>
                    Create {entityType} for{' '}
                    <span
                      style={{
                        textDecoration: 'underline',
                        textDecorationColor: 'rgba(197,160,89,0.45)',
                        textUnderlineOffset: '6px',
                        textDecorationThickness: '2px',
                      }}
                    >
                      {entityName}
                    </span>
                  </>
                ) : (
                  <>Create {entityType} for {entityName}</>
                )}
              </h1>
            </div>

            {/* Clean Narrative Statements (No boxes, space-driven structure) */}
            <div className="flex flex-col space-y-4 py-(--ag-space-md) my-(--ag-space-sm) text-2xl font-light text-ag-text font-ag-display leading-relaxed">
              <p className="opacity-90">Requested from corporate email</p>
              <p className="opacity-90">Validated against governance rules</p>
              <p className="opacity-90 flex items-center gap-3">
                {status === 'AWAITING' ? (
                  <>
                    <span className="w-2.5 h-2.5 rounded-full bg-amber-500 shrink-0 animate-pulse"></span>
                    Awaiting human confirmation
                  </>
                ) : status === 'COMMITTED' ? (
                  <>
                    <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 shrink-0"></span>
                    Committed by reviewer
                  </>
                ) : (
                  <>
                    <span className="w-2.5 h-2.5 rounded-full bg-red-500 shrink-0"></span>
                    Rejected by reviewer
                  </>
                )}
              </p>
            </div>

            {/* Contextual Evidence (Large Editorial Typography) — click to edit */}
            <div className="space-y-4 pt-6">
              <span className="text-ag-text-muted/30 block font-ag-code text-[10px] uppercase tracking-[0.3em]">CONTEXTUAL EVIDENCE</span>
              
              {editingField === 'evidence' ? (
                <textarea
                  rows={4}
                  autoFocus
                  className="w-full p-5 bg-white/50 border border-aureate/40 rounded-[20px] text-lg font-ag-display focus:outline-none focus:ring-1 focus:ring-aureate focus:border-aureate leading-relaxed text-ag-text transition-all resize-none"
                  value={draftEvidence}
                  onChange={(e) => setDraftEvidence(e.target.value)}
                  onBlur={() => commitField('evidence')}
                  onKeyDown={(e) => { if (e.key === 'Escape') setEditingField(null); }}
                />
              ) : (
                <div
                  className={`group relative border-l border-aureate/20 pl-8 py-2 transition-all ${status === 'AWAITING' ? 'cursor-text hover:border-aureate/40' : ''}`}
                  onClick={() => startEditing('evidence')}
                  title={status === 'AWAITING' ? 'Clique para editar' : undefined}
                >
                  <p className="text-2xl md:text-3xl text-ag-text font-ag-display font-light italic leading-relaxed">
                    "{draftEvidence.startsWith('...') ? '' : '...'}{contextualEvidence.slice(0, 120)}{contextualEvidence.length > 120 ? '...' : ''}"
                  </p>
                  {status === 'AWAITING' && (
                    <span className="material-symbols-outlined absolute top-2 right-0 text-[14px] text-aureate/50 opacity-0 group-hover:opacity-100 transition-opacity">
                      edit
                    </span>
                  )}
                </div>
              )}
            </div>
          </section>

          {/* Right Column: Data Mirror — always JSON, per-field inline editing (Span 5) */}
          <section className="lg:col-span-5 flex flex-col justify-center">
            
            <div className="flex flex-col relative overflow-hidden p-0">
              
              {/* JSON Mirror Label */}
              <div className="mb-4 flex items-center gap-3">
                <span className="font-ag-code text-[10px] text-ag-text-muted/30 uppercase tracking-[0.3em]">JSON Mirror</span>
                {status === 'AWAITING' && (
                  <span className="font-ag-code text-[9px] text-ag-blue/50 uppercase tracking-[0.2em]">
                    — clique nos campos para editar
                  </span>
                )}
              </div>

              {/* JSON Mirror: always rendered, fields become inputs inline on click */}
              <div className="rounded-[28px] bg-[rgba(248,249,252,0.72)] border border-black/4 font-ag-code p-(--ag-space-md) mb-(--ag-space-md) overflow-hidden">
                <pre className="font-ag-code text-[11px] leading-loose text-[#121317] whitespace-pre-wrap">
                  <code>
                    {`{\n`}
                    {`  `}<span className="text-[#121317]/65">"entity"</span>{': '}
                    <span className="text-[#121317]/40">"Organization"</span>,
                    {`\n  `}<span className="text-[#121317]/65">"payload"</span>{': {\n'}
                    {`    `}<span className="text-[#121317]/65">"name"</span>{': '}
                  </code>
                </pre>
                {/* Inline field: payload.name */}
                {editingField === 'entityName' ? (
                  <input
                    autoFocus
                    type="text"
                    value={draftEntityName}
                    onChange={(e) => setDraftEntityName(e.target.value)}
                    onBlur={() => commitField('entityName')}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter') commitField('entityName');
                      if (e.key === 'Escape') setEditingField(null);
                    }}
                    className="inline-block font-ag-code text-[11px] text-ag-blue font-semibold bg-ag-blue/5 border border-ag-blue/25 rounded-[6px] px-2 py-0.5 focus:outline-none focus:ring-1 focus:ring-ag-blue/40 w-auto min-w-[120px] transition-all"
                    style={{ width: `${Math.max(draftEntityName.length * 7, 120)}px` }}
                  />
                ) : (
                  <span
                    className={`inline font-ag-code text-[11px] text-ag-blue font-semibold rounded-[4px] px-1 py-0.5 transition-all ${
                      status === 'AWAITING' ? 'hover:bg-ag-blue/8 cursor-text' : ''
                    }`}
                    onClick={() => startEditing('entityName')}
                    title={status === 'AWAITING' ? 'Clique para editar' : undefined}
                  >
                    "{entityName}"
                  </span>
                )}
                <pre className="font-ag-code text-[11px] leading-loose text-[#121317] whitespace-pre-wrap inline">{`,\n`}</pre>
                <pre className="font-ag-code text-[11px] leading-loose text-[#121317] whitespace-pre-wrap">
                  <code>
                    {`    `}<span className="text-[#121317]/65">"type"</span>{': '}
                  </code>
                </pre>
                {/* Inline field: payload.type */}
                {editingField === 'entityType' ? (
                  <input
                    autoFocus
                    type="text"
                    value={draftEntityType}
                    onChange={(e) => setDraftEntityType(e.target.value)}
                    onBlur={() => commitField('entityType')}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter') commitField('entityType');
                      if (e.key === 'Escape') setEditingField(null);
                    }}
                    className="inline-block font-ag-code text-[11px] text-ag-blue font-semibold bg-ag-blue/5 border border-ag-blue/25 rounded-[6px] px-2 py-0.5 focus:outline-none focus:ring-1 focus:ring-ag-blue/40 w-auto min-w-[100px] transition-all"
                    style={{ width: `${Math.max(draftEntityType.length * 7, 100)}px` }}
                  />
                ) : (
                  <span
                    className={`inline font-ag-code text-[11px] text-ag-blue font-semibold rounded-[4px] px-1 py-0.5 transition-all ${
                      status === 'AWAITING' ? 'hover:bg-ag-blue/8 cursor-text' : ''
                    }`}
                    onClick={() => startEditing('entityType')}
                    title={status === 'AWAITING' ? 'Clique para editar' : undefined}
                  >
                    "{entityType}"
                  </span>
                )}
                <pre className="font-ag-code text-[11px] leading-loose text-[#121317] whitespace-pre-wrap">
                  <code>
                    {`,\n    `}<span className="text-[#121317]/65">"hash_validation"</span>{': '}
                    <span className="text-ag-text-muted/60">"{dynamicHash.slice(0, 10)}..."</span>
                    {`\n  }\n}`}
                  </code>
                </pre>
              </div>

              {/* Status overlay — Locked Signal (shown after COMMIT or REJECT) */}
              {status !== 'AWAITING' && (
                <div 
                  className={`flex flex-col gap-4 mb-6 pl-5 transition-all duration-700 ${
                    status === 'COMMITTED'
                      ? 'border-l-2 border-emerald-500/50'
                      : 'border-l-2 border-red-400/50'
                  }`}
                >
                  <div className={`flex items-center gap-2.5 font-ag-code text-[9px] font-bold uppercase tracking-[0.3em] ${
                    status === 'COMMITTED' ? 'text-emerald-600' : 'text-red-500'
                  }`}>
                    <span className="material-symbols-outlined text-[18px]" style={{ fontVariationSettings: "'FILL' 1" }}>
                      {status === 'COMMITTED' ? 'lock' : 'block'}
                    </span>
                    {status === 'COMMITTED' ? 'Contrato assinado e congelado' : 'Intenção rejeitada'}
                  </div>

                  <div className="space-y-1 font-ag-code text-[10px] text-ag-text-muted">
                    <div>
                      <span className="opacity-50 uppercase tracking-widest text-[9px]">Reviewed by &nbsp;</span>
                      <span className="text-ag-text font-medium">{reviewedBy}</span>
                    </div>
                    <div>
                      <span className="opacity-50 uppercase tracking-widest text-[9px]">Timestamp &nbsp;</span>
                      <span className="font-ag-code text-[10px] text-ag-text">{reviewedAt}</span>
                    </div>
                    <div className="pt-1 opacity-40 break-all text-[9px] tracking-wider">
                      {dynamicHash}
                    </div>
                  </div>
                </div>
              )}

              {/* Action Buttons Panel — always visible, no edit mode toggle */}
              <div className="mt-12 flex flex-col gap-3">
                <div className="flex gap-3">
                  {/* Reject button */}
                  <button 
                    onClick={handleReject}
                    disabled={status !== 'AWAITING'}
                    className={`flex-1 py-3 rounded-full text-xs font-semibold tracking-wider uppercase transition-all flex items-center justify-center gap-1.5 border
                      ${status === 'AWAITING' 
                        ? 'border-red-500/20 text-red-600 bg-red-50/50 hover:bg-red-100/50 cursor-pointer' 
                        : 'border-black/4 text-ag-text-muted/20 bg-transparent cursor-not-allowed'
                      }
                    `}
                  >
                    <span className="material-symbols-outlined text-[15px]">close</span>
                    Rejeitar
                  </button>
                </div>

                {/* Commit button */}
                <button 
                  onClick={handleCommit}
                  disabled={status !== 'AWAITING'}
                  className={`w-full ag-button-primary text-xs font-bold tracking-widest uppercase flex items-center justify-center gap-2 transition-all
                    ${status === 'AWAITING'
                      ? 'bg-[#121317] text-white hover:bg-ag-blue cursor-pointer'
                      : 'bg-black/4 text-ag-text-muted/20 cursor-not-allowed shadow-none'
                    }
                  `}
                >
                  <span className="material-symbols-outlined text-[16px]">done_all</span>
                  Commit Controlled
                </button>
              </div>

            </div>
          </section>

        </div>
      </main>

      {/* Conversational Bottom Chat Bar */}
      <div 
        ref={chatBarRef}
        className="fixed bottom-0 left-0 md:left-20 right-0 p-6 bg-linear-to-t from-[#FAFAF9] via-[#FAFAF9]/95 to-[#FAFAF9]/0 z-30 flex justify-center"
      >
        <div className="max-w-[1000px] w-full relative">
          <div 
            className={`ag-surface ag-floating flex items-end gap-4 px-6 py-4 transition-all duration-300 min-h-ag-xl ${chatBarRadiusClass}`}
          >
            <span className="material-symbols-outlined text-ag-blue shrink-0 animate-pulse mb-2.5">
              lens_blur
            </span>
            <textarea
              ref={textareaRef}
              rows={1}
              placeholder="Digite uma instrução ou comando..."
              value={chatInput}
              onChange={(e) => setChatInput(e.target.value)}
              className="flex-1 bg-transparent border-none outline-none text-ag-text placeholder-ag-text-muted/35 font-sans font-normal resize-none overflow-y-auto mb-1.5 focus:ring-0 focus:outline-none"
              style={{
                ...inputStyle,
                maxHeight: '30vh',
              }}
            />
            <button className="w-10 h-10 rounded-full bg-ag-text hover:bg-ag-blue text-white flex items-center justify-center transition-colors shrink-0 cursor-pointer mb-1">
              <span className="material-symbols-outlined text-[20px]">
                arrow_upward
              </span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
