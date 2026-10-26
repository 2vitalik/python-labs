<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { getLabs } from '../api.js'
import Crumbs from '../components/Crumbs.vue'
import DeadlineForm from '../components/DeadlineForm.vue'
import IconArrows from '../components/IconArrows.vue'
import LabMatrix from '../components/LabMatrix.vue'
import { STATES } from '../labs.js'
import { toggleWide, wide } from '../wide.js'

// who met which lab's deadline (T235). The state lives in the URL: ?group=A,B the rows · ?state=check,miss rows with such a cell
const route = useRoute()
const router = useRouter()
const data = ref(null)
const error = ref('')
const editing = ref(null)  // the lab whose deadline form is open
const NONE = '-'
const groups = computed(() => [...new Set((data.value?.rows || []).map((r) => r.group || NONE))].sort())
const pickedGroups = computed(() => (route.query.group ? String(route.query.group).split(',') : []))
const pickedStates = computed(() => (route.query.state ? String(route.query.state).split(',') : []))
const shown = computed(() => data.value && {
  labs: data.value.labs,
  rows: data.value.rows.filter((r) => (!pickedGroups.value.length || pickedGroups.value.includes(r.group || NONE))
    && (!pickedStates.value.length || Object.values(r.cells).some((c) => pickedStates.value.includes(c.state)))),
})
const count = (k) => (data.value?.rows || []).filter((r) => Object.values(r.cells).some((c) => c.state === k)).length
const set = (patch) => router.replace({ query: { ...route.query, ...patch } })
const flip = (list, x) => (list.includes(x) ? list.filter((y) => y !== x) : [...list, x]).join() || undefined
const chip = (on) => (on ? 'btn-secondary' : 'btn-outline-secondary')

async function load() {
  try {
    data.value = await getLabs()
  } catch (e) {
    error.value = e.message
  }
}
function onCell(nick, lab, cell) {
  data.value.rows.find((r) => r.nick === nick).cells[lab] = cell
}
async function onDeadlines() {
  await load()  // every cell depends on the deadlines
}
onMounted(load)
</script>

<template>
  <div>
    <Crumbs :items="[['/students', 'Студенти'], 'Дедлайни']" />
    <div class="d-flex flex-wrap align-items-center gap-2 mb-3">
      <h1 class="h3 mb-0">Дедлайни</h1>
      <span v-if="shown" class="text-secondary">{{ shown.rows.length }} студентів</span>
      <button type="button" class="btn btn-outline-secondary btn-sm d-inline-flex align-items-center px-2 ms-auto"
              :title="wide ? 'Назад у колонку сторінки' : 'Таблиця на всю ширину'" @click="toggleWide"><IconArrows :out="!wide" /></button>
    </div>
    <div v-if="data" class="d-flex flex-wrap align-items-center gap-1 mb-3">
      <template v-if="groups.length > 1">
        <button v-for="g in groups" :key="g" type="button" class="btn btn-sm chip" :class="chip(pickedGroups.includes(g))"
                @click="set({ group: flip(pickedGroups, g) })">{{ g === NONE ? 'без групи' : g }}</button>
        <span class="mx-1 text-secondary">·</span>
      </template>
      <button v-for="[k, s] in Object.entries(STATES).filter(([k]) => k !== 'nodue' && count(k))" :key="k" type="button" class="btn btn-sm chip" :class="chip(pickedStates.includes(k))"
              :title="s.text" @click="set({ state: flip(pickedStates, k) })">{{ s.emoji }} {{ count(k) }}</button>
    </div>
    <div v-if="error" class="alert alert-danger">{{ error }}</div>
    <template v-if="shown">
      <DeadlineForm v-if="editing" :key="editing" :lab="editing" :deadlines="data.labs.find((l) => l.n === editing).deadlines"
                    :groups="groups.filter((g) => g !== NONE)" @saved="onDeadlines" @close="editing = null" />
      <LabMatrix :data="shown" @deadline="editing = $event" @cell="onCell" />
      <p class="small text-secondary mt-2">
        Клітинка — стан лаби студента, під емодзі — останній коміт до дедлайну або дата подовження «→»; ✍ — слово викладача; клік — подовження, вердикт, звіт.
        ✏️ у шапці — дедлайн лаби. Факти з репозиторіїв — <code>bin/repos pull</code> → <code>push</code>; звіти — <code>bin/repos reviews</code>.
      </p>
    </template>
  </div>
</template>
