<script setup>
import { computed, ref } from 'vue'

import { DAYS, hm } from '../week.js'
import { best, who } from '../weekSum.js'
import WeekWho from './WeekWho.vue'

// when a class could be: the starts with the fewest people against, the best first; a row opens who exactly.
// `list` — every start with its counts (windows() of weekSum.js); `picked` — the one looked at: a row, or a start chosen on the map
const props = defineProps({ list: { type: Array, required: true }, laid: { type: Array, required: true }, picked: Object })
defineEmits(['pick'])
const len = defineModel('len', { type: Number, required: true })
const LENS = [80, 90, 120, 160]
const busy = computed(() => props.list.some((w) => w.mine === 'no'))
const skip = ref(true)  // the hours the teacher can't are no hours for a class
const more = ref(false)
const rows = computed(() => {
  const tops = best(props.list.filter((w) => !skip.value || w.mine !== 'no'), len.value, more.value ? 40 : 10)
  return props.picked && !tops.includes(props.picked) ? [props.picked, ...tops] : tops
})
</script>

<template>
  <div class="mb-3">
    <div class="d-flex flex-wrap align-items-center gap-2 mb-2">
      <h2 class="h5 mb-0 me-1">Коли поставити пару</h2>
      <div class="btn-group btn-group-sm" title="Скільки триває пара">
        <button v-for="l in LENS" :key="l" type="button" class="btn" :class="l === len ? 'btn-secondary' : 'btn-outline-secondary'" @click="len = l">{{ hm(l) }}</button>
      </div>
      <div v-if="busy" class="form-check form-switch small mb-0">
        <input id="week-skip" v-model="skip" class="form-check-input" type="checkbox">
        <label for="week-skip" class="form-check-label">без годин, коли я не можу</label>
      </div>
    </div>
    <p v-if="!laid.length" class="text-secondary">Поки ніхто не позначив свій тиждень — обирати ні з чого.</p>
    <template v-else>
      <div class="small text-secondary mb-1">
        <span class="week-n no">не можуть</span> <span class="week-n meh">незручно</span> <span class="week-n ok">найкраще</span> решта — вільні ·
        клік по рядку чи по карті — хто саме
      </div>
      <div class="list-group mb-1">
        <template v-for="w in rows" :key="`${w.day}-${w.r0}`">
          <button type="button" class="list-group-item list-group-item-action d-flex flex-wrap align-items-center column-gap-2 py-1" :class="{ on: w === picked }"
                  @click="$emit('pick', w === picked ? null : w)">
            <b class="when">{{ DAYS[w.day] }} {{ hm(w.start) }}–{{ hm(w.end) }}</b>
            <span class="week-n no" :class="{ zero: !w.no }" title="Не можуть">{{ w.no }}</span>
            <span class="week-n meh" :class="{ zero: !w.meh }" title="Можуть, але незручно">{{ w.meh }}</span>
            <span class="week-n ok" :class="{ zero: !w.ok }" title="Найкращий для них час">{{ w.ok }}</span>
            <span class="small text-secondary">вільні {{ w.free }}</span>
            <span v-if="w.mine === 'no'" class="small text-danger">ти не можеш</span>
            <span v-else-if="w.mine === 'meh'" class="small text-secondary">тобі незручно</span>
          </button>
          <div v-if="w === picked" class="list-group-item"><WeekWho :found="who(laid, w)" /></div>
        </template>
      </div>
      <a href="#" class="small text-secondary" @click.prevent="more = !more">{{ more ? 'лише десять найкращих' : 'показати більше' }}</a>
    </template>
  </div>
</template>

<style scoped>
.when { min-width: 9.5rem; font-variant-numeric: tabular-nums; }
/* a phone: the row keeps to one line */
@media (max-width: 575.98px) { .when { min-width: 8.3rem; font-size: .9rem; } .list-group-item { padding-inline: .6rem; column-gap: .3rem !important; } }
.on { background: var(--bs-tertiary-bg); box-shadow: inset 2px 0 0 var(--bs-primary); }
</style>
