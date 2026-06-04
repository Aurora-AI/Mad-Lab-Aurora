import tailwindcss from '@tailwindcss/vite';
import react from '@vitejs/plugin-react';
import path from 'path';
import {defineConfig} from 'vite';

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, '.'),
      '@aurora-visual': path.resolve(__dirname, '../aurora-visual-assets'),
    },
  },
  server: {
    fs: {
      allow: [
        path.resolve(__dirname, '.'),
        path.resolve(__dirname, '../aurora-visual-assets'),
      ],
    },
    host: '0.0.0.0',
    port: 3000,
    // Preserve the option to disable HMR in constrained environments.
    hmr: process.env.DISABLE_HMR !== 'true',
  },
});

