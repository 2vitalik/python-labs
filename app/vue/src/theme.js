import { ref } from 'vue'

import { load, save } from './local.js'

// page theme: `auto` follows the device, `light` / `dark` are a choice; remembered in this browser.
// The first paint is public/theme-boot.js's, with the same rule
const KEY = 'theme'
const device = matchMedia('(prefers-color-scheme: dark)')
export const MODES = { light: 'Світла', dark: 'Темна', auto: 'Як на пристрої' }
export const mode = ref(load(KEY) in MODES ? load(KEY) : 'auto')

function apply() {
  const dark = mode.value === 'auto' ? device.matches : mode.value === 'dark'
  document.documentElement.dataset.bsTheme = dark ? 'dark' : 'light'
}
export function setMode(m) {
  mode.value = m
  save(KEY, m)
  apply()
}
device.addEventListener('change', apply)  // night mode on a schedule: an `auto` page follows at once
