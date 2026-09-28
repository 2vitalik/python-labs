import { ref } from 'vue'

import { load, save } from './local.js'

// light or dark page; the first value comes from public/theme-boot.js: the choice saved in this browser, else the system's
const KEY = 'theme'
const root = document.documentElement
export const dark = ref(root.dataset.bsTheme === 'dark')

function set(on) {
  dark.value = on
  root.dataset.bsTheme = on ? 'dark' : 'light'
}
export function toggleTheme() {
  set(!dark.value)
  save(KEY, root.dataset.bsTheme)
}
// nothing chosen here yet — the page keeps following the system (night mode on a schedule)
matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => load(KEY) || set(e.matches))
