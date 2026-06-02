import { useEffect } from 'react';

// power2.inOut — weighted toward center of scroll
function easeInOut(t: number): number {
  return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
}

function hexToRgb(hex: string): [number, number, number] {
  const r = parseInt(hex.slice(1, 3), 16);
  const g = parseInt(hex.slice(3, 5), 16);
  const b = parseInt(hex.slice(5, 7), 16);
  return [r, g, b];
}

function interpolateColor(from: string, to: string, t: number): string {
  const [r1, g1, b1] = hexToRgb(from);
  const [r2, g2, b2] = hexToRgb(to);
  const r = Math.round(r1 + (r2 - r1) * t);
  const g = Math.round(g1 + (g2 - g1) * t);
  const b = Math.round(b1 + (b2 - b1) * t);
  return `rgb(${r},${g},${b})`;
}

const BG_FROM   = '#000000';
const BG_TO     = '#f0ebe3';
const TEXT_FROM = '#ffffff';
const TEXT_TO   = '#111111';

export function useScrollProgress(): void {
  useEffect(() => {
    const root = document.documentElement;

    const update = () => {
      const scrollY  = window.scrollY;
      const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
      if (maxScroll <= 0) return;

      const raw    = Math.min(Math.max(scrollY / maxScroll, 0), 1);
      const eased  = easeInOut(raw);

      root.style.setProperty('--page-bg',   interpolateColor(BG_FROM,   BG_TO,   eased));
      root.style.setProperty('--page-text', interpolateColor(TEXT_FROM, TEXT_TO, eased));
    };

    window.addEventListener('scroll', update, { passive: true });
    update(); // init

    return () => window.removeEventListener('scroll', update);
  }, []);
}
