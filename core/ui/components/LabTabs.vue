<script setup>
import { pages } from '../guide.js'

// from one lab to any other without scrolling to the page's end (T291 §10): the numbers of all labs as the last crumb,
// the current one filled, a lab's title under the mouse. `labs` — site.guide entries with `n`
defineProps({ labs: Array, n: Number })
</script>

<template>
  <span class="labtabs">
    <RouterLink v-for="l in labs" :key="l.n" :to="l.path" class="tab" :class="{ on: l.n === n }" :aria-current="l.n === n ? 'page' : null"
                :title="pages[l.slug]?.title || `Лаба ${l.n}`">{{ l.n }}</RouterLink>
  </span>
</template>

<style scoped>
.labtabs { display: inline-flex; gap: .2rem; margin-left: .35rem; vertical-align: middle; }
@media (max-width: 575px) { .labtabs { gap: .15rem; margin-left: 0; } }  /* a phone: the numbers alone, so the crumbs stay one row */
.tab { min-width: 1.4rem; padding: 0 .3rem; border: 1px solid var(--bs-border-color); border-radius: .3rem; color: var(--bs-secondary-color) !important;
       font-size: .78rem; line-height: 1.25rem; text-align: center; text-decoration: none; }
.tab:hover { border-color: var(--bs-secondary-color); background: var(--bs-tertiary-bg); color: var(--bs-body-color) !important; }
.tab.on { border-color: var(--bs-primary); background: var(--bs-primary); color: #fff !important; font-weight: 600; }
</style>
