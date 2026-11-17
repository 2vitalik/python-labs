<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import { subStyle } from '../catalog.js'
import { isUnfolded, unfoldAll } from '../unfold.js'
import { user } from '@core/user.js'
import IdeaPop from './IdeaPop.vue'
import TaskCard from './TaskCard.vue'
import TaskEdit from './TaskEdit.vue'
import TaskMoreRow from './TaskMoreRow.vue'

// a category's subcategories, each a full-width row (T274 §1): its cards dealt into as many columns as fit (≈320 px),
// the first part of the list into the first column. The columns are separate stacks: an unfolded card lengthens only its own.
// Under «Основа» the cards «за запитом» wait behind a row at the end (T319, TaskMoreRow).
// `bare` — no ids on the subcategories: the catalog stands in a window over another page (T318)
const props = defineProps({ zone: String, color: String, subs: Array, bare: Boolean })
const admin = computed(() => user.value?.status === 'admin')
const scope = (s) => `${props.zone}/${s.key}`
const adding = ref('')  // the subcategory whose «＋» opened a new card's form over its columns
const blank = (s) => ({ zone: props.zone, subzone: s.key, status: 'draft' })

const el = ref(null)
const cols = ref(3)
let ro
onMounted(() => {
  ro = new ResizeObserver(([e]) => { cols.value = Math.max(1, Math.floor(e.contentRect.width / 320)) })
  ro.observe(el.value)
})
onBeforeUnmount(() => ro?.disconnect())

// consecutive runs whose sizes differ by one at most: 7 cards in 3 columns → 3 · 2 · 2; 2 in 3 → 1 · 1 · empty
function split(list, n) {
  const size = Math.floor(list.length / n), extra = list.length % n
  let at = 0
  return Array.from({ length: n }, (_, i) => list.slice(at, (at += size + (i < extra ? 1 : 0))))
}
</script>

<template>
  <div ref="el">
    <div v-for="s in subs" :id="bare ? null : `sub-${zone}-${s.key}`" :key="s.key" class="task-group noflash mb-3" :style="subStyle(color, s.i)">
      <div class="group-head d-flex align-items-center gap-1">
        <span>{{ s.icon }} {{ s.title }}</span>
        <span class="count">{{ s.list.length }}</span>
        <button type="button" class="iact ms-auto" :title="isUnfolded(scope(s)) ? 'згорнути всі' : 'розгорнути всі'"
                @click="unfoldAll(scope(s), !isUnfolded(scope(s)))">
          <Icon :name="isUnfolded(scope(s)) ? 'fold' : 'unfold'" />
        </button>
        <IdeaPop v-slot="{ toggle }" kind="idea" :zone :subzone="s.key">
          <button type="button" class="idea" title="Нема потрібної картки? Запропонуй її в цю підкатегорію" @click="toggle">💡 ідея</button>
        </IdeaPop>
        <button v-if="admin" type="button" class="iact add" title="Нова картка в цій підкатегорії" @click="adding = s.key">
          <Icon name="plus" />
        </button>
      </div>
      <TaskEdit v-if="adding === s.key" :task="blank(s)" class="mb-2" @done="adding = ''" />
      <div v-if="s.list.length" class="d-flex gap-3 align-items-start">
        <div v-for="(col, ci) in split(s.list, cols)" :key="ci" class="col-stack">
          <TaskCard v-for="t in col" :key="t.id" :task="t" />
        </div>
      </div>
      <TaskMoreRow :scope="scope(s)" :n="s.more" class="mt-1" />
    </div>
  </div>
</template>

<style scoped>
.col-stack { flex: 1 1 0; min-width: 0; }
.task-group { padding-left: .5rem; border-left: 3px solid var(--sc); }
.group-head { font-size: .85rem; font-weight: 600; color: var(--sc); margin-bottom: .25rem; }
.group-head .iact { width: 1.35rem; height: 1.35rem; font-size: .95rem; }
.group-head :deep(.pop-panel) { color: var(--bs-body-color); }  /* the idea's panel opens inside the coloured head */
.count { font-weight: 400; opacity: .55; font-size: .85em; }
.idea { padding: .05rem .4rem; border: 0; border-radius: .3rem; background: none; font-size: .75rem; font-weight: 400; color: var(--act-add); white-space: nowrap; }
.idea:hover { background: color-mix(in srgb, var(--act-add) 12%, transparent); }
[data-bs-theme=dark] .group-head { color: color-mix(in srgb, var(--sc) 60%, #fff); }
</style>
