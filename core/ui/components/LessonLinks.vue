<script setup>
import { computed } from 'vue'

import { follow, withInfo } from '../lesson.js'

// a lesson's links as buttons (the icon follows the host); a click is counted, and the teacher sees the counts on the button
const props = defineProps({ slug: String, links: Array, clicks: Object })
const shown = computed(() => withInfo(props.links))
const count = (url) => props.clicks?.[url]
</script>

<template>
  <div v-if="shown.length" class="d-flex flex-wrap gap-2">
    <a v-for="l in shown" :key="l.url" :href="l.url" target="_blank" rel="noopener" class="btn btn-outline-secondary btn-sm" @click="follow(slug, l.url)">
      {{ l.icon }} {{ l.label }}
      <span v-if="count(l.url)" class="clicks" :title="`${count(l.url).clicks} кліків · ${count(l.url).people} людей`">{{ count(l.url).people }}</span>
    </a>
  </div>
</template>

<style scoped>
.clicks { margin-left: .3rem; padding: 0 .35rem; border-radius: 1rem; background: var(--bs-tertiary-bg); color: var(--bs-secondary-color); font-size: .75em; }
</style>
