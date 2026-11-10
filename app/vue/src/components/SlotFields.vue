<script setup>
// inputs for a card's param slots, each with its label and unit, writing straight into the shared `params` object;
// no wrapper of its own — the caller's row lays them out
defineProps({ specs: Array, params: Object })
</script>

<template>
  <label v-for="s in specs" :key="s.key" class="slot">
    <template v-if="s.type === 'bool'">
      <input v-model="params[s.key]" type="checkbox" class="form-check-input m-0"> {{ s.label }}
    </template>
    <template v-else>
      <span class="name">{{ s.label }}<b v-if="s.required" class="req" title="обовʼязковий">*</b></span>
      <select v-if="s.type === 'choice'" v-model="params[s.key]" class="form-select form-select-sm w-auto">
        <option :value="undefined">—</option>
        <option v-for="o in s.options" :key="o" :value="o">{{ o }}</option>
      </select>
      <input v-else-if="s.type === 'text'" v-model="params[s.key]" class="form-control form-control-sm text">
      <input v-else v-model.number="params[s.key]" type="number" class="form-control form-control-sm num">
      <span v-if="s.unit" class="unit">{{ s.unit }}</span>
    </template>
  </label>
</template>

<style scoped>
.slot { display: inline-flex; align-items: center; gap: .3rem; margin: 0; font-size: .8rem; }
.name { color: var(--bs-secondary-color); white-space: nowrap; }
.req { margin-left: .1rem; color: var(--bs-danger); }
.unit { color: var(--bs-secondary-color); white-space: nowrap; }
.num { width: 4.5rem; }
.text { width: 9rem; }
</style>
