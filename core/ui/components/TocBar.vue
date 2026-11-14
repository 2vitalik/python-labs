<script setup>
import { computed, watchEffect } from 'vue'
import { useRouter } from 'vue-router'

import { guideClick } from '../anchors.js'
import { tocActive, tocBar, tocItems, tocUnder } from '../toc.js'

// «where am I» on a long page (T287): once a section's heading has scrolled under the menu, a thin row there names the
// section — and its chapter, when it is a sub-section; a click goes to its start. While the next heading stands at the
// top of the window the row steps aside: the heading says it better. A page that sticks its own headings (the game's
// sections) switches the row off through Toc's `bar`
defineProps({ wide: Boolean })
const router = useRouter()
const on = computed(() => tocBar.value && tocItems.value.length > 0)
const path = computed(() => {
  const i = on.value && tocUnder.value === tocActive.value ? tocItems.value.findIndex((h) => h.id === tocActive.value) : -1
  if (i < 0) return []
  const h = tocItems.value[i]
  const parent = h.depth === 3 && tocItems.value.slice(0, i).findLast((x) => x.label || x.depth < 3)
  return parent && !parent.label ? [parent, h] : [h]
})
// what is scrolled to lands under the row, not behind it (style.css: scroll-padding-top)
watchEffect(() => document.documentElement.classList.toggle('toc-bar', on.value))
</script>

<template>
  <div v-if="path.length" class="bar" @click="guideClick($event, router)">
    <div class="d-flex align-items-center" :class="wide ? 'container-fluid px-4' : 'page'">
      <template v-for="(h, i) in path" :key="h.id">
        <span v-if="i" class="sep">›</span>
        <a :href="'#' + h.id" class="name" :class="{ last: i === path.length - 1 }" title="До початку розділу">{{ h.text }}</a>
      </template>
    </div>
  </div>
</template>

<style scoped>
.bar { position: fixed; z-index: 1019; top: var(--nav-h, 0px); left: 0; right: 0; height: 2rem; display: flex; align-items: center;
       border-bottom: 1px solid var(--bs-border-color); background: var(--bs-body-bg); font-size: .9rem; }
.name { min-width: 0; overflow: hidden; color: var(--bs-secondary-color); text-decoration: none; text-overflow: ellipsis; white-space: nowrap; }
.name.last { color: var(--bs-body-color); font-weight: 700; }
.name:hover { text-decoration: underline; }
.sep { margin: 0 .4rem; color: var(--bs-secondary-color); }
@media print { .bar { display: none; } }
</style>
