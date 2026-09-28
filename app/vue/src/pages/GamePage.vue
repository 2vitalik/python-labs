<script setup>
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'

import Crumbs from '../components/Crumbs.vue'
import GuideText from '../components/GuideText.vue'
import TaskCatalog from '../components/TaskCatalog.vue'
import { AXES, games, KLASSES, loadCatalog, STATUSES } from '../catalog.js'
import { problem } from '../problem.js'
import { useTaskFilter } from '../taskFilter.js'
import { useTitle } from '../title.js'
import { user } from '../user.js'

const slug = useRoute().params.slug
const game = computed(() => games.value.find((g) => g.slug === slug))
useTitle(() => game.value?.title)
// one text for the guide's renderer: it draws the field grids of the examples
const EXAMPLES = '## Приклади ігрових ситуацій {#examples}\n\nСиня рамка — хто щойно зробив хід, жовта — що змінилось на полі.'
const text = computed(() => [game.value.description, game.value.examples && `${EXAMPLES}\n\n${game.value.examples}`].filter(Boolean).join('\n\n'))
const { grouped } = useTaskFilter(slug)
const shown = computed(() => grouped.value.reduce((n, z) => n + z.subs.reduce((m, s) => m + s.list.length, 0), 0))

const SHOW_TASKS = false  // «Завдання гри» hidden until the catalog has enough per-game cards (T125 п. 44)

onMounted(async () => {
  await loadCatalog()
  if (!game.value) problem.value = 'lost'
})
</script>

<template>
  <div v-if="game">
    <Crumbs :items="[['/method', 'Методичка'], ['/games', 'Ігри'], game.title]" />
    <div class="d-flex align-items-center gap-2 mb-1">
      <span class="fs-2">{{ game.icon }}</span>
      <h1 class="h3 mb-0">{{ game.title }}</h1>
      <span v-if="game.status !== 'active'" class="badge text-bg-light border text-secondary fw-normal">{{ STATUSES[game.status] }}</span>
      <RouterLink v-if="user?.status === 'admin'" :to="`/games/${game.slug}/edit`"
                  class="ms-auto text-decoration-none" title="Редагувати">✏️</RouterLink>
      <RouterLink v-if="user?.status === 'admin'" :to="`/games/history?slug=${game.slug}`"
                  class="text-decoration-none" title="Історія правок">🕘</RouterLink>
    </div>
    <p class="text-secondary">{{ game.summary }}</p>
    <p class="d-flex gap-2 flex-wrap">
      <span class="badge text-bg-primary">{{ KLASSES[game.klass] }}</span>
      <span v-for="(v, k) in game.axes" :key="k" class="badge text-bg-light border text-dark fw-normal">{{ AXES[k] }}: {{ v }}</span>
    </p>
    <GuideText :text class="mb-4" />

    <template v-if="SHOW_TASKS">
      <h2 id="catalog" class="h5">Завдання гри <span class="count fs-6">({{ shown }})</span></h2>
      <p class="text-secondary small">Лише специфічні для цієї гри; універсальні — у <RouterLink to="/tasks?game=universal">каталозі</RouterLink>.</p>
      <TaskCatalog :game="slug" />
    </template>
  </div>
</template>

<style scoped>
.count { font-weight: 400; opacity: .55; }
#catalog { scroll-margin-top: 1rem; }
</style>
