<script setup>
import GuideText from './GuideText.vue'

// markdown field of a form: the textarea and, under it, the text as the site shows it
const model = defineModel({ default: '' })
defineProps({ label: String, rows: { type: Number, default: 14 } })
</script>

<template>
  <div>
    <label class="form-label">{{ label }}</label>
    <textarea v-model="model" class="form-control font-monospace" :rows spellcheck="false"></textarea>
    <div v-if="model.trim()" class="preview border rounded px-3 py-2 mt-2"><GuideText :text="model" /></div>
  </div>
</template>

<style scoped>
textarea { font-size: .85rem; line-height: 1.4; }
.preview { overflow: auto; max-height: 70vh; font-size: .9rem; }
.preview :deep(.guide > :first-child) { margin-top: 0; }
</style>
