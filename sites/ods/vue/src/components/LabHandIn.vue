<script setup>
import { ref } from 'vue'

import Reveal from '@core/components/Reveal.vue'

import { pullLabFile, putMyLab } from '../api.js'
import LabDrop from './LabDrop.vue'
import LabDue from './LabDue.vue'

// «Здати»: the file is the way; a Colab link the site fetches the file by, or the answer line alone, wait behind
// «інший спосіб» — open from the start for someone who has handed in a line before and no file
const props = defineProps({ n: Number, lab: Object })
const emit = defineEmits(['got'])
// open from the start for a line without a file, and for a marimo file: it keeps no outputs, the line comes here
const other = ref((!!props.lab.line && !props.lab.file?.id) || (props.lab.file?.kind === 'marimo' && !props.lab.attempts))
const link = ref(props.lab.notebook || '')
const line = ref(props.lab.line || '')
const busy = ref('')  // which of the two is being sent
const error = ref({ link: '', line: '' })

async function run(what, job) {
  busy.value = what
  error.value[what] = ''
  try {
    emit('got', await job())
  } catch (e) {
    error.value[what] = e.message
  } finally {
    busy.value = ''
  }
}
const pull = () => run('link', async () => {
  await putMyLab(props.n, { notebook: link.value.trim() })
  return pullLabFile(props.n)
})
const check = () => run('line', async () => {
  const my = await putMyLab(props.n, { line: line.value })
  line.value = my.line
  return my
})
</script>

<template>
  <section class="mb-4">
    <h2 class="h5">Здати</h2>
    <p v-if="lab.due" class="small text-secondary mb-2"><LabDue :lab /></p>
    <LabDrop :n :count="lab.files?.length || 0" @got="emit('got', $event)" />
    <a href="#" class="lab-dot small d-inline-block mt-1" @click.prevent="other = !other">інший спосіб</a>
    <Reveal :show="other">
      <div class="pt-2">
        <label class="form-label mb-1" for="lab-link">Посилання на ноутбук у Colab чи на Google Drive — доступ «усі, хто має посилання»</label>
        <div class="d-flex gap-2 mb-1">
          <input id="lab-link" v-model="link" class="form-control" maxlength="300" placeholder="https://colab.research.google.com/…">
          <button type="button" class="btn btn-outline-primary text-nowrap" :disabled="!link.trim() || !!busy" @click="pull">Взяти файл за посиланням</button>
        </div>
        <p class="small text-danger lab-say">{{ error.link }}</p>
        <label class="form-label mb-1" for="lab-line">Рядок відповідей — те, що друкує остання клітинка ноутбука</label>
        <textarea id="lab-line" v-model="line" class="form-control font-monospace mb-2" rows="3" :placeholder="`LAB${n} ${lab.vid} d1=… r1=…`"></textarea>
        <button type="button" class="btn btn-outline-primary" :disabled="!line.trim() || !!busy" @click="check">Перевірити рядок</button>
        <span class="small text-danger ms-2">{{ error.line }}</span>
      </div>
    </Reveal>
  </section>
</template>

<style scoped>
.lab-dot { color: var(--bs-secondary-color); text-decoration: underline dotted; text-underline-offset: .2em; }
.lab-dot:hover { color: var(--bs-body-color); }
.lab-say { min-height: 1.3em; margin-bottom: .5rem; }
</style>
