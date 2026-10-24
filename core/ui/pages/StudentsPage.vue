<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

import { getStudents, importStudents } from '../api.js'
import Crumbs from '../components/Crumbs.vue'
import StudentFilters from '../components/StudentFilters.vue'
import StudentsTable from '../components/StudentsTable.vue'
import { site } from '../site.js'
import { useStudentFilter } from '../studentFilter.js'
import { studentsCrumbs, studentsHome } from '../students.js'
import { useTitle } from '../title.js'
import { user } from '../user.js'

// the admin's list of everyone; a student sees the slice the API gives them under the site's name for it (students.js)
const students = ref([])
const cards = site.students.cards  // the site's gallery, when it has one
const isAdmin = computed(() => user.value?.status === 'admin')
const view = ref(cards && (useRoute().query.view === 'cards' || !isAdmin.value) ? 'cards' : 'table')
const showImport = ref(false)
const importText = ref('')
const importResult = ref('')

const { shown, picked, active } = useStudentFilter(students)
// the gallery may be of some only (site.students.inGallery): the numbers in the heading and on the chips follow the view
const of = (list) => (view.value === 'cards' && site.students.inGallery ? list.filter(site.students.inGallery) : list)
const listed = computed(() => of(shown.value))
const total = computed(() => of(students.value).length)
const group = computed(() => picked.value.join(', '))  // picked groups read as a sub-page: crumb + title
const home = computed(() => studentsHome())
const crumbs = computed(() => studentsCrumbs(...(group.value ? [group.value] : [])))
useTitle(() => [home.value.name, group.value].filter(Boolean).join(' '))

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
      <h1 class="h3 mb-0">{{ home.name }} <span class="text-secondary fs-6">{{ group }} ({{ listed.length }}{{ active ? ` з ${total}` : '' }})</span></h1>
      <div v-if="cards" class="btn-group btn-group-sm ms-2">
        <button class="btn" :class="view === 'table' ? 'btn-primary' : 'btn-outline-secondary'" @click="view = 'table'">Таблиця</button>
        <button class="btn" :class="view === 'cards' ? 'btn-primary' : 'btn-outline-secondary'" @click="view = 'cards'">Картки</button>
      </div>
      <button v-if="isAdmin" class="btn btn-outline-primary btn-sm ms-auto" @click="showImport = !showImport">Додати студентів</button>
    </div>

    <div v-if="showImport" class="card mb-3">
      <div class="card-body">
        <label class="form-label">Встав список групи з ЦІСТ (шапки «Список групи …» перемикають групу) або учасників із DL (група й роль — з рядка, не студенти пропускаються); формат сайт впізнає сам, наявні студенти оновлюються, внесене ними не чіпається</label>
        <textarea v-model="importText" class="form-control font-monospace" rows="8"></textarea>
        <button class="btn btn-primary btn-sm mt-2" :disabled="!importText.trim()" @click="runImport">
          Імпортувати
        </button>
      </div>
    </div>
    <div v-if="importResult" class="alert alert-success">{{ importResult }}</div>

    <StudentFilters :students="of(students)" />
    <p v-if="active && !listed.length" class="text-secondary">Під ці фільтри ніхто не підходить.</p>
    <component :is="cards" v-else-if="view === 'cards'" :students="listed" />
    <StudentsTable v-else :students="listed" />
  </div>
</template>
