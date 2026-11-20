<script setup>
import { computed, onMounted, ref, shallowRef } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import Crumbs from '@core/components/Crumbs.vue'
import Lightbox from '@core/components/Lightbox.vue'
import { loadGuide } from '@core/guide.js'

import '../changes.css'
import ChangeFilters from '../components/ChangeFilters.vue'
import ChangeList from '../components/ChangeList.vue'
import ChangeSummary from '../components/ChangeSummary.vue'
import { filterOf, fits } from '../lectureChangeFilter.js'
import { useChangeWalk } from '../lectureChangeKeys.js'
import { loadChanges } from '../lectureChanges.js'

// what was changed in the lectures against the lecturer's slides (T374): at a glance, filters, the list; a change opens
// under its row as «Було | Стало». Everything is in the address (?lec=5&sev=3&id=05-A6) — a link can be passed on
const route = useRoute()
const router = useRouter()
const data = shallowRef(null)  // thousands of plain items: no proxy over each
const error = ref('')
const f = computed(() => filterOf(route.query))
const open = computed(() => route.query.id || null)
// the filters' changes; the open one stays among them whatever they say — a link to it shows it
const list = computed(() => data.value?.items.filter((it) => fits(it, f.value) || it.id === open.value) || [])
const set = (patch) => router.replace({ query: { ...route.query, ...patch } })
const { cur, limit, fit, toggle, shown } = useChangeWalk(list, open, set, () => JSON.stringify(f.value))

onMounted(async () => {
  loadGuide()
  try {
    data.value = await loadChanges()
    if (open.value) fit(open.value)
  } catch (e) {
    error.value = e.message
  }
})
</script>

<template>
  <div class="changes">
    <Crumbs :items="[['/lectures', 'Лекції'], 'Зміни']" />
    <h1 class="h2 mb-1">Зміни в лекціях</h1>
    <p class="quiet mb-3">Що в текстах лекцій інакше, ніж на слайдах лектора · клавіші: ↑ ↓ — по списку, Enter — відкрити, Esc — закрити</p>
    <div v-if="error" class="alert alert-danger">{{ error }}</div>
    <p v-else-if="!data" class="text-secondary">Завантажую…</p>
    <p v-else-if="!data.items.length" class="text-secondary my-4">Каталогу змін ще нема: його будує <code>bin/lecchanges build</code>, на сайт — <code>bin/content push lectures</code>.</p>
    <template v-else>
      <div class="chg-top">
        <ChangeSummary :items="data.items" :f :query="route.query" @set="set" />
        <ChangeFilters :items="data.items" :f :query="route.query" @set="set" />
      </div>
      <p class="chg-count"><b>{{ list.length }}</b> з {{ data.items.length }} змін</p>
      <ChangeList v-if="list.length" :list :items="data.items" :limit :open :cur @toggle="toggle" @more="limit += $event" @ready="shown" />
      <p v-else class="text-secondary">Під цей вибір нічого нема.</p>
    </template>
    <Lightbox />
  </div>
</template>
