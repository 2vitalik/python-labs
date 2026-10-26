<script setup>
import { computed, onMounted, ref } from 'vue'

import { getLabReview } from '../api.js'
import { VERDICTS, fmtWhen } from '../labs.js'
import { renderMd } from '../md.js'

// the agent's report on a student's lab, fetched when opened: the header line, then the markdown
const props = defineProps({ nick: { type: String, required: true }, lab: { type: [Number, String], required: true } })
const review = ref(null)
const error = ref('')
const html = computed(() => renderMd(review.value?.report || '*звіт без тексту*'))
onMounted(async () => {
  try {
    review.value = await getLabReview(props.nick, props.lab)
  } catch (e) {
    error.value = e.message
  }
})
</script>

<template>
  <div class="report border rounded p-3 mt-2">
    <div v-if="error" class="text-danger">{{ error }}</div>
    <template v-else-if="review">
      <div class="small text-secondary mb-2">
        зріз <code>{{ review.commit }}</code> — {{ VERDICTS[review.verdict] }}<template v-if="review.head"> · HEAD <code>{{ review.head }}</code> — {{ VERDICTS[review.head_verdict] || '?' }}</template>
        · {{ review.by }} · {{ fmtWhen(review.at) }}
      </div>
      <div class="md" v-html="html"></div>
    </template>
    <div v-else class="text-secondary">…</div>
  </div>
</template>

<style scoped>
.report { background: var(--bs-body-bg); }
.md :deep(h1) { font-size: 1.15rem; }
.md :deep(h2) { font-size: 1.05rem; }
.md :deep(h3) { font-size: 1rem; }
.md :deep(p:last-child) { margin-bottom: 0; }
</style>
