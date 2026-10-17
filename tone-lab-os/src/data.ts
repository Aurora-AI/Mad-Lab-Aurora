export const toneLabData = [
  {
    id: "amp-sig-01",
    name: "Signature Proto01",
    category: "Amplifiers",
    subCategory: "Heads",
    status: "Planned",
    priority: "P1",
    image: "/jtm.jpg",
    dossier: {
      refId: "M-SIG-001",
      subtitle: "Plataforma valvulada modular de baixa potência",
      description: "O Protótipo 01 é um amplificador valvulado concebido como plataforma de P&D para criação de timbres autorais, adotando a filosofia behavior-first.",
      role: "Plataforma de bancada para testar Pre-Shape, Gain Structure e Power Management sem os níveis de SPL de um head de 100W.",
      specs: [
        { parameter: "Baseline Técnico", value: "JCM800 Micro (EF80 push-pull)", source: "V1.1 Spec", status: "VERIFIED" },
        { parameter: "Potência", value: "Baixa (Uso de Estúdio)", source: "V1.1 Spec", status: "VERIFIED" },
        { parameter: "Construção", value: "Turret/Eyelet board", source: "Design Rule", status: "VERIFIED" },
        { parameter: "Chassis", value: "Head 50/100W (Superdimensionado)", source: "Design Rule", status: "VERIFIED" },
        { parameter: "Modo de Saída", value: "Power Management (FULL / STUDIO / NIGHT)", source: "R&D", status: "PENDING" }
      ],
      signalChain: [
        { stage: "01 / Source", label: "Guitar", desc: "Passive Hi-Z", image: "https://images.unsplash.com/photo-1564186763535-ebb21ef5277f?q=80&w=200&auto=format&fit=crop", isActive: false },
        { stage: "02 / Pre-Shape", label: "Ampero", desc: "Line Buffer / Modeler", image: "/ampero.jpg", isActive: false },
        { stage: "03 / Device", label: "Signature Proto01", desc: "Head Unit Under Test", image: "/jtm.jpg", isActive: true },
        { stage: "04 / Transducer", label: "1x12 Cab", desc: "Celestion G12M Greenback", image: "https://images.unsplash.com/photo-1623910271000-410a5eb578a0?q=80&w=200&auto=format&fit=crop", isActive: false }
      ]
    }
  },
  {
    id: "amp-origin-50c",
    name: "Marshall Origin 50C",
    category: "Amplifiers",
    subCategory: "Combos",
    status: "Owned",
    priority: "P1",
    image: "/origin.jpg",
    dossier: {
      refId: "M-ORIG-50C-8824",
      subtitle: "50-Watt Valve Combo • Celestion Midnight 60",
      description: "Pure vintage-voiced all-valve combo engineered for harmonic transparency and natural power-tube saturation.",
      role: "Maintained as the calibrated analog benchmark for testing high-gain front-end stages, dynamic clean headroom thresholds, and reactive load impulse response profiling.",
      specs: [
        { parameter: "Power Output", value: "50W (High) / 10W (Mid) / 5W (Low) Powerstem", source: "Marshall Official Spec", status: "VERIFIED" },
        { parameter: "Speaker Driver", value: "1×12″ Celestion G12N-60 Midnight 60 (16Ω)", source: "Marshall Official Spec", status: "VERIFIED" },
        { parameter: "Preamp Valves", value: "3× ECC83 (12AX7)", source: "Bench Inspection", status: "VERIFIED" },
        { parameter: "Power Amp Valves", value: "2× EL34 Matched Pair", source: "Bench Inspection", status: "VERIFIED" }
      ],
      signalChain: [
        { stage: "01 / Source", label: "Guitar", desc: "Passive Hi-Z / Single Coil", image: "https://images.unsplash.com/photo-1564186763535-ebb21ef5277f?q=80&w=200&auto=format&fit=crop", isActive: false },
        { stage: "02 / Front-End", label: "Pedals", desc: "True-Bypass Analog Rig", image: "https://images.unsplash.com/photo-1552399222-b4c6e93eb774?q=80&w=200&auto=format&fit=crop", isActive: false },
        { stage: "03 / Pre-Process", label: "Ampero", desc: "Line Buffer / Aux Modeler", image: "/ampero.jpg", isActive: false },
        { stage: "04 / Device", label: "Marshall Origin 50C", desc: "50W Valve Section (EL34)", image: "/origin.jpg", isActive: true },
        { stage: "05 / Transducer", label: "Cabinet", desc: "1×12 Celestion G12N-60", image: "https://images.unsplash.com/photo-1623910271000-410a5eb578a0?q=80&w=200&auto=format&fit=crop", isActive: false },
        { stage: "06 / Capture", label: "Mic Array", desc: "SM57 + Royer R121 Pair", image: "https://images.unsplash.com/photo-1598508962294-f2fec17ea18b?q=80&w=200&auto=format&fit=crop", isActive: false }
      ]
    }
  },
  {
    id: "pedal-ampero",
    name: "Ampero II Stomp",
    category: "Digital",
    subCategory: "Modeler",
    status: "Owned",
    priority: "P1",
    image: "/ampero.jpg",
    dossier: {
      refId: "H-AMP-II",
      subtitle: "Amp Modeler & Effects Processor",
      description: "DSP unit for hybrid routing, line buffering, and digital FX testing.",
      role: "Used as Pre-Shape testing platform, FX Return tests, and direct recording.",
      specs: [
        { parameter: "DSP", value: "Tri-core DSP", source: "Hotone", status: "VERIFIED" },
        { parameter: "I/O", value: "Stereo IN/OUT + FX Loop", source: "Hotone", status: "VERIFIED" }
      ],
      signalChain: [
        { stage: "01 / Source", label: "Guitar", desc: "Passive Hi-Z", image: "https://images.unsplash.com/photo-1564186763535-ebb21ef5277f?q=80&w=200&auto=format&fit=crop", isActive: false },
        { stage: "02 / Device", label: "Ampero II Stomp", desc: "Digital Modeler Under Test", image: "/ampero.jpg", isActive: true },
        { stage: "03 / Interface", label: "Scarlett 18i20", desc: "Audio Interface", image: "https://images.unsplash.com/photo-1598488035139-bdbb2231ce04?q=80&w=200&auto=format&fit=crop", isActive: false },
        { stage: "04 / Output", label: "DAW", desc: "Studio One", image: "https://images.unsplash.com/photo-1618609378039-b572a500bc9b?q=80&w=200&auto=format&fit=crop", isActive: false }
      ]
    }
  },
  {
    id: "amp-princeton-6g2",
    name: "Fender Princeton 6G2",
    category: "Amplifiers",
    subCategory: "Combos",
    status: "Research",
    priority: "P2",
    image: "/origin.jpg", // placeholder
    dossier: {
      refId: "F-6G2-PROTO",
      subtitle: "Brownface Circuit (1961–1964) • 12W RMS",
      description: "Replicação Artesanal de Bancada. O 6G2 é o elo acústico entre a compressão da era Tweed e a definição dos circuitos Blackface.",
      role: "Estudo de viés fixo não ajustável e tremolo valvulado modulador de bias.",
      specs: [
        { parameter: "Topologia", value: "Classe AB push-pull (Fixed Bias)", source: "Dossiê Técnico Executivo", status: "VERIFIED" },
        { parameter: "Preamp", value: "Ganho único (12AX7/7025)", source: "Dossiê Técnico Executivo", status: "VERIFIED" },
        { parameter: "Power Amp", value: "Par de 6V6GT (~12W RMS)", source: "Dossiê Técnico Executivo", status: "VERIFIED" },
        { parameter: "Tremolo", value: "Bias-wiggle tremolo", source: "Dossiê Técnico Executivo", status: "VERIFIED" }
      ],
      signalChain: [
        { stage: "01 / Source", label: "Guitar", desc: "Stratocaster Single Coil", image: "https://images.unsplash.com/photo-1564186763535-ebb21ef5277f?q=80&w=200&auto=format&fit=crop", isActive: false },
        { stage: "02 / Device", label: "Princeton 6G2", desc: "Combo under replication", image: "/origin.jpg", isActive: true },
        { stage: "03 / Capture", label: "SM57", desc: "Close Mic", image: "https://images.unsplash.com/photo-1598508962294-f2fec17ea18b?q=80&w=200&auto=format&fit=crop", isActive: false }
      ]
    }
  }
];
