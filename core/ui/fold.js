import { reactive } from 'vue'

import { load, save } from './local.js'

// how the reader left a section stays so on the next visit: a section of the game editor, a block of a game's page —
// open, folded away, or short (T284 §3: its beginning, fading into «Показати все»). The key names the place
// (`ed:rules`, `game:examples`), not the game — the habit is the reader's. «All at once» sets the page's default
// (`ed:*`, T298) and drops the sections' own; a section keeps its own state only while it differs from the default
const OPEN = 0, FOLDED = 1, SHORT = 2
const MODES = { open: OPEN, folded: FOLDED, short: SHORT }
const read = () => { try { return JSON.parse(load('folds') || '{}') } catch { return {} } }
const state = reactive(read())
const keep = () => save('folds', JSON.stringify(state))

const pageOf = (key) => key.slice(0, key.indexOf(':'))
const base = (key) => state[`${pageOf(key)}:*`] ?? OPEN
const at = (key) => state[key] ?? base(key)
function every(page, v) {
  for (const k of Object.keys(state)) if (k.startsWith(`${page}:`)) delete state[k]
  if (v !== OPEN) state[`${page}:*`] = v
  keep()
}
// `all` — ⌥-click on a heading: what this section gets, for every section of its page
function set(key, v, all) {
  if (all) return every(pageOf(key), v)
  if (v === base(key)) delete state[key]
  else state[key] = v
  keep()
}

export const isFolded = (key) => at(key) === FOLDED
export const isShort = (key) => at(key) === SHORT
export const isOwn = (key) => key in state
// short or in full unlike the page's default — the heading's «short» is blue then; unfolded under «all folded» is not
export const ownShort = (key) => isShort(key) !== (base(key) === SHORT)
export const setFold = (key, on) => set(key, on ? FOLDED : OPEN)
export const setShort = (key, on) => set(key, on ? SHORT : OPEN)
// unfolded, a section goes back to the page's default — open, where the default is folded
export const toggleFold = (key, all) => set(key, isFolded(key) ? (base(key) === FOLDED ? OPEN : base(key)) : FOLDED, all)
export const toggleShort = (key, all) => set(key, isShort(key) ? OPEN : SHORT, all)
// every section of a page (`ed`) at once: 'open' | 'short' | 'folded' — the page's default from now on
export const setAll = (page, mode) => every(page, MODES[mode])
export const allMode = (page) => Object.keys(MODES).find((m) => MODES[m] === (state[`${page}:*`] ?? OPEN))
