<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { usePolling } from '../activity.js'
import { getPolls } from '../api.js'
import Crumbs from '../components/Crumbs.vue'
import PollCard from '../components/PollCard.vue'
import PollChats from '../components/PollChats.vue'

// every poll, newest first, with where it went and how many answer; ?tag= — one kind of them. Refreshes itself while a poll is open
const route = useRoute()
const router = useRouter()
const polls = ref([])
const tags = ref([])
const loaded = ref(false)
const error = ref('')
const tag = computed(() => route.query.tag || '')

async function load() {
  try {
    const data = await getPolls({ tag: tag.value })
    polls.value = data.polls
    tags.value = data.tags
    error.value = ''
  } catch (e) {
    error.value = e.message
  }
  loaded.value = true
}
watch(tag, load, { immediate: true })
usePolling(() => polls.value.some((p) => p.status === 'open') && load(), 20)
const pick = (t) => router.replace({ query: { ...route.query, tag: t === tag.value ? undefined : t } })
</script>

<template>
  <div>
    <Crumbs :items="['Опитування']" />
    <div class="d-flex flex-wrap align-items-center gap-2 mb-3">
      <h1 class="h3 mb-0 me-auto">Опитування</h1>
      <RouterLink to="/polls/new" class="btn btn-primary btn-sm">➕ Нове опитування</RouterLink>
      <RouterLink to="/polls/templates" class="btn btn-outline-secondary btn-sm">📋 Шаблони</RouterLink>
      <RouterLink :to="{ path: '/polls/matrix', query: tag ? { tag } : {} }" class="btn btn-outline-secondary btn-sm">▦ Таблиця</RouterLink>
    </div>
    <div v-if="tags.length" class="d-flex flex-wrap gap-1 mb-3">
      <button type="button" class="btn btn-sm chip" :class="!tag ? 'btn-secondary' : 'btn-outline-secondary'" @click="pick('')">усі</button>
      <button v-for="t in tags" :key="t" type="button" class="btn btn-sm chip" :class="t === tag ? 'btn-secondary' : 'btn-outline-secondary'"
              @click="pick(t)">#{{ t }}</button>
    </div>
    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <div class="vstack gap-2">
      <PollCard v-for="p in polls" :key="p.id" :p />
    </div>
    <p v-if="loaded && !polls.length && !error" class="text-secondary text-center my-4">
      <template v-if="tag">З тегом #{{ tag }} опитувань нема.</template>
      <template v-else>Опитувань ще нема. Натисни «Нове опитування» — або спершу збери в «Шаблонах» ті, що повторюються.</template>
    </p>

    <details class="mt-4">
      <summary class="text-secondary">📍 Куди бот може слати</summary>
      <PollChats class="mt-2" />
    </details>
  </div>
</template>

<style scoped>
summary { cursor: pointer; }
</style>
