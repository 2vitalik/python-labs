<script setup>
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'

import Crumbs from '../components/Crumbs.vue'
import Md from '../components/Md.vue'
import TaskCatalog from '../components/TaskCatalog.vue'
import { AXES, games, KLASSES, loadCatalog, STATUSES } from '../catalog.js'
import { useTaskFilter } from '../taskFilter.js'
import { user } from '../user.js'

const slug = useRoute().params.slug
const game = computed(() => games.value.find((g) => g.slug === slug))
const { grouped } = useTaskFilter(slug)
const shown = computed(() => grouped.value.reduce((n, z) => n + z.subs.reduce((m, s) => m + s.list.length, 0), 0))

onMounted(loadCatalog)
</script>

<template>
  <div v-if="game">
    <Crumbs :items="[['/games', 'Ігри'], game.title]" />
    <div class="d-flex align-items-center gap-2 mb-1">
      <span class="fs-2">{{ game.icon }}</span>
      <h1 class="h3 mb-0">{{ game.title }}</h1>
      <span v-if="game.status !== 'active'" class="badge text-bg-light border text-secondary fw-normal">{{ STATUSES[game.status] }}</span>
      <RouterLink v-if="user?.status === 'admin'" :to="`/games/${game.slug}/edit`"
                  class="ms-auto text-decoration-none" title="Редагувати">✏️</RouterLink>
    </div>
    <p class="text-secondary">{{ game.summary }}</p>
    <p class="d-flex gap-2 flex-wrap">
      <span class="badge text-bg-primary">{{ KLASSES[game.klass] }}</span>
      <span v-for="(v, k) in game.axes" :key="k" class="badge text-bg-light border text-dark fw-normal">{{ AXES[k] }}: {{ v }}</span>
    </p>
    <Md :text="game.description" class="mb-4" />

    <h2 class="h5">Завдання гри <span class="count fs-6">({{ shown }})</span></h2>
    <p class="text-secondary small">Лише специфічні для цієї гри; універсальні — у <RouterLink to="/tasks?game=universal">каталозі</RouterLink>.</p>
    <TaskCatalog :game="slug" />
  </div>
  <p v-else class="text-center mt-5 text-secondary">Гру не знайдено або каталог ще вантажиться…</p>
</template>

<style scoped>
.count { font-weight: 400; opacity: .55; }
</style>
