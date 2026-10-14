<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { getAttendanceMatrix } from '../api.js'
import AttendanceMatrix from '../components/AttendanceMatrix.vue'
import Crumbs from '../components/Crumbs.vue'
import IconArrows from '../components/IconArrows.vue'
import { KINDS_MANY } from '../lesson.js'
import { toggleWide, wide } from '../wide.js'

// who was at which lesson, by Zoom (T222). The state lives in the URL: ?kind= one kind of lesson · ?group=A,B the rows
const route = useRoute()
const router = useRouter()
const data = ref(null)
const error = ref('')
const NONE = '-'
const kind = computed(() => route.query.kind || '')
const picked = computed(() => (route.query.group ? String(route.query.group).split(',') : []))
const kinds = computed(() => Object.keys(KINDS_MANY).filter((k) => data.value?.lessons.some((l) => l.kind === k)))
const groups = computed(() => [...new Set((data.value?.rows || []).map((r) => r.group || NONE))].sort())
const shown = computed(() => data.value && {
  lessons: data.value.lessons.filter((l) => !kind.value || l.kind === kind.value),
  rows: picked.value.length ? data.value.rows.filter((r) => picked.value.includes(r.group || NONE)) : data.value.rows,
})
const set = (patch) => router.replace({ query: { ...route.query, ...patch } })
const toggleGroup = (g) => set({ group: (picked.value.includes(g) ? picked.value.filter((x) => x !== g) : [...picked.value, g]).join() || undefined })
const chip = (on) => (on ? 'btn-secondary' : 'btn-outline-secondary')
onMounted(async () => {
  try {
    data.value = await getAttendanceMatrix()
  } catch (e) {
    error.value = e.message
  }
})
</script>

<template>
  <div>
    <Crumbs :items="[['/lessons', 'Заняття'], 'Відвідування']" />
    <div class="d-flex flex-wrap align-items-center gap-2 mb-3">
      <h1 class="h3 mb-0">Відвідування</h1>
      <span v-if="shown" class="text-secondary">{{ shown.lessons.length }} занять · {{ shown.rows.length }} студентів</span>
      <button type="button" class="btn btn-outline-secondary btn-sm d-inline-flex align-items-center px-2 ms-auto"
              :title="wide ? 'Назад у колонку сторінки' : 'Таблиця на всю ширину'" @click="toggleWide"><IconArrows :out="!wide" /></button>
    </div>
    <div v-if="kinds.length > 1 || groups.length > 1" class="d-flex flex-wrap align-items-center gap-1 mb-3">
      <template v-if="kinds.length > 1">
        <button type="button" class="btn btn-sm chip" :class="chip(!kind)" @click="set({ kind: undefined })">усі</button>
        <button v-for="k in kinds" :key="k" type="button" class="btn btn-sm chip" :class="chip(kind === k)" @click="set({ kind: kind === k ? undefined : k })">{{ KINDS_MANY[k] }}</button>
      </template>
      <template v-if="groups.length > 1">
        <span class="ms-2 small text-secondary">групи:</span>
        <button v-for="g in groups" :key="g" type="button" class="btn btn-sm chip" :class="chip(picked.includes(g))" @click="toggleGroup(g)">{{ g === NONE ? 'без групи' : g }}</button>
      </template>
    </div>
    <div v-if="error" class="alert alert-danger">{{ error }}</div>
    <template v-if="shown">
      <AttendanceMatrix v-if="shown.lessons.length" :data="shown" />
      <p v-else class="text-secondary text-center my-4">Відвідування ще не забиралось — «Оновити із Zoom» на сторінці заняття або <code>bin/zoom pull</code>.</p>
      <p v-if="shown.lessons.length" class="small text-secondary mt-2">
        У клітинці — хвилини в Zoom, зелень — частка заняття (наведи — точно) · <b>·</b> — не було · бліді — менше чверті заняття ·
        Σ — занять із чвертю й більше, годин разом · <span class="text-warning">+N?</span> під колонкою — імена, яких реєстр не знає.
      </p>
    </template>
  </div>
</template>
