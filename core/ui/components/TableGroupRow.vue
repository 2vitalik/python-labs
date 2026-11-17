<script setup>
import { computed } from 'vue'

import { facetText, facets } from '../table.js'
import { useTable } from '../tableCtx.js'
import IconChevron from './IconChevron.vue'

// a group's head in the grid (T315 §4): the fold, the group's name and size, indented by its level, and under each column what
// it adds up to in this group — «✅18», «✅12 🕒3», «Σ40»; only read, the line of totals under the headers is the one that filters
const props = defineProps({ g: { type: Object, required: true }, level: { type: Number, default: 0 }, folded: Boolean })
const emit = defineEmits(['fold'])
const t = useTable()
// words are told apart by a dot between them, emoji stand close
const sumOf = (c) => { const list = facets(c, props.g.rows); return list.map(facetText).join(list.some((f) => f.word) ? ' · ' : ' ') }
const sums = computed(() => Object.fromEntries(t.shown.map((c) => [c.key, sumOf(c)])))
</script>

<template>
  <tr class="grp" role="button" @click="emit('fold')">
    <th class="name" :style="{ paddingLeft: `${0.3 + level * 1.1}rem` }" :title="`${g.col.title}: ${g.text}`">
      <IconChevron :dir="folded ? 'right' : 'down'" :size="12" class="text-secondary" /> {{ g.text }} <span class="count">{{ g.rows.length }}</span>
    </th>
    <td v-for="c in t.shown" :key="c.key" class="sum" :class="{ quiet: t.quiet(c) }" :title="sums[c.key] && `${c.title}: ${sums[c.key]}`">{{ sums[c.key] }}</td>
  </tr>
</template>

<style scoped>
.grp { --bs-table-bg: var(--bs-tertiary-bg); }
.count { font-weight: 400; opacity: .55; font-size: .85em; }
.sum { max-width: 8rem; overflow: hidden; text-overflow: ellipsis; text-align: center; font-size: .72rem; color: var(--bs-secondary-color); font-variant-numeric: tabular-nums; }
</style>
