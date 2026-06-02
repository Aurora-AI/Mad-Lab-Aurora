import { useEffect } from 'react';
import { useLenis } from 'lenis/react';
import { useScrollProgress } from '../hooks/useScrollProgress';

// Mounts the global scroll → color interpolation.
// Exposes the Lenis instance to window.__lenis for synchronization with native components.
export default function ScrollDriver() {
  const lenis = useLenis();

  useEffect(() => {
    if (lenis) {
      (window as any).__lenis = lenis;
    }
    return () => {
      delete (window as any).__lenis;
    };
  }, [lenis]);

  useScrollProgress();
  return null;
}
