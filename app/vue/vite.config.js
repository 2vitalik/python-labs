import { fileURLToPath } from 'node:url'

import vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vite'

const core = fileURLToPath(new URL('../../core/ui', import.meta.url))  // the platform: source files, no package of its own

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: { '@core': core },
    dedupe: ['bootstrap', 'marked', 'vue', 'vue-router'],  // what core imports comes from this site's node_modules
  },
  server: {
    host: '127.0.0.1', // not `localhost`: Node binds it to ::1 only, and Telegram won't link localhost URLs
    port: 5030, // project #3 in the cross-project port scheme (dev-md-rules/DEV.md)
    strictPort: true,
    fs: { allow: ['.', core] },
    proxy: {
      // keep Host = localhost:5030 so the OAuth redirect_uri matches GCP
      '/api': { target: 'http://127.0.0.1:8030', changeOrigin: false },
    },
  },
})
