<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

import Crumbs from '@core/components/Crumbs.vue'
import { useTitle } from '@core/title.js'

import { getLabResults, putLabResult } from '../api.js'

// the teacher's table of a lab (T200): who holds which card, how many answers are right, the notebook, the mark
const route = useRoute()
const n = computed(() => Number(route.params.n))
const rows = ref([])
const group = ref('')
const saved = ref({})  // vid → '💾' | '⚠️ …'
useTitle(() => `Результати лаби ${n.value}`)

const groups = computed(() => [...new Set(rows.value.map((r) => r.group))])
const inGroup = (r) => !group.value || r.group === group.value
const shown = computed(() => rows.value.filter((r) => r.student && inGroup(r)))
const free = computed(() => rows.value.filter((r) => !r.student && r.n > 0 && inGroup(r)).length)
const fmt = (d) => (d ? new Date(d).toLocaleString('uk-UA', { day: 'numeric', month: 'numeric', hour: '2-digit', minute: '2-digit' }) : '')

async function save(r) {
  const points = r.points === '' || r.points === null ? null : Number(r.points)
  try {
    Object.assign(r, await putLabResult(n.value, r.vid, { points, note: r.note }))
    saved.value[r.vid] = '💾'
  } catch (e) {
    saved.value[r.vid] = `⚠️ ${e.message}`
  }
}

onMounted(async () => (rows.value = await getLabResults(n.value)))
</script>

<template>
  <div>
    <Crumbs :items="[['/labs', 'Лаби'], [`/labs/${n}`, `Лаба ${n}`], 'Результати']" />
    <div class="d-flex flex-wrap align-items-baseline gap-3 mb-3">
      <h1 class="h2 mb-0">Результати лаби {{ n }}</h1>
      <select v-model="group" class="form-select form-select-sm w-auto">
        <option value="">усі групи</option>
        <option v-for="g in groups" :key="g" :value="g">{{ g }}</option>
      </select>
      <span class="small text-secondary">картки взяли: {{ shown.length }} · вільних: {{ free }}</span>
    </div>
    <p v-if="rows.length && !shown.length" class="text-secondary">Ніхто ще не відкривав свою картку.</p>
    <div v-else-if="rows.length" class="table-responsive">
      <table class="table table-sm align-middle">
        <thead>
          <tr><th>Студент</th><th>Варіант</th><th>✅</th><th>Спроб</th><th>Ноутбук</th><th>Перевірено</th><th>Бали</th><th>Нотатка</th><th></th></tr>
        </thead>
        <tbody>
          <tr v-for="r in shown" :key="r.vid">
            <td>{{ r.who?.name || r.student }} <span class="small text-secondary">{{ r.who?.nick }} · {{ r.group }}</span></td>
            <td><code>{{ r.vid }}</code></td>
            <td class="text-nowrap">{{ r.ok }} / {{ r.total }}</td>
            <td>{{ r.attempts }}</td>
            <td><a v-if="r.notebook" :href="r.notebook" target="_blank" rel="noopener">відкрити ↗</a></td>
            <td class="text-nowrap small">{{ fmt(r.checked_at) }}</td>
            <td><input v-model="r.points" type="number" min="0" max="20" class="form-control form-control-sm points" @change="save(r)"></td>
            <td><input v-model="r.note" class="form-control form-control-sm" @change="save(r)"></td>
            <td class="small text-nowrap">{{ saved[r.vid] }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <p v-else class="text-secondary">Варіантів цієї лаби на сайті ще нема: імпорт — lab_io.py в api сайту.</p>
  </div>
</template>

<style scoped>
.points { width: 4.5rem; }
</style>
