import { ref } from 'vue'

import { load, save } from './local.js'

// page theme: `auto` follows the device, `light` / `dark` are pinned; remembered in this browser.
// The first paint is public/theme-boot.js's, with the same rule
const KEY = 'theme'
const device = matchMedia('(prefers-color-scheme: dark)')
const own = () => (device.matches ? 'dark' : 'light')  // the device's scheme
const saved = load(KEY)
export const mode = ref(saved === 'light' || saved === 'dark' ? saved : 'auto')

function apply() {
  document.documentElement.dataset.bsTheme = mode.value === 'auto' ? own() : mode.value
}
// clicks go round three modes: auto → the other scheme → the device's scheme → auto.
// `auto` comes after the scheme the device has: that click unpins the page and leaves it as it looks
export function nextTheme() {
  if (mode.value === 'auto') mode.value = own() === 'dark' ? 'light' : 'dark'
  else mode.value = mode.value === own() ? 'auto' : own()
  save(KEY, mode.value)
  apply()
}
apply()
device.addEventListener('change', apply)  // night mode on a schedule: an `auto` page follows at once
