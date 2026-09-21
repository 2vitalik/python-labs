<script setup>
import { computed, nextTick, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { flash, guideClick, toTop } from '../anchors.js'
import { getGuidePage } from '../api.js'
import Crumbs from '../components/Crumbs.vue'
import GuideText from '../components/GuideText.vue'
import Toc from '../components/Toc.vue'
import { ALL } from '../guide.js'

// the whole guide on one page — Ctrl+F and printing; ids get the section prefix (#score-79)
const route = useRoute()
const router = useRouter()
const items = ref([])
const toc = computed(() => items.value.map((s) => ({ id: s.slug, text: s.title, depth: s.n ? 3 : 2 })))

Promise.all(ALL.map((s) => getGuidePage(s.slug))).then(async (list) => {
  items.value = list.map((p, i) => ({ ...ALL[i], ...p, text: `${p.brief}\n\n${p.body}` }))
  await nextTick()
  if (route.hash) flash(route.hash.slice(1))  // section-level targets (#labs) sit outside GuideText
})
</script>

<template>
  <div>
    <Crumbs :items="['Методичка']" />
    <h1 class="h2">Методичка</h1>
    <p class="text-secondary">Усі розділи на одній сторінці — для пошуку (Ctrl+F) і друку.</p>
    <!-- contents: ↗ opens the section as its own page, the title is an anchor down this page (both go through guideClick) -->
    <nav v-if="items.length" class="toc border rounded px-3 py-2 mb-4" @click="guideClick($event, router)">
      <div v-for="s in items" :key="s.slug" class="d-flex align-items-center gap-2" :class="{ 'ps-4': s.n }">
        <a :href="s.path" class="ibtn" title="Відкрити розділ окремою сторінкою">↗</a>
        <a :href="'#' + s.slug" class="text-decoration-none">{{ s.title }}</a>
      </div>
    </nav>
    <section v-for="s in items" :id="s.slug" :key="s.slug" class="mt-5">
      <h2 class="d-flex align-items-center gap-2 border-bottom pb-2" @click="guideClick($event, router)">
        <a :href="s.path" class="ibtn" title="Відкрити розділ окремою сторінкою">↗</a>
        <span>{{ s.title }}</span>
        <a :href="'#' + s.slug" class="ibtn link ms-auto" title="Скопіювати посилання">🔗</a>
        <a href="#" class="ibtn" title="Наверх" @click.stop.prevent="toTop">↑</a>
      </h2>
      <GuideText :text="s.text" :prefix="s.slug" />
    </section>
    <Toc :items="toc" />
  </div>
</template>

<style scoped>
.toc { width: fit-content; min-width: 20rem; font-size: .875rem; line-height: 1.35; }
.toc > div { padding: .1rem 0; }
.toc .ibtn { width: 1.3rem; height: 1.3rem; }
</style>
