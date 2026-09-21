<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

import { getStudents, importStudents } from '../api.js'
import Avatar from '../components/Avatar.vue'
import Crumbs from '../components/Crumbs.vue'
import StudentsTable from '../components/StudentsTable.vue'
import { user } from '../user.js'

const route = useRoute()
const students = ref([])
const denied = ref(false)
const view = ref('table')
const showImport = ref(false)
const importText = ref('')
const importResult = ref('')

const isAdmin = computed(() => user.value?.status === 'admin')
const group = computed(() => route.query.group || '')  // one group as its own sub-page
const shown = computed(() => (group.value ? students.value.filter((s) => s.group === group.value) : students.value))
const crumbs = computed(() => (group.value ? [['/students', 'Студи'], group.value] : ['Студи']))
const fio = (s) => s.name || s.nick

async function load() {
  try {
    students.value = await getStudents()
  } catch {
    denied.value = true
  }
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
  <p v-if="denied" class="text-center mt-5">Сторінка для учасників курсу — увійди з поштою @nure.ua.</p>
  <div v-else>
    <Crumbs :items="crumbs" />
    <div class="d-flex align-items-center gap-2 mb-3">
      <h1 class="h3 mb-0">Студенти <span class="text-secondary fs-6">{{ group }} ({{ shown.length }})</span></h1>
      <div v-if="isAdmin" class="btn-group btn-group-sm ms-2">
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

    <StudentsTable v-if="isAdmin && view === 'table'" :students="shown" />
    <div v-else class="row g-3">
      <div v-for="s in shown" :key="s.nick" class="col-md-6 col-lg-4">
        <RouterLink :to="`/students/${s.nick}`" class="card h-100 text-decoration-none text-body">
          <img v-if="s.game.cover" :src="s.game.cover" class="card-img-top object-fit-cover cover">
          <div class="card-body">
            <div class="d-flex align-items-center gap-2">
              <Avatar :user="s" :size="28" />
              <span class="fw-semibold">{{ fio(s) }}</span>
              <span v-if="s.status === 'admin'" class="badge text-bg-secondary fw-normal">викладач</span>
              <span v-else-if="s.status === 'pending'" class="badge text-bg-warning fw-normal">очікує</span>
              <span class="text-secondary small ms-auto">{{ s.group }}</span>
            </div>
            <div v-if="s.game.id" class="mt-1">
              🎮 {{ s.game.title }}
              <div class="text-secondary small">вікон: {{ s.game.windows }} · меню: {{ s.game.menus }} · заявок: {{ s.game.claims }}</div>
            </div>
            <div v-else class="text-secondary mt-1">Гра ще не створена</div>
          </div>
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<style scoped>
.cover { height: 140px; }
</style>
