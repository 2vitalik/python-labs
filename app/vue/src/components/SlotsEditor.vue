<script setup>
import { reactive } from 'vue'

import Icon from '@core/components/Icon.vue'
import { TIPS } from '../taskTips.js'

// a card's claim params (Task.slots), a row each: what a student states when claiming the card; each field explains itself
// under the mouse. A unit is rare: it comes by «＋ одиниця» (T291 §4), shown at once where there is one
const slots = defineModel({ type: Array, default: () => [] })
const TYPES = { int: 'число', text: 'текст', bool: 'так / ні', choice: 'вибір' }
const withUnit = reactive(new Set(slots.value.filter((s) => s.unit)))  // the slots whose unit field is in the row
const csv = (s) => s.split(',').map((x) => x.trim()).filter(Boolean)
const add = () => (slots.value = [...slots.value, { key: '', label: '', type: 'int', unit: '', required: false, options: [] }])
const drop = (i) => (slots.value = slots.value.filter((_, j) => j !== i))
</script>

<template>
  <div class="vstack gap-1">
    <div v-for="(s, i) in slots" :key="i" class="row-f align-items-center">
      <input v-model="s.key" class="form-control form-control-sm font-monospace key" placeholder="key" :title="TIPS.slot.key">
      <input v-model="s.label" class="form-control form-control-sm grow" placeholder="підпис: Кожні" :title="TIPS.slot.label">
      <select v-model="s.type" class="form-select form-select-sm w-auto" :title="TIPS.slot.type">
        <option v-for="(label, k) in TYPES" :key="k" :value="k">{{ label }}</option>
      </select>
      <template v-if="s.type !== 'bool'">
        <input v-if="withUnit.has(s)" v-model="s.unit" class="form-control form-control-sm unit" placeholder="одиниця" :title="TIPS.slot.unit">
        <button v-else type="button" class="more-field" :title="TIPS.slot.unit" @click="withUnit.add(s)"><Icon name="plus" /> одиниця</button>
      </template>
      <input v-if="s.type === 'choice'" :value="(s.options || []).join(', ')" class="form-control form-control-sm grow"
             placeholder="варіанти через кому" :title="TIPS.slot.options" @change="s.options = csv($event.target.value)">
      <label class="d-inline-flex align-items-center gap-1 m-0 small" :title="TIPS.slot.required">
        <input v-model="s.required" type="checkbox" class="form-check-input m-0"> <span class="tip">обовʼязковий</span>
      </label>
      <button type="button" class="iact del" title="Прибрати параметр" @click="drop(i)"><Icon name="minus" /></button>
    </div>
    <div><button type="button" class="btn btn-sm btn-add" @click="add"><Icon name="plus" /> параметр</button></div>
  </div>
</template>

<style scoped>
.key { width: 6rem; }
.unit { width: 5.5rem; }
</style>
