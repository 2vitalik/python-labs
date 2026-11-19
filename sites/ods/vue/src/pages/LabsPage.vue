<script setup>
import { computed, ref } from 'vue'

import Crumbs from '@core/components/Crumbs.vue'
import { loadGuide, pages } from '@core/guide.js'
import { user } from '@core/user.js'

import LabNav from '../components/LabNav.vue'
import { commons, labsWithCards, loadLabPages } from '../labPages.js'
import { LABS } from '../site.js'

// /labs: the pages common to all labs, then the labs that have a guide page — each with «Моя лаба» once it has cards,
// and the teacher's «Результати»; the teacher's archive of the old labs below
const ready = ref(false)
const held = ref([])
const admin = computed(() => user.value?.status === 'admin')
const labs = computed(() => LABS.filter((l) => pages.value[l.slug]))
const title = (l) => pages.value[l.slug].title.replace(/^(Лабораторна|Завдання)\s+\d+\.\s*/, '')  // the number stands beside it
const mine = (l) => held.value.some((c) => c.n === l.n)
Promise.all([loadGuide(), labsWithCards().then((l) => (held.value = l)), loadLabPages().catch(() => null)]).then(() => (ready.value = true))
</script>

<template>
  <Crumbs :items="['Лаби']" />
  <h1 class="h2 mb-3">Лаби</h1>
  <template v-if="ready">
    <section v-if="commons().length" class="mb-4">
      <LabNav class="mb-1" />
      <div class="small text-secondary">спільне для всіх лаб: як працюємо, оцінювання, захист, здача</div>
    </section>
    <ol class="labs list-unstyled">
      <li v-for="l in labs" :key="l.slug" class="position-relative">
        <span class="n text-secondary">{{ l.n }}</span>
        <RouterLink :to="l.path" class="stretched-link">{{ title(l) }}</RouterLink>
        <span v-if="mine(l)" class="acts btn-group btn-group-sm ms-auto text-nowrap">
          <RouterLink :to="`/labs/${l.n}/my`" class="btn btn-outline-primary">Моя лаба</RouterLink>
          <RouterLink v-if="admin" :to="`/labs/${l.n}/results`" class="btn btn-outline-secondary">Результати</RouterLink>
        </span>
      </li>
    </ol>
    <RouterLink v-if="admin" to="/labs/old" class="old small d-inline-block mt-3">Архів: старі лаби</RouterLink>
  </template>
</template>

<style scoped>
.labs li { display: flex; align-items: center; gap: .75rem; padding: .45rem .5rem; border-bottom: 1px solid var(--bs-border-color-translucent); }
.labs li:hover { background: var(--bs-tertiary-bg); }
.labs .n { min-width: 1.5rem; text-align: right; font-variant-numeric: tabular-nums; }
.labs a.stretched-link { text-decoration: none; }
.acts { position: relative; z-index: 2; }  /* above the row's link, which covers the whole row */
.old { color: var(--bs-secondary-color); text-decoration: underline dashed; text-underline-offset: .2em; }
.old:hover { color: var(--bs-body-color); }
</style>
