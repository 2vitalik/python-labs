<script setup>
import { nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

import { toTop } from '../anchors.js'
import { spy, tocItems, tocListed } from '../toc.js'
import Icon from './Icon.vue'
import TocList from './TocList.vue'

// the way around a long page (T284 §3): «↑» to the top once the page is scrolled, and «☰» — the page's contents in a
// panel — where the side column of Toc.vue is not shown (a narrow window, a page on the whole window: `wide`). Beside the
// page column while there is room for it, in the corner under the thumb otherwise. «☰» opens under a mouse that rests on
// it a moment and closes once the mouse has left the panel a while (T294 §11); a finger taps. It also runs the contents' spy (toc.js)
const props = defineProps({ wide: Boolean })
const far = ref(false)
const narrow = ref(false)
const open = ref(false)
const root = ref()
const roomy = matchMedia('(min-width: 76rem)')  // as Toc.vue's own breakpoint
let frame = 0
const look = () => { frame ||= requestAnimationFrame(() => { frame = 0; spy() }) }
const scrolled = () => { far.value = scrollY > 500; look() }
const sized = () => (narrow.value = !roomy.matches)
const outside = (e) => !root.value?.contains(e.target) && (open.value = false)
const hovers = matchMedia('(hover: hover)').matches
let timer
const hover = (on) => {
  if (!hovers) return
  clearTimeout(timer)
  timer = setTimeout(() => (open.value = on), on ? 200 : 400)
}
const tap = () => { clearTimeout(timer); open.value = hovers || !open.value }
const route = useRoute()
watch(() => route.path, () => (open.value = false))
watch(tocItems, () => nextTick(look))
const grown = new ResizeObserver(look)  // a section folded, a list loaded: the places moved without a scroll
onMounted(() => {
  addEventListener('scroll', scrolled, { passive: true })
  roomy.addEventListener('change', sized)
  document.addEventListener('mousedown', outside)
  grown.observe(document.body)
  scrolled()
  sized()
})
onBeforeUnmount(() => {
  removeEventListener('scroll', scrolled)
  roomy.removeEventListener('change', sized)
  document.removeEventListener('mousedown', outside)
  grown.disconnect()
  clearTimeout(timer)
})
</script>

<template>
  <div ref="root" class="jump" :class="{ beside: !narrow && !wide }" @mouseleave="hover(false)">
    <div v-if="open" class="panel shadow border rounded bg-body" @mouseenter="hover(true)">
      <div class="text-uppercase fw-semibold mb-1">Зміст</div>
      <TocList :items="tocListed" @went="open = false" />
    </div>
    <button v-if="(narrow || wide) && tocListed.length" type="button" class="round" :class="{ on: open }" title="Зміст сторінки" @click="tap" @mouseenter="hover(true)"><Icon name="list" /></button>
    <button v-if="far" type="button" class="round" title="Нагору" @click="toTop(); open = false"><Icon name="top" /></button>
  </div>
</template>

<style scoped>
.jump { position: fixed; z-index: 1030; right: .75rem; bottom: .75rem; display: flex; flex-direction: column; align-items: flex-end; gap: .4rem; }
/* where the side contents hang: the same distance from the page column, at the bottom */
.jump.beside { right: auto; left: calc(50% + var(--page-max) / 2 + 1rem); align-items: flex-start; }
.round { display: inline-flex; align-items: center; justify-content: center; width: 2.25rem; height: 2.25rem; padding: 0; border: 1px solid var(--bs-border-color);
         border-radius: 50%; background: color-mix(in srgb, var(--bs-body-bg) 88%, transparent); color: var(--bs-secondary-color);
         box-shadow: 0 1px 4px rgb(0 0 0 / .12); backdrop-filter: blur(4px); }
.round:hover, .round.on { border-color: var(--bs-secondary-color); color: var(--bs-body-color); }
.panel { width: 15rem; max-width: calc(100vw - 1.5rem); max-height: 70vh; overflow-y: auto; padding: .6rem .75rem; font-size: .85rem; line-height: 1.3; }
@media print { .jump { display: none; } }
</style>
