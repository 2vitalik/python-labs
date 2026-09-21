<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { guideClick } from '../anchors.js'
import { getGuidePage } from '../api.js'
import Crumbs from '../components/Crumbs.vue'
import GuideFoot from '../components/GuideFoot.vue'
import GuideText from '../components/GuideText.vue'
import { ALL, LABS, loadGuide, pages } from '../guide.js'
import { tocOf } from '../md.js'

const route = useRoute()
const router = useRouter()
const page = ref(null)  // null = loading, false = 404
const slug = computed(() => route.meta.slug || `lab${route.params.n}`)
const text = computed(() => (page.value ? `${page.value.brief}\n\n${page.value.body}` : ''))
const toc = computed(() => tocOf(text.value))
const lab = computed(() => LABS.find((l) => l.slug === slug.value))
const prev = computed(() => lab.value && LABS[lab.value.n - 2])
const next = computed(() => lab.value && LABS[lab.value.n])
const title = (l) => pages.value[l.slug]?.title || `Лаба ${l.n}`
const crumbs = computed(() => (lab.value ? [['/labs', 'Лаби'], `Лаба ${lab.value.n}`] : [ALL.find((s) => s.slug === slug.value)?.nav]))

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
    <GuideText :text="text" />
    <nav v-if="lab" class="labs-nav mt-4 pt-3 border-top">
      <RouterLink v-if="prev" :to="prev.path">← {{ title(prev) }}</RouterLink><span v-else></span>
      <RouterLink to="/labs" class="text-secondary">Усі лаби</RouterLink>
      <RouterLink v-if="next" :to="next.path">{{ title(next) }} →</RouterLink><span v-else></span>
    </nav>
    <GuideFoot :updated="page.updated" />
    <nav v-if="toc.length > 1" class="toc" @click="guideClick($event, router)">
      <div class="text-uppercase fw-semibold mb-1">Зміст</div>
      <a v-for="h in toc" :key="h.id" :href="'#' + h.id" class="d-block text-decoration-none text-secondary"
         :class="{ 'ps-3': h.depth === 3 }">{{ h.text }}</a>
    </nav>
  </div>
</template>

<style scoped>
/* equal side columns keep «Усі лаби» centred whatever the neighbours' widths (or absence) */
.labs-nav { display: grid; grid-template-columns: 1fr auto 1fr; gap: 1rem; }
.labs-nav > :nth-child(3) { text-align: right; }
/* fixed beside the page column: shown only when the side margin fits it (page 52rem + 2 × (11rem + gap)) */
.toc { display: none; position: fixed; top: 50%; transform: translateY(-50%); left: calc(50% + var(--page-max) / 2 + 1rem);
       width: 11rem; max-height: 80vh; overflow-y: auto; padding-left: .75rem; border-left: 2px solid var(--bs-border-color);
       font-size: .8rem; line-height: 1.3; }
.toc a { padding: .15rem 0; }
.toc a:hover { color: var(--bs-body-color) !important; }
@media (min-width: 76rem) { .toc { display: block; } }
</style>
