<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'

import { rowGone } from '../labRow.js'
import LabNav from './LabNav.vue'

// the lab's pages as a row of pills on the page itself, under its title (T381): it wraps, never scrolls sideways. Once
// it has gone under the shelf, the lab's bar (LabBar) shows the same pills; back in sight — the bar lets them go
defineProps({ n: Number })
const el = ref()
function check() {
  const shelf = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--nav-h')) || 0
  const r = el.value.getBoundingClientRect()
  rowGone.value = r.height > 0 && r.bottom <= shelf  // no pills yet (or none at all): nothing has gone
}
// its size too: the pills may come after the page (LabNav loads them itself), and the row is laid out only once it is in
// the page — a lab's text renders its icons with a render() of its own (iconHtml.js), which runs onMounted before that
const sized = new ResizeObserver(check)
onMounted(() => {
  sized.observe(el.value)
  addEventListener('scroll', check, { passive: true })
  addEventListener('resize', check)
})
onBeforeUnmount(() => {
  sized.disconnect()
  removeEventListener('scroll', check)
  removeEventListener('resize', check)
  rowGone.value = false
})
</script>

<template>
  <div ref="el" class="lab-row"><LabNav :n /></div>
</template>

<style scoped>
.lab-row:empty { display: none; }  /* a lab of one page has no row: no margin either */
</style>
