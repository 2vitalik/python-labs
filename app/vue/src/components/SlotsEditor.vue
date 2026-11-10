<script setup>
import Icon from '@core/components/Icon.vue'

// a card's claim params (Task.slots), a row each: what a student states when claiming the card
const slots = defineModel({ type: Array, default: () => [] })
const TYPES = { int: 'число', text: 'текст', bool: 'так / ні', choice: 'вибір' }
const csv = (s) => s.split(',').map((x) => x.trim()).filter(Boolean)
const add = () => (slots.value = [...slots.value, { key: '', label: '', type: 'int', unit: '', required: false, options: [] }])
const drop = (i) => (slots.value = slots.value.filter((_, j) => j !== i))
</script>

<template>
  <div class="vstack gap-1">
    <div class="hint">Параметри — числа й вибори, які студент вказує, заявляючи картку: «кожні 20 тіків», «глибина 3»</div>
    <div v-for="(s, i) in slots" :key="i" class="row-f align-items-center">
      <input v-model="s.key" class="form-control form-control-sm font-monospace key" placeholder="key" title="ключ латиницею">
      <input v-model="s.label" class="form-control form-control-sm grow" placeholder="підпис: Кожні">
      <select v-model="s.type" class="form-select form-select-sm w-auto">
        <option v-for="(label, k) in TYPES" :key="k" :value="k">{{ label }}</option>
      </select>
      <input v-if="s.type !== 'bool'" v-model="s.unit" class="form-control form-control-sm unit" placeholder="одиниця">
      <input v-if="s.type === 'choice'" :value="(s.options || []).join(', ')" class="form-control form-control-sm grow"
             placeholder="варіанти через кому" @change="s.options = csv($event.target.value)">
      <label class="d-inline-flex align-items-center gap-1 m-0 small">
        <input v-model="s.required" type="checkbox" class="form-check-input m-0"> обовʼязковий
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
