import { useEffect } from 'react';

/**
 * useTerminalGrid
 * 
 * Implements the 'Aino' math-grid pattern.
 * Dynamically calculates character width and viewport columns,
 * injecting them into the :root as CSS variables.
 */
export const useTerminalGrid = () => {
  useEffect(() => {
    const calculateGrid = () => {
      // Create a temporary element to measure character width precisely
      const measure = document.createElement('span');
      measure.innerText = '0';
      measure.style.fontFamily = 'monospace';
      measure.style.fontSize = '1rem';
      measure.style.visibility = 'hidden';
      measure.style.position = 'absolute';
      document.body.appendChild(measure);
      
      const charWidth = measure.getBoundingClientRect().width;
      const charHeight = measure.getBoundingClientRect().height;
      document.body.removeChild(measure);

      const viewportWidth = window.innerWidth;
      const columns = Math.floor(viewportWidth / charWidth);
      
      const root = document.documentElement;
      root.style.setProperty('--ch', `${charWidth}px`);
      root.style.setProperty('--cv', `${charHeight}px`);
      root.style.setProperty('--cols', `${columns}`);
      root.style.setProperty('--col-width', `${charWidth}px`);
      
      // Aino style 'gutter' or grid unit (e.g. 4 chars per 'logical' column)
      root.style.setProperty('--grid-unit', `${charWidth * 4}px`);
    };

    calculateGrid();
    window.addEventListener('resize', calculateGrid);
    return () => window.removeEventListener('resize', calculateGrid);
  }, []);
};
