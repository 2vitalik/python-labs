<script setup>
import { computed } from 'vue'

import { short } from '../studentFilter.js'
import { DAYS, hm, span } from '../week.js'

// what the pointer is over on the strips (T186): the class that would start there — how many can't, by group, and how many
// would, had the whole stream marked; then whose strip it is, with their day. `minute` — the slot under the pointer, its mark
// stands out. The tip keeps off the window's edges: past the middle it turns to the other side
const props = defineProps({ w: Object, p: Object, day: { type: Number, required: true }, minute: Number, at: { type: Object, required: true },
                            groups: { type: Array, required: true }, total: Number })
const marked = computed(() => Object.fromEntries(props.groups.map((g) => [g.name, g.list.length])))
const by = computed(() => props.w && Object.entries(props.w.by).map(([g, n]) => `${short(g || '-')} — ${n} з ${marked.value[g]}`).join(' · '))
const marks = computed(() => props.p?.s.week.marks.filter((m) => m.day === props.day) || [])
const est = computed(() => props.w && Math.round(props.w.est))
const place = computed(() => {
  const { x, y } = props.at
  const [left, up] = [x > innerWidth - 360, y > innerHeight * 0.6]
  return { [left ? 'right' : 'left']: `${left ? innerWidth - x + 14 : x + 14}px`, [up ? 'bottom' : 'top']: `${up ? innerHeight - y + 14 : y + 14}px` }
})
</script>

<template>
  <div class="tip small" :style="place">
    <template v-if="w">
      <div><b>{{ DAYS[w.day] }} {{ hm(w.start) }}–{{ hm(w.end) }}</b>
        <span v-if="w.mine === 'no'" class="text-danger"> · ти не можеш</span><span v-else-if="w.mine === 'meh'" class="text-secondary"> · тобі незручно</span></div>
      <div class="my-1">
        <span class="week-n no">{{ w.no }}</span> <span class="week-n meh">{{ w.meh }}</span> <span class="week-n ok">{{ w.ok }}</span> вільні {{ w.free }}
      </div>
      <div v-if="est !== w.no" class="text-secondary">якби позначили всі {{ total }}, не змогли б ≈ {{ est }}</div>
      <div v-if="by" class="text-secondary">не можуть: {{ by }}</div>
    </template>
    <template v-if="p">
      <hr v-if="w" class="my-2">
      <div class="mb-1"><b>{{ p.s.name || p.s.nick }}</b> · {{ p.s.group || 'без групи' }}<span v-if="!p.s.week.done_at"> · ✍️ без «Готово»</span></div>
      <div v-for="(m, k) in marks" :key="k" :class="{ now: m.start <= minute && minute < m.end }">
        <span class="week-n" :class="m.soft ? 'no' : m.kind">{{ span(m) }}</span> {{ m.why }}<span v-if="m.soft" class="text-secondary"> · рахується як «незручно»</span>
      </div>
      <div v-if="!marks.length" class="text-secondary">цього дня може будь-коли</div>
      <div v-if="p.s.week.comment" class="mt-1">💬 {{ p.s.week.comment }}</div>
    </template>
  </div>
</template>

<style scoped>
.tip { position: fixed; z-index: 1080; max-width: 21rem; padding: .5rem .65rem; pointer-events: none; background: var(--bs-body-bg);
       border: 1px solid var(--bs-border-color); border-radius: var(--bs-border-radius); box-shadow: var(--bs-box-shadow); }
.week-n { min-width: 1.6rem; }
.now { font-weight: 600; }
</style>
