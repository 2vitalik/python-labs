<script setup>
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'

import CoinBadge from '../components/CoinBadge.vue'
import Md from '../components/Md.vue'
import { AXES, games, KLASSES, loadCatalog, STATUSES, tasks, zones } from '../catalog.js'
import { user } from '../user.js'

const slug = useRoute().params.slug
const game = computed(() => games.value.find((g) => g.slug === slug))
const gameTasks = computed(() => tasks.value.filter((t) => !t.games.length || t.games.includes(slug)))
const byZone = computed(() => {
  const map = {}
  for (const t of gameTasks.value) (map[t.zone] ??= []).push(t)
  return map
})

onMounted(loadCatalog)
</script>

<template>
  <div v-if="game" class="col-lg-9 mx-auto">
    <RouterLink to="/games" class="d-inline-block mb-2">← До ігор</RouterLink>
    <div class="d-flex align-items-center gap-2 mb-1">
      <span class="fs-2">{{ game.icon }}</span>
      <h1 class="h3 mb-0">{{ game.title }}</h1>
      <span v-if="game.status !== 'active'" class="badge text-bg-warning">{{ STATUSES[game.status] }}</span>
      <RouterLink v-if="user?.status === 'admin'" :to="`/games/${game.slug}/edit`"
                  class="btn btn-outline-secondary btn-sm ms-auto">✏️ Редагувати</RouterLink>
    </div>
    <p class="text-secondary">{{ game.summary }}</p>
    <p class="d-flex gap-2 flex-wrap">
      <span class="badge text-bg-primary">{{ KLASSES[game.klass] }}</span>
      <span v-for="(v, k) in game.axes" :key="k" class="badge text-bg-light border text-dark fw-normal">{{ AXES[k] }}: {{ v }}</span>
    </p>
    <Md :text="game.description" class="mb-4" />

    <h2 class="h5">Завдання гри <span class="text-secondary fs-6">({{ gameTasks.length }})</span></h2>
    <div v-for="(list, z) in byZone" :key="z" class="mb-3">
      <div class="text-secondary small fw-semibold mb-1">{{ zones[z]?.icon }} {{ zones[z]?.title || z }}</div>
      <ul class="list-unstyled mb-0">
        <li v-for="t in list" :key="t.id" class="d-flex gap-2 py-1 border-bottom">
          <span>{{ t.title }}</span>
          <span v-if="t.tags.includes('algo')" title="алгоритмічне">⭐</span>
          <CoinBadge class="ms-auto" :coin="t.coin" :amount="t.amount" />
        </li>
      </ul>
    </div>
    <RouterLink :to="`/tasks?game=${slug}`" class="btn btn-outline-primary btn-sm mt-2">Відкрити в каталозі →</RouterLink>
  </div>
  <p v-else class="text-center mt-5 text-secondary">Гру не знайдено або каталог ще вантажиться…</p>
</template>
