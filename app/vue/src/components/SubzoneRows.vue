<script setup>
import { computed } from 'vue'

import { zones } from '../catalog.js'
import { useEd } from '../ed.js'
import ClaimLinkRow from './ClaimLinkRow.vue'
import ClaimRow from './ClaimRow.vue'

// claims under small subzone labels in the catalog's order; a card the catalog does not place goes last under «інше».
// `where` — each row says what it is anchored to; `table` — rows of a table with the link a column (T278 §10)
const p = defineProps({ claims: Array, where: Boolean, table: Boolean })
const ed = useEd()
const home = (c) => {
  const t = ed.info(c.task)
  return t && zones.value[t.zone]?.subzones[t.subzone] ? `${t.zone}/${t.subzone}` : ''
}
const groups = computed(() => {
  const by = {}
  for (const c of p.claims) (by[home(c)] ??= []).push(c)
  const order = Object.entries(zones.value).flatMap(([z, zone]) =>
    Object.entries(zone.subzones).map(([s, [title, icon]]) => ({ key: `${z}/${s}`, label: `${icon} ${title}` })))
  return [...order, { key: '', label: 'інше' }].filter((g) => by[g.key]).map((g) => ({ ...g, list: by[g.key] }))
})
</script>

<template>
  <div class="vstack gap-2" :class="{ links: table }">
    <div v-if="table" class="thead"><span>картка</span><span>посилання</span><span>нотатка</span></div>
    <div v-for="g in groups" :key="g.key" class="vstack" :class="{ 'gap-1': !table }">
      <div class="sub">{{ g.label }}</div>
      <template v-for="c in g.list" :key="c.id">
        <ClaimLinkRow v-if="table" :claim="c" />
        <ClaimRow v-else :claim="c" :where />
      </template>
    </div>
  </div>
</template>

<style scoped>
.sub { font-size: .75rem; color: var(--bs-secondary-color); }
/* the columns every row of the table shares: fractions, not content, so they line up across rows */
.links { --cols: minmax(0, 2fr) minmax(0, 1.4fr) minmax(0, 1.4fr) 1.2rem; }
.thead { display: grid; grid-template-columns: var(--cols); column-gap: .6rem; padding: 0 .45rem; border-bottom: 1px solid var(--bs-border-color);
         font-size: .7rem; color: var(--bs-secondary-color); }
@media (max-width: 575px) { .thead { display: none; } }
</style>
