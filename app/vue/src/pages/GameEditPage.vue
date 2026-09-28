<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import Crumbs from '../components/Crumbs.vue'

import { postGame, putGame } from '../api.js'
import BaseGameForm from '../components/BaseGameForm.vue'
import { games, loadCatalog } from '../catalog.js'
import { problem } from '../problem.js'
import { useTitle } from '../title.js'
import { user } from '../user.js'

const route = useRoute()
const router = useRouter()
const form = reactive({ slug: '', title: '', icon: '', klass: '', axes: {}, summary: '', description: '', examples: '', status: 'draft', order: 0 })
const id = ref('')
useTitle(() => id.value && `Гра: ${form.title}`)
const crumbs = computed(() => [['/method', 'Методичка'], ['/games', 'Ігри'], ...(id.value ? [[`/games/${form.slug}`, form.title], 'Редагування'] : ['Нова гра'])])
const saved = ref(false)
const error = ref('')

onMounted(async () => {
  await loadCatalog()
  const g = games.value.find((x) => x.slug === route.params.slug)
  if (!g && route.params.slug) problem.value = 'lost'
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
    <div class="d-flex align-items-baseline gap-3 mb-4">
      <h1 class="h3 mb-0 me-auto">{{ id ? `Гра: ${form.title}` : 'Нова гра' }}</h1>
      <RouterLink v-if="id" :to="`/games/history?slug=${route.params.slug}`" class="small text-decoration-none">🕘 історія</RouterLink>
    </div>

    <BaseGameForm v-model="form" @save="save" />

    <div v-if="saved" class="alert alert-success mt-3">Збережено ✓</div>
    <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
  </div>
  <p v-else class="text-center mt-5">Сторінка доступна лише викладачу.</p>
</template>
