<script setup>
import { FIELDS, long, show } from '../cardFields.js'
import Diff from '@core/components/Diff.vue'

// one edit of a task or a game, field by field: short values as «було → стало», texts as a line diff
defineProps({ changes: { type: Object, required: true } })
</script>

<template>
  <div class="small">
    <div v-for="(c, field) in changes" :key="field" class="mb-1">
      <span class="text-secondary">{{ FIELDS[field] || field }}:</span>
      <Diff v-if="long(c)" :old="c.old || ''" :new="c.new || ''" class="mt-1" />
      <template v-else>
        <span v-if="c.old != null" class="was">{{ show(field, c.old) }}</span>
        <span v-if="c.old != null" class="text-secondary"> → </span>
        <span class="now">{{ show(field, c.new) }}</span>
      </template>
    </div>
  </div>
</template>

<style scoped>
.was { background: var(--bs-danger-bg-subtle); padding: 0 .25rem; border-radius: .25rem; }
.now { background: var(--bs-success-bg-subtle); padding: 0 .25rem; border-radius: .25rem; }
</style>
