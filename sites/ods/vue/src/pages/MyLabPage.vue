<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

import Crumbs from '@core/components/Crumbs.vue'
import { useTitle } from '@core/title.js'

import { getMyLab, putMyLab } from '../api.js'

// the student's own card of a lab and where the answer line is handed in (T200): the numbers are checked here, the notebook stays theirs
const MISSING = 'нема в рядку'  // the API's word for an answer the line lacks
const route = useRoute()
const n = computed(() => Number(route.params.n))
const lab = ref(null)
const gone = ref('')  // why there is no card for them: the API's own words
const line = ref('')
const notebook = ref('')
const busy = ref(false)
const error = ref('')
const copied = ref(false)
useTitle(() => `Моя лаба ${n.value}`)

const rows = computed(() => Object.entries(lab.value?.verdict || {}))
const icon = (v) => (v.ok ? '✅' : v.why === MISSING ? '⬜' : '❌')
const fmt = (d) => new Date(d).toLocaleString('uk-UA', { day: 'numeric', month: 'numeric', hour: '2-digit', minute: '2-digit' })

async function load() {
  try {
    lab.value = await getMyLab(n.value)
    line.value = lab.value.line
    notebook.value = lab.value.notebook
  } catch (e) {
    if (e.status !== 404) throw e
    gone.value = e.message
  }
}

async function copy() {
  await navigator.clipboard.writeText(lab.value.card)
  copied.value = true
  setTimeout(() => (copied.value = false), 1500)
}

async function send() {
  busy.value = true
  error.value = ''
  try {
    lab.value = await putMyLab(n.value, { line: line.value, notebook: notebook.value })
    line.value = lab.value.line
  } catch (e) {
    error.value = e.message
  } finally {
    busy.value = false
  }
}

onMounted(load)
</script>

<template>
  <div>
    <Crumbs :items="[['/labs', 'Лаби'], [`/labs/${n}`, `Лаба ${n}`], 'Моя лаба']" />
    <h1 class="h2 mb-3">Моя лаба {{ n }}</h1>
    <p v-if="gone" class="text-secondary">{{ gone }}</p>
    <template v-else-if="lab">
      <h2 class="h5">Картка варіанта <code>{{ lab.vid }}</code></h2>
      <p class="small text-secondary mb-2">Встав цей блок у першу клітинку з кодом ноутбука замість рядка-заглушки.</p>
      <div class="position-relative mb-3">
        <button type="button" class="btn btn-sm btn-outline-secondary copy" @click="copy">{{ copied ? '✅ скопійовано' : 'Скопіювати' }}</button>
        <pre class="code"><code>{{ lab.card }}</code></pre>
      </div>
      <h2 class="h5">Питання на захист</h2>
      <ol class="mb-4"><li v-for="q in lab.ask" :key="q">{{ q }}</li></ol>

      <h2 class="h5">Здати</h2>
      <form @submit.prevent="send">
        <label class="form-label mb-1">Рядок відповідей — те, що друкує остання клітинка ноутбука</label>
        <textarea v-model="line" class="form-control font-monospace mb-2" rows="3" :placeholder="`LAB${n} ${lab.vid} d1=… r1=…`"></textarea>
        <label class="form-label mb-1">Посилання на ноутбук</label>
        <input v-model="notebook" class="form-control mb-2" maxlength="300" placeholder="https://colab.research.google.com/…">
        <button class="btn btn-primary" :disabled="busy || (!line.trim() && !notebook.trim())">Перевірити й зберегти</button>
        <span v-if="error" class="text-danger ms-2">{{ error }}</span>
      </form>

      <template v-if="rows.length">
        <p class="mt-3 mb-1"><b>{{ lab.ok }} із {{ lab.total }} ✅</b> · спроба {{ lab.attempts }} · перевірено {{ fmt(lab.checked_at) }}</p>
        <table class="table table-sm w-auto">
          <tbody>
            <tr v-for="[name, v] in rows" :key="name">
              <td>{{ icon(v) }}</td>
              <td><code>{{ name }}</code></td>
              <td class="text-secondary">{{ v.why }}</td>
            </tr>
          </tbody>
        </table>
      </template>
      <p v-if="lab.points !== null" class="alert alert-success">Оцінка: <b>{{ lab.points }}</b><template v-if="lab.note"> — {{ lab.note }}</template></p>
    </template>
  </div>
</template>

<style scoped>
.code { background: var(--bs-tertiary-bg); padding: .75rem; border-radius: .25rem; font-size: .8rem; overflow-x: auto; }
.copy { position: absolute; top: .4rem; right: .4rem; }
</style>
