<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import Crumbs from '../components/Crumbs.vue'

import { postGame, putGame } from '../api.js'
import BaseGameForm from '../components/BaseGameForm.vue'
import { games, loadCatalog } from '../catalog.js'
import { user } from '../user.js'

const route = useRoute()
const router = useRouter()
const form = reactive({ slug: '', title: '', icon: '', klass: '', axes: {}, summary: '', description: '', status: 'draft', order: 0 })
const id = ref('')
const crumbs = computed(() => [['/games', 'Ігри'], ...(id.value ? [[`/games/${form.slug}`, form.title], 'Редагування'] : ['Нова гра'])])
const saved = ref(false)
const error = ref('')

onMounted(async () => {
  await loadCatalog()
  const g = games.value.find((x) => x.slug === route.params.slug)
  if (!g) return
  id.value = g.id
  for (const k in form) form[k] = k === 'axes' ? { ...g.axes } : g[k]
})

async function save() {
  error.value = ''
  try {
    const g = id.value ? await putGame(id.value, form) : await postGame(form)
    id.value = g.id
    saved.value = true
    setTimeout(() => (saved.value = false), 2000)
    router.replace(`/games/${g.slug}/edit`)
    await loadCatalog()
  } catch (e) {
    error.value = e.message
  }
}
</script>

<template>
  <div v-if="user?.status === 'admin'">
    <Crumbs :items="crumbs" />
    <h1 class="h3 mb-4">{{ id ? `Гра: ${form.title}` : 'Нова гра' }}</h1>

    <BaseGameForm v-model="form" @save="save" />

    <div v-if="saved" class="alert alert-success mt-3">Збережено ✓</div>
    <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
  </div>
  <p v-else class="text-center mt-5">Сторінка доступна лише викладачу.</p>
</template>
