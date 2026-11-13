import { reactive } from 'vue'

import { load, save } from '@core/local.js'

// how the reader left a section stays so on the next visit: a section of the game editor, a block of a game's page —
// open, folded away, or short (T284 §3: its beginning, fading into «Показати все»). The key names the place
// (`ed:rules`, `game:examples`), not the game — the habit is the reader's
const FOLDED = 1, SHORT = 2
const read = () => { try { return JSON.parse(load('folds') || '{}') } catch { return {} } }
const state = reactive(read())

function set(key, v) {
  if (v) state[key] = v
  else delete state[key]
  save('folds', JSON.stringify(state))
}
export const isFolded = (key) => state[key] === FOLDED
export const isShort = (key) => state[key] === SHORT
export const setFold = (key, on) => set(key, on ? FOLDED : 0)
export const setShort = (key, on) => set(key, on ? SHORT : 0)
export const toggleFold = (key) => setFold(key, !isFolded(key))
// every section at once: 'open' | 'short' | 'folded'
export const setAll = (keys, mode) => keys.forEach((k) => set(k, { folded: FOLDED, short: SHORT }[mode] || 0))
export const allAre = (keys, mode) => keys.every((k) => (state[k] || 0) === ({ folded: FOLDED, short: SHORT }[mode] || 0))
