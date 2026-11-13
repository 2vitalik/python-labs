<script setup>
import { computed, onMounted, ref, watchEffect } from 'vue'
import { useRoute } from 'vue-router'

import { getStudents, importStudents } from '../api.js'
import Crumbs from '../components/Crumbs.vue'
import StudentFilters from '../components/StudentFilters.vue'
import StudentsTable from '../components/StudentsTable.vue'
import { load as recall, save } from '../local.js'
import { site } from '../site.js'
import { byGroup, keepOrder, useStudentFilter } from '../studentFilter.js'
import { studentsCrumbs, studentsHome } from '../students.js'
import { useTitle } from '../title.js'
import { user } from '../user.js'

// the admin's list of everyone; a student sees the slice the API gives them under the site's name for it (students.js)
const students = ref([])
const cards = site.students.cards  // the site's gallery, when it has one
const isAdmin = computed(() => user.value?.status === 'admin')
const route = useRoute()
// the look last chosen is remembered, so the menu's link comes back to it; a link with ?view= says its own
const view = ref((cards && (route.query.view || recall('students-view') || (isAdmin.value ? 'table' : 'cards'))) === 'cards' ? 'cards' : 'table')
const look = (v) => { view.value = v; save('students-view', v) }
const showImport = ref(false)
const importText = ref('')
const importResult = ref('')

const { shown, picked, active, q, setQ, restore } = useStudentFilter(students)
restore()
// the gallery may be of some only (site.students.inGallery): the numbers in the heading and on the chips follow the view
const of = (list) => (view.value === 'cards' && site.students.inGallery ? list.filter(site.students.inGallery) : list)
const listed = computed(() => of(shown.value))
const total = computed(() => of(students.value).length)
const group = computed(() => picked.value.join(', '))  // picked groups read as a sub-page: crumb + title
const home = computed(() => studentsHome())
const crumbs = computed(() => studentsCrumbs(...(group.value ? [group.value] : [])))
useTitle(() => [home.value.name, group.value].filter(Boolean).join(' '))
// the rows in the order they are seen, for paging on a student's page; not on the way out, when the query is the next page's
const here = route.path
const seen = computed(() => (view.value === 'cards' ? listed.value : byGroup(listed.value).flatMap((g) => g.list)))
watchEffect(() => { if (route.path === here && students.value.length) keepOrder(seen.value.map((s) => s.nick)) })

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
    <div class="d-flex flex-wrap align-items-center gap-2 mb-3">
      <h1 class="h3 mb-0">{{ home.name }} <span class="text-secondary fs-6">{{ group }} ({{ listed.length }}{{ active ? ` з ${total}` : '' }})</span></h1>
      <div v-if="cards" class="btn-group btn-group-sm ms-2">
        <button class="btn" :class="view === 'table' ? 'btn-primary' : 'btn-outline-secondary'" @click="look('table')">Таблиця</button>
        <button class="btn" :class="view === 'cards' ? 'btn-primary' : 'btn-outline-secondary'" @click="look('cards')">Картки</button>
      </div>
      <input type="search" :value="q" class="form-control form-control-sm w-auto ms-auto" placeholder="Пошук: ПІБ, нік…"
             title="За початком слова: прізвище, імʼя, нік, Telegram" @input="setQ($event.target.value)">
      <button v-if="isAdmin" class="btn btn-outline-primary btn-sm" @click="showImport = !showImport">Додати студентів</button>
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
