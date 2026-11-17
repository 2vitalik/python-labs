<script setup>
import { computed, ref, watch } from 'vue'

import { moved, useDragSort } from '../dragSort.js'
import { useTable } from '../tableCtx.js'
import { sortOf } from '../tableViews.js'
import Icon from './Icon.vue'
import TableHeadMenu from './TableHeadMenu.vue'

// the grid's head (T315 §3–4): a band over the columns of one group, then a header per column — its short name and only the
// marks that say something: the sort's way (and its level, when there are several), a filter, a grouping. A click opens the
// column's menu, one for the table; a drag puts the column in another place
const t = useTable()
const menu = ref(null)  // { c, el } — the header whose menu is open
let dropped = 0  // browsers send no click after a drag as a rule; this keeps a stray one from opening the menu
const drag = useDragSort((from, to) => t.setCols(moved(t.shown.map((c) => c.id), from.i, to.i)), { axis: 'x' })
const bands = computed(() => t.shown.reduce((out, c) => {
  if (out.at(-1)?.name === c.group) out.at(-1).span++
  else out.push({ name: c.group, span: 1 })
  return out
}, []))
const levels = computed(() => t.state.sort.map(sortOf))
const marks = computed(() => Object.fromEntries(t.shown.map((c) => {
  const n = levels.value.findIndex((l) => l.id === c.id)
  const m = { sort: n < 0 ? '' : levels.value[n].desc ? 'down' : 'up', level: levels.value.length > 1 ? n + 1 : 0,
              filter: !!t.state.filters[c.id], group: t.state.group.includes(c.id) }
  return [c.key, m.sort || m.filter || m.group ? m : null]
})))
const ended = () => (dropped = Date.now())
watch(() => t.shown, (cols) => {  // its column hidden or turned to another lab: the header it hangs on is gone
  if (menu.value && !cols.some((c) => c.key === menu.value.c.key)) menu.value = null
})
function open(c, e) {
  if (Date.now() - dropped < 400) return
  menu.value = menu.value?.c.key === c.key ? null : { c, el: e.currentTarget }
}
</script>

<template>
  <tr class="bands">
    <th class="name"></th>
    <th v-for="(b, i) in bands" :key="i" :colspan="b.span">{{ b.name }}</th>
  </tr>
  <tr>
    <th class="name">Студент</th>
    <th v-for="(c, i) in t.shown" :key="c.key" v-bind="drag.item(i)" class="hd" :class="{ quiet: t.quiet(c), on: marks[c.key]?.filter, open: menu?.c.key === c.key }"
        :title="`${c.title}\nклік — меню колонки, перетягни — на інше місце`" @click="open(c, $event)" @dragend="ended">
      {{ c.short }}<span v-if="marks[c.key]" class="mk">
        <Icon v-if="marks[c.key].sort" :name="marks[c.key].sort" /><sub v-if="marks[c.key].sort && marks[c.key].level">{{ marks[c.key].level }}</sub>
        <Icon v-if="marks[c.key].filter" name="filter" />
        <Icon v-if="marks[c.key].group" name="layers" />
      </span>
    </th>
  </tr>
  <TableHeadMenu v-if="menu" :key="menu.c.key" :c="menu.c" :anchor="menu.el" @close="menu = null" />
</template>

<style scoped>
.bands th { text-align: center; font-size: .72rem; font-weight: 500; color: var(--bs-secondary-color); border-bottom: 0; padding-bottom: 0; }
.bands th + th { border-left: 1px solid var(--bs-border-color); }
.hd { min-width: 2.6rem; text-align: center; font-size: .85rem; line-height: 1.2; vertical-align: bottom; cursor: pointer; user-select: none; }
.hd:hover { --bs-table-bg: var(--bs-tertiary-bg); }
.hd.on { --bs-table-bg: var(--bs-warning-bg-subtle); }
.hd.open { --bs-table-bg: var(--bs-secondary-bg); }
.mk { display: inline-flex; align-items: center; gap: .1rem; margin-left: .15rem; font-size: .68rem; color: var(--bs-secondary-color); vertical-align: middle; }
.mk sub { bottom: 0; margin-left: -.1rem; font-size: .85em; }
</style>
