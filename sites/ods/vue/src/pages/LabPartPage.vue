<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

import { getGuidePage } from '@core/api.js'
import Crumbs from '@core/components/Crumbs.vue'
import GuideBody from '@core/components/GuideBody.vue'
import Toc from '@core/components/Toc.vue'
import { textOf } from '@core/drafts.js'
import { tocOf } from '@core/md.js'
import { problem } from '@core/problem.js'
import { useTitle } from '@core/title.js'

import LabFiles from '../components/LabFiles.vue'
import LabParts from '../components/LabParts.vue'
import { labPages, loadLabPages } from '../labPages.js'

// a part of a lab (/labs/3/guide → the guide page lab3-guide) or a page common to all labs (/labs/about/grading → labs-grading)
const route = useRoute()
const about = computed(() => !!route.meta.about)
const n = computed(() => Number(route.params.n))
const slug = computed(() => (about.value ? `labs-${route.params.part}` : `lab${n.value}-${route.params.part}`))
const here = computed(() => labPages.value.find((p) => p.slug === slug.value))
const page = ref(null)
const toc = computed(() => tocOf(textOf(page.value)))
const crumbs = computed(() => [['/labs', 'Лаби'], ...(about.value ? [] : [[`/labs/${n.value}`, `Лаба ${n.value}`]]), here.value?.nav || page.value?.title || ''])
useTitle(() => page.value?.title)

async function load() {
  page.value = null
  loadLabPages()
  try {
    page.value = await getGuidePage(slug.value)
  } catch (e) {
    if (e.status !== 404) throw e
    problem.value = 'lost'
  }
}
watch(slug, load, { immediate: true })
</script>

<template>
  <Crumbs :items="crumbs">
    <RouterLink v-if="!about" :to="`/labs/${n}/my`" class="btn btn-sm btn-outline-primary">Моя лаба</RouterLink>
  </Crumbs>
  <div v-if="page">
    <h1 class="h2 mb-3">{{ page.title }}</h1>
    <LabParts :n="about ? undefined : n" />
    <GuideBody v-model:page="page" />
    <Toc :items="toc" />
    <LabFiles :slug />
  </div>
</template>
