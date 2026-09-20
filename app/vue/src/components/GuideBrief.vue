<script setup>
import { computed } from 'vue'

import { pages } from '../guide.js'
import GuideText from './GuideText.vue'

// one collapsible section on the home page: brief from the API + link to the full page
const props = defineProps({ slug: String, to: String, open: Boolean })
const page = computed(() => pages.value[props.slug])
</script>

<template>
  <details v-if="page" class="brief card mb-2" :open="open">
    <summary class="card-header h5 mb-0 py-2">{{ page.title }}</summary>
    <div class="card-body pt-2">
      <GuideText :text="page.brief" />
      <RouterLink v-if="to" :to="to" class="d-inline-block mt-2 fw-semibold">Уся сторінка →</RouterLink>
    </div>
  </details>
</template>

<style scoped>
summary { cursor: pointer; list-style: none; }
summary::before { content: '▸'; display: inline-block; width: 1.1rem; opacity: .5; transition: transform .15s; }
details[open] summary::before { transform: rotate(90deg); }
summary::-webkit-details-marker { display: none; }
</style>
