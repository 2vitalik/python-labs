<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

import Crumbs from '@core/components/Crumbs.vue'
import Toc from '@core/components/Toc.vue'
import LudoHead from '../components/LudoHead.vue'
import Md from '@core/components/Md.vue'
import { getLudoGame, SECTIONS } from '../ludopedia.js'
import { problem } from '@core/problem.js'
import { useTitle } from '@core/title.js'

// one game of the corpus: the head, then the 13 sections of the file as they are (Markdown), contents beside
const route = useRoute()
const game = ref(null)
useTitle(() => game.value?.title)
const filled = computed(() => SECTIONS.filter(([k]) => game.value?.sections[k] && game.value.sections[k] !== '—'))
const toc = computed(() => filled.value.map(([k, text]) => ({ id: `s-${k}`, text, depth: 2 })))

async function load() {
  game.value = null
  try {
    game.value = await getLudoGame(route.params.slug)
  } catch (e) {
    problem.value = e.status === 404 ? 'lost' : e.message
  }
}
onMounted(load)
watch(() => route.params.slug, (s) => s && load())
</script>

<template>
  <div v-if="game">
    <Crumbs :items="[['/ludopedia', 'Ігротека'], game.title]">
      <RouterLink :to="{ path: '/ludopedia', query: { fam: game.family } }" class="btn btn-outline-secondary btn-sm">Сімʼя</RouterLink>
    </Crumbs>
    <LudoHead :game />
    <template v-for="[k, text] in filled" :key="k">
      <h2 :id="`s-${k}`" class="h5 mt-4 mb-2">{{ text }}</h2>
      <Md :text="game.sections[k]" class="sec" />
    </template>
    <p class="small text-secondary mt-4 mb-0">Файл корпусу: <code>data/ludopedia/{{ game.path }}</code></p>
    <Toc :items="toc" />
  </div>
</template>

<style scoped>
h2 { scroll-margin-top: 1rem; }
.sec :deep(table) { width: 100%; font-size: .9rem; }
.sec :deep(th), .sec :deep(td) { padding: .25rem .5rem; border-bottom: 1px solid var(--bs-border-color); vertical-align: top; }
.sec :deep(th) { text-align: left; color: var(--bs-secondary-color); font-weight: 600; }
.sec :deep(code) { font-size: .85em; }
</style>
