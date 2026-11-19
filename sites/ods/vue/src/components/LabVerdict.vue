<script setup>
import { computed } from 'vue'

import { markOf } from '../labText.js'

// what the site made of the answer line: an answer a row — ✅ / ❌ / ⬜, its name, why it is wrong when the site knows
const props = defineProps({ verdict: { type: Object, default: () => ({}) } })
const rows = computed(() => Object.entries(props.verdict || {}))
</script>

<template>
  <table v-if="rows.length" class="table table-sm w-auto mb-0">
    <tbody>
      <tr v-for="[name, v] in rows" :key="name">
        <td>{{ markOf(v) }}</td>
        <td><code>{{ name }}</code></td>
        <td class="text-secondary">{{ v.why }}</td>
      </tr>
    </tbody>
  </table>
</template>
