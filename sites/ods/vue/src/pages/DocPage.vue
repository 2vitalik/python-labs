<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { getGuidePage } from '@core/api.js'
import Crumbs from '@core/components/Crumbs.vue'
import GuideBody from '@core/components/GuideBody.vue'
import Toc from '@core/components/Toc.vue'
import { textOf } from '@core/drafts.js'
import { tocOf } from '@core/md.js'
import { problem } from '@core/problem.js'
import { site } from '@core/site.js'
import { useTitle } from '@core/title.js'

import Slides from '../components/Slides.vue'
import { KINDS } from '../site.js'
import { slidesOf } from '../slides.js'

// a lecture or a lab: the text with its contents, or its slides one at a time (?slide=N, the number from the md)
const route = useRoute()
const router = useRouter()
const kind = computed(() => route.meta.kind)
const list = computed(() => site.guide.filter((s) => s.kind === kind.value))
const doc = computed(() => list.value.find((s) => String(s.n) === route.params.n))
const prev = computed(() => list.value[list.value.indexOf(doc.value) - 1])
const next = computed(() => list.value[list.value.indexOf(doc.value) + 1])
const page = ref(null)
const slides = computed(() => slidesOf(textOf(page.value)))
const plain = (text) => text.replace(/\$([^$]+)\$/g, (_, tex) => tex.replace(/[{}\\]/g, ''))  // the contents are text: $R^{2}$ → R^2
const toc = computed(() => tocOf(textOf(page.value)).map((h) => ({ ...h, text: plain(h.text) })))
const slide = computed({
  get: () => (route.query.slide === undefined ? null : Number(route.query.slide)),
  set: (n) => router.replace({ query: n === null ? {} : { slide: n } }),
})
const fmt = (d) => new Date(d).toLocaleDateString('uk-UA')
useTitle(() => page.value?.title)

async function load() {
  page.value = null
  if (!doc.value) return (problem.value = 'lost')
  page.value = await getGuidePage(doc.value.slug)
}
watch(doc, load, { immediate: true })
</script>

<template>
  <Crumbs :items="[[`/${kind}`, KINDS[kind]], doc?.nav]">
    <div v-if="slides.length > 1" class="btn-group btn-group-sm">
      <button class="btn btn-outline-secondary" :class="{ active: slide === null }" @click="slide = null">Текст</button>
      <button class="btn btn-outline-secondary" :class="{ active: slide !== null }" @click="slide = slide ?? slides[0].n">Слайди</button>
    </div>
  </Crumbs>
  <div v-if="page">
    <h1 class="h2 mb-3">{{ page.title }}</h1>
    <Slides v-if="slide !== null && slides.length" v-model="slide" :slides />
    <template v-else>
      <GuideBody v-model:page="page" />
      <Toc :items="toc" />
    </template>
    <nav class="docs-nav mt-4 pt-3 border-top">
      <RouterLink v-if="prev" :to="prev.path">← {{ prev.nav }}</RouterLink><span v-else></span>
      <RouterLink :to="`/${kind}`" class="text-secondary">{{ KINDS[kind] }}</RouterLink>
      <RouterLink v-if="next" :to="next.path">{{ next.nav }} →</RouterLink><span v-else></span>
    </nav>
    <div class="small text-body-tertiary text-end mt-3">Оновлено {{ fmt(page.updated) }}</div>
  </div>
</template>

<style scoped>
/* equal side columns keep the middle link centred whatever the neighbours' widths (or absence) */
.docs-nav { display: grid; grid-template-columns: 1fr auto 1fr; gap: 1rem; }
.docs-nav > :nth-child(3) { text-align: right; }
</style>
