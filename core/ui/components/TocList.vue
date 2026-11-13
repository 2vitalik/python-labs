<script setup>
import { useRouter } from 'vue-router'

import { guideClick } from '../anchors.js'

// the links of a page's contents: [{id, text, depth}], {label} rows split groups; a click scrolls there and lights the place
defineProps({ items: Array })
defineEmits(['went'])
const router = useRouter()
</script>

<template>
  <div @click="guideClick($event, router); $event.target.closest('a') && $emit('went')">
    <template v-for="(h, i) in items" :key="i">
      <div v-if="h.label" class="text-uppercase fw-semibold mt-2 mb-1">{{ h.label }}</div>
      <a v-else :href="'#' + h.id" class="row-link d-block text-decoration-none text-secondary" :class="{ 'ps-3': h.depth === 3 }">{{ h.text }}</a>
    </template>
  </div>
</template>

<style scoped>
.row-link { padding: .15rem 0; }
.row-link:hover { color: var(--bs-body-color) !important; }
</style>
