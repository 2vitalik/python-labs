<script setup>
import { computed } from 'vue'

import { diff } from '../tableDiff.js'
import { columns } from '../tableCols.js'
import { store } from '../viewStore.js'
import Icon from './Icon.vue'

// what differs from `a` to `b` — { title, query } of two views or versions (T315 §8): in a few words, or `full` — every
// change on a line of its own under its part (columns, filters, groups, sort, the lab), each with its mark: added,
// removed, changed, moved. `cols` — the columns to read the queries with; the table's own when not given
const props = defineProps({ a: { type: Object, required: true }, b: { type: Object, required: true }, cols: Array, full: Boolean })
const SIGN = { add: ['plus', 'додано'], del: ['minus', 'прибрано'], chg: ['arrow', 'змінено'], move: ['sort', 'переставлено'] }
const d = computed(() => diff(props.a.query, props.b.query, props.cols || columns(store.data)))
const parts = computed(() => {
  const by = {}
  for (const l of d.value.lines) (by[l.what] ||= []).push(l)
  return Object.entries(by)
})
</script>

<template>
  <div class="vdiff">
    <p v-if="d.same" class="mb-0 text-secondary">однакові</p>
    <p v-else-if="!full" class="mb-0">{{ d.brief.join(' · ') }}</p>
    <div v-else class="vdiff-parts">
      <section v-for="[what, lines] in parts" :key="what">
        <div class="vdiff-cap">{{ what }}</div>
        <div v-for="(l, i) in lines" :key="i" class="vdiff-line" :title="SIGN[l.kind][1]">
          <Icon :name="SIGN[l.kind][0]" :class="l.kind" />
          <span><span class="visually-hidden">{{ SIGN[l.kind][1] }}: </span>{{ l.text }}</span>
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped>
.vdiff-parts { display: grid; grid-template-columns: repeat(auto-fill, minmax(14rem, 1fr)); gap: .5rem 1.25rem; }
.vdiff-cap { margin-bottom: .1rem; font-size: .68rem; font-weight: 600; letter-spacing: .05em; text-transform: uppercase; color: var(--bs-secondary-color); }
.vdiff-line { display: flex; align-items: baseline; gap: .35rem; font-size: .85rem; }
.vdiff-line .icon { position: relative; top: .1em; color: var(--bs-secondary-color); }
.vdiff-line .icon.add { color: var(--bs-success); }
.vdiff-line .icon.del { color: var(--bs-danger); }
</style>
