<script setup>
import { computed, ref, watch } from 'vue'
import { onBeforeRouteLeave, onBeforeRouteUpdate, useRoute } from 'vue-router'

import Crumbs from '@core/components/Crumbs.vue'
import { useTitle } from '@core/title.js'

import { getLabReview } from '../api.js'
import LabBar from '../components/LabBar.vue'
import LabWide from '../components/LabWide.vue'
import ReviewHead from '../components/ReviewHead.vue'
import ReviewLeft from '../components/ReviewLeft.vue'
import ReviewPanel from '../components/ReviewPanel.vue'
import { nbMode } from '../labNb.js'
import { useShown } from '../labReview.js'

// the teacher's desk for one work (T354 §6): the notebook on the left; the hint, the key, the levels and the marks in
// a panel on the right that stays in sight; stacked on a narrow screen, the panel first
const route = useRoute()
const n = computed(() => Number(route.params.n))
const vid = computed(() => route.params.vid)
const doc = ref(null)
const error = ref('')
const panel = ref()
const { shown, nb, loading, error: nbError, compare, other, open } = useShown(() => doc.value?.files)
useTitle(() => (doc.value ? `${doc.value.who?.name || doc.value.vid} · перевірка` : 'Перевірка'))

// FACTS of the version shown say which tasks are done; the lab's shape — which there are
const tasks = computed(() => {
  const facts = nb.value?.facts?.tasks || doc.value?.facts?.tasks || []
  const all = doc.value?.shape?.tasks?.length ? doc.value.shape.tasks : facts
  return all.map((t) => ({ ...t, done: facts.find((f) => f.key === t.key)?.done ?? null }))
})

async function reload() {
  try {
    doc.value = await getLabReview(n.value, vid.value)
    error.value = ''
  } catch (e) {
    error.value = e.message
  }
}
watch([n, vid], async () => {
  doc.value = null
  open(null)
  await reload()
  open(doc.value?.file?.id || null)
}, { immediate: true })
// a freed card has no file any more: the former holder's notebook leaves the page with it
async function freed() {
  open(null)
  await reload()
}

const leave = () => !panel.value?.dirty() || confirm('Бали не збережено. Піти без збереження?')
onBeforeRouteUpdate(leave)
onBeforeRouteLeave(leave)
</script>

<template>
  <div class="rv">
    <LabBar />
    <Crumbs :items="[['/labs', 'Лаби'], [`/labs/${n}`, `Лаба ${n}`], [`/labs/${n}/results`, 'Результати'], doc?.vid || vid]"><LabWide /></Crumbs>
    <p v-if="error || nbError" class="text-danger">{{ error || nbError }}</p>
    <template v-if="doc">
      <ReviewHead :n :doc />
      <div class="rv-grid">
        <ReviewLeft v-model:mode="nbMode" class="rv-left" :nb :tasks :other :loading :colab="doc.notebook" />
        <aside class="rv-side">
          <ReviewPanel ref="panel" v-model:compare="compare" :n :doc :shown @show="shown = $event" @saved="reload" @freed="freed" />
        </aside>
      </div>
    </template>
  </div>
</template>

<style scoped>
.rv { container-type: inline-size; }
.rv-grid { display: grid; gap: 1.25rem; }
.rv-left { min-width: 0; }
.rv-side { order: -1; }
@container (min-width: 56rem) {
  .rv-grid { grid-template-columns: minmax(0, 2fr) minmax(19rem, 1fr); align-items: start; }
  .rv-side { order: 0; position: sticky; top: calc(var(--nav-h, 3.5rem) + .75rem); max-height: calc(100vh - var(--nav-h, 3.5rem) - 1.5rem);
             overflow-y: auto; overscroll-behavior: contain; padding-right: .25rem; }
}
</style>
