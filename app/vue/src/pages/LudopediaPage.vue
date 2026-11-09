<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import Crumbs from '@core/components/Crumbs.vue'
import LudoTable from '../components/LudoTable.vue'
import { FAMILIES, getLudoGames, KLASSES, STAGES } from '../ludopedia.js'
import { norm } from '../taskFilter.js'

// the corpus of reference games (data/ludopedia/): filters live in the URL — ?fam= ?klass= ?stage= ?mech= ?q=
const route = useRoute()
const router = useRouter()
const games = ref([])
const error = ref('')
const loaded = ref(false)
const f = computed(() => ({ fam: route.query.fam || '', klass: route.query.klass || '', stage: route.query.stage || '', mech: route.query.mech || '', q: route.query.q || '' }))
function set(patch) {
  const q = { ...route.query, ...patch }
  for (const k in q) if (!q[k]) delete q[k]
  router.replace({ query: q })
}
const toggle = (k, v) => set({ [k]: f.value[k] === v ? '' : v })

function matches(g, skip = '') {
  const v = f.value
  if (skip !== 'fam' && v.fam && g.family !== v.fam && !g.also.includes(v.fam)) return false
  if (v.klass && g.klass !== v.klass) return false
  if (v.stage && g.stage !== v.stage) return false
  if (v.mech && !g.mechanics.includes(v.mech) && !g.mechanics.includes(`+${v.mech}`)) return false
  return !v.q || norm([g.title, g.headline, ...g.aka, g.slug, ...g.mechanics].join(' ')).includes(norm(v.q))
}
const found = computed(() => games.value.filter((g) => matches(g)))
const famCounts = computed(() => {
  const c = {}
  for (const g of games.value) if (matches(g, 'fam')) c[g.family] = (c[g.family] || 0) + 1
  return c
})
const groups = computed(() => (f.value.fam ? [{ key: f.value.fam, list: found.value }]
  : Object.keys(FAMILIES).map((key) => ({ key, list: found.value.filter((g) => g.family === key) })).filter((x) => x.list.length)))

onMounted(async () => {
  try { games.value = await getLudoGames() } catch (e) { error.value = e.message }
  loaded.value = true
})
</script>

<template>
  <div>
    <Crumbs :items="['Лудопедія']" />
    <div class="d-flex flex-wrap align-items-baseline gap-2 mb-2">
      <h1 class="h3 mb-0">Лудопедія <span class="text-secondary fs-6">({{ found.length }} з {{ games.length }})</span></h1>
      <span class="text-secondary small">референсні ігри, розкладені мовою опису студентських ігор: сутності · правила · вікна · фічі</span>
    </div>

    <div class="d-flex flex-wrap gap-1 mb-2">
      <button type="button" class="btn btn-sm" :class="!f.fam ? 'btn-secondary' : 'btn-outline-secondary'" @click="set({ fam: '' })">усі сімʼї</button>
      <button v-for="(fam, key) in FAMILIES" :key type="button" class="btn btn-sm" :class="f.fam === key ? 'btn-secondary' : 'btn-outline-secondary'"
              :title="fam[1]" @click="toggle('fam', key)">{{ fam[0] }} <span class="opacity-75">{{ famCounts[key] || 0 }}</span></button>
    </div>
    <div class="d-flex flex-wrap align-items-center gap-1 mb-3">
      <button v-for="(label, k) in KLASSES" :key="k" type="button" class="btn btn-sm" :class="f.klass === k ? 'btn-primary' : 'btn-outline-primary'" @click="toggle('klass', k)">{{ label }}</button>
      <span class="vr mx-1"></span>
      <button v-for="(label, s) in STAGES" :key="s" type="button" class="btn btn-sm" :class="f.stage === s ? 'btn-success' : 'btn-outline-success'" :title="label" @click="toggle('stage', s)">{{ s }}</button>
      <span v-if="f.mech" class="badge text-bg-warning fw-normal ms-1">механіка: <code>{{ f.mech }}</code>
        <RouterLink v-if="!f.mech.startsWith('+')" :to="`/tasks?q=${f.mech}`" class="ms-1 text-decoration-none" title="Картка каталогу">↗</RouterLink>
        <button type="button" class="btn-close btn-close-sm ms-1 align-middle" title="Зняти" @click="set({ mech: '' })"></button></span>
      <input :value="f.q" class="form-control form-control-sm ms-auto search" placeholder="назва, інша назва, тег…" @input="set({ q: $event.target.value })">
    </div>
    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <template v-for="g in groups" :key="g.key">
      <h2 v-if="!f.fam" class="h6 text-secondary mt-3 mb-1">{{ FAMILIES[g.key]?.[0] || g.key }} <span class="opacity-75">· {{ g.list.length }}</span></h2>
      <LudoTable :list="g.list" :family="!!f.fam" />
    </template>
    <p v-if="loaded && !found.length && !error" class="text-secondary text-center my-4">Нічого не знайшлось — зніми фільтр або зміни запит.</p>
  </div>
</template>

<style scoped>
.search { max-width: 16rem; }
.btn-close-sm { font-size: .6rem; }
</style>
