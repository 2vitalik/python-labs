<script setup>
import { computed, onMounted, ref } from 'vue'

import { getStudents, importStudents } from '../api.js'
import Crumbs from '../components/Crumbs.vue'
import StudentFilters from '../components/StudentFilters.vue'
import StudentsTable from '../components/StudentsTable.vue'
import { site } from '../site.js'
import { useStudentFilter } from '../studentFilter.js'
import { useTitle } from '../title.js'
import { user } from '../user.js'

const students = ref([])
const cards = site.students.cards  // the site's gallery, when it has one
const view = ref('table')
const showImport = ref(false)
const importText = ref('')
const importResult = ref('')

const isAdmin = computed(() => user.value?.status === 'admin')
const { shown, picked, active } = useStudentFilter(students)
const group = computed(() => picked.value.join(', '))  // picked groups read as a sub-page: crumb + title
const crumbs = computed(() => (group.value ? [['/students', 'Студи'], group.value] : ['Студи']))
useTitle(() => group.value && `Студенти ${group.value}`)

async function load() {
  students.value = await getStudents()
}

async function runImport() {
  const r = await importStudents(importText.value)
  importResult.value = `Додано: ${r.added} · оновлено: ${r.updated} · без змін: ${r.unchanged}`
  importText.value = ''
  await load()
}

onMounted(load)
</script>

<template>
  <div>
    <Crumbs :items="crumbs" />
    <div class="d-flex align-items-center gap-2 mb-3">
      <h1 class="h3 mb-0">Студенти <span class="text-secondary fs-6">{{ group }} ({{ shown.length }}{{ active ? ` з ${students.length}` : '' }})</span></h1>
      <div v-if="isAdmin && cards" class="btn-group btn-group-sm ms-2">
        <button class="btn" :class="view === 'table' ? 'btn-primary' : 'btn-outline-secondary'" @click="view = 'table'">Таблиця</button>
        <button class="btn" :class="view === 'cards' ? 'btn-primary' : 'btn-outline-secondary'" @click="view = 'cards'">Картки</button>
      </div>
      <button v-if="isAdmin" class="btn btn-outline-primary btn-sm ms-auto" @click="showImport = !showImport">Додати студентів</button>
    </div>

    <div v-if="showImport" class="card mb-3">
      <div class="card-body">
        <label class="form-label">Встав списки груп як у ЦІСТ (шапки «Список групи …» перемикають групу; наявні студенти оновлюються, внесене ними не чіпається)</label>
        <textarea v-model="importText" class="form-control font-monospace" rows="8"></textarea>
        <button class="btn btn-primary btn-sm mt-2" :disabled="!importText.trim()" @click="runImport">
          Імпортувати
        </button>
      </div>
    </div>
    <div v-if="importResult" class="alert alert-success">{{ importResult }}</div>

    <StudentFilters v-if="isAdmin" :students="students" />
    <p v-if="active && !shown.length" class="text-secondary">Під ці фільтри ніхто не підходить.</p>
    <StudentsTable v-else-if="isAdmin && (view === 'table' || !cards)" :students="shown" />
    <component :is="cards" v-else-if="cards" :students="shown" />
  </div>
</template>
