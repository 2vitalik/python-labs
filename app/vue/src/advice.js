import { reactive } from 'vue'

import { load, save } from '@core/local.js'
import { PAIRS } from './catalog.js'

// the functions a window type or an element hints at: one or a few alternatives (PAIRS), any of them claimed — no advice
export const answersOf = (slug) => [PAIRS[slug] || []].flat()

// advice waved off as «не про мою гру» (T278 §11): by game, in this browser only — it is no data of the game, just
// «don't bother». `text` — to list it back under «чого бракує»
const read = () => { try { return JSON.parse(load('advice') || '{}') } catch { return {} } }
const hidden = reactive(read())
const keep = () => save('advice', JSON.stringify(hidden))

export const hiddenOf = (game) => hidden[game] || []
export const isHidden = (game, key) => hiddenOf(game).some((a) => a.key === key)
export function hide(game, key, text) {
  if (!isHidden(game, key)) hidden[game] = [...hiddenOf(game), { key, text }]
  keep()
}
export function unhide(game, key) {
  hidden[game] = hiddenOf(game).filter((a) => a.key !== key)
  if (!hidden[game].length) delete hidden[game]
  keep()
}
