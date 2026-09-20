<script setup>
import { computed, nextTick, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { flash, guideClick } from '../anchors.js'
import { getGuidePage } from '../api.js'
import Crumbs from '../components/Crumbs.vue'
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
const updated = computed(() => page.value && new Date(page.value.updated).toLocaleDateString('uk-UA'))

async function load() {
  page.value = null
  try { page.value = await getGuidePage(slug.value) } catch { page.value = false }
  await nextTick()
  if (route.hash) flash(route.hash.slice(1))
}
watch(slug, load, { immediate: true })
watch(() => route.hash, (h) => h && flash(h.slice(1)))
loadGuide()
</script>

<template>
  <Crumbs :items="crumbs" />
  <div v-if="page === false" class="text-center text-secondary mt-5">Такої сторінки нема.</div>
  <div v-else-if="page">
    <h1 class="h2 mb-3">{{ page.title }}</h1>
    <GuideText :text="text" />
    <nav v-if="lab" class="d-flex justify-content-between gap-3 mt-4 pt-3 border-top">
      <RouterLink v-if="prev" :to="prev.path">← {{ title(prev) }}</RouterLink><span v-else></span>
      <RouterLink to="/labs" class="text-secondary">Усі лаби</RouterLink>
      <RouterLink v-if="next" :to="next.path" class="text-end">{{ title(next) }} →</RouterLink><span v-else></span>
    </nav>
    <p class="text-body-tertiary small text-end mt-4 mb-0">Оновлено {{ updated }}</p>
    <nav v-if="toc.length > 1" class="toc" @click="guideClick($event, router)">
      <div class="text-uppercase fw-semibold mb-1">Зміст</div>
      <a v-for="h in toc" :key="h.id" :href="'#' + h.id" class="d-block text-decoration-none text-secondary"
         :class="{ 'ps-3': h.depth === 3 }">{{ h.text }}</a>
    </nav>
  </div>
</template>

<style scoped>
/* fixed beside the page column: shown only when the side margin fits it (page 52rem + 2 × (11rem + gap)) */
.toc { display: none; position: fixed; top: 50%; transform: translateY(-50%); left: calc(50% + var(--page-max) / 2 + 1rem);
       width: 11rem; max-height: 80vh; overflow-y: auto; padding-left: .75rem; border-left: 2px solid var(--bs-border-color);
       font-size: .8rem; line-height: 1.3; }
.toc a { padding: .15rem 0; }
.toc a:hover { color: var(--bs-body-color) !important; }
@media (min-width: 76rem) { .toc { display: block; } }
</style>
