<script setup>
import Icon from '@core/components/Icon.vue'
import { jump } from '../jump.js'

// «чого бракує» — a few gentle lines; a click shows the place: the page scrolls there and it flashes
defineProps({ items: Array })
</script>

<template>
  <ul v-if="items.length" class="hints list-unstyled small mb-0 vstack gap-1">
    <li v-for="h in items" :key="h.text" role="button" class="d-flex gap-1 align-items-baseline" title="показати, де це" @click="jump(h.to)">
      <span>💡</span><span class="text">{{ h.text }}</span><span class="go text-nowrap">показати <Icon name="right" /></span>
    </li>
  </ul>
</template>

<style scoped>
.text { color: var(--bs-secondary-color); }
.go { margin-left: .25rem; font-size: .75rem; color: var(--bs-secondary-color); opacity: 0; }
.hints li:hover .text { color: var(--bs-body-color); }
.hints li:hover .go { opacity: 1; }
</style>
