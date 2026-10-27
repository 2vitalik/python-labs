<script setup>
import { computed, ref } from 'vue'

import { compare, groupOf, total } from '../table.js'
import Avatar from './Avatar.vue'
import IconChevron from './IconChevron.vue'
import LabEdit from './LabEdit.vue'
import TableCell from './TableCell.vue'
import TableFilter from './TableFilter.vue'

// the grid of /table (T240): a band of headers per column group, a header per column (click — sort, ▾ — filter), rows in folding groups,
// the «Разом» row; a lab cell opens LabEdit under the row, an editable cell edits in place (TableCell)
const props = defineProps({ rows: { type: Array, required: true }, cols: { type: Array, required: true }, group: Object, sort: String, filters: Object })
const emit = defineEmits(['sort', 'filter', 'save'])
const folded = ref(new Set())
const filtering = ref('')
const picked = ref(null)  // {nick, lab}
const bands = computed(() => props.cols.reduce((out, c) => {
  if (out.at(-1)?.name === c.group) out.at(-1).span++
  else out.push({ name: c.group, span: 1 })
  return out
}, []))
const groups = computed(() => {
  if (!props.group) return [{ key: '', text: '', list: props.rows }]
  const out = new Map()
  for (const r of props.rows) {
    const g = groupOf(props.group, r)
    const id = String(g.key)
    out.set(id, out.get(id) || { ...g, list: [] })
    out.get(id).list.push(r)
  }
  return [...out.values()].sort((a, b) => (a.key === null) - (b.key === null) || compare(a.key, b.key))
})
const toggle = (key) => (folded.value.has(key) ? folded.value.delete(key) : folded.value.add(key))
const sortMark = (c) => (props.sort === c.key ? '▲' : props.sort === `-${c.key}` ? '▼' : '')
const pick = (r, c) => (picked.value = picked.value?.nick === r.nick && picked.value.lab === c.lab ? null : { nick: r.nick, lab: c.lab, key: c.key })
</script>

<template>
  <div class="wrap border rounded">
    <table class="table table-sm align-middle mb-0">
      <thead>
        <tr class="bands">
          <th class="name"></th>
          <th v-for="(b, i) in bands" :key="i" :colspan="b.span">{{ b.name }}</th>
        </tr>
        <tr>
          <th class="name">Студент</th>
          <th v-for="c in cols" :key="c.key" class="col" :class="{ on: filters[c.key] }" :title="`${c.title}\nклік — сортування`">
            <a href="#" class="head" @click.prevent="emit('sort', c.key)">{{ c.short }}<small v-if="sortMark(c)">{{ sortMark(c) }}</small></a>
            <a href="#" class="flt" :class="{ 'is-on': filters[c.key] }" title="Фільтр" @click.prevent="filtering = filtering === c.key ? '' : c.key">▾</a>
            <TableFilter v-if="filtering === c.key" :col="c" :spec="filters[c.key] || ''" @set="emit('filter', c.key, $event)" @close="filtering = ''" />
          </th>
        </tr>
      </thead>
      <tbody v-for="g in groups" :key="String(g.key)">
        <tr v-if="group" class="table-light" role="button" @click="toggle(String(g.key))">
          <th class="name"><IconChevron :dir="folded.has(String(g.key)) ? 'right' : 'down'" :size="12" class="text-secondary" /> {{ g.text }} <span class="count">{{ g.list.length }}</span></th>
          <td :colspan="cols.length"></td>
        </tr>
        <template v-if="!folded.has(String(g.key))">
          <template v-for="r in g.list" :key="r.nick">
            <tr>
              <th class="name fw-normal">
                <Avatar :user="r" :size="20" /> <RouterLink :to="`/students/${r.nick}/edit`">{{ r.name || r.nick }}</RouterLink>
                <small v-if="group?.key !== 'group'" class="text-secondary ms-1">{{ r.group }}</small>
              </th>
              <td v-for="c in cols" :key="c.key" class="cell" :class="{ active: picked?.nick === r.nick && picked.key === c.key }">
                <TableCell :col="c" :row="r" @pick="pick(r, c)" @save="emit('save', c, r, $event)" />
              </td>
            </tr>
            <tr v-if="picked?.nick === r.nick">
              <td :colspan="cols.length + 1" class="p-2 editor">
                <LabEdit :key="picked.lab" :nick="r.nick" :lab="picked.lab" :cell="r.labs[picked.lab]" @saved="r.labs[picked.lab] = $event" @close="picked = null" />
              </td>
            </tr>
          </template>
        </template>
      </tbody>
      <tfoot>
        <tr>
          <th class="name fw-normal text-secondary">Разом · {{ rows.length }}</th>
          <td v-for="c in cols" :key="c.key" class="sum">{{ total(c, rows) }}</td>
        </tr>
      </tfoot>
    </table>
    <p v-if="!rows.length" class="text-secondary text-center my-3 mb-2">Під ці фільтри ніхто не підходить.</p>
  </div>
</template>

<style scoped>
.wrap { overflow-x: auto; }
th, td { white-space: nowrap; }
.editor { white-space: normal; max-width: 0; }
.name { position: sticky; left: 0; z-index: 1; min-width: 12rem; max-width: 18rem; overflow: hidden; text-overflow: ellipsis; }
.name a { color: inherit; text-decoration: none; }
.name a:hover { text-decoration: underline; }
.bands th { text-align: center; font-size: .72rem; font-weight: 500; color: var(--bs-secondary-color); border-bottom: 0; padding-bottom: 0; }
.bands th + th { border-left: 1px solid var(--bs-border-color); }
.col { position: relative; min-width: 2.6rem; text-align: center; font-size: .85rem; line-height: 1.2; vertical-align: bottom; padding-right: .9rem; }
.col.on { background: var(--bs-warning-bg-subtle); }
.head { color: inherit; text-decoration: none; }
.head small { display: block; font-size: .6rem; line-height: 1; color: var(--bs-secondary-color); }
.flt { position: absolute; right: .1rem; bottom: .25rem; font-size: .7rem; color: var(--bs-tertiary-color); text-decoration: none; }
.flt:hover, .flt.is-on { color: var(--bs-body-color); }
.cell { padding: .1rem; text-align: center; }
.cell.active { outline: 1px solid var(--bs-border-color); background: var(--bs-tertiary-bg); }
.sum { text-align: center; color: var(--bs-secondary-color); font-size: .75rem; white-space: normal; max-width: 6rem; }
.count { font-weight: 400; opacity: .55; font-size: .85em; }
@media (max-width: 576px) { .name { min-width: 8rem; max-width: 10rem; } }
</style>
