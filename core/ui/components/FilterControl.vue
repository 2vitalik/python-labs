<script setup>
import { computed, ref, watch } from 'vue'

import { facets, hasValue, optionLabel, picks } from '../table.js'
import Icon from './Icon.vue'
import TableDateCond from './TableDateCond.vue'

// one column's filter condition, by what its cells hold (T315 §5, §12.1) — no frame, no caption: it stands in a header's menu
// and in a line of «Фільтри» alike. Yes · no; the answers with their counts over `rows`; from–to; a substring; a date.
// `set` — the new condition, or '' for none
const props = defineProps({ col: { type: Object, required: true }, spec: { type: String, default: '' }, rows: { type: Array, default: () => [] } })
const emit = defineEmits(['set'])
const set = (s) => emit('set', s)
const flip = (s) => set(props.spec === s ? '' : s)
const yes = computed(() => ['bool', 'link'].includes(props.col.type))
const empty = computed(() => props.rows.filter((r) => !hasValue(props.col.get(r))).length)
const counts = computed(() => Object.fromEntries(facets(props.col, props.rows).map((f) => [f.id, f.n])))
const chosen = computed(() => (props.spec && props.spec !== '+' ? props.spec.split(',') : []))
const pick = (id) => set((chosen.value.includes(id) ? chosen.value.filter((x) => x !== id) : [...chosen.value, id]).join())
// typed values apply as they are typed (a press outside closes the menu before a field could report a change); a condition
// set elsewhere — the line of totals, «є» — comes back into the fields
const from = ref('')
const to = ref('')
const text = ref('')
const range = () => (from.value !== '' || to.value !== '' ? `${from.value}-${to.value}` : '')
watch(() => props.spec, (s) => {
  if (s === (props.col.type === 'number' ? range() : text.value)) return  // it came from these fields: leave them as typed
  const m = s.match(/^(\d*\.?\d*)-(\d*\.?\d*)$/)
  from.value = m?.[1] || ''
  to.value = m?.[2] || ''
  text.value = s === '+' || s === '-' ? '' : s
}, { immediate: true })
const number = () => set(range())
</script>

<template>
  <div class="fc">
    <div v-if="yes" class="d-flex gap-1">
      <button type="button" class="opt" :class="{ on: spec === '1' }" @click="flip('1')">так <i>{{ counts['1'] || 0 }}</i></button>
      <button type="button" class="opt" :class="{ on: spec === '0' }" @click="flip('0')">ні <i>{{ rows.length - (counts['1'] || 0) }}</i></button>
    </div>
    <div v-else-if="picks(col)" class="d-flex flex-column">
      <button v-for="[id, o] in Object.entries(col.options || {})" :key="id" type="button" class="line" :class="{ on: chosen.includes(id), zero: !counts[id] }" @click="pick(id)">
        <span class="text-truncate">{{ optionLabel(o) }}</span><i>{{ counts[id] || 0 }}</i><Icon v-if="chosen.includes(id)" name="check" /></button>
      <button type="button" class="line" :class="{ on: chosen.includes('-'), zero: !empty }" @click="pick('-')">
        <span class="text-secondary">порожньо</span><i>{{ empty }}</i><Icon v-if="chosen.includes('-')" name="check" /></button>
    </div>
    <template v-else>
      <div v-if="col.type === 'number'" class="d-flex align-items-center gap-1 mb-1">
        від <input v-model="from" type="number" step="any" class="form-control form-control-sm" @input="number">
        до <input v-model="to" type="number" step="any" class="form-control form-control-sm" @input="number">
      </div>
      <input v-else-if="col.type === 'text'" v-model.trim="text" class="form-control form-control-sm mb-1" placeholder="містить…" @input="set(text)">
      <TableDateCond v-else-if="col.type === 'date'" :spec @set="set" />
      <div class="d-flex gap-1">
        <button type="button" class="opt" :class="{ on: spec === '+' }" @click="flip('+')">є <i>{{ rows.length - empty }}</i></button>
        <button type="button" class="opt" :class="{ on: spec === '-' }" @click="flip('-')">{{ col.type === 'date' ? 'нема' : 'порожньо' }} <i>{{ empty }}</i></button>
      </div>
    </template>
    <button v-if="spec" type="button" class="off" @click="set('')">зняти</button>
  </div>
</template>

<style scoped>
.fc { font-size: .85rem; }
.fc input[type=number] { width: 5rem; }
.opt, .line { border: 1px solid var(--bs-border-color); border-radius: .35rem; background: none; color: var(--bs-body-color); padding: .1rem .5rem; white-space: nowrap; }
.opt:hover, .line:hover { background: var(--bs-tertiary-bg); }
.opt.on, .line.on { background: var(--bs-warning-bg-subtle); border-color: var(--bs-warning-border-subtle); }
i { font-style: normal; font-size: .78em; color: var(--bs-secondary-color); font-variant-numeric: tabular-nums; }
.line { display: flex; align-items: center; gap: .4rem; border-color: transparent; text-align: start; min-width: 0; }
.line i { margin-left: auto; }
.line.zero:not(.on) { color: var(--bs-tertiary-color); }
.off { display: block; margin-top: .4rem; padding: 0; border: 0; background: none; color: var(--bs-secondary-color); font-size: .78rem;
       text-decoration: underline dashed; text-underline-offset: .2em; }
.off:hover { color: var(--bs-body-color); }
</style>
