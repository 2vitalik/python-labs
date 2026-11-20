<script>
let kept = { n: -1, left: 0 }  // the pills' scroll: a page of another kind (Моя лаба, Результати) mounts a bar of its own
</script>

<script setup>
import { nextTick, onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

import LabNav from './LabNav.vue'

// the lab's pages in its bar (LabBar): one row that scrolls sideways — a finger, a wheel — when it does not fit, a soft fade
// at an edge with more behind it, the open page's pill in sight: at once on a strip just filled, gently after a click, not
// at all when it is in sight already. `away` (LabBar: the page's own row is in sight) — faded out, its room kept
const props = defineProps({ n: Number })
const route = useRoute()
const strip = ref()
const fade = reactive({ l: false, r: false })
const FADE = 24  // px, the fade's width in the style below
function edges() {
  const el = strip.value
  if (!el) return
  fade.l = el.scrollLeft > 1
  fade.r = el.scrollLeft + el.clientWidth < el.scrollWidth - 1
  kept = { n: props.n, left: el.scrollLeft }
}
let filled = -1  // the lab whose pills the strip holds
function place() {
  const el = strip.value
  if (!el) return
  const fresh = filled !== props.n
  if (fresh) el.scrollLeft = kept.n === props.n ? kept.left : 0
  filled = props.n
  const here = el.querySelector('.here')?.getBoundingClientRect(), s = el.getBoundingClientRect()
  if (here && (here.left < s.left + FADE || here.right > s.right - FADE))
    el.scrollBy({ left: here.left + here.width / 2 - s.left - s.width / 2, behavior: fresh ? 'instant' : 'smooth' })
  edges()
}
// once the whole flush is drawn: a lab's text renders its icons with a render() of its own (iconHtml.js), and that runs
// the watchers queued after the render before the pills are drawn
watch([() => route.path, strip], () => nextTick(place))
onMounted(() => addEventListener('resize', edges))
onBeforeUnmount(() => removeEventListener('resize', edges))

// a mouse wheel moves the pills that do not fit; at their end the page scrolls on
function wheel(e) {
  const el = strip.value, d = e.deltaY
  const room = d > 0 ? el.scrollWidth - el.clientWidth - el.scrollLeft : el.scrollLeft
  if (Math.abs(e.deltaX) >= Math.abs(d) || room <= 1) return  // a pixel: a strip of a fractional width ends there
  e.preventDefault()
  el.scrollLeft += d
}
</script>

<template>
  <div ref="strip" class="strip" :class="fade" @scroll="edges" @wheel="wheel"><LabNav :n /></div>
</template>

<style scoped>
.strip { display: flex; flex: 1 1 auto; align-items: center; align-self: stretch; min-width: 0; overflow-x: auto; scrollbar-width: none;
         mask-image: linear-gradient(to right, transparent, #000 var(--fl, 0px), #000 calc(100% - var(--fr, 0px)), transparent);
         transition: opacity .25s, visibility .25s; }
.strip.away { opacity: 0; visibility: hidden; }
.strip::-webkit-scrollbar { display: none; }
.strip.l { --fl: 1.5rem; }
.strip.r { --fr: 1.5rem; }
.strip :deep(.lab-nav) { flex: none; flex-wrap: nowrap; gap: .3rem; }
.strip :deep(.pill) { padding: .15rem .6rem; font-size: .85rem; white-space: nowrap; }
@media (pointer: coarse) { .strip :deep(.pill) { padding-block: .3rem; } }  /* a finger: taller to tap, the same widths */
</style>
