<script setup>
import { computed } from 'vue'

import { vHint } from '@core/hint.js'
import { fmtWhen } from '@core/labs.js'

import { cellHint, toneOf } from '../intake.js'

// the cards' numbers of each lab a notebook came for (T368 §2.7): a number with a file wears its tone — on time · late ·
// no deadline — filled once the file is on the site, a frame till then; the rest stay empty; a click leads to the file's
// row below. All cells are one size, a long row wraps
const props = defineProps({ strips: Array })
defineEmits(['go'])
const rows = computed(() => props.strips.map((s) => {
  const by = new Map(s.cells.map((c) => [c.n, c]))
  const top = Math.max(s.top || 0, ...s.cells.map((c) => c.n))
  return { ...s, at: Array.from({ length: top }, (_, i) => by.get(i + 1) || { n: i + 1 }) }
}))
</script>

<template>
  <section class="strips mb-3">
    <div v-for="s in rows" :key="s.lab" class="strip">
      <div class="lbl">
        <span class="fw-semibold">Лаба {{ s.lab }}</span>
        <span v-if="s.due" v-hint="`дедлайн ${fmtWhen(s.due)}`" class="due">до {{ fmtWhen(s.due, true) }}</span>
      </div>
      <div class="cells">
        <template v-for="c in s.at" :key="c.n">
          <button v-if="c.id" v-hint="cellHint(c)" type="button" class="cell" :class="toneOf(c)" @click="$emit('go', c.id)">{{ c.n }}</button>
          <span v-else class="cell">{{ c.n }}</span>
        </template>
      </div>
    </div>
    <div class="legend">
      <span><i class="cell ok moved" /> вчасно</span> · <span><i class="cell late moved" /> після дедлайну</span> ·
      <span><i class="cell free moved" /> без дедлайну</span> · <span><i class="cell" /> файла нема</span> ·
      <span><i class="cell ok moved" /> на сайті</span> · <span><i class="cell ok" /> ще ні</span>
    </div>
  </section>
</template>

<style scoped>
.strip { display: grid; grid-template-columns: 5.5rem minmax(0, 1fr); column-gap: .5rem; align-items: start; margin-bottom: .4rem; }
.lbl { display: flex; flex-direction: column; font-size: .85rem; line-height: 1.25; }
.due { color: var(--bs-secondary-color); font-size: .75rem; }
.cells { display: flex; flex-wrap: wrap; gap: .2rem; }
.cell { display: inline-flex; align-items: center; justify-content: center; width: 1.7rem; height: 1.45rem; padding: 0;
        border: 1px solid var(--bs-border-color); border-radius: .25rem; background: none; color: var(--bs-secondary-color);
        font-size: .72rem; font-variant-numeric: tabular-nums; }
button.cell { cursor: pointer; }
button.cell:hover { outline: 2px solid var(--bs-secondary-color); outline-offset: 1px; }
.cell.ok { --tone: var(--bs-success); }
.cell.late { --tone: var(--bs-warning); }
.cell.free { --tone: var(--bs-primary); }
/* not on the site yet — a frame of the tone; on the site — filled too (border-box: the size stays) */
.cell.ok, .cell.late, .cell.free { border: 2px solid color-mix(in srgb, var(--tone) 75%, var(--bs-body-bg)); color: var(--bs-body-color); font-weight: 600; }
.cell.moved { border-width: 1px; border-color: color-mix(in srgb, var(--tone) 60%, var(--bs-body-bg)); background: color-mix(in srgb, var(--tone) 35%, var(--bs-body-bg)); }
.legend { color: var(--bs-secondary-color); font-size: .75rem; }
.legend span { white-space: nowrap; }
.legend .cell { width: .75rem; height: .75rem; vertical-align: -.1em; }
@media (max-width: 575px) { .strip { grid-template-columns: minmax(0, 1fr); } .lbl { flex-direction: row; gap: .4rem; align-items: baseline; } }
</style>
