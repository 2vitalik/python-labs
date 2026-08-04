<script setup>
import { onMounted, ref } from 'vue'

import { getStudents, importStudents } from '../api.js'
import { user } from '../user.js'

const students = ref([])
const showImport = ref(false)
const importText = ref('')
const importResult = ref('')

const fio = (s) => [s.last_name, s.first_name, s.patronymic].filter(Boolean).join(' ') || '—'
const repoName = (url) => url.replace('https://github.com/', '')

async function load() {
  students.value = await getStudents()
}

async function runImport() {
  const r = await importStudents(importText.value)
  importResult.value = `Додано: ${r.added}, вже були: ${r.skipped}` + (r.group ? ` · група ${r.group}` : '')
  importText.value = ''
  await load()
}

onMounted(load)
</script>

<template>
  <div v-if="user?.status === 'admin'">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h1 class="h3 mb-0">Студенти <span class="text-secondary fs-6">({{ students.length }})</span></h1>
      <button class="btn btn-outline-primary btn-sm" @click="showImport = !showImport">Додати студентів</button>
    </div>

    <div v-if="showImport" class="card mb-3">
      <div class="card-body">
        <label class="form-label">Встав список групи (як у ЦІСТ: ПІБ, номер залікової, пошта)</label>
        <textarea v-model="importText" class="form-control font-monospace" rows="8"></textarea>
        <button class="btn btn-primary btn-sm mt-2" :disabled="!importText.trim()" @click="runImport">
          Імпортувати
        </button>
      </div>
    </div>
    <div v-if="importResult" class="alert alert-success">{{ importResult }}</div>

    <table class="table table-hover align-middle">
      <thead>
        <tr><th>ПІБ</th><th>Пошта</th><th>Група</th><th>GitHub</th><th>Telegram</th><th>Статус</th></tr>
      </thead>
      <tbody>
        <tr v-for="s in students" :key="s.id" role="button" @click="$router.push(`/students/${s.id}`)">
          <td>{{ fio(s) }}</td>
          <td>{{ s.email }}</td>
          <td>{{ s.group || '—' }}</td>
          <td>
            <a v-if="s.github" :href="s.github" target="_blank" @click.stop>{{ repoName(s.github) }}</a>
            <span v-else class="text-secondary">—</span>
          </td>
          <td>
            <span v-if="s.tg_username">@{{ s.tg_username }} <span v-if="s.tg_linked">✅</span></span>
            <span v-else class="text-secondary">—</span>
          </td>
          <td><span class="badge" :class="s.status === 'student' ? 'text-bg-primary' : 'text-bg-secondary'">{{ s.status }}</span></td>
        </tr>
      </tbody>
    </table>
  </div>
  <p v-else class="text-center mt-5">Сторінка доступна лише викладачу.</p>
</template>
