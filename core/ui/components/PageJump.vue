<script setup>
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

import { toTop } from '../anchors.js'
import { tocItems } from '../toc.js'
import Icon from './Icon.vue'
import TocList from './TocList.vue'

// the way around a long page, in the corner under the thumb (T284 §3): «↑» to the top once the page is scrolled, and
// «☰» — the page's contents in a panel — where the side column of Toc.vue does not fit
const far = ref(false)
const narrow = ref(false)
const open = ref(false)
const root = ref()
const wide = matchMedia('(min-width: 76rem)')  // as Toc.vue's own breakpoint
const scrolled = () => (far.value = scrollY > 500)
const sized = () => (narrow.value = !wide.matches)
const outside = (e) => !root.value?.contains(e.target) && (open.value = false)
const route = useRoute()
watch(() => route.path, () => (open.value = false))
onMounted(() => {
  addEventListener('scroll', scrolled, { passive: true })
  wide.addEventListener('change', sized)
  document.addEventListener('mousedown', outside)
  scrolled()
  sized()
})
onBeforeUnmount(() => {
  removeEventListener('scroll', scrolled)
  wide.removeEventListener('change', sized)
  document.removeEventListener('mousedown', outside)
})
</script>

<template>
  <div ref="root" class="jump">
    <div v-if="open" class="panel shadow border rounded bg-body">
      <div class="text-uppercase fw-semibold mb-1">Зміст</div>
      <TocList :items="tocItems" @went="open = false" />
    </div>
    <button v-if="narrow && tocItems.length" type="button" class="round" :class="{ on: open }" title="Зміст сторінки" @click="open = !open"><Icon name="list" /></button>
    <button v-if="far" type="button" class="round" title="Нагору" @click="toTop(); open = false"><Icon name="top" /></button>
  </div>
</template>

<style scoped>
.jump { position: fixed; z-index: 1030; right: .75rem; bottom: .75rem; display: flex; flex-direction: column; align-items: flex-end; gap: .4rem; }
.round { display: inline-flex; align-items: center; justify-content: center; width: 2.25rem; height: 2.25rem; padding: 0; border: 1px solid var(--bs-border-color);
         border-radius: 50%; background: color-mix(in srgb, var(--bs-body-bg) 88%, transparent); color: var(--bs-secondary-color);
         box-shadow: 0 1px 4px rgb(0 0 0 / .12); backdrop-filter: blur(4px); }
.round:hover, .round.on { border-color: var(--bs-secondary-color); color: var(--bs-body-color); }
.panel { width: 15rem; max-width: calc(100vw - 1.5rem); max-height: 70vh; overflow-y: auto; padding: .6rem .75rem; font-size: .85rem; line-height: 1.3; }
@media print { .jump { display: none; } }
</style>
