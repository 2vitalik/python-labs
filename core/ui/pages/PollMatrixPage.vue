<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { PERIODS } from '../activity.js'
import { getPollMatrix, getPollTemplates } from '../api.js'
import Crumbs from '../components/Crumbs.vue'
import IconArrows from '../components/IconArrows.vue'
import PollMatrix from '../components/PollMatrix.vue'
import { plural } from '../polls.js'
import { toggleWide, wide } from '../wide.js'

// how each student answered each poll. The state lives in the URL, so a view can be bookmarked:
// ?tag= · ?template= · ?days= (polls sent within that many days) · ?group=A,B (rows)
const route = useRoute()
const router = useRouter()
const data = ref(null)
const templates = ref([])
const tags = ref([])
const error = ref('')
const NONE = '-'  // «no group» in ?group=
const asked = computed(() => ({ tag: route.query.tag || '', template: route.query.template || '', days: route.query.days || '' }))
const days = computed(() => Number(route.query.days || 0))
const picked = computed(() => (route.query.group ? String(route.query.group).split(',') : []))
const groups = computed(() => [...new Set((data.value?.rows || []).map((r) => r.group || NONE))].sort())
const shown = computed(() => data.value && {
  ...data.value, rows: picked.value.length ? data.value.rows.filter((r) => picked.value.includes(r.group || NONE)) : data.value.rows,
})
const set = (patch) => router.replace({ query: { ...route.query, ...patch } })
const toggleGroup = (g) => set({ group: (picked.value.includes(g) ? picked.value.filter((x) => x !== g) : [...picked.value, g]).join() || undefined })
const chip = (on) => (on ? 'btn-secondary' : 'btn-outline-secondary')

async function load() {
  try {
    data.value = await getPollMatrix(asked.value)
    error.value = ''
  } catch (e) {
    error.value = e.message
  }
}
watch(() => JSON.stringify(asked.value), load, { immediate: true })
onMounted(async () => {
  const t = await getPollTemplates()
  templates.value = t.templates
  tags.value = t.tags
})
</script>

<template>
  <div>
    <Crumbs :items="[['/polls', 'Опитування'], 'Таблиця']" />
    <div class="d-flex flex-wrap align-items-center gap-2 mb-3">
      <h1 class="h3 mb-0">Хто як відповідав</h1>
      <span v-if="shown" class="text-secondary">{{ shown.polls.length }} {{ plural(shown.polls.length, 'опитування', 'опитування', 'опитувань') }} ·
        {{ shown.rows.length }} {{ plural(shown.rows.length, 'студент', 'студенти', 'студентів') }}</span>
      <button type="button" class="btn btn-outline-secondary btn-sm d-inline-flex align-items-center px-2 ms-auto"
              :title="wide ? 'Назад у колонку сторінки' : 'Таблиця на всю ширину'" @click="toggleWide"><IconArrows :out="!wide" /></button>
    </div>

    <div class="d-flex flex-wrap align-items-center gap-1 mb-2">
      <button type="button" class="btn btn-sm chip" :class="chip(!asked.tag)" @click="set({ tag: undefined })">усі теги</button>
      <button v-for="t in tags" :key="t" type="button" class="btn btn-sm chip" :class="chip(asked.tag === t)" @click="set({ tag: asked.tag === t ? undefined : t })">#{{ t }}</button>
      <select v-if="templates.length" class="form-select form-select-sm w-auto ms-2" :value="asked.template" @change="set({ template: $event.target.value || undefined })">
        <option value="">усі шаблони</option>
        <option v-for="t in templates" :key="t.id" :value="t.id">{{ t.title }}</option>
      </select>
    </div>
    <div class="d-flex flex-wrap align-items-center gap-1 mb-3">
      <button v-for="[n, text] in PERIODS" :key="n" type="button" class="btn btn-sm chip" :class="chip(days === n)" @click="set({ days: n || undefined })">{{ text }}</button>
      <span v-if="groups.length > 1" class="ms-2 small text-secondary">групи:</span>
      <template v-if="groups.length > 1">
        <button v-for="g in groups" :key="g" type="button" class="btn btn-sm chip" :class="chip(picked.includes(g))" @click="toggleGroup(g)">{{ g === NONE ? 'без групи' : g }}</button>
      </template>
    </div>

    <div v-if="error" class="alert alert-danger">{{ error }}</div>
    <template v-if="shown">
      <PollMatrix v-if="shown.polls.length" :data="shown" />
      <p v-else class="text-secondary text-center my-4">
        {{ asked.tag || asked.template || days ? 'Під ці фільтри надісланих опитувань нема.' : 'Надісланих опитувань ще нема — таблиця зʼявиться з першим.' }}
      </p>
      <p v-if="shown.polls.length" class="small text-secondary mt-2">
        У клітинці — емодзі відповіді (наведи — текст і час) · <b>·</b> — голосу нема · ↩︎ — голос відкликано ·
        🚫 — бот не привʼязаний: такі голоси — серед «Інших голосів» · заголовок колонки веде на опитування.
      </p>
    </template>
  </div>
</template>
