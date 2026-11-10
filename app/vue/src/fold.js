import { reactive } from 'vue'

import { load, save } from '@core/local.js'

// what the reader folded away stays folded on the next visit: a section of the game editor, a block of a game's page.
// The key names the place (`ed:rules`, `game:examples`), not the game — the habit is the reader's
const read = () => { try { return JSON.parse(load('folds') || '{}') } catch { return {} } }
const folded = reactive(read())

export const isFolded = (key) => !!folded[key]
export function setFold(key, on) {
  if (on) folded[key] = 1
  else delete folded[key]
  save('folds', JSON.stringify(folded))
}
export const toggleFold = (key) => setFold(key, !folded[key])
export const foldAll = (keys, on) => keys.forEach((k) => setFold(k, on))
