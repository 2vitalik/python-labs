<script setup>
import { computed, ref, watch } from 'vue'

import { dayTitle, usePolling } from '../activity.js'
import { getActivity } from '../api.js'
import ActivityRow from './ActivityRow.vue'
import Avatar from './Avatar.vue'

// everything that happened, newest first, a heading per day; refreshes itself, «показати ще» goes back in time
const props = defineProps({ nick: String, src: String, staff: Boolean })
const rows = ref([])
const people = ref({})
const one = ref('')
const more = ref(false)
const loaded = ref(false)
const error = ref('')
// no chips — `none`: the person's heading stays without rows; an empty `src` would bring the default set
const params = computed(() => ({ user: props.nick, src: props.src || 'none', staff: props.staff }))
const person = computed(() => people.value[one.value])
const days = computed(() => {
  const out = []
  for (const r of rows.value) {
    const title = dayTitle(r.at)
    if (out.at(-1)?.title !== title) out.push({ title, rows: [] })
    out.at(-1).rows.push(r)
  }
  return out
})

// `extra.before` — an older page; without it — the newest rows, merged into what is already shown
async function load(extra = {}) {
  const asked = JSON.stringify(params.value)
  try {
    const data = await getActivity({ ...params.value, ...extra })
    if (asked !== JSON.stringify(params.value)) return  // the filters changed while we waited
    const known = new Set(rows.value.map((r) => r.id))
    rows.value = [...rows.value, ...data.rows.filter((r) => !known.has(r.id))].sort((a, b) => new Date(b.at) - new Date(a.at) || (a.id < b.id ? 1 : -1))
    people.value = { ...people.value, ...data.people }
    one.value = data.one
    if (extra.before || !loaded.value) more.value = data.more
    error.value = ''
  } catch (e) {
    error.value = e.message
  }
  loaded.value = true
}

watch(params, () => {
  rows.value = []
  loaded.value = false
  load()
}, { immediate: true })
usePolling(load, 15)
</script>

<template>
  <div v-if="person" class="d-flex align-items-center gap-2 border rounded px-3 py-2 mb-3">
    <Avatar :user="person" :size="32" />
    <div class="me-auto">
      <div class="fw-semibold">{{ person.name || person.nick }}</div>
      <div class="small text-secondary">{{ [person.group, one].filter(Boolean).join(' · ') }}</div>
    </div>
    <RouterLink :to="`/students/${person.nick}/edit`" class="btn btn-outline-secondary btn-sm">Профіль</RouterLink>
    <RouterLink :to="`/students/${person.nick}`" class="btn btn-outline-secondary btn-sm">Гра</RouterLink>
    <RouterLink :to="{ query: { ...$route.query, user: undefined } }" class="btn btn-outline-secondary btn-sm" title="Показати всіх">✕</RouterLink>
  </div>
  <div v-if="error" class="alert alert-danger">{{ error }}</div>
  <section v-for="d in days" :key="d.title" class="mb-3">
    <h2 class="day">{{ d.title }} <span class="fw-normal">· {{ d.rows.length }}</span></h2>
    <ActivityRow v-for="r in d.rows" :key="r.id" :row="r" :people :one />
  </section>
  <p v-if="loaded && !rows.length && !error" class="text-secondary text-center mt-4">{{ src ? 'Тут поки тихо.' : 'Оберіть, що показувати.' }}</p>
  <div v-if="more" class="text-center">
    <button class="btn btn-outline-secondary btn-sm" @click="load({ before: rows.at(-1).at })">Показати ще</button>
  </div>
</template>

<style scoped>
.day { font-size: .8rem; font-weight: 600; color: var(--bs-secondary-color); margin: 0; padding: .25rem 0;
       position: sticky; top: 0; background: var(--bs-body-bg); border-bottom: 1px solid var(--bs-border-color); z-index: 1; }
</style>
