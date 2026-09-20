<script setup>
import { nextTick, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

import { flash } from '../anchors.js'
import { getGuidePage } from '../api.js'
import GuideText from '../components/GuideText.vue'
import { ALL } from '../guide.js'

// the whole guide on one page — Ctrl+F and printing; ids get the section prefix (#score-79)
const route = useRoute()
const items = ref([])

Promise.all(ALL.map((s) => getGuidePage(s.slug))).then(async (list) => {
  items.value = list.map((p, i) => ({ ...p, path: ALL[i].path, text: `${p.brief}\n\n${p.body}` }))
  await nextTick()
  if (route.hash) flash(route.hash.slice(1))
})
watch(() => route.hash, (h) => h && flash(h.slice(1)))
</script>

<template>
  <div class="col-lg-9 mx-auto">
    <h1 class="h2">Методичка</h1>
    <p class="text-secondary">
      Усі розділи на одній сторінці — для пошуку (Ctrl+F) і друку. Окремо:
      <template v-for="(s, i) in items" :key="s.slug">
        <RouterLink :to="s.path">{{ s.title }}</RouterLink><span v-if="i < items.length - 1"> · </span>
      </template>
    </p>
    <section v-for="s in items" :id="s.slug" :key="s.slug" class="mt-5">
      <h2 class="border-bottom pb-2"><RouterLink :to="s.path" class="text-decoration-none text-reset">{{ s.title }}</RouterLink></h2>
      <GuideText :text="s.text" :prefix="s.slug" />
    </section>
  </div>
</template>
