import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
export default defineConfig({
  base: '/panel/',
  plugins: [react()],
  server: { port: 5176, host: '127.0.0.1', proxy: { '/api': { target: 'http://localhost:8091', rewrite: (p) => p.replace(/^\/api/, '') } } },
})
