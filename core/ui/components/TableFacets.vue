<script setup>
import { computed, ref } from 'vue'

import { facets, hasValue, picks, yes } from '../table.js'
import { useTable } from '../tableCtx.js'

// the line of totals under the headers (T315 §5) — the quick filter too. «✅ 84»: a click keeps those 84, again — those
// without (struck, with their count), again — all; an answer's «🕒3»: a click adds it to the answers kept or takes it off.
// Counted over the search and the other columns' filters (t.pool), so a column's own filter leaves its chips in place.
// A sum and a count of filled cells are only read
const t = useTable()
const answers = (spec) => (spec && spec !== '+' ? spec.split(',') : [])

function chipsOf(c) {
  const rows = t.pool(c.id)
  const spec = t.state.filters[c.id] || ''
  const list = facets(c, rows)
  if (yes(c)) {
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
// a column of many answers would grow the head a dozen lines tall: the answers kept by the filter and the biggest stay,
// the rest wait behind «ще N» — a click lays them all out
const MOST = 4
const all = ref(new Set())
const few = computed(() => Object.fromEntries(t.shown.map((c) => {
  const list = chips.value[c.key]
  if (list.length <= MOST || all.value.has(c.key)) return [c.key, list]
  const keep = new Set([...list].sort((a, b) => !!b.on - !!a.on || b.n - a.n).slice(0, MOST - 1))
  return [c.key, list.filter((f) => keep.has(f))]
})))
const more = (c) => (all.value.has(c.key) ? all.value.delete(c.key) : all.value.add(c.key))
function flip(c, f) {
  const spec = t.state.filters[c.id] || ''
  if (yes(c)) return t.setFilter(c.id, spec === '' ? '1' : spec === '1' ? '0' : '')
  const on = answers(spec)
  t.setFilter(c.id, (on.includes(f.id) ? on.filter((x) => x !== f.id) : [...on, f.id]).join())
}
</script>

<template>
  <tr class="facets">
    <th class="name fw-normal">{{ t.rows.length }}<template v-if="t.rows.length !== t.data.rows.length"> з {{ t.data.rows.length }}</template></th>
    <td v-for="c in t.shown" :key="c.key" :class="{ quiet: t.quiet(c), on: t.state.filters[c.id] }">
      <template v-for="f in few[c.key]" :key="f.id">
        <button v-if="f.id" type="button" class="chip" :class="{ on: f.on, not: f.not, word: f.word }" :title="f.title" @click="flip(c, f)"><span class="e">{{ f.text }}</span>{{ f.n }}</button>
        <span v-else class="sum" :title="f.title">{{ f.text }} {{ f.n }}</span>
      </template>
      <button v-if="chips[c.key].length > MOST" type="button" class="more" :title="all.has(c.key) ? 'Лишити найбільші' : 'Показати всі варіанти'" @click="more(c)">
        {{ all.has(c.key) ? 'згорнути' : `ще ${chips[c.key].length - few[c.key].length}` }}</button>
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
.chip.word .e { margin-right: .3rem; }
.more { padding: 0 .2rem; border: 0; background: none; color: var(--bs-secondary-color); font-size: .7rem; white-space: nowrap;
        text-decoration: underline dotted; text-underline-offset: .2em; }
.more:hover { color: var(--bs-body-color); }
.chip.not .e { text-decoration: line-through; text-decoration-color: var(--bs-secondary-color); opacity: .55; }
.sum { white-space: nowrap; font-variant-numeric: tabular-nums; }
</style>
