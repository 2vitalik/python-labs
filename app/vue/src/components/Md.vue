<script setup>
import { marked } from 'marked'
import { computed } from 'vue'

import { markHtml } from '../taskFilter.js'

// `q` — search words to highlight in the rendered text
const props = defineProps({ text: String, q: { type: String, default: '' } })
const html = computed(() => markHtml(marked.parse(props.text || ''), props.q))
</script>

<template>
  <div class="md" v-html="html"></div>
</template>

<style scoped>
.md :deep(:last-child) { margin-bottom: 0; }
.md :deep(h2) { font-size: 1.1rem; margin-top: 1rem; }
.md :deep(h3) { font-size: 1rem; margin-top: 0.75rem; }
</style>
