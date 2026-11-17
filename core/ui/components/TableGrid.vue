<script setup>
import { computed, ref } from 'vue'

import { groups } from '../tableOrder.js'
import { useTable } from '../tableCtx.js'
import Avatar from './Avatar.vue'
import LabEdit from './LabEdit.vue'
import TableCell from './TableCell.vue'
import TableFacets from './TableFacets.vue'
import TableGroupRow from './TableGroupRow.vue'
import TableHead from './TableHead.vue'

// the grid of /table (T240, T315 §2): the head — bands, headers, the line of totals that filters — then the rows, in groups
// inside groups, each folding and adding up its own. A lab cell opens LabEdit under its row, an editable cell edits in place
const t = useTable()
const folded = ref(new Set())  // ids of the groups folded; a folded group hides the ones inside it too
const picked = ref(null)  // { nick, lab, key } — the lab cell whose editor is open under its row
const error = ref('')
const byGroup = computed(() => t.groupCols.some((c) => c.key === 'group'))
// the groups laid out as lines: a group's head, then its groups or its rows
function walk(list, level, out) {
  for (const g of list) {
    out.push({ key: `g${g.id}`, g, level })
    if (folded.value.has(g.id)) continue
    if (g.kids) walk(g.kids, level + 1, out)
    else out.push(...g.rows.map((r) => ({ key: r.nick, r })))
  }
  return out
}
const lines = computed(() => {
  const top = groups(t.rows, t.groupCols)
  return top ? walk(top, 0, []) : t.rows.map((r) => ({ key: r.nick, r }))
})
const fold = (id) => (folded.value.has(id) ? folded.value.delete(id) : folded.value.add(id))
const pick = (r, c) => (picked.value = picked.value?.nick === r.nick && picked.value.key === c.key ? null : { nick: r.nick, lab: c.lab, key: c.key })
const edit = (c, r, value) => t.edit(c, r, value).then(() => (error.value = ''), (e) => (error.value = e.message))
</script>

<template>
  <div>
    <div class="wrap border rounded">
      <table class="table table-sm align-middle mb-0">
        <thead>
          <TableHead />
          <TableFacets />
        </thead>
        <tbody>
          <template v-for="x in lines" :key="x.key">
            <TableGroupRow v-if="x.g" :g="x.g" :level="x.level" :folded="folded.has(x.g.id)" @fold="fold(x.g.id)" />
            <template v-else>
              <tr>
                <th class="name fw-normal">
                  <Avatar :user="x.r" :size="20" /> <RouterLink :to="`/students/${x.r.nick}/edit`">{{ x.r.name || x.r.nick }}</RouterLink>
                  <small v-if="!byGroup" class="text-secondary ms-1">{{ x.r.group }}</small>
                </th>
                <td v-for="c in t.shown" :key="c.key" class="cell" :class="{ quiet: t.quiet(c), active: picked?.nick === x.r.nick && picked.key === c.key }">
                  <TableCell :col="c" :row="x.r" @pick="pick(x.r, c)" @save="edit(c, x.r, $event)" />
                </td>
              </tr>
              <tr v-if="picked?.nick === x.r.nick">
                <td :colspan="t.shown.length + 1" class="p-2 editor">
                  <LabEdit :key="picked.lab" :nick="x.r.nick" :lab="picked.lab" :cell="x.r.labs[picked.lab]" @saved="x.r.labs[picked.lab] = $event" @close="picked = null" />
                </td>
              </tr>
            </template>
          </template>
        </tbody>
      </table>
      <p v-if="!t.rows.length" class="text-secondary text-center my-3 mb-2">Під ці фільтри ніхто не підходить.</p>
    </div>
    <p v-if="error" class="text-danger small mt-1 mb-0">{{ error }}</p>
  </div>
</template>

<style scoped>
.wrap { overflow-x: auto; }
.wrap :deep(th), .wrap :deep(td) { white-space: nowrap; }
/* the name stays at the left as the table scrolls; its ground hides the cells that pass under it */
.wrap :deep(.name) { position: sticky; left: 0; z-index: 1; min-width: 12rem; max-width: 18rem; overflow: hidden; text-overflow: ellipsis;
                     background: var(--bs-table-bg, var(--bs-body-bg)); }
.wrap :deep(.quiet) { opacity: .55; transition: opacity .15s; }
.wrap :deep(.quiet:hover) { opacity: 1; }
.name a { color: inherit; text-decoration: none; }
.name a:hover { text-decoration: underline; }
.editor { white-space: normal; max-width: 0; }
.cell { padding: .1rem; text-align: center; }
.cell.active { outline: 1px solid var(--bs-border-color); background: var(--bs-tertiary-bg); }
@media (max-width: 576px) { .wrap :deep(.name) { min-width: 8rem; max-width: 10rem; } }
</style>
