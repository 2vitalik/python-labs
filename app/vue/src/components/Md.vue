<script setup>
import { marked } from 'marked'
import { computed } from 'vue'

const props = defineProps({ text: String })
const html = computed(() => marked.parse(props.text || ''))
</script>

<template>
  <div class="md" v-html="html"></div>
</template>

<style scoped>
.md :deep(:last-child) { margin-bottom: 0; }
.md :deep(h2) { font-size: 1.1rem; margin-top: 1rem; }
.md :deep(h3) { font-size: 1rem; margin-top: 0.75rem; }
</style>
