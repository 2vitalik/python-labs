<script setup>
import { computed, onBeforeUnmount, watchEffect } from 'vue'

import { toTop } from '../anchors.js'
import { tocBar, tocItems, tocListed } from '../toc.js'
import TocList from './TocList.vue'

// contents fixed beside the page column: [{id, text, depth}] links, {label} rows split groups (guide text · catalog zones).
// Where the side margin does not fit it (a narrow window, a phone, `side` off — the page takes the whole window) the same
// items open from the «☰» of PageJump. `bar` off — the page sticks its own headings, TocBar stays away
const props = defineProps({ items: { type: Array, default: () => [] }, side: { type: Boolean, default: true }, bar: { type: Boolean, default: true } })
const links = computed(() => props.items.filter((h) => !h.label && !h.quiet).length)
watchEffect(() => {
  tocItems.value = links.value > 1 ? props.items : []
  tocBar.value = props.bar
})
onBeforeUnmount(() => {
  tocItems.value = []
  tocBar.value = true
})
</script>

<template>
  <nav v-if="side && links > 1" class="toc">
    <a href="#" class="top d-block text-uppercase fw-semibold mb-1 text-decoration-none text-reset" title="Наверх"
       @click.stop.prevent="toTop">Зміст <span class="text-secondary">↑</span></a>
    <TocList :items="tocListed" />
  </nav>
</template>

<style scoped>
/* shown only when the side margin fits it (page 52rem + 2 × (11rem + gap)) */
.toc { display: none; position: fixed; top: 50%; transform: translateY(-50%); left: calc(50% + var(--page-max) / 2 + 1rem);
       width: 11rem; max-height: 80vh; overflow-y: auto; font-size: .8rem; line-height: 1.3; }
@media (min-width: 76rem) { .toc { display: block; } }
</style>
