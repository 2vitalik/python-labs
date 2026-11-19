<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

import Crumbs from '@core/components/Crumbs.vue'
import { fmtWhen } from '@core/labs.js'
import { useTitle } from '@core/title.js'

import { getMyLab } from '../api.js'
import LabCard from '../components/LabCard.vue'
import LabClaim from '../components/LabClaim.vue'
import LabDefence from '../components/LabDefence.vue'
import LabHandIn from '../components/LabHandIn.vue'
import LabSeen from '../components/LabSeen.vue'

// the student's own lab (T200, T354), as steps top to bottom: the card and the notebook to start from → the defence
// questions → hand the file in → what the site sees in it → how to defend → the mark. Whatever comes back from the API
// replaces MY whole, and only the blocks below the one in use change
const route = useRoute()
const n = computed(() => Number(route.params.n))
const lab = ref(null)
const gone = ref('')  // why there is no card for them: the API's own words
useTitle(() => `Моя лаба ${n.value}`)

const live = computed(() => {
  const l = lab.value?.formats?.live && lab.value.live
  return l && { ok: Object.values(l.names || {}).filter((x) => x.ok).length, at: l.at }
})

async function load() {
  lab.value = null
  gone.value = ''
  try {
    lab.value = await getMyLab(n.value)
  } catch (e) {
    if (e.status !== 404) throw e
    gone.value = e.message
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
    <LabClaim v-if="gone" :n :why="gone" @got="got" />
    <template v-else-if="lab">
      <LabCard :n :lab />
      <section v-if="lab.ask?.length" class="mb-4">
        <h2 class="h5">Питання на захист</h2>
        <ol class="mb-0"><li v-for="q in lab.ask" :key="q">{{ q }}</li></ol>
      </section>
      <LabHandIn :key="lab.vid" :n :lab @got="got" />
      <LabSeen v-if="lab.file?.id || lab.line" :n :lab />
      <LabDefence :n :lab @got="got" />
      <p v-if="lab.points !== null && lab.points !== undefined" class="alert alert-success">
        Оцінка: <b>{{ lab.points }}</b><template v-if="lab.note"> — {{ lab.note }}</template></p>
      <p v-if="live" class="small text-secondary">Ноутбук на звʼязку: {{ live.ok }} із {{ lab.total }} ✅<template v-if="live.at">,
        востаннє {{ fmtWhen(live.at) }}</template></p>
    </template>
  </div>
</template>
