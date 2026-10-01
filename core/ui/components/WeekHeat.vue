<script setup>
import { computed } from 'vue'

import { DAYS, box, hm, startOf } from '../week.js'
import WeekGrid from './WeekGrid.vue'

// everyone's weeks over one grid: a cell says how many people marked it with the layer's kind — the more, the deeper;
// the number stands where a run of equal slots begins, the hint tells the whole slot.
// `mine` — the teacher's own cells, hatched where they can't; `picked` — the window looked at, framed
const props = defineProps({ frame: { type: Object, required: true }, counts: { type: Array, required: true }, layer: { type: String, required: true },
                            mine: Array, picked: Object })
defineEmits(['pick'])
const TONE = { no: 'danger', meh: 'warning', ok: 'success' }
const top = computed(() => Math.max(1, ...props.counts.flat().map((c) => c[props.layer])))  // the deepest tone is the fullest slot
const n = (day, row) => props.counts[day][row]?.[props.layer]
function look(day, row) {
  const c = props.counts[day][row]
  const tone = n(day, row) && `color-mix(in srgb, var(--bs-${TONE[props.layer]}) ${Math.round(12 + (58 * n(day, row)) / top.value)}%, var(--bs-body-bg))`
  return { class: { busy: props.mine?.[day][row]?.kind === 'no' }, style: tone ? { backgroundColor: tone } : null,
           title: `${DAYS[day]} ${hm(startOf(props.frame, row))} · не можуть ${c.no} · незручно ${c.meh} · найкраще ${c.ok}` }
}
</script>

<template>
  <WeekGrid :frame :look @pick="(day, row) => $emit('pick', day, row)">
    <template #default="{ day, row }">{{ n(day, row) && n(day, row) !== n(day, row - 1) ? n(day, row) : '' }}</template>
    <template #over>
      <div v-if="picked" class="picked" :style="box(frame, { d0: picked.day, d1: picked.day, r0: picked.r0, r1: picked.r0 + picked.n - 1 })"></div>
    </template>
  </WeekGrid>
</template>

<style scoped>
:deep(.cell.busy) { background-image: repeating-linear-gradient(135deg, transparent 0 5px, color-mix(in srgb, var(--bs-body-color) 22%, transparent) 5px 6px); }
.picked { position: absolute; border: 2px solid var(--bs-primary); border-radius: .25rem; pointer-events: none; }
</style>
