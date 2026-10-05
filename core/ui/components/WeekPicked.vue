<script setup>
import { computed } from 'vue'

import { short } from '../studentFilter.js'
import { DAYS, hm } from '../week.js'
import { who } from '../weekSum.js'
import WeekWho from './WeekWho.vue'

// the window pinned on the grid or in the list (T186): its numbers, who can't by group, then who exactly and why.
// `groups` — arrange() of weekStrips.js: how many of each group have marked; `total` — the stream as shown
const props = defineProps({ w: Object, laid: { type: Array, required: true }, groups: { type: Array, required: true }, total: Number })
defineEmits(['close'])
const marked = computed(() => Object.fromEntries(props.groups.map((g) => [g.name, g.list.length])))
const est = computed(() => props.w && Math.round(props.w.est))
</script>

<template>
  <div>
    <div class="d-flex align-items-center gap-2 mb-2">
      <h2 class="h5 mb-0">{{ w ? `${DAYS[w.day]} ${hm(w.start)}–${hm(w.end)}` : 'Хто саме' }}</h2>
      <button v-if="w" type="button" class="btn-close btn-sm" title="Відкріпити" @click="$emit('close')"></button>
    </div>
    <p v-if="!w" class="small text-secondary">Клік по сітці або по рядку списку закріплює вікно — тут видно, хто не може і чому.</p>
    <template v-else>
      <div class="small mb-1">
        <span class="week-n no">{{ w.no }}</span> <span class="week-n meh">{{ w.meh }}</span> <span class="week-n ok">{{ w.ok }}</span> вільні {{ w.free }}
        <span v-if="w.mine === 'no'" class="text-danger"> · ти не можеш</span><span v-else-if="w.mine === 'meh'" class="text-secondary"> · тобі незручно</span>
      </div>
      <div v-if="est !== w.no" class="small text-secondary">якби позначили всі {{ total }}, не змогли б ≈ {{ est }}</div>
      <div v-if="w.no" class="small text-secondary">
        не можуть: <template v-for="(n, g, i) in w.by" :key="g">{{ i ? ' · ' : '' }}{{ short(g || '-') }} — {{ n }} з {{ marked[g] }}</template>
      </div>
      <WeekWho class="mt-2" :found="who(laid, w)" />
    </template>
  </div>
</template>
