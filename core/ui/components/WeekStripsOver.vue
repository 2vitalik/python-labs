<script setup>
import { computed } from 'vue'

import { place } from '../weekStrips.js'

// what lies over a day's strips (T186): the hours the teacher can't, the window under the pointer (`ruler`), the window pinned
const props = defineProps({ day: { type: Number, required: true }, mine: Array, ruler: Object, picked: Object })
// the teacher's own «не можу» as runs of rows
const busy = computed(() => {
  const runs = []
  ;(props.mine?.[props.day] || []).forEach((c, r) => {
    if (c?.kind !== 'no') return
    if (runs.at(-1)?.end === r) runs.at(-1).end++
    else runs.push({ r0: r, end: r + 1 })
  })
  return runs
})
</script>

<template>
  <div class="over">
    <div v-for="b in busy" :key="b.r0" class="busy" :style="place(b.r0, b.end - b.r0)"></div>
    <div v-if="ruler" class="ruler" :style="place(ruler.r0, ruler.n)"></div>
    <div v-if="picked?.day === day" class="pin" :style="place(picked.r0, picked.n)"></div>
  </div>
</template>

<style scoped>
.over { position: absolute; left: 0; right: 0; top: calc(var(--label) + var(--names)); height: calc(var(--slot) * var(--rows)); z-index: 3; pointer-events: none; }
.over > * { position: absolute; left: 0; right: 0; }
.busy { background: repeating-linear-gradient(135deg, transparent 0 5px, color-mix(in srgb, var(--bs-body-color) 30%, transparent) 5px 6px); }
.ruler { border: 1px dashed var(--bs-primary); border-radius: 3px; }
.pin { border: 2px solid var(--bs-primary); border-radius: 3px; box-shadow: 0 0 0 1px var(--bs-body-bg); }
</style>
