<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import { subStyle } from '../catalog.js'
import { isUnfolded, unfoldAll } from '../unfold.js'
import { user } from '@core/user.js'
import TaskCard from './TaskCard.vue'
import TaskEdit from './TaskEdit.vue'

const props = defineProps({ zone: String, color: String, subs: Array })
const admin = computed(() => user.value?.status === 'admin')
const scope = (s) => `${props.zone}/${s.key}`
const adding = ref('')  // the subzone whose «＋» opened a new card's form at its top
const blank = (s) => ({ zone: props.zone, subzone: s.key, status: 'draft' })

const el = ref(null)
const cols = ref(3)
let ro
onMounted(() => {
  ro = new ResizeObserver(([e]) => { cols.value = Math.max(1, Math.floor(e.contentRect.width / 320)) })
  ro.observe(el.value)
})
onBeforeUnmount(() => ro?.disconnect())

// greedy shortest-column packing; depends only on card counts, so expanding a card never reshuffles
const columns = computed(() => {
  const out = Array.from({ length: cols.value }, () => ({ h: 0, groups: [] }))
  for (const s of props.subs) {
    const col = out.reduce((a, b) => (b.h < a.h ? b : a))
    col.groups.push(s)
    col.h += 2 + s.list.length
  }
  return out.map((c) => c.groups)
})
</script>

<template>
  <div ref="el" class="d-flex gap-3 align-items-start">
    <div v-for="(col, ci) in columns" :key="ci" class="col-stack">
      <div v-for="s in col" :key="s.key" class="task-group mb-3" :style="subStyle(color, s.i)">
        <div class="group-head d-flex align-items-center gap-1">
          <span>{{ s.icon }} {{ s.title }}</span>
          <span class="count">{{ s.list.length }}</span>
          <button type="button" class="iact ms-auto" :title="isUnfolded(scope(s)) ? 'згорнути всі' : 'розгорнути всі'"
                  @click="unfoldAll(scope(s), !isUnfolded(scope(s)))">
            <Icon :name="isUnfolded(scope(s)) ? 'fold' : 'unfold'" />
          </button>
          <button v-if="admin" type="button" class="iact add" title="Нова картка в цій підзоні" @click="adding = s.key">
            <Icon name="plus" />
          </button>
        </div>
        <TaskEdit v-if="adding === s.key" :task="blank(s)" class="mb-1" @done="adding = ''" />
        <TaskCard v-for="t in s.list" :key="t.id" :task="t" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.col-stack { flex: 1 1 0; min-width: 0; }
.task-group { padding-left: .5rem; border-left: 3px solid var(--sc); }
.group-head { font-size: .85rem; font-weight: 600; color: var(--sc); margin-bottom: .25rem; }
.group-head .iact { width: 1.35rem; height: 1.35rem; font-size: .95rem; }
.count { font-weight: 400; opacity: .55; font-size: .85em; }
[data-bs-theme=dark] .group-head { color: color-mix(in srgb, var(--sc) 60%, #fff); }
</style>
