<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

import { getGuidePage } from '@core/api.js'
import Crumbs from '@core/components/Crumbs.vue'
import GuideBody from '@core/components/GuideBody.vue'
import Lightbox from '@core/components/Lightbox.vue'
import Toc from '@core/components/Toc.vue'
import { textOf } from '@core/drafts.js'
import { tocOf } from '@core/md.js'
import { problem } from '@core/problem.js'
import { useTitle } from '@core/title.js'

import LabBar from '../components/LabBar.vue'
import LabFiles from '../components/LabFiles.vue'
import { gates, loadGates } from '../labGates.js'
import { labsWithCards, lineOf, loadLabPages, pageWord, pathOf } from '../labPages.js'
import { vRich } from '../rich.js'

// a lab's page or a part of it (/labs/3 → lab3, /labs/3/case1 → lab3-case1), or a page common to all labs
// (/labs/about/grading → labs-grading): the text with its contents and files, «← · →» along the lab's pages; the
// lab's pages, «Моя лаба» and the other labs — in the bar on the shelf (LabBar)
const route = useRoute()
const about = computed(() => !!route.meta.about)
const n = computed(() => (about.value ? 0 : Number(route.params.n)))
const part = computed(() => route.params.part || '')
const slug = computed(() => (about.value ? `labs-${part.value}` : `lab${n.value}${part.value && `-${part.value}`}`))
const line = computed(() => lineOf(n.value))
const i = computed(() => line.value.findIndex((p) => p.slug === slug.value))  // -1: a lab of one page, not in the list
const page = ref(null)
const my = ref(false)
const word = computed(() => (i.value < 0 ? page.value?.title || '' : pageWord(line.value[i.value])))
const crumbs = computed(() => [['/labs', 'Лаби'],
  ...(about.value ? ['Про лаби', word.value] : part.value ? [[`/labs/${n.value}`, `Лаба ${n.value}`], word.value] : [`Лаба ${n.value}`])])
const step = (p) => p && { to: pathOf(p), text: pageWord(p) }
const back = computed(() => step(line.value[i.value - 1]))
const ahead = computed(() => (i.value >= 0 && step(line.value[i.value + 1])) || (my.value ? { to: `/labs/${n.value}/my`, text: 'Моя лаба' } : null))
const middle = computed(() => (part.value && !about.value ? [`/labs/${n.value}`, `Лаба ${n.value}`] : ['/labs', 'Лаби']))
const plain = (text) => text.replace(/\$([^$]+)\$/g, (_, tex) => tex.replace(/[{}\\]/g, ''))  // the contents are text: $R^{2}$ → R^2
const toc = computed(() => tocOf(textOf(page.value)).map((h) => ({ ...h, text: plain(h.text) })))
const fmt = (d) => new Date(d).toLocaleDateString('uk-UA')
// how the lab is open (labGates.js), in words under the title: the teacher sees a hidden lab and should know it is one
const note = computed(() => {
  const gate = !about.value && gates.value?.[n.value]
  if (gate === 'hidden') return 'Студенти цієї лаби не бачать — стан міняється на сторінці «Лаби»'
  return gate === 'telegram' ? 'Файл цієї лаби здаємо викладачеві в Telegram' : ''
})
useTitle(() => page.value?.title)

// all at once: the crumbs and «Моя лаба →» at the end come with the text, nothing moves after it. The page before stays
// until the next one is here — no blank flash between the parts of a lab. A lab this reader has no gate of — hidden
// from students, or none at all — is not asked for
async function load() {
  const s = slug.value
  if (!about.value && !(await loadGates())[n.value]) {
    if (s === slug.value) problem.value = 'lost'
    return
  }
  try {
    const [p, held] = await Promise.all([getGuidePage(s), labsWithCards(), loadLabPages().catch(() => null)])
    if (s !== slug.value) return  // the reader has gone on to another page meanwhile
    my.value = held.some((l) => l.n === n.value)
    page.value = p
  } catch (e) {
    if (e.status !== 404) throw e
    problem.value = 'lost'
  }
}
watch(slug, load, { immediate: true })
</script>

<template>
  <LabBar />
  <div v-if="page">
    <Crumbs :items="crumbs" />
    <h1 class="h2 mb-3">{{ page.title }}</h1>
    <p v-if="note" class="small text-secondary mb-3">{{ note }}</p>
    <!-- keyed by the page shown: an editor left open on the page before must not save into this one -->
    <div :key="page.slug" v-rich="page.slug"><GuideBody v-model:page="page" /></div>
    <Toc :items="toc" />
    <LabFiles :slug />
    <nav class="docs-nav mt-4 pt-3 border-top">
      <RouterLink v-if="back" :to="back.to">← {{ back.text }}</RouterLink><span v-else></span>
      <RouterLink :to="middle[0]" class="text-secondary">{{ middle[1] }}</RouterLink>
      <RouterLink v-if="ahead" :to="ahead.to">{{ ahead.text }} →</RouterLink><span v-else></span>
    </nav>
    <div class="small text-body-tertiary text-end mt-3">Оновлено {{ fmt(page.updated) }}</div>
  </div>
  <Lightbox />
</template>

<style scoped>
/* equal side columns keep the middle link centred whatever the neighbours' widths (or absence) */
.docs-nav { display: grid; grid-template-columns: 1fr auto 1fr; gap: 1rem; }
.docs-nav > :nth-child(3) { text-align: right; }
</style>
