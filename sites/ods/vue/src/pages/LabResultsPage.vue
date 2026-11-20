<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

import Crumbs from '@core/components/Crumbs.vue'
import { useTitle } from '@core/title.js'

import { getLabResults } from '../api.js'
import LabBar from '../components/LabBar.vue'
import LabLoose from '../components/LabLoose.vue'
import LabResultsRow from '../components/LabResultsRow.vue'
import LabStats from '../components/LabStats.vue'
import LabWide from '../components/LabWide.vue'

// the teacher's table of a lab (T200, T354): whom which card is pinned to, the answers, the file and what it has, the
// hint by the levels, the defence, the mark; a name leads to the review of that work; students without a card — below
const route = useRoute()
const n = computed(() => Number(route.params.n))
const rows = ref([])
const group = ref('')
const quick = ref('all')
const picked = ref(null)  // the vids a quick filter took when chosen: a row stays while its mark is being typed
useTitle(() => `Результати лаби ${n.value}`)

const hasFile = (r) => !!r.file?.id
const QUICK = { all: ['усі', () => true], file: ['з файлом', hasFile], nofile: ['без файла', (r) => !hasFile(r)],
                nopoints: ['без балів', (r) => r.points === null || r.points === undefined || r.points === ''] }
const groups = computed(() => [...new Set(rows.value.map((r) => r.group))])
const inGroup = (r) => !group.value || r.group === group.value
const real = computed(() => rows.value.filter((r) => r.n > 0 && inGroup(r)))  // n = 0 — the demo card
const taken = computed(() => rows.value.filter((r) => r.student && inGroup(r)))
const shown = computed(() => taken.value.filter((r) => !picked.value || picked.value.has(r.vid)))
const count = (k) => taken.value.filter((r) => r.n > 0 && QUICK[k][1](r)).length  // the demo's row is shown, not counted
const runs = computed(() => rows.value.some((r) => r.file?.run))  // the rerun column only once there is a rerun

function choose(k) {
  quick.value = k
  picked.value = k === 'all' ? null : new Set(rows.value.filter(QUICK[k][1]).map((r) => r.vid))
}

const load = async () => (rows.value = await getLabResults(n.value))
// the lab's bar leads from a lab's results to another lab's: the same page, another lab's rows, the filters afresh
watch(n, () => {
  rows.value = []
  group.value = ''
  choose('all')
  load()
}, { immediate: true })
</script>

<template>
  <div>
    <LabBar />
    <Crumbs :items="[['/labs', 'Лаби'], [`/labs/${n}`, `Лаба ${n}`], 'Результати']"><LabWide /></Crumbs>
    <div class="d-flex flex-wrap align-items-baseline gap-3 mb-2">
      <h1 class="h2 mb-0">Результати лаби {{ n }}</h1>
      <select v-model="group" class="form-select form-select-sm w-auto">
        <option value="">усі групи</option>
        <option v-for="g in groups" :key="g" :value="g">{{ g }}</option>
      </select>
      <span class="small text-secondary">карток закріплено {{ taken.filter((r) => r.n > 0).length }} із {{ real.length }}</span>
    </div>
    <div v-if="taken.length" class="d-flex flex-wrap align-items-center gap-1 mb-3">
      <span class="small text-secondary me-1">показати</span>
      <button v-for="(q, k) in QUICK" :key="k" type="button" class="btn btn-sm chip" :class="quick === k ? 'btn-secondary' : 'btn-outline-secondary'"
              @click="choose(k)">{{ q[0] }} <span class="opacity-75">{{ count(k) }}</span></button>
    </div>
    <LabStats v-if="taken.length" :key="n" :n />
    <p v-if="rows.length && !taken.length" class="text-secondary">Карток цієї лаби ще ні за ким не закріплено.</p>
    <div v-else-if="rows.length" class="table-responsive">
      <table class="table table-sm align-middle">
        <thead class="small">
          <tr><th>Студент</th><th>Варіант</th><th>Відповіді</th><th>Файл</th><th>Пункти</th><th v-if="runs">Перезапуск</th><th>Захист</th>
            <th>Підказка</th><th>Бали</th><th>Нотатка</th><th></th></tr>
        </thead>
        <tbody>
          <LabResultsRow v-for="r in shown" :key="r.vid" :n :r :runs />
        </tbody>
      </table>
    </div>
    <p v-else class="text-secondary">Варіантів цієї лаби на сайті ще нема: імпорт — lab_io.py в api сайту.</p>
    <LabLoose v-if="rows.length" :key="n" :n @pinned="load" />
  </div>
</template>
