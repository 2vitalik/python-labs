import vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      // keep Host = localhost:5173 so the OAuth redirect_uri matches GCP
      '/api': { target: 'http://127.0.0.1:8000', changeOrigin: false },
    },
  },
})
