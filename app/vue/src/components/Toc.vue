<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

import { guideClick } from '../anchors.js'

// contents fixed beside the page column: [{id, text, depth}] links, {label} rows split groups (guide text · catalog zones)
const props = defineProps({ items: { type: Array, default: () => [] } })
const router = useRouter()
const links = computed(() => props.items.filter((h) => !h.label).length)
</script>

<template>
  <nav v-if="links > 1" class="toc" @click="guideClick($event, router)">
    <div class="text-uppercase fw-semibold mb-1">Зміст</div>
    <template v-for="(h, i) in items" :key="i">
      <div v-if="h.label" class="text-uppercase fw-semibold mt-2 mb-1">{{ h.label }}</div>
      <a v-else :href="'#' + h.id" class="d-block text-decoration-none text-secondary" :class="{ 'ps-3': h.depth === 3 }">{{ h.text }}</a>
    </template>
  </nav>
</template>

<style scoped>
/* shown only when the side margin fits it (page 52rem + 2 × (11rem + gap)) */
.toc { display: none; position: fixed; top: 50%; transform: translateY(-50%); left: calc(50% + var(--page-max) / 2 + 1rem);
       width: 11rem; max-height: 80vh; overflow-y: auto; padding-left: .75rem; border-left: 2px solid var(--bs-border-color);
       font-size: .8rem; line-height: 1.3; }
.toc a { padding: .15rem 0; }
.toc a:hover { color: var(--bs-body-color) !important; }
@media (min-width: 76rem) { .toc { display: block; } }
</style>
