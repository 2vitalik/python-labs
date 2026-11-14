import { ref } from 'vue'

import { load, save } from './local.js'

// a meta.wide page on the whole window instead of the page column — the reader's choice, remembered in this browser.
// `meta.wide` names the memory: true — the tables and the catalog share one, 'game' — a game's description has its own
function memo(key) {
  const on = ref(load(key) === '1')
  return { on, toggle: () => { on.value = !on.value; save(key, on.value ? '1' : '0') } }
}
const kinds = { tasks: memo('tasks-wide'), game: memo('game-wide') }
export const wideOf = (name) => kinds[name === true ? 'tasks' : name]
export const { on: wide, toggle: toggleWide } = kinds.tasks
