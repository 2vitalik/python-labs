<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'

import { subStyle } from '../catalog.js'
import { user } from '../user.js'
import TaskCard from './TaskCard.vue'

const props = defineProps({ zone: String, color: String, subs: Array })

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
          <RouterLink v-if="user?.status === 'admin'" :to="`/tasks/new?zone=${zone}&sub=${s.key}`"
                      class="ms-auto add text-decoration-none" title="Нове завдання в цій підзоні">＋</RouterLink>
        </div>
        <TaskCard v-for="t in s.list" :key="t.id" :task="t" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.col-stack { flex: 1 1 0; min-width: 0; }
.task-group { padding-left: .5rem; border-left: 3px solid var(--sc); }
.group-head { font-size: .85rem; font-weight: 600; color: var(--sc); margin-bottom: .25rem; }
.count { font-weight: 400; opacity: .55; font-size: .85em; }
.add { color: var(--sc); opacity: .4; }
.add:hover { opacity: 1; }
</style>
