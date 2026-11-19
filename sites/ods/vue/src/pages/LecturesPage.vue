<script setup>
import { computed } from 'vue'

import Crumbs from '@core/components/Crumbs.vue'
import { loadGuide, pages } from '@core/guide.js'

import LectureFind from '../components/LectureFind.vue'
import { labsOf, lectures, shortTitle } from '../lectures.js'

// the lectures: search over their texts above, the list stays under the results; a pill — a lab that needs the lecture
const list = computed(lectures)
loadGuide()
</script>

<template>
  <Crumbs :items="['Лекції']" />
  <h1 class="h2 mb-3">Лекції</h1>
  <LectureFind />
  <ol class="docs list-unstyled">
    <li v-for="d in list" :key="d.slug">
      <span class="n text-secondary">{{ d.n }}</span>
      <RouterLink :to="d.path">{{ shortTitle(pages[d.slug].title) }}</RouterLink>
      <span class="labs">
        <RouterLink v-for="lab in labsOf(d.n)" :key="lab" :to="`/labs/${lab}`" :title="`Лекція потрібна для лаби ${lab}`"
                    class="lab badge rounded-pill border fw-normal text-body-secondary">Лаба {{ lab }}</RouterLink>
      </span>
    </li>
  </ol>
</template>

<style scoped>
.docs li { display: flex; align-items: baseline; gap: .75rem; padding: .35rem 0; border-bottom: 1px solid var(--bs-border-color-translucent); }
.docs .n { min-width: 1.5rem; text-align: right; font-variant-numeric: tabular-nums; }
.docs a { text-decoration: none; }
.docs a:hover { text-decoration: underline; }
.labs { display: flex; gap: .25rem; margin-left: auto; flex-shrink: 0; }
.docs .lab:hover { text-decoration: none; color: var(--bs-body-color) !important; }
</style>
