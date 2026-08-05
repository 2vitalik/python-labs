<script setup>
import { ref } from 'vue'

import { STATUSES } from '../catalog.js'
import { user } from '../user.js'
import CoinBadge from './CoinBadge.vue'
import Md from './Md.vue'

defineProps({ task: Object })
const open = ref(false)
</script>

<template>
  <div class="border rounded mb-1">
    <div class="d-flex align-items-center gap-2 px-2 py-1" role="button" @click="open = !open">
      <span>{{ task.title }}</span>
      <span v-if="task.tags.includes('algo')" title="алгоритмічне — золото">⭐</span>
      <span v-if="task.variants.length" class="badge text-bg-light border text-secondary">{{ task.variants.length }} вар.</span>
      <span v-if="task.max_count !== 1" title="можна зараховувати кілька разів">🔁</span>
      <span v-if="user?.status === 'admin' && task.status !== 'active'" class="badge text-bg-warning">{{ STATUSES[task.status] }}</span>
      <CoinBadge class="ms-auto" :coin="task.coin" :amount="task.amount" />
    </div>

    <div v-if="open" class="px-3 py-2 border-top bg-body-tertiary rounded-bottom">
      <Md v-if="task.description" :text="task.description" class="mb-2" />
      <table v-if="task.variants.length" class="table table-sm w-auto mb-2">
        <tbody>
          <tr v-for="v in task.variants" :key="v.slug">
            <td>{{ v.title }}</td>
            <td class="text-end ps-3"><CoinBadge :coin="v.coin" :amount="v.amount" /></td>
          </tr>
        </tbody>
      </table>
      <div class="d-flex gap-2 flex-wrap align-items-center small">
        <span v-if="task.max_count === 0" class="text-secondary">без ліміту повторів</span>
        <span v-else-if="task.max_count > 1" class="text-secondary">до {{ task.max_count }} разів</span>
        <span v-for="g in task.games" :key="g" class="badge text-bg-light border text-dark">{{ g }}</span>
        <span v-if="!task.games.length" class="text-secondary">універсальне</span>
        <RouterLink v-if="user?.status === 'admin'" :to="`/tasks/${task.slug}/edit`" class="ms-auto">✏️ Редагувати</RouterLink>
      </div>
    </div>
  </div>
</template>
