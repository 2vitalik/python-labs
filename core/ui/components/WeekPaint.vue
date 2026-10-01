<script setup>
import { computed, ref, watch } from 'vue'

import { box, hours, paint, rect, toCells, toMarks, wipes } from '../week.js'
import { usePaint } from '../weekPaint.js'
import { emojiOf } from '../weekWhy.js'
import WeekGrid from './WeekGrid.vue'

// the grid a person paints their week on: every stroke is a rectangle of the chosen kind, shown while it is drawn.
// `drag` goes up with the hours of the stroke under way — the finger hides the very cells it paints
const props = defineProps({ frame: { type: Object, required: true }, tool: { type: String, required: true } })
const emit = defineEmits(['drag'])
const marks = defineModel({ type: Array, required: true })
const grid = ref()
const base = computed(() => toCells(marks.value, props.frame))
const { drag } = usePaint(() => grid.value.cells, () => props.frame, (a, b) => {
  const next = toMarks(paint(base.value, a, b, props.tool), props.frame)
  if (JSON.stringify(next) !== JSON.stringify(marks.value)) marks.value = next
})
const cells = computed(() => (drag.value ? paint(base.value, drag.value.a, drag.value.b, props.tool) : base.value))
const stroke = computed(() => drag.value && rect(drag.value.a, drag.value.b))
watch(stroke, (s) => emit('drag', s && `${hours(props.frame, s)}${wipes(base.value, drag.value.a, props.tool) ? ' — стерти' : ''}`))
const look = (day, row) => ({ class: cells.value[day][row]?.kind })
// a red mark opens with its reason's emoji, or with «?» while it has none
const signs = computed(() => cells.value.map((col) => col.map((c, row) => {
  const up = col[row - 1]
  if (c?.kind !== 'no' || (up?.kind === 'no' && up.why === c.why)) return ''
  return c.why.trim() ? emojiOf(c.why) || '✏️' : '?'
})))
</script>

<template>
  <WeekGrid ref="grid" :frame :look>
    <template #default="{ day, row }"><span v-if="signs[day][row]" :class="{ ask: signs[day][row] === '?' }">{{ signs[day][row] }}</span></template>
    <template #over><div v-if="stroke" class="stroke" :style="box(frame, stroke)"></div></template>
  </WeekGrid>
</template>

<style scoped>
.ask { font-weight: 700; font-size: .8rem; color: var(--bs-danger-text-emphasis); }
.stroke { position: absolute; border: 2px solid var(--bs-primary); border-radius: .25rem; pointer-events: none; }
</style>
