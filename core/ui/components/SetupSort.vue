<script setup>
import { computed, ref } from 'vue'

import { moved, useDragSort } from '../dragSort.js'
import { useTable } from '../tableCtx.js'
import { sortOf } from '../tableViews.js'
import ColPick from './ColPick.vue'
import Icon from './Icon.vue'
import Reveal from './Reveal.vue'
import SetupName from './SetupName.vue'
import SetupRow from './SetupRow.vue'

// the panel «Сортування» (T315 §4): «first by…, then by…» in rows, each with its way up or down (a click turns it),
// put in order by dragging; with none the rows stand as the list has them — by group and surname
const t = useTable()
const adding = ref(false)
const levels = computed(() => t.state.sort.map(sortOf).map((s) => ({ ...s, col: t.col(s.id) })).filter((s) => s.col))
const write = (list) => t.set({ sort: list.map((s) => (s.desc ? '-' : '') + s.id) })
const drag = useDragSort((from, to) => write(moved(levels.value, from.i, to.i)))
const turn = (l) => write(levels.value.map((s) => (s === l ? { ...s, desc: !s.desc } : s)))
function add(col) {
  write([...levels.value, { id: col.id, desc: false }])
  adding.value = false
}
</script>

<template>
  <div>
    <SetupRow v-for="(l, i) in levels" :key="l.id" v-bind="drag.item(i)" @off="write(levels.filter((s) => s !== l))">
      <span class="lv-n">{{ i + 1 }}</span><SetupName :col="l.col" class="flex-grow-1" />
      <button type="button" class="lv-dir" :title="l.desc ? 'Від більшого до меншого — клік: навпаки' : 'Від меншого до більшого — клік: навпаки'" @click="turn(l)">
        <Icon :name="l.desc ? 'down' : 'up'" />{{ l.desc ? 'спадання' : 'зростання' }}</button>
    </SetupRow>
    <div v-if="!levels.length" class="small text-secondary">Як у списку: за групою й прізвищем</div>
    <button type="button" class="btn btn-sm btn-add py-0 mt-2" :class="{ active: adding }" :aria-expanded="adding" @click="adding = !adding"><Icon name="plus" /> ще за…</button>
    <Reveal :show="adding"><ColPick class="mt-2" :skip="levels.map((s) => s.id)" @pick="add" /></Reveal>
  </div>
</template>

<style scoped>
.lv-n { flex-shrink: 0; width: 1rem; color: var(--bs-secondary-color); font-size: .72rem; text-align: end; }
.lv-dir { display: inline-flex; flex-shrink: 0; align-items: center; gap: .2rem; padding: 0 .35rem; border: 1px solid var(--bs-border-color);
          border-radius: .3rem; background: none; color: var(--bs-secondary-color); font-size: .72rem; }
.lv-dir:hover { background: var(--bs-tertiary-bg); color: var(--bs-body-color); }
</style>
