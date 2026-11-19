<script setup>
import { computed, ref } from 'vue'

import Crumbs from '@core/components/Crumbs.vue'
import { loadGuide, pages } from '@core/guide.js'
import { user } from '@core/user.js'

import LabGate from '../components/LabGate.vue'
import LabNav from '../components/LabNav.vue'
import { gates, loadGates } from '../labGates.js'
import { commons, labsWithCards, loadLabPages } from '../labPages.js'
import { LABS } from '../site.js'

// /labs: the pages common to all labs, then the labs that have a guide page — each with «Моя лаба» once it has cards,
// and the teacher's «Результати»; a lab hidden from students (labGates.js) is in the teacher's list only, with the
// switch of how open it is on every row; the teacher's archive of the old labs below
const ready = ref(false)
const held = ref([])
const admin = computed(() => user.value?.status === 'admin')
const labs = computed(() => LABS.filter((l) => pages.value[l.slug]))
const title = (l) => pages.value[l.slug].title.replace(/^(Лабораторна|Завдання)\s+\d+\.\s*/, '')  // the number stands beside it
const mine = (l) => held.value.some((c) => c.n === l.n)
Promise.all([loadGuide(), loadGates(), labsWithCards().then((l) => (held.value = l)), loadLabPages().catch(() => null)])
  .then(() => (ready.value = true))
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
      <li v-for="l in labs" :key="l.slug" class="position-relative" :class="{ shut: gates[l.n] === 'hidden' }">
        <span class="n text-secondary">{{ l.n }}</span>
        <RouterLink :to="l.path" class="stretched-link">{{ title(l) }}</RouterLink>
        <span class="acts d-flex align-items-center gap-2 ms-auto text-nowrap">
          <LabGate v-if="admin" :n="l.n" />
          <span v-else-if="gates[l.n] === 'telegram'" class="small text-secondary">здаємо в Telegram</span>
          <span v-if="mine(l)" class="btn-group btn-group-sm">
            <RouterLink :to="`/labs/${l.n}/my`" class="btn btn-outline-primary">Моя лаба</RouterLink>
            <RouterLink v-if="admin" :to="`/labs/${l.n}/results`" class="btn btn-outline-secondary">Результати</RouterLink>
          </span>
        </span>
      </li>
    </ol>
    <RouterLink v-if="admin" to="/labs/old" class="old small d-inline-block mt-3">Архів: старі лаби</RouterLink>
  </template>
</template>

<style scoped>
/* on a narrow screen the row's actions go under the title, to the right, and wrap among themselves */
.labs li { display: flex; flex-wrap: wrap; align-items: center; gap: .35rem .75rem; padding: .45rem .5rem; border-bottom: 1px solid var(--bs-border-color-translucent); }
.labs li:hover { background: var(--bs-tertiary-bg); }
.labs .n { min-width: 1.5rem; text-align: right; font-variant-numeric: tabular-nums; }
.labs a.stretched-link { flex: 1 1 12rem; min-width: 0; text-decoration: none; }
.labs .shut a.stretched-link { color: var(--bs-secondary-color); }  /* students do not see this lab */
.acts { position: relative; z-index: 2; flex-wrap: wrap; justify-content: flex-end; }  /* above the row's link, which covers the whole row */
.old { color: var(--bs-secondary-color); text-decoration: underline dashed; text-underline-offset: .2em; }
.old:hover { color: var(--bs-body-color); }
</style>
