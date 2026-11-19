<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

import { lineOf, loadLabPages, pageWord, pathOf } from '../labPages.js'

// a lab's pages as a row of pills (`n`), or the pages common to all labs; the page open now is marked; a lab of one page
// has no row
const props = defineProps({ n: Number })
const route = useRoute()
const pages = computed(() => lineOf(props.n))
loadLabPages()
</script>

<template>
  <nav v-if="pages.length > (n ? 1 : 0)" class="lab-nav d-flex flex-wrap align-items-center gap-2" :aria-label="n ? 'Сторінки лаби' : 'Про лаби'">
    <span v-if="!n" class="small text-secondary me-1">Про лаби</span>
    <template v-for="p in pages" :key="p.slug">
      <span v-if="route.path === pathOf(p)" class="pill here" aria-current="page">{{ pageWord(p) }}</span>
      <RouterLink v-else :to="pathOf(p)" class="pill">{{ pageWord(p) }}</RouterLink>
    </template>
  </nav>
</template>

<style scoped>
.pill { padding: .2rem .75rem; border: 1px solid var(--bs-border-color); border-radius: 1rem; font-size: .9rem; line-height: 1.35;
        color: var(--bs-body-color); text-decoration: none; }
a.pill:hover { background: var(--bs-tertiary-bg); }
.pill.here { border-color: var(--bs-primary-border-subtle); background: var(--bs-primary-bg-subtle); color: var(--bs-primary-text-emphasis); }
</style>
