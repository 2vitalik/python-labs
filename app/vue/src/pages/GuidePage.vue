<script setup>
import { computed, nextTick, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { flash, guideClick } from '../anchors.js'
import { getGuidePage } from '../api.js'
import GuideText from '../components/GuideText.vue'
import { LABS, loadGuide, pages } from '../guide.js'
import { tocOf } from '../md.js'

const route = useRoute()
const router = useRouter()
const page = ref(null)  // null = loading, false = 404
const slug = computed(() => route.meta.slug || `lab${route.params.n}`)
const text = computed(() => (page.value ? `${page.value.brief}\n\n${page.value.body}` : ''))
const toc = computed(() => tocOf(page.value?.body))
const lab = computed(() => LABS.find((l) => l.slug === slug.value))
const prev = computed(() => lab.value && LABS[lab.value.n - 2])
const next = computed(() => lab.value && LABS[lab.value.n])
const title = (l) => pages.value[l.slug]?.title || `Лаба ${l.n}`
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
  <div v-if="page === false" class="text-center text-secondary mt-5">Такої сторінки нема.</div>
  <div v-else-if="page" class="row">
    <div :class="toc.length > 1 ? 'col-lg-9' : 'col-lg-9 mx-auto'">
      <h1 class="h2 mb-3">{{ page.title }}</h1>
      <GuideText :text="text" />
      <nav v-if="lab" class="d-flex justify-content-between gap-3 mt-4 pt-3 border-top">
        <RouterLink v-if="prev" :to="prev.path">← {{ title(prev) }}</RouterLink><span v-else></span>
        <RouterLink to="/labs" class="text-secondary">Усі лаби</RouterLink>
        <RouterLink v-if="next" :to="next.path" class="text-end">{{ title(next) }} →</RouterLink><span v-else></span>
      </nav>
      <p class="text-secondary small mt-4 mb-0">Оновлено {{ updated }}</p>
    </div>
    <aside v-if="toc.length > 1" class="col-lg-3 d-none d-lg-block toc">
      <nav class="sticky-top pt-1" style="top: 1rem" @click="guideClick($event, router)">
        <div class="small text-uppercase text-secondary mb-1">На цій сторінці</div>
        <a v-for="h in toc" :key="h.id" :href="'#' + h.id" class="d-block small text-decoration-none py-1"
           :class="{ 'ps-3': h.depth === 3 }">{{ h.text }}</a>
      </nav>
    </aside>
  </div>
</template>
