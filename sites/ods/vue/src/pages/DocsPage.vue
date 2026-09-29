<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

import Crumbs from '@core/components/Crumbs.vue'
import { loadGuide, pages } from '@core/guide.js'
import { site } from '@core/site.js'

import { KINDS } from '../site.js'

const route = useRoute()
const kind = computed(() => route.meta.kind)
const docs = computed(() => site.guide.filter((s) => s.kind === kind.value && pages.value[s.slug]))
const title = (d) => pages.value[d.slug].title.replace(/^(Тема|Завдання)\s+\d+\.\s*/, '')  // the number stands beside it
loadGuide()
</script>

<template>
  <Crumbs :items="[KINDS[kind]]" />
  <h1 class="h2 mb-3">{{ KINDS[kind] }}</h1>
  <ol class="docs list-unstyled">
    <li v-for="d in docs" :key="d.slug">
      <span class="n text-secondary">{{ d.n }}</span>
      <RouterLink :to="d.path">{{ title(d) }}</RouterLink>
    </li>
  </ol>
</template>

<style scoped>
.docs li { display: flex; gap: .75rem; padding: .35rem 0; border-bottom: 1px solid var(--bs-border-color-translucent); }
.docs .n { min-width: 1.5rem; text-align: right; font-variant-numeric: tabular-nums; }
.docs a { text-decoration: none; }
.docs a:hover { text-decoration: underline; }
</style>
