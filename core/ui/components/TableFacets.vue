<script setup>
import { computed } from 'vue'

import { facets, hasValue, picks } from '../table.js'
import { useTable } from '../tableCtx.js'

// the line of totals under the headers (T315 §5) — the quick filter too. «✅ 84»: a click keeps those 84, again — those
// without (struck, with their count), again — all; an answer's «🕒3»: a click adds it to the answers kept or takes it off.
// Counted over the search and the other columns' filters (t.pool), so a column's own filter leaves its chips in place.
// A sum and a count of filled cells are only read
const t = useTable()
const YES = ['bool', 'link']
const answers = (spec) => (spec && spec !== '+' ? spec.split(',') : [])

function chipsOf(c) {
  const rows = t.pool(c.id)
  const spec = t.state.filters[c.id] || ''
  const list = facets(c, rows)
  if (YES.includes(c.type)) {
    const f = list[0]
    if (spec === '0') return [{ ...f, n: rows.length - f.n, on: true, not: true, title: `${c.title}: ні — ще клік знімає фільтр` }]
    return [{ ...f, on: spec === '1', title: `${c.title}: так — клік лишає цих, ще клік — тих, у кого нема` }]
  }
  if (!picks(c)) return list.map((f) => ({ ...f, title: f.text ? `${c.title}: сума` : `${c.title}: заповнено` }))
  const on = answers(spec)
  const gone = on.filter((id) => !list.some((f) => f.id === id))  // kept by the filter, yet none left by the others
    .map((id) => (id === '-' ? { id, text: 'порожньо', n: rows.filter((r) => !hasValue(c.get(r))).length } : { id, text: c.options?.[id]?.emoji || id, n: 0 }))
  return [...list, ...gone].map((f) => ({ ...f, on: on.includes(f.id), title: `${f.title || f.text}: ${f.n} — клік лишає цих` }))
}
const chips = computed(() => Object.fromEntries(t.shown.map((c) => [c.key, chipsOf(c)])))
function flip(c, f) {
  const spec = t.state.filters[c.id] || ''
  if (YES.includes(c.type)) return t.setFilter(c.id, spec === '' ? '1' : spec === '1' ? '0' : '')
  const on = answers(spec)
  t.setFilter(c.id, (on.includes(f.id) ? on.filter((x) => x !== f.id) : [...on, f.id]).join())
}
</script>

<template>
  <tr class="facets">
    <th class="name fw-normal">{{ t.rows.length }}<template v-if="t.rows.length !== t.data.rows.length"> з {{ t.data.rows.length }}</template></th>
    <td v-for="c in t.shown" :key="c.key" :class="{ quiet: t.quiet(c), on: t.state.filters[c.id] }">
      <template v-for="f in chips[c.key]" :key="f.id">
        <button v-if="f.id" type="button" class="chip" :class="{ on: f.on, not: f.not }" :title="f.title" @click="flip(c, f)"><span class="e">{{ f.text }}</span>{{ f.n }}</button>
        <span v-else class="sum" :title="f.title">{{ f.text }} {{ f.n }}</span>
      </template>
    </td>
  </tr>
</template>

<style scoped>
thead tr.facets > * { padding-top: .15rem; padding-bottom: .2rem; font-size: .75rem; color: var(--bs-secondary-color); text-align: center; vertical-align: top;
              white-space: normal; max-width: 8rem; }
.facets > .name { text-align: start; white-space: nowrap; font-variant-numeric: tabular-nums; }
.facets > .on { --bs-table-bg: color-mix(in srgb, var(--bs-warning-bg-subtle) 55%, var(--bs-body-bg)); }
.chip { display: inline-block; margin: 0 .05rem .1rem; padding: 0 .25rem; border: 1px solid transparent; border-radius: .35rem; background: none;
        color: var(--bs-body-color); white-space: nowrap; font-variant-numeric: tabular-nums; line-height: 1.35; }
.chip:hover { background: var(--bs-tertiary-bg); border-color: var(--bs-border-color); }
.chip.on { background: var(--bs-warning-bg-subtle); border-color: var(--bs-warning-border-subtle); }
.chip .e { margin-right: .1rem; }
.chip.not .e { text-decoration: line-through; text-decoration-color: var(--bs-secondary-color); opacity: .55; }
.sum { white-space: nowrap; font-variant-numeric: tabular-nums; }
</style>
