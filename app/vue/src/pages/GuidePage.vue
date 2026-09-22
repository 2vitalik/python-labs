<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

import { getGuidePage } from '../api.js'
import ChangesDraft from '../components/ChangesDraft.vue'
import Crumbs from '../components/Crumbs.vue'
import GuideBody from '../components/GuideBody.vue'
import GuideFoot from '../components/GuideFoot.vue'
import Toc from '../components/Toc.vue'
import { ALL, LABS, loadGuide, pages } from '../guide.js'
import { tocOf } from '../md.js'
import { user } from '../user.js'

const route = useRoute()
const page = ref(null)  // null = loading, false = 404
const slug = computed(() => route.meta.slug || `lab${route.params.n}`)
const toc = computed(() => tocOf(page.value?.body))
const admin = computed(() => user.value?.status === 'admin')
const lab = computed(() => LABS.find((l) => l.slug === slug.value))
const prev = computed(() => lab.value && LABS[lab.value.n - 2])
const next = computed(() => lab.value && LABS[lab.value.n])
const title = (l) => pages.value[l.slug]?.title || `Лаба ${l.n}`
const crumbs = computed(() => [['/method', 'Методичка'],
  ...(lab.value ? [['/labs', 'Лаби'], `Лаба ${lab.value.n}`] : [ALL.find((s) => s.slug === slug.value)?.nav])])

async function load() {
  page.value = null
  try { page.value = await getGuidePage(slug.value) } catch { page.value = false }
}
watch(slug, load, { immediate: true })
loadGuide()
</script>

<template>
  <Crumbs :items="crumbs" />
  <div v-if="page === false" class="text-center text-secondary mt-5">Такої сторінки нема.</div>
  <div v-else-if="page">
    <h1 class="h2 mb-3">{{ page.title }}</h1>
    <ChangesDraft v-if="slug === 'changes' && admin" @published="load" />
    <GuideBody v-model:page="page" />
    <nav v-if="lab" class="labs-nav mt-4 pt-3 border-top">
      <RouterLink v-if="prev" :to="prev.path">← {{ title(prev) }}</RouterLink><span v-else></span>
      <RouterLink to="/labs" class="text-secondary">Усі лаби</RouterLink>
      <RouterLink v-if="next" :to="next.path">{{ title(next) }} →</RouterLink><span v-else></span>
    </nav>
    <GuideFoot :updated="page.updated" />
    <Toc :items="toc" />
  </div>
</template>

<style scoped>
/* equal side columns keep «Усі лаби» centred whatever the neighbours' widths (or absence) */
.labs-nav { display: grid; grid-template-columns: 1fr auto 1fr; gap: 1rem; }
.labs-nav > :nth-child(3) { text-align: right; }
</style>
