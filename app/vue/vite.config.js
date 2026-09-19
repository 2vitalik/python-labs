import vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '127.0.0.1', // not `localhost`: Node binds it to ::1 only, and Telegram won't link localhost URLs
    port: 5030, // project #3 in the cross-project port scheme (dev-md-rules/DEV.md)
    strictPort: true,
    proxy: {
      // keep Host = localhost:5030 so the OAuth redirect_uri matches GCP
      '/api': { target: 'http://127.0.0.1:8030', changeOrigin: false },
    },
  },
})
