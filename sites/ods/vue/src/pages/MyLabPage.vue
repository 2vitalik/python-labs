<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

import Crumbs from '@core/components/Crumbs.vue'
import { fmtWhen } from '@core/labs.js'
import { problem } from '@core/problem.js'
import { useTitle } from '@core/title.js'
import { user } from '@core/user.js'

import { findMyLab } from '../api.js'
import LabByTelegram from '../components/LabByTelegram.vue'
import LabCard from '../components/LabCard.vue'
import LabClaim from '../components/LabClaim.vue'
import LabDefence from '../components/LabDefence.vue'
import LabHandIn from '../components/LabHandIn.vue'
import LabSeen from '../components/LabSeen.vue'
import { gates, loadGates } from '../labGates.js'

// the student's own lab (T200, T354), as steps top to bottom: the card and the notebook to start from → the defence
// questions → hand the file in → what the site sees in it → how to defend → the mark. Whatever comes back from the API
// replaces MY whole, and only the blocks below the one in use change. A lab handed in by Telegram (labGates.js) has
// words in place of the hand-in; a lab hidden from students is not there
const route = useRoute()
const n = computed(() => Number(route.params.n))
const lab = ref(null)
const gone = ref('')  // why there is no card for them: the API's own words
const here = computed(() => user.value?.status === 'admin' || gates.value?.[n.value] === 'site')  // files go through the site
useTitle(() => `Моя лаба ${n.value}`)

const live = computed(() => {
  const l = lab.value?.formats?.live && lab.value.live
  return l && { ok: Object.values(l.names || {}).filter((x) => x.ok).length, at: l.at }
})

async function load() {
  lab.value = null
  gone.value = ''
  if (!(await loadGates())[n.value]) return (problem.value = 'lost')
  try {
    const my = await findMyLab(n.value)
    if (my.vid) lab.value = my
    else gone.value = my.why
  } catch (e) {
    if (e.status !== 404) throw e
    problem.value = 'lost'  // «no card yet» comes softly; a 404 is a lab hidden since the gates were read
  }
}
function got(my) {
  lab.value = my
  gone.value = ''
}
watch(n, load, { immediate: true })
</script>

<template>
  <div>
    <Crumbs :items="[['/labs', 'Лаби'], [`/labs/${n}`, `Лаба ${n}`], 'Моя лаба']" />
    <h1 class="h2 mb-3">Моя лаба {{ n }}</h1>
    <LabClaim v-if="gone" :n :why="gone" :drop="here" @got="got" />
    <template v-else-if="lab">
      <LabCard :n :lab />
      <section v-if="lab.ask?.length" class="mb-4">
        <h2 class="h5">Питання на захист</h2>
        <ol class="mb-0"><li v-for="q in lab.ask" :key="q">{{ q }}</li></ol>
      </section>
      <LabByTelegram v-if="lab.handin === 'telegram'" :lab />
      <LabHandIn v-else :key="lab.vid" :n :lab @got="got" />
      <LabSeen v-if="lab.file?.id || lab.line" :n :lab />
      <LabDefence :n :lab @got="got" />
      <p v-if="lab.points !== null && lab.points !== undefined" class="alert alert-success">
        Оцінка: <b>{{ lab.points }}</b><template v-if="lab.note"> — {{ lab.note }}</template></p>
      <p v-if="live" class="small text-secondary">Ноутбук на звʼязку: {{ live.ok }} із {{ lab.total }} ✅<template v-if="live.at">,
        востаннє {{ fmtWhen(live.at) }}</template></p>
    </template>
  </div>
</template>
