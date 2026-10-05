<script setup>
import { computed, ref, watchEffect } from 'vue'

import Crumbs from '../components/Crumbs.vue'
import WeekBar from '../components/WeekBar.vue'
import WeekDayNav from '../components/WeekDayNav.vue'
import WeekHeat from '../components/WeekHeat.vue'
import WeekPairs from '../components/WeekPairs.vue'
import WeekPicked from '../components/WeekPicked.vue'
import WeekProgress from '../components/WeekProgress.vue'
import WeekStrips from '../components/WeekStrips.vue'
import WeekStuck from '../components/WeekStuck.vue'
import WeekWhys from '../components/WeekWhys.vue'
import WeekWindows from '../components/WeekWindows.vue'
import { problem } from '../problem.js'
import { useTitle } from '../title.js'
import { user } from '../user.js'
import { DAY_NAMES } from '../week.js'
import { stateOf } from '../weekSum.js'
import { useWeekView } from '../weekView.js'
import MyWeekPage from './MyWeekPage.vue'

// the stream's week (T177, T186). A student sees their own week here; the teacher — everyone's: each person a strip, group by group,
// on the whole window, or one day of it on /week/3. What it counts and where the view is kept — weekView.js
const admin = user.value?.status === 'admin'
const { data, error, frame, day, demo, chips, toggleGroup, shown, len, view, layer, sort, soft, withStuck, skip,
        mine, laid, groups, total, counts, list, busy, free, tops, stuckOnes, windowAt, picked, pick } = admin ? useWeekView() : {}
const lit = ref(null)  // the reason whose chip the pointer is over
const strips = computed(() => day.value !== null || view.value === 'strips')
const days = computed(() => (day.value === null ? [...Array(frame.value.days).keys()] : [day.value]))
const NONE = '-'  // «no group» among a chip's keys, as studentFilter.js counts it
const done = (g) => data.value.students.filter((s) => g.keys.includes(s.group || NONE) && stateOf(s) === 'done').length
if (admin) {
  useTitle(() => (day.value === null ? '' : `${DAY_NAMES[day.value]} · Тиждень потоку`))
  watchEffect(() => {
    if (frame.value && day.value !== null && !(day.value >= 0 && day.value < frame.value.days)) problem.value = 'lost'
  })
}
</script>

<template>
  <MyWeekPage v-if="!admin" />
  <div v-else>
    <Crumbs :items="day === null ? ['Тиждень потоку'] : [[{ path: '/week', query: $route.query }, 'Тиждень потоку'], DAY_NAMES[day]]" />
    <div class="d-flex flex-wrap align-items-center gap-2 mb-3">
      <h1 class="h3 mb-0 me-auto">{{ day === null ? 'Тиждень потоку' : DAY_NAMES[day] }}</h1>
      <WeekDayNav v-if="day !== null && frame" :day :days="frame.days" />
      <RouterLink to="/my/week" class="btn btn-outline-secondary btn-sm">🗓 Мій тиждень</RouterLink>
    </div>
    <div v-if="error" class="alert alert-danger">{{ error }}</div>
    <div v-if="demo" class="alert alert-warning py-2">🧪 Вигадані дані: так сторінка виглядатиме, коли позначать {{ demo }} % потоку ·
      <RouterLink :to="{ query: { ...$route.query, demo: undefined } }">до справжніх</RouterLink></div>
    <template v-if="data">
      <div class="d-flex flex-wrap gap-1 mb-2">
        <button v-for="g in chips" :key="g.name" type="button" class="btn btn-sm chip" :class="g.on ? 'btn-secondary' : 'btn-outline-secondary'"
                :title="`${g.name}: заповнили ${done(g)} з ${g.n}`" @click="toggleGroup(g)">{{ g.text }} <span class="count">{{ done(g) }}/{{ g.n }}</span></button>
      </div>
      <WeekBar v-model:view="view" v-model:len="len" v-model:sort="sort" v-model:layer="layer" :roomy="day !== null" :busy />
      <WeekWhys v-model:soft="soft" v-model:lit="lit" :laid />
      <WeekStrips v-if="strips" class="mb-4" :frame :days :groups :counts :tops :window-at="windowAt"
                  :total :mine :picked :lit :roomy="day !== null" @pick="pick" />
      <WeekHeat v-else class="mb-4" :frame :counts :layer :mine :picked @pick="pick" />
      <div class="row g-4">
        <div class="col-lg-6">
          <WeekWindows v-model:skip="skip" :free :tops :len :picked :total :busy :empty="!laid.length" @pick="(w) => pick(w.day, w.r0)" />
          <WeekStuck v-model="withStuck" :people="stuckOnes" />
          <WeekProgress :students="shown" />
        </div>
        <div class="col-lg-6"><WeekPicked :w="picked" :laid :groups :total @close="pick(null)" /></div>
      </div>
      <WeekPairs v-if="day === null" :list :laid :len />
    </template>
  </div>
</template>

<style scoped>
.count { font-weight: 400; opacity: .55; font-size: .85em; }
</style>
