<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'

import { zones } from '../catalog.js'
import { useEd } from '../ed.js'
import { dense, fitCols, oneCol, split } from '../layout.js'
import ClaimLinkRow from './ClaimLinkRow.vue'
import ClaimRow from './ClaimRow.vue'

// claims under their subcategories in the catalog's order; a card the catalog does not place goes last under «інше».
// `where` — each row says what it is anchored to; `table` — rows of a table with the link a column (T278 §10);
// `cols` — a section's own look (T291 §1): a subcategory is a row across the section, its cards under it in columns,
// dealt evenly as on «Таски»; a table on a wide page becomes two or three tables side by side.
// `anchors` — each subcategory gets an id (`<anchors>-<zone>-<subzone>`) the contents can name
const p = defineProps({ claims: Array, where: Boolean, table: Boolean, cols: Boolean, anchors: String })
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
const idOf = (g) => (p.anchors ? `${p.anchors}-${g.key.replace('/', '-') || 'other'}` : null)

const el = ref()
const width = ref(0)
let ro
onMounted(() => {
  ro = new ResizeObserver(([e]) => (width.value = e.contentRect.width))
  ro.observe(el.value)
})
onBeforeUnmount(() => ro?.disconnect())
const tables = computed(() => Math.max(1, Math.min(dense.value ? 3 : 2, Math.floor(width.value / (dense.value ? 440 : 520)))))
const n = computed(() => (!p.cols || oneCol.value ? 1 : p.table ? tables.value : fitCols(width.value, 330)))

// a table's subcategories in `n` runs of about as many rows each, in the catalog's order
const runs = computed(() => {
  const rows = (g) => g.list.length + 1
  const total = groups.value.reduce((s, g) => s + rows(g), 0)
  const out = [[]]
  let sum = 0
  for (const g of groups.value) {
    if (out.at(-1).length && out.length < n.value && sum + rows(g) / 2 > (total * out.length) / n.value) out.push([])
    out.at(-1).push(g)
    sum += rows(g)
  }
  return out
})
</script>

<template>
  <div ref="el" :class="{ links: table, roomy: cols }">
    <div v-if="table" class="d-flex align-items-start gap-4">
      <div v-for="(run, i) in runs" :key="i" class="stack vstack gap-2">
        <div class="thead"><span>картка</span><span>посилання</span><span>нотатка</span></div>
        <div v-for="g in run" :id="idOf(g)" :key="g.key" class="vstack noflash">
          <div class="sub">{{ g.label }}</div>
          <ClaimLinkRow v-for="c in g.list" :key="c.id" :claim="c" />
        </div>
      </div>
    </div>
    <template v-else>
      <div v-for="g in groups" :id="idOf(g)" :key="g.key" class="group noflash">
        <div class="sub">{{ g.label }}</div>
        <div class="d-flex align-items-start gap-2">
          <div v-for="(col, i) in split(g.list, n)" :key="i" class="stack vstack gap-1">
            <ClaimRow v-for="c in col" :key="c.id" :claim="c" :where />
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped>
.stack { flex: 1 1 0; min-width: 0; }
.sub { margin-bottom: .15rem; font-size: .75rem; color: var(--bs-secondary-color); }
.group + .group { margin-top: .5rem; }
/* in a section of its own a subcategory is a row across it: a stronger name over a line, and air before the next one */
.roomy .sub { padding-bottom: .1rem; border-bottom: 1px solid var(--bs-border-color-translucent); font-size: .8rem; font-weight: 600; }
.roomy .group + .group { margin-top: 1.1rem; }
.roomy .group .sub { margin-bottom: .35rem; }
/* the columns every row of the table shares: fractions, not content, so they line up across rows */
.links { --cols: minmax(0, 2fr) minmax(0, 1.4fr) minmax(0, 1.4fr) 2.6rem; }
.thead { display: grid; grid-template-columns: var(--cols); column-gap: .6rem; padding: 0 .45rem; border-bottom: 1px solid var(--bs-border-color);
         font-size: .7rem; color: var(--bs-secondary-color); }
.links .sub { margin-top: .35rem; }
@media (max-width: 575px) { .thead { display: none; } }
</style>
