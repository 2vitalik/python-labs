import { ref } from 'vue'

import { load, save } from './local.js'

// a meta.wide page on the whole window instead of the page column — the reader's choice, remembered in this browser.
// `meta.wide` names the memory: true — the tables and the catalog share one, 'game' — a game's description has its own,
// 'table' — the table of students
function memo(key, first = false) {
  const on = ref((load(key) ?? (first ? '1' : '0')) === '1')
  return { on, toggle: () => { on.value = !on.value; save(key, on.value ? '1' : '0') } }
}
const kinds = { tasks: memo('tasks-wide'), game: memo('game-wide'), table: memo('table-wide', true) }  // /table is wide till told otherwise: its columns do not fit a page
export const wideOf = (name) => kinds[name === true ? 'tasks' : name]
export const { on: wide, toggle: toggleWide } = kinds.tasks
