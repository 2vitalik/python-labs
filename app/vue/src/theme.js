import { ref } from 'vue'

import { load, save } from './local.js'

// page theme: `auto` follows the device, `light` / `dark` are pinned; remembered in this browser.
// The first paint is public/theme-boot.js's, with the same rule
const KEY = 'theme'
const device = matchMedia('(prefers-color-scheme: dark)')
const own = () => (device.matches ? 'dark' : 'light')  // the device's scheme
const saved = load(KEY)
export const mode = ref(saved === 'light' || saved === 'dark' ? saved : 'auto')
export const shown = ref()  // what the page wears now

function apply() {
  shown.value = mode.value === 'auto' ? own() : mode.value
  document.documentElement.dataset.bsTheme = shown.value
}
// clicks go round three modes: auto → the other scheme → the device's scheme → auto;
// the page turns over on every click but the last one
export function nextTheme() {
  if (mode.value === 'auto') mode.value = own() === 'dark' ? 'light' : 'dark'
  else mode.value = mode.value === own() ? 'auto' : own()
  save(KEY, mode.value)
  apply()
}
apply()
device.addEventListener('change', apply)  // night mode on a schedule: an `auto` page follows at once
