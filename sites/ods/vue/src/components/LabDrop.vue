<script setup>
import { ref } from 'vue'

import Icon from '@core/components/Icon.vue'

import { sendLabFile } from '../api.js'

// where a notebook file is handed in: dropped or picked. The box keeps its height — the server's words (what is wrong
// with the file) and «прийнято» take its last line, nothing around moves; `got` — the API's MY after the upload;
// `count` — the versions there were: the same bytes again make no new one, and the box says so
const props = defineProps({ n: Number, count: { type: Number, default: -1 } })
const emit = defineEmits(['got'])
const over = ref(false)
const busy = ref(false)
const error = ref('')
const done = ref('')
const MAX = 12 * 1024 * 1024  // the server's MAX_BYTES (models/lab_file.py): said here, before the file travels
const TOO_BIG = 'Файл завеликий: ліміт 12 МБ — прибери з ноутбука великі виводи (таблиці, зайві картинки) і збережи ще раз'
// the web server in front of the API may cut a request shorter than that, and answers without words of its own
const CUT = 'Сервер не прийняв файл такого розміру. Здай ноутбук посиланням — «інший спосіб» нижче — і напиши викладачеві'

async function send(file) {
  over.value = false
  if (!file || busy.value) return
  error.value = done.value = ''
  if (file.size > MAX) return (error.value = TOO_BIG)
  busy.value = true
  try {
    const had = props.count, my = await sendLabFile(props.n, file)
    emit('got', my)
    done.value = my.files?.length === had ? `Такий самий файл уже тут — нової версії не додано` : `Прийнято: ${file.name} — що побачив сайт, нижче`
  } catch (e) {
    error.value = e.status === 413 ? CUT : e.message
  } finally {
    busy.value = false
  }
}
function picked(e) {
  send(e.target.files[0])
  e.target.value = ''  // the same file again is a new hand-in
}
</script>

<template>
  <label class="lab-drop" :class="{ over, busy }" @dragover.prevent="over = true" @dragleave="over = false" @drop.prevent="send($event.dataTransfer.files[0])">
    <input type="file" accept=".ipynb,.py" class="d-none" :disabled="busy" @change="picked">
    <Icon name="upload" class="lab-drop-i" />
    <span v-if="busy">Читаю ноутбук…</span>
    <span v-else>Перетягни сюди файл ноутбука — <b>.ipynb</b> або marimo <b>.py</b> — чи <u>вибери файл</u></span>
    <span class="lab-drop-say" :class="error ? 'text-danger' : 'text-success'">{{ error || done }}</span>
  </label>
</template>

<style scoped>
.lab-drop { display: flex; flex-direction: column; align-items: center; justify-content: center; gap: .2rem; min-height: 7.5rem; padding: .75rem 1rem;
            border: 2px dashed var(--bs-border-color); border-radius: .5rem; text-align: center; cursor: pointer; transition: background .15s, border-color .15s; }
.lab-drop > * { pointer-events: none; }
.lab-drop:hover, .lab-drop.over { border-color: var(--bs-primary); background: var(--bs-primary-bg-subtle); }
.lab-drop.busy { cursor: progress; opacity: .7; }
.lab-drop-i { font-size: 1.4rem; color: var(--bs-secondary-color); }
.lab-drop-say { min-height: 1.3em; font-size: .85rem; }
</style>
