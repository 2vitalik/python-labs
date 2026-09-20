<script setup>
import { nextTick, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { flash, guideClick } from '../anchors.js'
import { getGuidePage } from '../api.js'
import Crumbs from '../components/Crumbs.vue'
import GuideText from '../components/GuideText.vue'
import { ALL } from '../guide.js'

// the whole guide on one page — Ctrl+F and printing; ids get the section prefix (#score-79)
const route = useRoute()
const router = useRouter()
const items = ref([])

Promise.all(ALL.map((s) => getGuidePage(s.slug))).then(async (list) => {
  items.value = list.map((p, i) => ({ ...ALL[i], ...p, text: `${p.brief}\n\n${p.body}` }))
  await nextTick()
  if (route.hash) flash(route.hash.slice(1))
})
watch(() => route.hash, (h) => h && flash(h.slice(1)))
</script>

<template>
  <div>
    <Crumbs :items="['Методичка']" />
    <h1 class="h2">Методичка</h1>
    <p class="text-secondary">Усі розділи на одній сторінці — для пошуку (Ctrl+F) і друку.</p>
    <!-- contents: anchors down this page; ↗ opens the section as its own page (both go through guideClick) -->
    <nav v-if="items.length" class="border rounded px-3 py-2 mb-4" @click="guideClick($event, router)">
      <div v-for="s in items" :key="s.slug" class="py-1" :class="{ 'ps-4': s.n }">
        <a :href="'#' + s.slug" class="text-decoration-none">{{ s.title }}</a>
        <a :href="s.path" class="text-secondary text-decoration-none ms-1" title="Відкрити окремою сторінкою">↗</a>
      </div>
    </nav>
    <section v-for="s in items" :id="s.slug" :key="s.slug" class="mt-5">
      <h2 class="border-bottom pb-2"><RouterLink :to="s.path" class="text-decoration-none text-reset">{{ s.title }}</RouterLink></h2>
      <GuideText :text="s.text" :prefix="s.slug" />
    </section>
  </div>
</template>
