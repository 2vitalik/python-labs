import { ref } from 'vue'

import { postError } from './api.js'

// what went wrong on the open page: 'lost' — the 404 page takes its place, 'broken' — the «Щось пішло не так» block
// goes above it (the page stays: a form keeps what was typed); the router clears it on the way to the next page
export const problem = ref('')

const MAX = 5  // reports per page load: a broken row of a list fails once per row
const told = new Set()

// every error nobody caught: Vue's errorHandler, window `error` and `unhandledrejection` (main.js)
export function report(e, vm, info) {
  console.error(e)
  if (e?.status === 0 || e?.status === 401) return  // the banner is up · on the way to /login
  problem.value = e?.status === 404 ? 'lost' : 'broken'
  if (e?.status) return  // the API answered: its own failures it reports itself
  const message = (e instanceof Error ? `${e.name}: ${e.message}` : String(e)).slice(0, 300)
  if (told.has(message) || told.size >= MAX) return
  told.add(message)
  const where = [vm?.$options.__name, info].filter(Boolean).join(' · ')
  postError({ message, stack: e?.stack || '', path: location.pathname + location.search, where }).catch(() => {})
}
