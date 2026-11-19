<script setup>
import { computed } from 'vue'

import { labPages } from '../labPages.js'

// what a page hands out — notebooks and the like, kept next to its text in the base (content_io.py)
const props = defineProps({ slug: String })
const files = computed(() => labPages.value.find((p) => p.slug === props.slug)?.files || [])
</script>

<template>
  <div v-if="files.length" class="lab-files mt-4">
    <div class="small text-secondary mb-1">Файли</div>
    <ul class="list-unstyled mb-0">
      <li v-for="f in files" :key="f.name"><a :href="f.url" :download="f.name">{{ f.title || f.name }}</a> <span class="small text-body-tertiary">{{ f.name }}</span></li>
    </ul>
  </div>
</template>
