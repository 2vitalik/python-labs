<script setup>
import { vHint } from '@core/hint.js'
import { BASE, FEATURES } from '../features.js'
import { SECTIONS } from '../sections.js'
import FeatureCheck from './FeatureCheck.vue'

// «Можна додати» in «Можливості» (T348): the page from top to bottom — its own switches, then the sections in the page's
// order. A section that is a feature of its own is a box with its name; a base one is its name, with the features inside
// it on its line. `busy`, `run` — the panel's: one change at a time
defineProps({ busy: Boolean, run: Function })
const ROWS = [
  { title: 'Сторінка', opts: FEATURES.filter((f) => f.place === 'page') },
  ...SECTIONS.map((id) => ({ self: FEATURES.find((f) => f.section === id), base: BASE.find((b) => b.place === id), opts: FEATURES.filter((f) => f.place === id) }))
    .filter((r) => r.self || r.opts.length),
]
</script>

<template>
  <div class="map">
    <template v-for="r in ROWS" :key="r.self?.id || r.base?.place || r.title">
      <div class="where" :class="{ wide: !r.opts.length }">
        <FeatureCheck v-if="r.self" :f="r.self" :busy :run />
        <span v-else-if="r.base" v-hint="{ title: r.base.title, text: `${r.base.text} — є завжди` }" class="place">{{ r.base.icon }} {{ r.base.title }}</span>
        <span v-else class="place">{{ r.title }}</span>
      </div>
      <div v-if="r.opts.length" class="opts">
        <FeatureCheck v-for="f in r.opts" :key="f.id" :f :busy :run />
      </div>
    </template>
  </div>
</template>

<style scoped>
.map { display: grid; grid-template-columns: max-content 1fr; align-items: start; column-gap: 1.1rem; row-gap: .15rem; }
.where.wide { grid-column: 1 / -1; }
/* a base section has no box: its name stands where the boxed names begin, level with the first line of its features */
.place { display: inline-block; padding: .1rem 0 .1rem calc(1em + .4rem); font-weight: 600; cursor: default; }
.where :deep(.name) { font-weight: 600; }
.opts { display: flex; flex-wrap: wrap; column-gap: .9rem; row-gap: .1rem; min-width: 0; }
/* a phone has one column, and its sheet (Pop) scrolls: the features go under their section's name */
@media (max-width: 575px) {
  .map { grid-template-columns: 1fr; }
  .opts { padding-left: calc(1em + .4rem); margin-bottom: .25rem; }
}
</style>
