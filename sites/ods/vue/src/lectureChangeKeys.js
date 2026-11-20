import { nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'

import { box } from '@core/lightbox.js'

// the walk through the list of changes (T374 PAGE §5): ↑ ↓ — row by row (an open change hands over to its neighbour),
// Enter opens and shuts, Esc shuts; the list comes a portion at a time, and an open change comes into sight
export const STEP = 200
const rowOf = (id) => document.getElementById(`chg-${id}`)
// the keys' row holds the focus: Enter after a click on a pill would press the pill again
const hold = (id) => rowOf(id)?.focus({ preventScroll: true })

// `filters` — a getter of what the filters are: another choice starts the list from its first portion
export function useChangeWalk(list, open, set, filters) {
  const cur = ref(open.value)  // the row the keys stand on
  const limit = ref(STEP)
  // the portion grows to a change that is to be seen
  function fit(id) {
    const i = list.value.findIndex((it) => it.id === id)
    if (i >= limit.value) limit.value = Math.ceil((i + 1) / STEP) * STEP
  }
  watch(filters, () => {
    limit.value = STEP
    if (open.value) fit(open.value)
  })
  watch(open, (id) => {  // a link to a change followed on this page too
    if (!id) return
    fit(id)
    cur.value = id
  })
  // the row stays where it was while a change above it folds
  async function toggle(id) {
    const was = rowOf(id)?.getBoundingClientRect().top
    cur.value = id
    await set({ id: open.value === id ? undefined : id })
    await nextTick()
    if (was !== undefined && rowOf(id)) scrollBy({ top: rowOf(id).getBoundingClientRect().top - was })
    hold(id)
  }
  // the open one, once its blocks are in
  async function shown() {
    await nextTick()
    reveal(rowOf(open.value), rowOf(open.value)?.nextElementSibling)
  }
  function step(d) {
    const all = list.value
    if (!all.length) return false
    const i = all.findIndex((it) => it.id === (open.value || cur.value))
    const id = all[i < 0 ? 0 : Math.max(0, Math.min(all.length - 1, i + d))].id
    fit(id)
    if (open.value) return id !== open.value && toggle(id)
    cur.value = id
    nextTick(() => {
      reveal(rowOf(id))
      hold(id)
    })
  }
  useKeys({
    ArrowDown: () => step(1),
    ArrowUp: () => step(-1),
    Enter: () => (cur.value ? toggle(cur.value) : false),
    Escape: () => (open.value ? set({ id: undefined }) : false),
  })
  return { cur, limit, fit, toggle, shown }
}

// not while typing, nor over a picture in the lightbox; Enter on a focused button or link is that button's own.
// An act that returns false leaves the key to the page
function useKeys(acts) {
  function key(e) {
    if (box.value || e.altKey || e.ctrlKey || e.metaKey || e.shiftKey) return
    const t = e.target
    if (t.closest?.('input, textarea, select, [contenteditable=true]')) return
    if (e.key === 'Enter' && t.closest?.('button, a')) return
    if (acts[e.key] && acts[e.key]() !== false) e.preventDefault()
  }
  onMounted(() => document.addEventListener('keydown', key))
  onBeforeUnmount(() => document.removeEventListener('keydown', key))
}

// in sight under the menu: the page moves only when the row is out of sight, and only as far as it takes; a row with
// what opened under it taller than the window — to its top
function reveal(row, under = row) {
  if (!row) return
  const top = (parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--nav-h')) || 0) + 8
  const a = row.getBoundingClientRect().top, b = (under || row).getBoundingClientRect().bottom
  if (a >= top && b <= innerHeight - 8) return
  scrollBy({ top: a < top || b - a > innerHeight - top - 8 ? a - top : b - innerHeight + 8 })
}
