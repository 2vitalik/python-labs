<script setup>
import { moved, useDragSort } from '../dragSort.js'
import { useTable } from '../tableCtx.js'
import SetupCatalog from './SetupCatalog.vue'
import SetupName from './SetupName.vue'
import SetupRow from './SetupRow.vue'

// the panel «Колонки» (T315 §3): on the left the columns the view shows — dragged into order, ✕ hides one; on the right
// the catalog of all there are
const t = useTable()
const drag = useDragSort((from, to) => t.setCols(moved(t.shown.map((c) => c.id), from.i, to.i)))
</script>

<template>
  <div class="scols">
    <div class="scols-shown">
      <div class="group-cap">Показані · {{ t.shown.length }}</div>
      <div class="scols-list">
        <SetupRow v-for="(c, i) in t.shown" :key="c.key" v-bind="drag.item(i)" off="Сховати" @off="t.hide(c.id)"><SetupName :col="c" class="flex-grow-1" /></SetupRow>
        <div v-if="!t.shown.length" class="small text-secondary">Нічого — увімкни колонки в каталозі</div>
      </div>
    </div>
    <SetupCatalog />
  </div>
</template>

<style scoped>
.scols { display: grid; grid-template-columns: minmax(0, 17rem) minmax(0, 1fr); gap: 1rem; }
.scols-shown { min-width: 0; }
.scols-list { max-height: min(62vh, 33rem); overflow-y: auto; font-size: .82rem; }
@media (max-width: 720px) { .scols { grid-template-columns: minmax(0, 1fr); } }
</style>
