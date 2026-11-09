<script setup>
import { vocab } from '../catalog.js'

// an entity's stats as rows «назва = значення одиниця»; a known stat fills its label and unit from the vocab
const stats = defineModel({ type: Array, default: () => [] })
const known = (key) => vocab.value.stats.find((s) => s.key === key || s.label === key)
function onKey(row) {
  const k = known(row.key)
  if (k) Object.assign(row, { key: k.key, label: k.label, unit: row.unit || k.unit })
}
const add = () => (stats.value = [...stats.value, { key: '', label: '', value: '', unit: '' }])
const remove = (i) => (stats.value = stats.value.filter((_, j) => j !== i))
</script>

<template>
  <div class="vstack gap-1">
    <div v-for="(s, i) in stats" :key="i" class="input-group input-group-sm">
      <input v-model="s.key" class="form-control" placeholder="HP, життя, швидкість…" list="stat-keys" @change="onKey(s)">
      <span class="input-group-text">=</span>
      <input v-model="s.value" class="form-control" placeholder="3" style="max-width: 6rem">
      <input v-model="s.unit" class="form-control" placeholder="од." style="max-width: 6rem">
      <button type="button" class="btn btn-outline-secondary" title="Прибрати" @click="remove(i)">✕</button>
    </div>
    <datalist id="stat-keys"><option v-for="s in vocab.stats" :key="s.key" :value="s.key">{{ s.icon }} {{ s.label }}</option></datalist>
    <button type="button" class="btn btn-link btn-sm p-0 text-decoration-none align-self-start" @click="add">＋ параметр</button>
  </div>
</template>
