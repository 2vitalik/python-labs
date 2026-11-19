<script setup>
import { computed } from 'vue'

import { markOf } from '../labText.js'

// the answers of a work next to the key (the teacher's eyes only): the student's number, the mark, the key ± its step,
// and under a wrong one the trap it fell into, when the site knows it
const props = defineProps({ answers: { type: Object, default: () => ({}) }, values: { type: Object, default: () => ({}) },
                            verdict: { type: Object, default: () => ({}) } })
const rows = computed(() => Object.entries(props.answers || {}).map(([name, a]) => {
  const v = props.verdict?.[name]
  return { name, got: props.values?.[name], mark: markOf(v), trap: v && !v.ok && markOf(v) === '❌' ? v.why : '', a }
}))
</script>

<template>
  <table class="table table-sm mb-0 ans">
    <thead class="small text-secondary"><tr><th>назва</th><th>студент</th><th></th><th>ключ</th></tr></thead>
    <tbody>
      <template v-for="r in rows" :key="r.name">
        <tr :class="{ 'no-line': r.trap }">
          <td><code>{{ r.name }}</code></td>
          <td class="num">{{ r.got ?? '—' }}</td>
          <td>{{ r.mark }}</td>
          <td class="num">{{ r.a.value }}<span v-if="r.a.step" class="text-secondary small"> ± {{ r.a.step }}</span></td>
        </tr>
        <tr v-if="r.trap" class="trap"><td></td><td colspan="3">{{ r.trap }}</td></tr>
      </template>
    </tbody>
  </table>
</template>

<style scoped>
.ans { font-size: .85rem; }
.num { font-variant-numeric: tabular-nums; overflow-wrap: anywhere; }
.no-line td { border-bottom: 0; }
.trap td { padding-top: 0; color: var(--bs-danger-text-emphasis); font-size: .78rem; }
</style>
