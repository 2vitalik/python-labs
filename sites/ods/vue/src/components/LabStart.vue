<script setup>
import { ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import Reveal from '@core/components/Reveal.vue'
import { load, save } from '@core/local.js'

import { getLabStart, labStartUrl } from '../api.js'
import { marimoLink } from '../marimoLink.js'

// where to start: the lab's notebook with the card in it — Jupyter / Colab, marimo, or marimo in the browser (T354 §8:
// the code runs on the student's computer). marimo.app keeps one notebook per browser and our link opens a clean
// template over it, so once a lab is started there the main way is back to marimo.app; a clean start asks twice
const props = defineProps({ n: Number, lab: Object })
const KEY = `ods-marimo-${props.n}`
const started = ref(load(KEY) === '1')
const sure = ref(false)
const error = ref('')
let code = null  // the marimo notebook, fetched under the mouse: a window opened right in the click is not blocked

const fetchCode = () => (code ??= getLabStart(props.n, 'marimo').catch((e) => { code = null; throw e }))
async function fresh() {
  error.value = ''
  try {
    window.open(marimoLink(await fetchCode()), '_blank', 'noopener')
    save(KEY, '1')
    started.value = true
    sure.value = false
  } catch (e) {
    error.value = e.message
  }
}
const resume = () => window.open('https://marimo.app', '_blank', 'noopener')
const warm = () => fetchCode().catch(() => {})
</script>

<template>
  <div v-if="lab.formats?.jupyter || lab.formats?.marimo">
    <div class="d-flex flex-wrap align-items-center gap-2">
      <span class="fw-semibold">Почати:</span>
      <span class="text-secondary">ноутбук із моєю карткою —</span>
      <a v-if="lab.formats.jupyter" :href="labStartUrl(n, 'jupyter')" download class="btn btn-sm btn-outline-primary">
        <Icon name="download" /> Jupyter / Colab (.ipynb)</a>
      <a v-if="lab.formats.marimo" :href="labStartUrl(n, 'marimo')" download class="btn btn-sm btn-outline-primary">
        <Icon name="download" /> marimo (.py)</a>
    </div>
    <div v-if="lab.formats.marimo" class="d-flex flex-wrap align-items-center gap-2 mt-2">
      <span class="text-secondary">або одразу в браузері —</span>
      <button v-if="started" type="button" class="btn btn-sm btn-outline-primary" @click="resume"><Icon name="open" /> Продовжити в marimo</button>
      <button v-else type="button" class="btn btn-sm btn-outline-primary" @pointerenter="warm" @focus="warm" @click="fresh">
        <Icon name="open" /> Відкрити в браузері</button>
      <a v-if="started" href="#" class="lab-dot small" @pointerenter="warm" @click.prevent="sure = !sure">почати з чистого шаблону</a>
    </div>
    <Reveal :show="sure">
      <div class="d-flex flex-wrap align-items-center gap-2 pt-2 small">
        <span>Чистий шаблон зітре роботу, яку ти вже зробив у marimo в цьому браузері.</span>
        <button type="button" class="btn btn-sm btn-outline-secondary" @click="sure = false">Скасувати</button>
        <button type="button" class="btn btn-sm btn-danger" @click="fresh">Почати з чистого</button>
      </div>
    </Reveal>
    <p v-if="lab.formats.marimo" class="small text-secondary mt-1 mb-0">marimo у браузері: код виконується на твоєму компʼютері, перше
      відкриття — до пів хвилини, з телефона лише дивитись. Робота зберігається сама, але тільки в цьому браузері. Щоб здати:
      Ctrl/Cmd+S → ☰ → Export… → Python → файл notebook.py (не порожній) — сюди.</p>
    <p v-if="error" class="small text-danger mt-1 mb-0">{{ error }}</p>
  </div>
</template>

<style scoped>
.lab-dot { color: var(--bs-secondary-color); text-decoration: underline dotted; text-underline-offset: .2em; }
.lab-dot:hover { color: var(--bs-body-color); }
</style>
