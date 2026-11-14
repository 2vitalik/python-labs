import { computed, ref } from 'vue'

import { load, save } from '@core/local.js'

// how the reader wants a game's description laid out, remembered in this browser (T287, T291 §1): one column read top to
// bottom · several — as many as fit · dense — narrower columns, more of them. Dense is the default: in the page column
// it changes nothing, on the whole window it shows at once that the mode exists
export const oneCol = ref(load('game-cols') === '1')
export const dense = ref(load('game-dense') !== '0')
export const edWidth = ref(0)  // the editor's own width (GameEditor measures it): what the switch decides by

// columns of at least `col` px in `width`: two at least once `min` is there, four at most — six when dense
export function fitCols(width, col = 380, min = 620, tight = dense.value) {
  if (width < min) return 1
  return tight ? Math.min(6, Math.max(2, Math.floor(width / (col * 0.75)))) : Math.min(4, Math.max(2, Math.floor(width / col)))
}
export const canCols = computed(() => fitCols(edWidth.value, 380, 620, false) > 1)  // else there is nothing to switch
export const canDense = computed(() => fitCols(edWidth.value, 380, 620, true) > fitCols(edWidth.value, 380, 620, false))
export const colsMode = computed(() => (oneCol.value ? 'one' : dense.value && canDense.value ? 'dense' : 'some'))

function set(one, tight) {
  oneCol.value = one
  save('game-cols', one ? '1' : '')
  if (tight === undefined) return
  dense.value = tight
  save('game-dense', tight ? '' : '0')
}
// one → several → dense → one; where dense gives no more columns than several, the two that differ
export function nextCols() {
  if (colsMode.value === 'one') set(false, canDense.value ? false : undefined)
  else if (colsMode.value === 'some' && canDense.value) set(false, true)
  else set(true)
}

// consecutive runs whose sizes differ by one at most: 7 in 3 columns → 3 · 2 · 2
export function split(list, n) {
  const size = Math.floor(list.length / n), extra = list.length % n
  let at = 0
  return Array.from({ length: n }, (_, i) => list.slice(at, (at += size + (i < extra ? 1 : 0))))
}
