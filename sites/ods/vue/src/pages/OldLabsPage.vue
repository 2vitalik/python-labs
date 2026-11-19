<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

import { getGuidePage } from '@core/api.js'
import Crumbs from '@core/components/Crumbs.vue'
import GuideBody from '@core/components/GuideBody.vue'
import Icon from '@core/components/Icon.vue'
import Lightbox from '@core/components/Lightbox.vue'
import Toc from '@core/components/Toc.vue'
import { textOf } from '@core/drafts.js'
import { loadGuide, pages } from '@core/guide.js'
import { tocOf } from '@core/md.js'
import { problem } from '@core/problem.js'
import { useTitle } from '@core/title.js'

import { vRich } from '../rich.js'

// /labs/old — the labs as they were before (old-lab1…5), the teacher's only: the API hides them from students too (GUIDE_STAFF);
// /labs/old/N — one of them as text
const route = useRoute()
const n = computed(() => Number(route.params.n) || 0)
const ready = ref(false)
const old = computed(() => [1, 2, 3, 4, 5].filter((k) => pages.value[`old-lab${k}`]))
const i = computed(() => old.value.indexOf(n.value))
const back = computed(() => old.value[i.value - 1])
const ahead = computed(() => (i.value < 0 ? undefined : old.value[i.value + 1]))
const title = (k) => pages.value[`old-lab${k}`].title.replace(/^(Лабораторна|Завдання)\s+\d+\.\s*/, '')
const page = ref(null)
const plain = (text) => text.replace(/\$([^$]+)\$/g, (_, tex) => tex.replace(/[{}\\]/g, ''))  // the contents are text: $R^{2}$ → R^2
const toc = computed(() => tocOf(textOf(page.value)).map((h) => ({ ...h, text: plain(h.text) })))
const fmt = (d) => new Date(d).toLocaleDateString('uk-UA')
useTitle(() => page.value?.title || 'Архів')

async function load() {
  const slug = `old-lab${n.value}`
  await loadGuide()
  ready.value = true
  if (!n.value) return (page.value = null)  // the lab before stays only while the next one loads
  try {
    const p = await getGuidePage(slug)
    if (slug === `old-lab${n.value}`) page.value = p
  } catch (e) {
    if (e.status !== 404) throw e
    problem.value = 'lost'
  }
}
watch(n, load, { immediate: true })
</script>

<template>
  <template v-if="!n">
    <Crumbs :items="[['/labs', 'Лаби'], 'Архів']" />
    <h1 class="h2 mb-1">Архів: старі лаби</h1>
    <div class="small text-secondary mb-3">Студенти цих сторінок не бачать</div>
    <ol v-if="old.length" class="docs list-unstyled">
      <li v-for="k in old" :key="k">
        <span class="n text-secondary">{{ k }}</span>
        <RouterLink :to="`/labs/old/${k}`">{{ title(k) }}</RouterLink>
      </li>
    </ol>
    <p v-else-if="ready" class="text-secondary">Архів порожній: імпорт старих лаб ще не запускали</p>
  </template>
  <template v-else>
    <Crumbs :items="[['/labs', 'Лаби'], ['/labs/old', 'Архів'], `Лаба ${n}`]" />
    <div v-if="page">
      <div class="archive small text-secondary mb-3">
        <Icon name="archive" /> Архів: стара версія лаби. Студенти цієї сторінки не бачать
      </div>
      <h1 class="h2 mb-3">{{ page.title }}</h1>
      <div :key="page.slug" v-rich="page.slug"><GuideBody v-model:page="page" /></div>
      <Toc :items="toc" />
      <nav class="docs-nav mt-4 pt-3 border-top">
        <RouterLink v-if="back" :to="`/labs/old/${back}`">← Лаба {{ back }}</RouterLink><span v-else></span>
        <RouterLink to="/labs/old" class="text-secondary">Архів</RouterLink>
        <RouterLink v-if="ahead" :to="`/labs/old/${ahead}`">Лаба {{ ahead }} →</RouterLink><span v-else></span>
      </nav>
      <div class="small text-body-tertiary text-end mt-3">Оновлено {{ fmt(page.updated) }}</div>
    </div>
    <Lightbox />
  </template>
</template>

<style scoped>
.docs li { display: flex; gap: .75rem; padding: .35rem 0; border-bottom: 1px solid var(--bs-border-color-translucent); }
.docs .n { min-width: 1.5rem; text-align: right; font-variant-numeric: tabular-nums; }
.docs a { text-decoration: none; }
.docs a:hover { text-decoration: underline; }
.archive { padding: .35rem .75rem; border-radius: .375rem; background: var(--bs-tertiary-bg); }
/* equal side columns keep the middle link centred whatever the neighbours' widths (or absence) */
.docs-nav { display: grid; grid-template-columns: 1fr auto 1fr; gap: 1rem; }
.docs-nav > :nth-child(3) { text-align: right; }
</style>
