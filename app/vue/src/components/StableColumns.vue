<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue'

import { fitCols, MIN2, modeOf } from '../layout.js'
import { rows as rowsLook } from '../looks.js'

// columns that never reshuffle (T270 §2): a card stays in its column whatever grows inside it; a new card goes to the
// shortest column. Two columns in the page column, more on a wide page (`col` px each at least; narrower and more of
// them when the reader chose «щільно»), one on a narrow screen or when the reader asked for one (layout.js) — then in
// the list's order; `scope` — the section whose own look counts (layout.js). In rows (looks.js, T296 §6) the same
// number of columns, the cards in the list's order a row at a time, each row from one line. <StableColumns :items v-slot="{ item }">…
const props = defineProps({ items: Array, by: { type: String, default: 'id' }, min: { type: Number, default: MIN2 }, col: { type: Number, default: 380 }, scope: String })
const root = ref()
const cols = []
const home = reactive({})  // item key → its column
const width = ref(props.min)  // two columns until measured
const mode = computed(() => modeOf(props.scope))
const n = computed(() => (mode.value === 'one' ? 1 : fitCols(width.value, props.col, props.min, mode.value === 'dense')))
const inRows = computed(() => n.value > 1 && rowsLook.of(props.scope) === 'rows')
const key = (it) => it[props.by]
const shortest = (heights) => heights.indexOf(Math.min(...heights))
let watcher

async function place() {
  const keys = props.items.map(key)
  for (const k of Object.keys(home)) if (!keys.includes(k)) delete home[k]
  const fresh = keys.filter((k) => !(k in home))
  if (!fresh.length || n.value === 1) return
  if (fresh.length < keys.length) {
    for (const k of fresh) {
      home[k] = shortest(Array.from({ length: n.value }, (_, c) => cols[c]?.offsetHeight || 0))
      await nextTick()
    }
    return
  }
  fresh.forEach((k, i) => (home[k] = i % n.value))  // the first fill goes by turns, then once by the real heights
  await nextTick()
  if (!root.value) return
  const tall = Object.fromEntries([...root.value.querySelectorAll(':scope > .col > [data-k]')].map((el) => [el.dataset.k, el.offsetHeight]))
  const sum = Array(n.value).fill(0)
  for (const k of keys) {
    const c = shortest(sum)
    home[k] = c
    sum[c] += tall[k] || 1
  }
}
watch(() => props.items.map(key).join(), place, { immediate: true })
// another number of columns is another layout, so is the way back from rows: every card is dealt again
watch([n, inRows], () => {
  for (const k of Object.keys(home)) delete home[k]
  place()
})
onMounted(() => {
  watcher = new ResizeObserver(() => (width.value = root.value.offsetWidth))
  watcher.observe(root.value)
})
onBeforeUnmount(() => watcher?.disconnect())
</script>

<template>
  <div ref="root" class="stable" :class="{ rows: inRows }" :style="inRows ? { '--n': n } : null">
    <template v-if="inRows">
      <div v-for="it in items" :key="key(it)" :data-k="key(it)" class="cell"><slot :item="it" /></div>
    </template>
    <template v-else>
      <div v-for="c in n" :key="c" :ref="(el) => (cols[c - 1] = el)" class="col">
        <div v-for="it in items.filter((it) => n === 1 || home[key(it)] === c - 1)" :key="key(it)" :data-k="key(it)" class="cell">
          <slot :item="it" />
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped>
/* a little air between cards, so each reads as a block of its own (T294 §7) */
.stable { display: flex; align-items: flex-start; gap: .75rem; }
.stable.rows { display: grid; grid-template-columns: repeat(var(--n), minmax(0, 1fr)); column-gap: .75rem; row-gap: 0; }
.col { flex: 1 1 0; min-width: 0; }
.cell { margin-bottom: .75rem; }
</style>
