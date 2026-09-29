import 'bootstrap/dist/css/bootstrap.min.css'

import './style.css'
import './dark.css'

import { createApp } from 'vue'

import App from './App.vue'
import { report } from './problem.js'
import { site } from './site.js'

// `about` — the site's own site.js, `router` — makeRouter() over its routes
export function start(about, router) {
  Object.assign(site, about)
  const app = createApp(App)
  app.config.errorHandler = report
  window.addEventListener('error', (e) => e.error && report(e.error))  // no `error` — not our code: a browser notice, a foreign script
  window.addEventListener('unhandledrejection', (e) => report(e.reason))
  app.use(router).mount('#app')
}
