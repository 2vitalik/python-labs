<script setup>
import { computed } from 'vue'

import { piecesOf } from '../labText.js'

// what the file has of the lab (FACTS.count) as quiet pills; a whole piece is green
const props = defineProps({ count: Object })
const pieces = computed(() => piecesOf(props.count))
</script>

<template>
  <span class="pcs">
    <span v-for="p in pieces" :key="p.text" class="pcs-p" :class="{ full: p.full }">{{ p.text }}</span>
  </span>
</template>

<style scoped>
.pcs { display: inline-flex; flex-wrap: wrap; gap: .2rem; }
.pcs-p { padding: 0 .4rem; border: 1px solid var(--bs-border-color); border-radius: 1rem; color: var(--bs-secondary-color); font-size: .75rem; white-space: nowrap; }
.pcs-p.full { border-color: var(--bs-success-border-subtle); background: var(--bs-success-bg-subtle); color: var(--bs-success-text-emphasis); }
</style>
