<script setup>
import { computed, ref } from 'vue'

import { COINS, STATUSES } from '../catalog.js'
import { user } from '../user.js'
import CoinBadge from './CoinBadge.vue'
import Md from './Md.vue'

const props = defineProps({ task: Object })
const open = ref(false)
// family header shows the set of variant coins instead of the card's reference coin
const famCoins = computed(() => Object.keys(COINS).filter((c) => props.task.variants.some((v) => v.coin === c)))
</script>

<template>
  <div class="border rounded mb-1 task" :class="{ stack: task.variants.length, ['st-' + task.status]: true }">
    <div class="d-flex align-items-center gap-2 px-2 py-1" role="button" @click="open = !open">
      <span class="title">{{ task.title }}</span>
      <span v-if="task.tags.includes('algo')" title="алгоритмічне — золото">⭐</span>
      <span v-if="task.max_count !== 1" title="можна зараховувати кілька разів">🔁</span>
      <span v-if="user?.status === 'admin' && task.status !== 'active'"
            class="badge text-bg-light border text-secondary fw-normal">{{ STATUSES[task.status] }}</span>
      <span v-if="task.variants.length" class="badge text-bg-primary ms-auto" title="сімʼя: кілька варіантів, кожен зі своєю ціною">×{{ task.variants.length }}</span>
      <span v-if="task.variants.length" class="text-nowrap" title="монетки варіантів">
        <span v-for="c in famCoins" :key="c">{{ COINS[c] }}</span>
      </span>
      <CoinBadge v-else class="ms-auto" :coin="task.coin" :amount="task.amount" />
    </div>

    <div v-if="open" class="px-2 py-2 border-top bg-body-tertiary rounded-bottom">
      <Md v-if="task.description" :text="task.description" class="mb-2 small" />
      <div v-for="v in task.variants" :key="v.slug"
           class="border rounded bg-body d-flex align-items-center gap-2 px-2 py-1 mb-1">
        <span>{{ v.title }}</span>
        <CoinBadge class="ms-auto" :coin="v.coin" :amount="v.amount" />
      </div>
      <div class="d-flex gap-2 flex-wrap align-items-center small mt-2">
        <span v-if="task.max_count === 0" class="text-secondary">без ліміту повторів</span>
        <span v-else-if="task.max_count > 1" class="text-secondary">до {{ task.max_count }} разів</span>
        <span v-for="g in task.games" :key="g" class="badge text-bg-light border text-dark">{{ g }}</span>
        <span v-if="!task.games.length" class="text-secondary">універсальне</span>
        <RouterLink v-if="user?.status === 'admin'" :to="`/tasks/${task.slug}/edit`" class="ms-auto">✏️ Редагувати</RouterLink>
      </div>
    </div>
  </div>
</template>

<style scoped>
.task { background: var(--bs-body-bg); }
/* family looks like a small stack of cards */
.stack { box-shadow: 3px 3px 0 -1px var(--bs-body-bg), 3px 3px 0 0 var(--bs-border-color); }
/* drafts fade into the background instead of shouting */
.st-draft { border-style: dashed; }
.st-draft .title { color: var(--bs-secondary-color); }
.st-archived { opacity: .5; }
.st-archived .title { text-decoration: line-through; }
</style>
