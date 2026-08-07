<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { postTask, putTask } from '../api.js'
import TaskForm from '../components/TaskForm.vue'
import { loadCatalog, tasks } from '../catalog.js'
import { user } from '../user.js'

const route = useRoute()
const router = useRouter()
const form = reactive({
  slug: '', title: '', description: '', zone: route.query.zone || 'entities', subzone: route.query.sub || '',
  tags: '', games: '', coin: '', amount: 1, max_count: 1, parent: route.query.parent || '', status: 'draft', order: 0,
})
const id = ref('')
const saved = ref(false)
const error = ref('')
const csv = (s) => s.split(',').map((x) => x.trim()).filter(Boolean)

onMounted(async () => {
  await loadCatalog()
  const t = tasks.value.find((x) => x.slug === route.params.slug)
  if (!t) return
  id.value = t.id
  for (const k in form) {
    if (k === 'tags' || k === 'games') form[k] = t[k].join(', ')
    else form[k] = t[k]
  }
})

async function save() {
  error.value = ''
  const payload = { ...form, tags: csv(form.tags), games: csv(form.games) }
  try {
    const t = id.value ? await putTask(id.value, payload) : await postTask(payload)
    id.value = t.id
    saved.value = true
    setTimeout(() => (saved.value = false), 2000)
    router.replace(`/tasks/${t.slug}/edit`)
    await loadCatalog()
  } catch (e) {
    error.value = e.message
  }
}
</script>

<template>
  <div v-if="user?.status === 'admin'" class="col-lg-8 mx-auto">
    <RouterLink :to="`/tasks?zone=${form.zone}`" class="d-inline-block mb-2">← До каталогу</RouterLink>
    <h1 class="h3 mb-4">{{ id ? `Завдання: ${form.title}` : 'Нове завдання' }}</h1>

    <TaskForm v-model="form" @save="save" />

    <div v-if="saved" class="alert alert-success mt-3">Збережено ✓</div>
    <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
  </div>
  <p v-else class="text-center mt-5">Сторінка доступна лише викладачу.</p>
</template>
