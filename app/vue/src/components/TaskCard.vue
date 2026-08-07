<script setup>
import { computed, ref } from 'vue'

import { COINS, kidsOf, STATUSES } from '../catalog.js'
import { user } from '../user.js'
import CoinBadge from './CoinBadge.vue'
import Md from './Md.vue'

const props = defineProps({ task: Object })
const open = ref(false)
const kids = computed(() => kidsOf.value[props.task.slug] || [])
// family shows the min‥max range of its children's coins instead of the card's reference coin
const range = computed(() => {
  const present = Object.keys(COINS).filter((c) => kids.value.some((k) => k.coin === c))
  if (!present.length) return []
  return present.length === 1 || present[0] === present.at(-1) ? [present[0]] : [present[0], present.at(-1)]
})
</script>

<template>
  <div class="border rounded mb-1 task" :class="{ stack: kids.length, ['st-' + task.status]: true }">
    <div class="d-flex align-items-start gap-2 px-2 py-1" role="button" @click="open = !open">
      <span class="title me-auto">
        {{ task.title }}
        <span v-if="task.tags.includes('algo')" class="ms-1" title="алгоритмічне — золото">⭐</span>
        <span v-if="task.max_count !== 1" class="ms-1" title="можна зараховувати кілька разів">🔁</span>
        <span v-if="user?.status === 'admin' && task.status !== 'active'"
              class="badge text-bg-light border text-secondary fw-normal ms-1">{{ STATUSES[task.status] }}</span>
      </span>
      <span v-if="kids.length" class="badge fam" title="сімʼя: кілька варіантів, кожен зі своєю ціною">×{{ kids.length }}</span>
      <span v-if="kids.length" class="text-nowrap" title="діапазон цін варіантів">
        <template v-for="(c, i) in range" :key="c"><span v-if="i" class="text-secondary">‥</span>{{ COINS[c] }}</template>
      </span>
      <CoinBadge v-else :coin="task.coin" :amount="task.amount" />
    </div>

    <div v-if="open" class="px-2 py-2 border-top rounded-bottom" :class="kids.length ? 'bg-body' : 'bg-body-tertiary'">
      <div v-if="task.description || user?.status === 'admin'" class="d-flex align-items-start gap-2 mb-2">
        <Md v-if="task.description" :text="task.description" class="small flex-grow-1" />
        <RouterLink v-if="user?.status === 'admin'" :to="`/tasks/${task.slug}/edit`"
                    class="ms-auto text-decoration-none" title="Редагувати">✏️</RouterLink>
      </div>
      <TaskCard v-for="k in kids" :key="k.id" :task="k" />
      <div v-if="task.max_count !== 1 || task.games.length"
           class="d-flex gap-2 flex-wrap align-items-center small mt-2">
        <span v-if="task.max_count === 0" class="text-secondary">без ліміту повторів</span>
        <span v-else-if="task.max_count > 1" class="text-secondary">до {{ task.max_count }} разів</span>
        <RouterLink v-for="g in task.games" :key="g" :to="`/games/${g}`"
                    class="badge text-bg-light border fw-normal text-decoration-none game-tag">{{ g }}</RouterLink>
      </div>
    </div>
  </div>
</template>

<style scoped>
.task { background: var(--bs-body-bg); }
/* family looks like a small stack of cards */
.stack { box-shadow: 3px 3px 0 -1px var(--bs-body-bg), 3px 3px 0 0 var(--bs-border-color); }
.fam { background: var(--bs-tertiary-bg); color: var(--bs-secondary-color); border: 1px solid var(--bs-border-color); }
.game-tag { color: var(--bs-link-color); }
/* drafts fade into the background instead of shouting */
.st-draft { border-style: dashed; }
.st-draft > div > .title { color: var(--bs-secondary-color); }
.st-archived { opacity: .5; }
.st-archived > div > .title { text-decoration: line-through; }
</style>
