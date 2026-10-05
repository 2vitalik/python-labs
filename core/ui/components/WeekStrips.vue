<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'

import { hm } from '../week.js'
import WeekStripsDay from './WeekStripsDay.vue'
import WeekTip from './WeekTip.vue'

// everyone's week as strips (T186): a day is a column a person, group by group, the hours on the left. Under the pointer —
// the class that would start there and whose strip it is; a click pins the window. `days` — all of them, or one on its own
// page (`roomy`: wide strips, names, a reason's emoji in a red mark). The rest is what useWeekView() counts
const props = defineProps({
  frame: { type: Object, required: true }, days: { type: Array, required: true }, groups: { type: Array, required: true },
  counts: { type: Array, required: true }, tops: { type: Array, required: true }, windowAt: { type: Function, required: true },
  total: Number, mine: Array, picked: Object, lit: Number, roomy: Boolean,
})
const emit = defineEmits(['pick'])
const hover = ref(null)  // { day, row, nick }: row is null over the names, nick — over the Σ
const pointer = ref(null)
const rows = computed(() => (props.frame.to - props.frame.from) / props.frame.step)
const hours = computed(() => Array.from({ length: (props.frame.to - props.frame.from) / 60 + 1 }, (_, i) => hm(props.frame.from + i * 60)))
const top = computed(() => Math.max(1, ...props.counts.flat().map((c) => c.no)))  // the deepest Σ is the fullest slot of the week
const person = computed(() => hover.value?.nick && props.groups.flatMap((g) => g.list).find((p) => p.s.nick === hover.value.nick))
const here = computed(() => hover.value && hover.value.row !== null && props.windowAt(hover.value.day, hover.value.row))  // the class that would start here

// the slot and the person under the pointer: a day's body tells the row by height, a strip or a name — the person
function under(e) {
  const nick = e.target.closest('[data-nick]')?.dataset.nick || null
  const body = e.target.closest('[data-day]')
  if (!body) return nick && { day: Number(e.target.closest('[data-d]').dataset.d), row: null, nick }
  const box = body.getBoundingClientRect()
  return { day: Number(body.dataset.day), row: Math.min(rows.value - 1, Math.max(0, Math.floor(((e.clientY - box.top) / box.height) * rows.value))), nick }
}
function move(e) {
  if (e.pointerType === 'touch') return  // a finger has no hover: a tap pins the window
  const h = under(e)
  pointer.value = { x: e.clientX, y: e.clientY }
  if (JSON.stringify(h) !== JSON.stringify(hover.value)) hover.value = h
}
function click(e) {
  const h = under(e)
  if (h && h.row !== null) emit('pick', h.day, h.row)
}
const leave = () => (hover.value = null)
onMounted(() => addEventListener('scroll', leave, { passive: true }))  // the tip would stay where the pointer was
onUnmounted(() => removeEventListener('scroll', leave))
</script>

<template>
  <div class="scroll">
    <div class="strips" :class="{ roomy }" :style="{ '--rows': rows, '--hour': 60 / frame.step }" @pointermove="move" @pointerleave="leave" @click="click">
      <div class="hours"><span v-for="h in hours" :key="h">{{ h }}</span></div>
      <WeekStripsDay v-for="d in days" :key="d" :day="d" :frame :groups :counts :top :tops :mine :picked :lit :roomy
                     :ruler="hover?.day === d ? here || null : null" :nick="hover?.nick || null" />
    </div>
    <WeekTip v-if="hover && pointer" :w="here || null" :p="person || null" :day="hover.day" :at="pointer" :groups :total
             :minute="hover.row === null ? null : frame.from + hover.row * frame.step" />
  </div>
</template>

<style scoped>
.scroll { overflow-x: auto; }
.strips { --slot: .875rem; --label: .9rem; --names: 0rem; --dayname: 1.2rem; --sum: 1.25rem; --gut: .9rem; --gap: 3px;
          --strip-min: 0rem; --strip-max: 1.25rem; --day-min: 8rem; --day-gap: .5rem;
          display: flex; padding-bottom: .5rem; user-select: none; -webkit-user-select: none; cursor: crosshair; }
.strips.roomy { --slot: 1.2rem; --names: 5.5rem; --dayname: 0rem; --gap: .5rem; --strip-min: .75rem; --strip-max: 2.5rem; }
/* the hours stay at hand while a wide day scrolls sideways */
.hours { position: sticky; left: 0; z-index: 4; flex: 0 0 2.6rem; padding: calc(var(--dayname) + var(--label) + var(--names)) .4rem 0 0;
         background: var(--bs-body-bg); text-align: right; font-size: .7rem; color: var(--bs-secondary-color); }
/* an hour's label sits on its line, not under it */
.hours span { display: block; height: calc(var(--slot) * var(--hour)); line-height: 1; transform: translateY(-.35rem); }
.hours span:last-child { height: 0; }
</style>
