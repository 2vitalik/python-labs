<script setup>
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { usePolling } from '../activity.js'
import { getWeeks } from '../api.js'
import Crumbs from '../components/Crumbs.vue'
import WeekHeat from '../components/WeekHeat.vue'
import WeekPairs from '../components/WeekPairs.vue'
import WeekProgress from '../components/WeekProgress.vue'
import WeekWindows from '../components/WeekWindows.vue'
import { useStudentFilter } from '../studentFilter.js'
import { user } from '../user.js'
import { toCells } from '../week.js'
import { lay, stateOf, tally, windows } from '../weekSum.js'
import MyWeekPage from './MyWeekPage.vue'

// the stream's week (T177). A student sees their own week here; the teacher — everyone's weeks over one grid:
// where a class would hit the fewest people, and who exactly. The view lives in the URL: ?group=A,B (as on /students) · ?layer= · ?len= (minutes)
const route = useRoute()
const router = useRouter()
const admin = user.value?.status === 'admin'
const LAYERS = { no: 'Не можуть', meh: 'Незручно', ok: 'Найкраще' }
const data = ref(null)
const error = ref('')
const at = ref(null)  // the window looked at: its day and first row
const set = (patch) => router.replace({ query: { ...route.query, ...patch } })

const { shown, groups, toggleGroup } = useStudentFilter(() => data.value?.students || [])
const NONE = '-'  // «no group» among a chip's keys, as studentFilter.js counts it
const done = (g) => data.value.students.filter((s) => g.keys.includes(s.group || NONE) && stateOf(s) === 'done').length
const layer = computed(() => (route.query.layer in LAYERS ? route.query.layer : 'no'))
const len = computed({ get: () => Number(route.query.len) || 90, set: (v) => set({ len: v === 90 ? undefined : v }) })

const laid = computed(() => lay(shown.value, data.value.frame))
const counts = computed(() => tally(laid.value, data.value.frame))
const mine = computed(() => data.value.me && toCells(data.value.me.marks, data.value.frame))
const list = computed(() => windows(laid.value, data.value.frame, len.value, mine.value))
// a start chosen on the map near the end of the day is the last class that still fits
const picked = computed(() => at.value && list.value.find((w) => w.day === at.value.day && w.r0 === Math.min(at.value.r0, list.value.at(-1).r0)))

async function load() {
  try {
    data.value = await getWeeks()
    error.value = ''
  } catch (e) {
    error.value = e.message
  }
}
if (admin) {
  load()
  usePolling(load, 30)  // the numbers grow while the stream fills its weeks in
}
</script>

<template>
  <MyWeekPage v-if="!admin" />
  <div v-else>
    <Crumbs :items="['Тиждень потоку']" />
    <div class="d-flex flex-wrap align-items-center gap-2 mb-3">
      <h1 class="h3 mb-0 me-auto">Тиждень потоку</h1>
      <RouterLink to="/my/week" class="btn btn-outline-secondary btn-sm">🗓 Мій тиждень</RouterLink>
    </div>
    <div v-if="error" class="alert alert-danger">{{ error }}</div>
    <template v-if="data">
      <div class="d-flex flex-wrap gap-1 mb-2">
        <button v-for="g in groups" :key="g.name" type="button" class="btn btn-sm chip" :class="g.on ? 'btn-secondary' : 'btn-outline-secondary'"
                :title="`${g.name}: заповнили ${done(g)} з ${g.n}`" @click="toggleGroup(g)">{{ g.text }} <span class="count">{{ done(g) }}/{{ g.n }}</span></button>
      </div>
      <WeekProgress :students="shown" />
      <div class="d-flex flex-wrap align-items-center gap-2 mb-2">
        <div class="btn-group btn-group-sm">
          <button v-for="(text, key) in LAYERS" :key="key" type="button" class="btn" :class="key === layer ? 'btn-secondary' : 'btn-outline-secondary'"
                  @click="set({ layer: key === 'no' ? undefined : key })">{{ text }}</button>
        </div>
        <span class="small text-secondary">у клітинці — скільки людей із {{ laid.length }} ·
          {{ data.me ? 'заштриховано — ти не можеш' : 'познач у «Мій тиждень» свої години — їх буде викреслено' }}</span>
      </div>
      <WeekHeat class="mb-4" :frame="data.frame" :counts :layer :mine :picked @pick="(day, r0) => (at = { day, r0 })" />
      <WeekWindows v-model:len="len" :list :laid :picked @pick="(w) => (at = w && { day: w.day, r0: w.r0 })" />
      <WeekPairs :list :laid :len />
    </template>
  </div>
</template>

<style scoped>
.count { font-weight: 400; opacity: .55; font-size: .85em; }
</style>
