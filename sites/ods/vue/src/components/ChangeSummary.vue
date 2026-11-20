<script setup>
import { computed } from 'vue'

import { pages } from '@core/guide.js'
import { vHint } from '@core/hint.js'

import { cleared, fits, PRESETS } from '../lectureChangeFilter.js'
import { GROUPS, groupOf } from '../lectureChanges.js'
import { shortTitle } from '../lectures.js'

// at a glance: lectures × groups — how many changes each cell holds with the other filters kept (the deeper the tint, the
// more in its column); a click on a cell, a lecture or a group filters by it. Beside — the counts that wait for the teacher
const props = defineProps({ items: Array, f: Object, query: Object })
const emit = defineEmits(['set'])
const lecs = computed(() => [...new Map(props.items.map((it) => [it.lec, it.slug]))])
const groups = computed(() => Object.keys(GROUPS).filter((g) => props.items.some((it) => groupOf(it) === g)))
const grid = computed(() => {
  const m = {}
  for (const it of props.items) if (fits(it, props.f, ['lec', 'group'])) for (const k of [`${it.lec}|${groupOf(it)}`, `${it.lec}|`, `|${groupOf(it)}`, '|']) m[k] = (m[k] || 0) + 1
  return m
})
const n = (l, g) => grid.value[`${l}|${g}`] || 0
const top = computed(() => Object.fromEntries(groups.value.map((g) => [g, Math.max(...lecs.value.map(([l]) => n(l, g)))])))
const heat = (l, g) => n(l, g) && { '--c': `var(--g-${g})`, '--k': `${Math.round(8 + 34 * n(l, g) / top.value[g])}%` }
const only = (key, v) => props.f[key].length === 1 && props.f[key][0] === String(v)
const lit = (l, g) => (props.f.lec.length || props.f.group.length) && (!props.f.lec.length || props.f.lec.includes(String(l))) && (!props.f.group.length || props.f.group.includes(g))
const pick = (l, g) => emit('set', only('lec', l) && only('group', g) ? { lec: undefined, group: undefined } : { lec: String(l), group: g })
const lecTitle = (slug) => shortTitle(pages.value[slug]?.title || '')

const count = (fn) => props.items.filter(fn).length
const tallies = computed(() => [
  { key: 'crit', word: 'критично', n: count((it) => it.sev === 3), q: { sev: '3' }, cls: 's3', hint: PRESETS.crit.hint },
  { key: 'open', word: 'чекає рішення', n: count((it) => it.status === 'open'), q: { status: 'open' }, cls: 'open', hint: 'сумнівні місця й розкладка, що важить' },
  { key: 'lector', word: 'для лектора', n: count(PRESETS.lector.fits), q: { for: 'lector' }, cls: 'lector', hint: PRESETS.lector.hint },
  { key: 'todo', word: 'без типу', n: count((it) => it.kind === 'todo'), q: { kind: 'todo' }, cls: 'todo', hint: 'правки, яких ще не класифіковано' },
].filter((t) => t.n || t.key !== 'todo'))
const on = (t) => Object.keys(cleared()).every((k) => (props.query[k] || undefined) === t.q[k])
</script>

<template>
  <div class="chg-sum">
    <table class="chg-matrix">
      <thead>
        <tr>
          <th><button type="button" class="cell" @click="emit('set', { lec: undefined, group: undefined })">усі</button></th>
          <th v-for="g in groups" :key="g"><button v-hint="GROUPS[g][1]" type="button" class="cell" :class="{ on: only('group', g) }"
                                                   @click="emit('set', { group: only('group', g) ? undefined : g })"><span class="g-dot" :style="{ '--c': `var(--g-${g})` }" /><span class="gw">{{ GROUPS[g][0] }}</span></button></th>
          <th class="tot">разом</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="[l, slug] in lecs" :key="l">
          <th><button v-hint="lecTitle(slug)" type="button" class="cell" :class="{ on: only('lec', l) }" @click="emit('set', { lec: only('lec', l) ? undefined : String(l) })">{{ l }}</button></th>
          <td v-for="g in groups" :key="g"><button type="button" class="cell num" :class="{ lit: lit(l, g), zero: !n(l, g) }" :style="heat(l, g)" @click="pick(l, g)">{{ n(l, g) || '·' }}</button></td>
          <td class="tot">{{ n(l, '') }}</td>
        </tr>
      </tbody>
      <tfoot>
        <tr><th>разом</th><td v-for="g in groups" :key="g" class="tot">{{ n('', g) }}</td><td class="tot">{{ n('', '') }}</td></tr>
      </tfoot>
    </table>
    <div class="chg-tallies">
      <button v-for="t in tallies" :key="t.key" v-hint="t.hint" type="button" class="tally" :class="[t.cls, { on: on(t) }]"
              @click="emit('set', { ...cleared(), ...(on(t) ? {} : t.q) })"><b>{{ t.n }}</b> {{ t.word }}</button>
    </div>
  </div>
</template>
