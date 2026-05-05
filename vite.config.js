import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// GH Pages serves at /constructor/ — keep relative for portability.
export default defineConfig({
  plugins: [react()],
  base: './',
  build: {
    outDir: 'dist',
    sourcemap: false,
    target: 'es2022',
  },
})
