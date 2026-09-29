import { fileURLToPath } from 'node:url'

import vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vite'

const core = fileURLToPath(new URL('../../../core/ui', import.meta.url))  // the platform: source files, no package of its own

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: { '@core': core },
    dedupe: ['bootstrap', 'marked', 'vue', 'vue-router'],  // what core imports comes from this site's node_modules
  },
  server: {
    host: '127.0.0.1', // not `localhost`: Node binds it to ::1 only, and Telegram won't link localhost URLs
    port: 5035, // project #3 (dev-md-rules/DEV.md), its spare slot 5 — the second site of the repo
    strictPort: true,
    fs: { allow: ['.', core] },
    proxy: {
      '/api': { target: 'http://127.0.0.1:8035', changeOrigin: false },
    },
  },
})
