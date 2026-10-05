<script setup>
import { computed, ref } from 'vue'

import { DAYS, hm } from '../week.js'
import { best } from '../weekSum.js'

// when a class could be (T177, T186): the starts with the fewest people against, the best first; 1–5 are the ones marked
// on the grid. `free` — the windows to choose from (useWeekView()); a row pins its window, the pinned one stays on top
const props = defineProps({ free: { type: Array, required: true }, tops: { type: Array, required: true }, len: { type: Number, required: true },
                            picked: Object, total: Number, busy: Boolean, empty: Boolean })
defineEmits(['pick'])
const skip = defineModel('skip', { type: Boolean, required: true })
const more = ref(false)
const rows = computed(() => {
  const list = best(props.free, props.len, more.value ? 40 : 10)
  return props.picked && !list.includes(props.picked) ? [props.picked, ...list] : list
})
const est = (w) => Math.round(w.est)
</script>

<template>
  <div class="mb-3">
    <div class="d-flex flex-wrap align-items-center gap-2 mb-2">
      <h2 class="h5 mb-0 me-1">Коли поставити пару</h2>
      <div v-if="busy" class="form-check form-switch small mb-0">
        <input id="week-skip" v-model="skip" class="form-check-input" type="checkbox">
        <label for="week-skip" class="form-check-label">без годин, коли я не можу</label>
      </div>
    </div>
    <p v-if="empty" class="text-secondary">Поки ніхто не позначив свій тиждень — обирати ні з чого.</p>
    <template v-else>
      <div class="small text-secondary mb-1">
        <span class="week-n no">не можуть</span> <span class="week-n meh">незручно</span> <span class="week-n ok">найкраще</span> решта — вільні ·
        ≈ — скільки не змогли б, якби позначили всі {{ total }}
      </div>
      <div class="list-group mb-1">
        <button v-for="w in rows" :key="`${w.day}-${w.r0}`" type="button" class="list-group-item list-group-item-action d-flex flex-wrap align-items-center column-gap-2 py-1"
                :class="{ on: w === picked }" @click="$emit('pick', w)">
          <span class="rank" :class="{ top: tops.includes(w) }">{{ tops.includes(w) ? tops.indexOf(w) + 1 : '' }}</span>
          <b class="when">{{ DAYS[w.day] }} {{ hm(w.start) }}–{{ hm(w.end) }}</b>
          <span class="week-n no" :class="{ zero: !w.no }" title="Не можуть">{{ w.no }}</span>
          <span class="week-n meh" :class="{ zero: !w.meh }" title="Можуть, але незручно">{{ w.meh }}</span>
          <span class="week-n ok" :class="{ zero: !w.ok }" title="Найкращий для них час">{{ w.ok }}</span>
          <span class="small text-secondary">вільні {{ w.free }}</span>
          <span v-if="est(w) !== w.no" class="small text-secondary" :title="`Якби позначили всі ${total}`">≈ {{ est(w) }}</span>
          <span v-if="w.mine === 'no'" class="small text-danger">ти не можеш</span>
          <span v-else-if="w.mine === 'meh'" class="small text-secondary">тобі незручно</span>
        </button>
      </div>
      <a href="#" class="small text-secondary" @click.prevent="more = !more">{{ more ? 'лише десять найкращих' : 'показати більше' }}</a>
    </template>
  </div>
</template>

<style scoped>
.when { min-width: 9.5rem; font-variant-numeric: tabular-nums; }
.rank { width: .9rem; height: .9rem; border-radius: 50%; font: 600 .6rem/.9rem var(--bs-font-sans-serif); text-align: center; }
.rank.top { background: var(--bs-primary); color: #fff; }
/* a phone: the row keeps to one line */
@media (max-width: 575.98px) { .when { min-width: 8.3rem; font-size: .9rem; } .list-group-item { padding-inline: .6rem; column-gap: .3rem !important; } }
.on { background: var(--bs-tertiary-bg); box-shadow: inset 2px 0 0 var(--bs-primary); }
</style>
