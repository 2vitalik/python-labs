<script setup>
import { computed, ref } from 'vue'

import { DAYS, hm } from '../week.js'
import { pairs } from '../weekPairs.js'

// no hour suits everyone? Two classes a week, each person comes to one of them: the pairs of windows that leave the fewest out.
// Counted when opened; the hours the teacher can't are never offered
const props = defineProps({ list: { type: Array, required: true }, laid: { type: Array, required: true }, len: { type: Number, required: true } })
const open = ref(false)
const free = computed(() => props.list.filter((w) => w.mine !== 'no'))
const clear = computed(() => free.value.some((w) => !w.no))  // an hour nobody refuses: one class will do
const tops = computed(() => (open.value && !clear.value ? pairs(props.laid, free.value, props.len, 5) : []))
const name = (w) => `${DAYS[w.day]} ${hm(w.start)}–${hm(w.end)}`
</script>

<template>
  <details v-if="laid.length" class="mb-3" @toggle="open = $event.target.open">
    <summary>Якщо одного вікна на всіх нема — дві пари на тиждень</summary>
    <p v-if="clear" class="small text-secondary mt-2 mb-0">Є вікно, де ніхто не каже «не можу», — двох пар не треба.</p>
    <p v-else class="small text-secondary mt-2 mb-1">Кожен ходить на одну з двох. Нижче — пари вікон, що лишають найменше людей без жодної.</p>
    <div v-for="p in tops" :key="`${p.a.day}-${p.a.r0}-${p.b.day}-${p.b.r0}`" class="small border-top py-1">
      <b>{{ name(p.a) }}</b> + <b>{{ name(p.b) }}</b> ·
      <span :class="p.none.length ? 'text-danger' : 'text-success'">нікуди {{ p.none.length }}</span> ·
      лише на першу {{ p.onlyA }} · лише на другу {{ p.onlyB }} · на будь-яку {{ p.both }}
      <div v-if="p.none.length" class="text-secondary">Нікуди: {{ p.none.map((s) => s.name || s.nick).join(', ') }}</div>
    </div>
  </details>
</template>
