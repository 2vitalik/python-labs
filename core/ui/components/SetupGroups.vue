<script setup>
import { ref } from 'vue'

import { moved, useDragSort } from '../dragSort.js'
import { picks } from '../table.js'
import { useTable } from '../tableCtx.js'
import ColPick from './ColPick.vue'
import Icon from './Icon.vue'
import Reveal from './Reveal.vue'
import SetupName from './SetupName.vue'
import SetupRow from './SetupRow.vue'

// the panel «Групи» (T315 §4): the levels of grouping in rows — the first splits the rows, the next splits each group —
// put in order by dragging, ✕ takes one off; «＋ рівень» offers what groups well: the group, checkmarks, links, icons, dates
const t = useTable()
const adding = ref(false)
const ids = () => t.groupCols.map((c) => c.id)
const drag = useDragSort((from, to) => t.set({ group: moved(ids(), from.i, to.i) }))
const fits = (c) => c.key === 'group' || ['bool', 'link', 'date'].includes(c.type) || picks(c)
function add(col) {
  t.set({ group: [...ids(), col.id] })
  adding.value = false
}
</script>

<template>
  <div>
    <SetupRow v-for="(c, i) in t.groupCols" :key="c.id" v-bind="drag.item(i)" off="Прибрати рівень" @off="t.set({ group: ids().filter((x) => x !== c.id) })">
      <span class="lv-n">{{ i + 1 }}</span><SetupName :col="c" />
    </SetupRow>
    <div v-if="!t.groupCols.length" class="small text-secondary">Без груп</div>
    <button type="button" class="btn btn-sm btn-add py-0 mt-2" :class="{ active: adding }" :aria-expanded="adding" @click="adding = !adding"><Icon name="plus" /> рівень</button>
    <Reveal :show="adding"><ColPick class="mt-2" :only="fits" :skip="ids()" @pick="add" /></Reveal>
  </div>
</template>

<style scoped>
.lv-n { flex-shrink: 0; width: 1rem; color: var(--bs-secondary-color); font-size: .72rem; text-align: end; }
</style>
