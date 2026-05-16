import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],
  server: {
    port: 5173,       // Fuerza a Vite a usar siempre el puerto 5173
    strictPort: true, // Si el 5173 está ocupado por un proceso colgado, da un error en vez de saltar al 5174
  },
})