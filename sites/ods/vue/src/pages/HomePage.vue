<script setup>
import { computed, ref, watch } from 'vue'

import StartSteps from '@core/components/StartSteps.vue'
import { loadGuide, pages } from '@core/guide.js'
import { site } from '@core/site.js'
import { canAccess, user } from '@core/user.js'

import { KINDS } from '../site.js'

const active = computed(() => canAccess('active'))
const known = ref(false)  // the guide's list is here: a number counts the pages this reader has — a hidden lab is not one
const count = (kind) => site.guide.filter((s) => s.kind === kind && pages.value[s.slug]).length
const firstName = computed(() => user.value.first_name || user.value.name?.split(' ')[0] || user.value.email)
watch(active, (a) => a && loadGuide().then(() => (known.value = true)), { immediate: true })
</script>

<template>
  <div>
    <h1 class="mb-1">Основи Data Science</h1>
    <p class="text-secondary mb-4">Лекції, слайди й лабораторні курсу<template v-if="user">. Привіт, {{ firstName }}!</template></p>
    <StartSteps />
    <div v-if="active" class="row g-3">
      <div v-for="(title, kind) in KINDS" :key="kind" class="col-sm-6">
        <RouterLink :to="`/${kind}`" class="card h-100 text-decoration-none">
          <div class="card-body">
            <div class="h4 mb-1">{{ title }}</div>
            <div class="text-secondary">{{ known ? count(kind) : ' ' }}</div>
          </div>
        </RouterLink>
      </div>
    </div>
  </div>
</template>
