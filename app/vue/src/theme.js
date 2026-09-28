import { ref } from 'vue'

import { load, save } from './local.js'

// page theme: `auto` follows the device, `light` / `dark` are a choice; remembered in this browser.
// The first paint is public/theme-boot.js's, with the same rule
const KEY = 'theme'
const device = matchMedia('(prefers-color-scheme: dark)')
const scheme = (dark) => (dark ? 'dark' : 'light')
const saved = load(KEY)
export const mode = ref(saved === 'light' || saved === 'dark' ? saved : 'auto')

const shown = () => (mode.value === 'auto' ? scheme(device.matches) : mode.value)
const apply = () => (document.documentElement.dataset.bsTheme = shown())

// every click turns the page over; a turn back to the device's scheme means following the device again
export function toggleTheme() {
  const next = scheme(shown() !== 'dark')
  mode.value = next === scheme(device.matches) ? 'auto' : next
  save(KEY, mode.value)
  apply()
}
device.addEventListener('change', apply)  // night mode on a schedule: an `auto` page follows at once
