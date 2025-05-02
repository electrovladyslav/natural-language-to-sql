import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
    },
  },
  esbuild: {
    // Target older browsers for compatibility
    target: ['es2020', 'chrome67', 'firefox68', 'safari12', 'edge79'],
  }
}); 