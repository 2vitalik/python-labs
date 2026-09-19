<script setup>
// inputs for a card's param slots, writing straight into the shared `params` object
defineProps({ specs: Array, params: Object })
</script>

<template>
  <template v-for="s in specs" :key="s.key">
    <label v-if="s.type === 'bool'" class="form-check form-check-inline small align-self-center m-0">
      <input v-model="params[s.key]" type="checkbox" class="form-check-input"> {{ s.label }}
    </label>
    <select v-else-if="s.type === 'choice'" v-model="params[s.key]" class="form-select form-select-sm w-auto">
      <option :value="undefined" disabled>{{ s.label }}…</option>
      <option v-for="o in s.options" :key="o" :value="o">{{ o }}</option>
    </select>
    <div v-else class="input-group input-group-sm w-auto flex-nowrap">
      <span class="input-group-text">{{ s.label }}{{ s.required ? '*' : '' }}</span>
      <input v-if="s.type === 'text'" v-model="params[s.key]" class="form-control" style="min-width: 8em">
      <input v-else v-model.number="params[s.key]" type="number" class="form-control" style="width: 5em">
      <span v-if="s.unit" class="input-group-text">{{ s.unit }}</span>
    </div>
  </template>
</template>
