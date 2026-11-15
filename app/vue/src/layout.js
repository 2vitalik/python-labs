import { computed, reactive, ref } from 'vue'

import { load, save } from '@core/local.js'

// how the reader wants a game's description laid out, remembered in this browser (T287, T291 §1): one column read top to
// bottom · several — as many as fit · dense — narrower columns, more of them. Dense is the default: in the page column
// it changes nothing, on the whole window it shows at once that the mode exists. A section may keep a look of its own
// (T294 §2), set on its heading; the button on top sets every section and drops their own, as «unfold all» does
export const oneCol = ref(load('game-cols') === '1')
export const dense = ref(load('game-dense') !== '0')
export const edWidth = ref(0)  // the editor's own width (GameEditor measures it): what the switch decides by
const read = () => { try { return JSON.parse(load('game-cols-own') || '{}') } catch { return {} } }
export const own = reactive(read())  // section id → 'one' | 'some' | 'dense'
const keepOwn = () => save('game-cols-own', JSON.stringify(own))

// two columns from this width on: half a laptop's screen still holds two cards side by side (T296 §4)
export const MIN2 = 540
// columns of at least `col` px in `width`: two at least once `min` is there, four at most — six when dense
export function fitCols(width, col = 380, min = MIN2, tight = dense.value) {
  if (width < min) return 1
  return tight ? Math.min(6, Math.max(2, Math.floor(width / (col * 0.75)))) : Math.min(4, Math.max(2, Math.floor(width / col)))
}
export const canCols = computed(() => fitCols(edWidth.value, 380, MIN2, false) > 1)  // else there is nothing to switch
export const canDense = computed(() => fitCols(edWidth.value, 380, MIN2, true) > fitCols(edWidth.value, 380, MIN2, false))
const fit = (m) => (m === 'dense' && !canDense.value ? 'some' : m)
export const colsMode = computed(() => fit(oneCol.value ? 'one' : dense.value ? 'dense' : 'some'))
// a section's look: its own, else the page's
export const modeOf = (id) => (id && own[id] ? fit(own[id]) : colsMode.value)
export const ownCount = computed(() => Object.keys(own).length)
const after = (m) => (m === 'one' ? 'some' : m === 'some' && canDense.value ? 'dense' : 'one')
export const nextOf = (id) => after(modeOf(id))

function set(one, tight) {
  oneCol.value = one
  save('game-cols', one ? '1' : '')
  if (tight === undefined) return
  dense.value = tight
  save('game-dense', tight ? '' : '0')
}
// one → several → dense → one; where dense gives no more columns than several, the two that differ. Without `id` — every
// section, their own looks dropped
export function nextCols(id) {
  const m = nextOf(id)
  if (id) {
    own[id] = m
    return keepOwn()
  }
  for (const k of Object.keys(own)) delete own[k]
  keepOwn()
  if (m === 'one') set(true)
  else set(false, m === 'dense' || (canDense.value ? false : undefined))
}

// consecutive runs whose sizes differ by one at most: 7 in 3 columns → 3 · 2 · 2
export function split(list, n) {
  const size = Math.floor(list.length / n), extra = list.length % n
  let at = 0
  return Array.from({ length: n }, (_, i) => list.slice(at, (at += size + (i < extra ? 1 : 0))))
}
