<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

import { commons, loadLabPages, partsOf, pathOf } from '../labPages.js'

// the pages that stand together as one row of links: a lab's own page with its parts (`n`), or the pages common to all labs.
// The page open now is marked; a lab of one page has no row
const props = defineProps({ n: Number })
const route = useRoute()
const pages = computed(() => (props.n ? partsOf(props.n) : commons()))
loadLabPages()
</script>

<template>
  <nav v-if="pages.length > (n ? 1 : 0)" class="lab-parts d-flex flex-wrap align-items-baseline mb-3" :aria-label="n ? 'Сторінки лаби' : 'Про лаби'">
    <span v-if="!n" class="text-secondary me-2">Про лаби:</span>
    <template v-for="(p, i) in pages" :key="p.slug">
      <span v-if="i" class="dot text-body-tertiary">·</span>
      <RouterLink :to="pathOf(p)" :class="{ here: route.path === pathOf(p) }">{{ p.nav }}</RouterLink>
    </template>
  </nav>
</template>

<style scoped>
.lab-parts { font-size: .95rem; }
.dot { margin: 0 .5rem; }
.lab-parts a { text-decoration: none; }
.lab-parts a:hover { text-decoration: underline; }
.lab-parts a.here { color: var(--bs-body-color); font-weight: 600; pointer-events: none; }
</style>
