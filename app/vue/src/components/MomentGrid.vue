<script setup>
import { computed, ref } from 'vue'

import { useCellFit } from '../cellFit.js'
import { useMomentEd } from '../momentEd.js'

// the field of the frame in work (T276): the cell under the mouse or a finger takes the brush, the eraser's empty cell or
// a frame mark, and the stroke goes on over every cell it crosses; a mark stroke puts what its first cell switched to.
// The page does not scroll under a drawing finger; the cells shrink so that a wide field fits its box (a phone, a card)
const ed = useMomentEd()
const root = ref()
const cols = computed(() => Math.max(1, ...ed.frame.grid.map((row) => row.length)))
const cell = useCellFit(root, cols, { reserve: 64 })  // the field's frame and the size controls at its sides
let value = null  // what this stroke puts; null — no stroke
let last = ''
function cellAt(e) {
  const el = document.elementFromPoint(e.clientX, e.clientY)?.closest('[data-r]')
  return el && root.value.contains(el) ? [+el.dataset.r, +el.dataset.c] : null
}
function down(e) {
  const p = cellAt(e)
  if (!p || e.button > 0) return
  e.preventDefault()
  root.value.setPointerCapture(e.pointerId)  // the moves keep coming here when the pointer leaves the field
  const mark = ed.frame.grid[p[0]][p[1]].mark
  value = { paint: ed.brush, erase: '' }[ed.tool] ?? (mark === ed.tool ? '' : ed.tool)
  last = ''
  move(e)
}
function move(e) {
  if (value === null) return
  const p = cellAt(e)
  if (!p || p.join() === last) return
  last = p.join()
  ed.put(p[0], p[1], value)
}
const up = () => (value = null)
</script>

<template>
  <div ref="root" class="cells" :style="{ '--cell': `${cell}px` }" @pointerdown="down" @pointermove="move" @pointerup="up" @pointercancel="up" @lostpointercapture="up">
    <div v-for="(row, r) in ed.frame.grid" :key="r" class="line">
      <span v-for="(c, k) in row" :key="k" class="c" :class="c.mark" :data-r="r" :data-c="k">{{ c.icon }}</span>
    </div>
  </div>
</template>

<style scoped>
/* the same look as a ```field on the page (GuideText) */
.cells { width: fit-content; padding: .35rem; border: 1px solid var(--bs-border-color);
         border-radius: .375rem; background: var(--bs-tertiary-bg); font-size: calc(var(--cell) * .62); line-height: 1;
         touch-action: none; user-select: none; -webkit-user-select: none; cursor: crosshair; }
.line { display: flex; }
.c { display: inline-flex; align-items: center; justify-content: center; width: var(--cell); height: var(--cell); flex-shrink: 0; border-radius: .3rem; }
.c:hover { background: color-mix(in srgb, var(--bs-body-color) 10%, transparent); }
.who { box-shadow: inset 0 0 0 2px var(--bs-primary); }
.new { box-shadow: inset 0 0 0 2px var(--bs-warning); }
</style>
