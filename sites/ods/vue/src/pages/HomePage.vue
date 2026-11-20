<script setup>
import { computed, ref, watch } from 'vue'

import StartSteps from '@core/components/StartSteps.vue'
import { loadGuide, pages } from '@core/guide.js'
import { site } from '@core/site.js'
import { canAccess, user } from '@core/user.js'

import '../labColors.css'
import LabMine from '../components/LabMine.vue'
import { labsWithCards } from '../labPages.js'
import { KINDS } from '../site.js'

// the home page: the first steps, the lectures and the labs, and — for a student with cards — their own labs, each in a
// few words (LabMine): where it is handed in, the deadline, what the site has
const active = computed(() => canAccess('active'))
const known = ref(false)  // the guide's list is here: a number counts the pages this reader has — a hidden lab is not one
const mine = ref([])
const count = (kind) => site.guide.filter((s) => s.kind === kind && pages.value[s.slug]).length
const firstName = computed(() => user.value.first_name || user.value.name?.split(' ')[0] || user.value.email)
const labTitle = (n) => (pages.value[`lab${n}`]?.title || '').replace(/^(Лабораторна|Завдання)\s+\d+\.\s*/, '')
watch(active, async (a) => {
  if (!a) return
  const [, labs] = await Promise.all([loadGuide(), labsWithCards()])
  mine.value = labs.filter((l) => l.mine)
  known.value = true
}, { immediate: true })
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
            <div class="text-secondary">{{ known ? count(kind) : ' ' }}</div>
          </div>
        </RouterLink>
      </div>
    </div>
    <section v-if="mine.length" class="mt-4">
      <h2 class="h5 mb-2">Мої лаби</h2>
      <RouterLink v-for="m in mine" :key="m.n" :to="`/labs/${m.n}/my`" class="my-lab">
        <span class="lab-n lab-tint" :class="`lab-c${m.n}`">{{ m.n }}</span>
        <span class="text-body">{{ labTitle(m.n) }}</span>
        <LabMine :m class="small ms-auto" />
      </RouterLink>
    </section>
  </div>
</template>

<style scoped>
.my-lab { display: flex; flex-wrap: wrap; align-items: center; gap: .35rem .75rem; padding: .45rem .5rem; border-bottom: 1px solid var(--bs-border-color-translucent);
          text-decoration: none; }
.my-lab:hover { background: var(--bs-tertiary-bg); }
</style>
