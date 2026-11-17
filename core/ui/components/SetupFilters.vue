<script setup>
import { ref } from 'vue'

import { yes } from '../table.js'
import { useTable } from '../tableCtx.js'
import ColPick from './ColPick.vue'
import FilterControl from './FilterControl.vue'
import Icon from './Icon.vue'
import Reveal from './Reveal.vue'
import SetupName from './SetupName.vue'

// the panel «Фільтри» (T315 §5): a line a filter — the column, its condition by the column's type, ✕; «＋ фільтр» picks a
// column and starts it with «так» (a checkmark, a link) or «є» (anything else). With no filters the pick is open at once
const t = useTable()
const adding = ref(!t.filters.length)
function add(col) {
  t.setFilter(col.id, yes(col) ? '1' : '+')
  adding.value = false
}
</script>

<template>
  <div>
    <div v-for="f in t.filters" :key="f.col.id" class="sf-row">
      <div class="d-flex align-items-center gap-1">
        <SetupName :col="f.col" class="fw-semibold" />
        <button type="button" class="iact mini ms-auto" title="Прибрати фільтр" @click="t.setFilter(f.col.id, '')"><Icon name="x" /></button>
      </div>
      <FilterControl :col="f.col" :spec="f.spec" :rows="t.pool(f.col.id)" @set="(spec) => t.setFilter(f.col.id, spec)" />
    </div>
    <div v-if="!t.filters.length" class="small text-secondary">Без фільтрів — видно всіх</div>
    <div class="d-flex align-items-center gap-2 mt-2">
      <button type="button" class="btn btn-sm btn-add py-0" :class="{ active: adding }" :aria-expanded="adding" @click="adding = !adding"><Icon name="plus" /> фільтр</button>
      <button v-if="t.filters.length > 1" type="button" class="more-field ms-auto" @click="t.set({ filters: {} })">зняти всі</button>
    </div>
    <Reveal :show="adding"><ColPick class="mt-2" :skip="t.filters.map((f) => f.col.id)" @pick="add" /></Reveal>
  </div>
</template>

<style scoped>
.sf-row { padding: .3rem 0 .45rem; border-bottom: 1px solid var(--bs-border-color-translucent); }
</style>
