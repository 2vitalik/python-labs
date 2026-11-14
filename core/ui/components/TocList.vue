<script setup>
import { nextTick, ref, watch } from 'vue'
import { useRouter } from 'vue-router'

import { guideClick } from '../anchors.js'
import { tocMarked } from '../toc.js'

// the links of a page's contents: [{id, text, depth}], {label} rows split groups; a click scrolls there and lights the place.
// The section being read is marked on the rail and kept in sight when the list itself scrolls; depth 4 — a sub-item of a
// title that starts with an icon: it stands right of the title's words, not of its icon
defineProps({ items: Array })
defineEmits(['went'])
const router = useRouter()
const root = ref()
watch(tocMarked, async () => {
  await nextTick()
  const on = root.value?.querySelector('.on'), box = root.value?.parentElement
  if (!on || !box) return
  const b = box.getBoundingClientRect(), r = on.getBoundingClientRect()
  if (r.top < b.top || r.bottom > b.bottom) box.scrollTop += r.top - b.top - b.height / 2
})
</script>

<template>
  <div ref="root" class="rail" @click="guideClick($event, router); $event.target.closest('a') && $emit('went')">
    <template v-for="(h, i) in items" :key="i">
      <div v-if="h.label" class="label text-uppercase fw-semibold mt-2 mb-1">{{ h.label }}</div>
      <a v-else :href="'#' + h.id" class="row-link d-block text-decoration-none" :class="{ sub: h.depth === 3, deep: h.depth === 4, on: h.id === tocMarked }"
         :aria-current="h.id === tocMarked ? 'location' : null">{{ h.text }}</a>
    </template>
  </div>
</template>

<style scoped>
.rail { border-left: 2px solid var(--bs-border-color); }
.label { padding-left: .7rem; }
.row-link { margin-left: -2px; padding: .15rem 0 .15rem .7rem; border-left: 2px solid transparent; color: var(--bs-secondary-color); }
.row-link.sub { padding-left: 1.6rem; }
.row-link.deep { padding-left: 2rem; font-size: .95em; }
.row-link:hover { color: var(--bs-body-color); }
/* bolder by a stroke, not by weight: a heavier face would re-wrap the row and shift its neighbours */
.row-link.on { border-left-color: var(--bs-primary); color: var(--bs-body-color); -webkit-text-stroke: .4px currentColor; }
</style>
