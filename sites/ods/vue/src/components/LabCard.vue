<script setup>
import { ref } from 'vue'

import Icon from '@core/components/Icon.vue'

import { getLabStart, labStartUrl } from '../api.js'
import { marimoLink } from '../marimoLink.js'

// the card of the variant and where to start: the block to paste, or the lab's notebook with the card already in it —
// Jupyter / Colab, marimo, or marimo in the browser (T354 §8: the code runs on the student's computer, not ours)
const props = defineProps({ n: Number, lab: Object })
const copied = ref(false)
const error = ref('')
let code = null  // the marimo notebook, fetched under the mouse: a window opened right in the click is not blocked

async function copy() {
  await navigator.clipboard.writeText(props.lab.card)
  copied.value = true
  setTimeout(() => (copied.value = false), 1500)
}
const fetchCode = () => (code ??= getLabStart(props.n, 'marimo').catch((e) => { code = null; throw e }))
async function browser() {
  error.value = ''
  try {
    window.open(marimoLink(await fetchCode()), '_blank', 'noopener')
  } catch (e) {
    error.value = e.message
  }
}
</script>

<template>
  <section class="mb-4">
    <h2 class="h5">Картка варіанта <code>{{ lab.vid }}</code></h2>
    <p class="small text-secondary mb-2">Встав цей блок у першу клітинку з кодом ноутбука замість рядка-заглушки.</p>
    <div class="position-relative mb-2">
      <button type="button" class="btn btn-sm btn-outline-secondary lab-copy" @click="copy">
        <Icon :name="copied ? 'check' : 'copy'" /> {{ copied ? 'скопійовано' : 'Скопіювати' }}
      </button>
      <pre class="lab-code"><code>{{ lab.card }}</code></pre>
    </div>
    <div v-if="lab.formats?.jupyter || lab.formats?.marimo">
      <div class="d-flex flex-wrap align-items-center gap-2">
        <span class="fw-semibold">Почати:</span>
        <span class="text-secondary">ноутбук із моєю карткою —</span>
        <a v-if="lab.formats.jupyter" :href="labStartUrl(n, 'jupyter')" download class="btn btn-sm btn-outline-primary">
          <Icon name="download" /> Jupyter / Colab (.ipynb)</a>
        <a v-if="lab.formats.marimo" :href="labStartUrl(n, 'marimo')" download class="btn btn-sm btn-outline-primary">
          <Icon name="download" /> marimo (.py)</a>
        <button v-if="lab.formats.marimo" type="button" class="btn btn-sm btn-outline-primary" @pointerenter="fetchCode().catch(() => {})"
                @focus="fetchCode().catch(() => {})" @click="browser"><Icon name="open" /> Відкрити в браузері</button>
      </div>
      <p v-if="lab.formats.marimo" class="small text-secondary mt-1 mb-0">marimo у браузері: код виконується на твоєму компʼютері,
        перше відкриття довге, з телефона не працює; щоб не втратити роботу — завантаж файл із меню marimo і здай його сюди.</p>
      <p v-if="error" class="small text-danger mt-1 mb-0">{{ error }}</p>
    </div>
  </section>
</template>

<style scoped>
.lab-code { margin: 0; padding: .75rem; border-radius: .25rem; background: var(--bs-tertiary-bg); font-size: .8rem; overflow-x: auto; }
.lab-copy { position: absolute; top: .4rem; right: .4rem; }
</style>
