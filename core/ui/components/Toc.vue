<script setup>
import { computed, onBeforeUnmount, watchEffect } from 'vue'

import { toTop } from '../anchors.js'
import { tocItems } from '../toc.js'
import TocList from './TocList.vue'

// contents fixed beside the page column: [{id, text, depth}] links, {label} rows split groups (guide text · catalog zones).
// Where the side margin does not fit it (a narrow window, a phone) the same items open from the «☰» of PageJump
const props = defineProps({ items: { type: Array, default: () => [] } })
const links = computed(() => props.items.filter((h) => !h.label).length)
watchEffect(() => (tocItems.value = links.value > 1 ? props.items : []))
onBeforeUnmount(() => (tocItems.value = []))
</script>

<template>
  <nav v-if="links > 1" class="toc">
    <a href="#" class="top d-block text-uppercase fw-semibold mb-1 text-decoration-none text-reset" title="Наверх"
       @click.stop.prevent="toTop">Зміст <span class="text-secondary">↑</span></a>
    <TocList :items />
  </nav>
</template>

<style scoped>
/* shown only when the side margin fits it (page 52rem + 2 × (11rem + gap)) */
.toc { display: none; position: fixed; top: 50%; transform: translateY(-50%); left: calc(50% + var(--page-max) / 2 + 1rem);
       width: 11rem; max-height: 80vh; overflow-y: auto; padding-left: .75rem; border-left: 2px solid var(--bs-border-color);
       font-size: .8rem; line-height: 1.3; }
@media (min-width: 76rem) { .toc { display: block; } }
</style>
