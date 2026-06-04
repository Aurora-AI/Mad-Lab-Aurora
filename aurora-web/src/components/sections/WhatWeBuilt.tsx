'use client';

import React from 'react';
import { ArrowRight } from 'lucide-react';
import { EthicalAnchor } from '../ui/EthicalAnchor';

const verticals = [
  {
    tag: 'Fábrica de Ativos',
    name: 'Mad Lab Aurora',
    status: 'Laboratório Interno',
    href: '/mad-lab',
    description: 'Onde a física digital encontra a precisão industrial. Nosso núcleo de P&D para ativos visuais S-Tier e algoritmos de soberania técnica.',
    features: ['Industrialização WebGL', 'Sistemas de Física Digital', 'Otimização de Hardware']
  },
  {
    tag: 'Estratégia Jurídica',
    name: 'Elysian Lex',
    status: 'Soberania Legal',
    href: '/lex',
    description: 'Motor de análise forense e proteção de PII. Onde o direito encontra o determinismo técnico para proteger sua reputação.',
    features: ['Proteção de PII nativa', 'Análise Forense de Contratos', 'Outputs Auditáveis']
  },
  {
    tag: 'Alta Alavancagem',
    name: 'CRM Aurora',
    status: 'Conversão Pura',
    href: '/crm',
    description: 'O sistema de operação comercial para quem não aceita perder receita por falta de clareza ou falha de processamento.',
    features: ['Governança de Pipeline', 'Automação Determinística', 'Rastreabilidade de Venda']
  }
];

export default function WhatWeBuilt() {
  return (
    <>
      <EthicalAnchor />
      
      <section
        id="sovereign-verticals"
        style={{
          padding: 'clamp(4rem, 10vw, 8rem) var(--px)',
          background: 'var(--page-bg)',
        }}
      >
        <div style={{ maxWidth: 'var(--max-width)', margin: '0 auto' }}>
          
          {/* Header Minimalista */}
          <div style={{ marginBottom: 'clamp(3rem, 6vw, 5rem)', maxWidth: '60ch' }}>
            <span style={{ 
              fontFamily: 'var(--font-mono)', 
              fontSize: '0.65rem', 
              letterSpacing: '0.25em', 
              color: 'var(--page-text-soft)', 
              opacity: 0.5,
              textTransform: 'uppercase',
              display: 'block',
              marginBottom: '1.5rem'
            }}>
              Verticals // 2026
            </span>
            <h2
              style={{
                fontFamily: 'var(--font-display)',
                fontStyle: 'italic',
                fontSize: 'clamp(2rem, 4vw, 3.5rem)',
                fontWeight: 500,
                lineHeight: 1.1,
                letterSpacing: '-0.02em',
                color: 'var(--page-text)',
              }}
            >
              Três pilares. 
              <br />
              <span style={{ color: 'var(--page-text-soft)', opacity: 0.3 }}>Uma única missão de clareza.</span>
            </h2>
          </div>

          {/* Grid de Cartas (Cubic-style) */}
          <div style={{ 
            display: 'grid', 
            gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', 
            gap: '1.5rem',
            perspective: '1000px'
          }}>
            {verticals.map((v, i) => (
              <div
                key={v.name}
                className="sovereign-card"
                style={{
                  background: 'rgba(255,255,255,0.4)',
                  backdropFilter: 'blur(10px)',
                  border: '1px solid var(--page-text)',
                  opacity: 0.05, /* Border opacity */
                  padding: '3rem',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '2rem',
                  transition: 'all 0.4s cubic-bezier(0.2, 1, 0.3, 1)',
                  borderRadius: '2px',
                  position: 'relative',
                  overflow: 'hidden',
                  cursor: 'pointer'
                }}
              >
                <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem', height: '100%', opacity: 1 /* Reset for content */ }}>
                {/* Visual Depth Elements */}
                <div style={{
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  width: '4px',
                  height: '100%',
                  background: i === 0 ? '#E6D5B8' : '#000', // Dourado para Mad Lab
                  opacity: 0.1
                }} />

                <div>
                  <div style={{ 
                    fontFamily: 'var(--font-mono, monospace)', 
                    fontSize: '0.55rem', 
                    color: '#999', 
                    letterSpacing: '0.2em', 
                    textTransform: 'uppercase',
                    marginBottom: '0.5rem'
                  }}>
                    {v.tag}
                  </div>
                  <h3 style={{
                    fontFamily: 'var(--font-body, system-ui)',
                    fontSize: '1.75rem',
                    fontWeight: 600,
                    color: '#111',
                    margin: 0
                  }}>
                    {v.name}
                  </h3>
                </div>

                <p style={{
                  fontFamily: 'var(--font-body, system-ui)',
                  fontSize: '0.95rem',
                  color: '#666',
                  lineHeight: 1.6,
                  margin: 0,
                  flex: 1
                }}>
                  {v.description}
                </p>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                  {v.features.map(f => (
                    <div key={f} style={{ 
                      display: 'flex', 
                      alignItems: 'center', 
                      gap: '0.75rem', 
                      fontFamily: 'var(--font-mono, monospace)',
                      fontSize: '0.7rem',
                      color: 'var(--page-text-soft)',
                      opacity: 0.7
                    }}>
                      <span style={{ width: 4, height: 4, background: 'var(--color-elysian-signal)', opacity: 0.5, borderRadius: '50%' }} />
                      {f}
                    </div>
                  ))}
                </div>

                  <a
                    href={v.href}
                    style={{
                      marginTop: '1rem',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '0.5rem',
                      fontFamily: 'var(--font-mono)',
                      fontSize: '0.75rem',
                      letterSpacing: '0.1em',
                      textTransform: 'uppercase',
                      color: 'var(--color-elysian-signal)',
                      textDecoration: 'none',
                      fontWeight: 700
                    }}
                  >
                    Explorar {v.status === 'Laboratório Interno' ? 'DNA' : 'Poder'}
                    <ArrowRight size={14} />
                  </a>
                </div>
              </div>
            ))}
          </div>
        </div>

        <style>{`
          .sovereign-card:hover {
            transform: translateY(-8px) rotateX(2deg);
            background: rgba(255,255,255,1);
            box-shadow: 0 40px 80px rgba(0,0,0,0.05);
            border-color: rgba(0,0,0,0.1);
          }
          .sovereign-card:hover h3 {
            color: #000;
          }
        `}</style>
      </section>
    </>
  );
}
