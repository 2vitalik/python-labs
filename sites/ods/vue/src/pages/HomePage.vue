<script setup>
import { computed } from 'vue'

import { site } from '@core/site.js'
import { canAccess, user } from '@core/user.js'

import { KINDS } from '../site.js'

const active = computed(() => canAccess('active'))
const count = (kind) => site.guide.filter((s) => s.kind === kind).length
const firstName = computed(() => user.value.first_name || user.value.name?.split(' ')[0] || user.value.email)
</script>

<template>
  <div>
    <h1 class="mb-1">Основи Data Science</h1>
    <p class="text-secondary mb-4">Лекції, слайди й лабораторні курсу<template v-if="user">. Привіт, {{ firstName }}!</template></p>
    <div v-if="active" class="row g-3">
      <div v-for="(title, kind) in KINDS" :key="kind" class="col-sm-6">
        <RouterLink :to="`/${kind}`" class="card h-100 text-decoration-none">
          <div class="card-body">
            <div class="h4 mb-1">{{ title }}</div>
            <div class="text-secondary">{{ count(kind) }}</div>
          </div>
        </RouterLink>
      </div>
    </div>
    <p v-else-if="user">Акаунт чекає підтвердження викладача. Щойно підтвердить, тут зʼявляться лекції й лаби.</p>
    <p v-else>Щоб читати, <RouterLink to="/login">увійди</RouterLink> з поштою NURE.</p>
  </div>
</template>
