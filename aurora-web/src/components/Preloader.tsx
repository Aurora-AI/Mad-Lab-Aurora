import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence, useReducedMotion } from 'framer-motion';

const characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+";

const ScrambleText = ({ text, duration = 2 }: { text: string; duration?: number }) => {
  const [display, setDisplay] = useState(text);

  useEffect(() => {
    let iteration = 0;
    const interval = setInterval(() => {
      setDisplay(prev => 
        prev.split("").map((char, index) => {
          if (index < iteration) return text[index];
          return characters[Math.floor(Math.random() * characters.length)];
        }).join("")
      );

      if (iteration >= text.length) clearInterval(interval);
      iteration += 1/15;
    }, 30);

    return () => clearInterval(interval);
  }, [text]);

  return <span>{display}</span>;
}

export default function Preloader({ onComplete }: { onComplete: () => void }) {
  const shouldReduceMotion = useReducedMotion();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setLoading(false);
      setTimeout(() => {
        onComplete();
      }, 1200);
    }, 3000); // Reduced to 3s for better UX
    return () => {
      clearTimeout(timer);
    };
  }, [onComplete]);

  return (
    <AnimatePresence>
      {loading && (
        <motion.div
          key="preloader"
          initial={{ opacity: 1 }}
          exit={{ opacity: 0, scale: 1.02, filter: "blur(10px)" }}
          transition={{ duration: 0.8, ease: [0.76, 0, 0.24, 1] }}
          style={{
            position: 'fixed',
            inset: 0,
            zIndex: 9999,
            background: 'var(--page-bg)',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            pointerEvents: 'none',
          }}
        >
          {/* Subtle Progress Bar */}
          <div style={{ position: 'relative', overflow: 'hidden', width: '240px', height: '1px', background: 'rgba(26, 26, 23, 0.05)', marginBottom: '3rem' }}>
            <motion.div
              initial={{ x: "-100%" }}
              animate={{ x: "0%" }}
              transition={{ duration: shouldReduceMotion ? 0 : 2.8, ease: "easeInOut" }}
              style={{ position: 'absolute', inset: 0, background: 'var(--page-accent)' }}
            />
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1.5rem' }}>
            <motion.div
              initial={{ opacity: 0, y: shouldReduceMotion ? 0 : 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: shouldReduceMotion ? 0 : 0.2 }}
              style={{
                fontFamily: 'var(--font-display)',
                fontSize: '2.5rem',
                letterSpacing: '0.3em',
                color: 'var(--page-text)',
                textTransform: 'uppercase',
                fontWeight: 300,
                fontStyle: 'italic'
              }}
            >
              <ScrambleText text="AURORA" />
            </motion.div>
            
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 0.4 }}
              transition={{ delay: shouldReduceMotion ? 0 : 1.2 }}
              style={{
                fontFamily: 'var(--font-mono)',
                fontSize: '0.65rem',
                letterSpacing: '0.4em',
                color: 'var(--page-text)',
                textTransform: 'uppercase'
              }}
            >
              ESTABLISHING_DETERMINISTIC_PROTOCOL
            </motion.div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

