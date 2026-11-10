<script setup>
import { computed } from 'vue'

import { zones } from '../catalog.js'
import { useEd } from '../ed.js'
import ClaimRow from './ClaimRow.vue'

// claims under small subzone labels in the catalog's order; a card the catalog does not place goes last under «інше».
// `where` — each row says what it is anchored to
const p = defineProps({ claims: Array, where: Boolean })
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
  <div class="vstack gap-2">
    <div v-for="g in groups" :key="g.key" class="vstack gap-1">
      <div class="sub">{{ g.label }}</div>
      <ClaimRow v-for="c in g.list" :key="c.id" :claim="c" :where />
    </div>
  </div>
</template>

<style scoped>
.sub { font-size: .75rem; color: var(--bs-secondary-color); }
</style>
