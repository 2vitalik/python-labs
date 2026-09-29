<script setup>
import { computed, ref } from 'vue'

import { getGuidePage, publishChange, putGuidePage } from '../api.js'
import GuideText from './GuideText.vue'

// admin box on /changes: the lines edit notes collected (T126 §5b) — publish one into the page below or drop it
const emit = defineEmits(['published'])
const draft = ref(null)
const error = ref('')
const lines = computed(() => (draft.value?.body || '').split('\n').filter((l) => l.trim()))
const load = () => getGuidePage('changes-draft').then((p) => (draft.value = p)).catch(() => (draft.value = null))

async function run(fn) {
  error.value = ''
  try {
    await fn()
    await load()
  } catch (e) {
    error.value = e.message
  }
}
const publish = (line) => run(async () => {
  await publishChange(line)
  emit('published')
})
const drop = (line) => run(() => putGuidePage('changes-draft', {
  title: draft.value.title, body: lines.value.filter((l) => l !== line).join('\n'), rev: draft.value.rev,
}))
load()
</script>

<template>
  <div v-if="lines.length" class="border rounded px-3 py-2 mb-4">
    <div class="small text-secondary mb-1">Чернетка з нотаток до правок — студентам не видно. «↑» переносить рядок у журнал нижче.</div>
    <div v-for="l in lines" :key="l" class="d-flex align-items-start gap-2 py-1">
      <GuideText :text="l.replace(/^- /, '')" class="flex-grow-1 small" />
      <button class="btn btn-outline-primary btn-sm py-0" title="Опублікувати" @click="publish(l)">↑</button>
      <button class="btn btn-outline-secondary btn-sm py-0" title="Прибрати" @click="drop(l)">✕</button>
    </div>
    <div v-if="error" class="text-danger small">{{ error }}</div>
  </div>
</template>
