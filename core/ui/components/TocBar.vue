<script setup>
import { computed, watchEffect } from 'vue'
import { useRouter } from 'vue-router'

import { goQuiet } from '../anchors.js'
import { chapterOf, TOC_ROW, tocActive, tocBar, tocItems, tocUnder, tocUnderRow } from '../toc.js'

// «where am I» on a long page (T287, T381): once a section's heading has scrolled under the menu, a row there names the
// section; once a sub-section's heading has gone under that row, a second row names the sub-section. While the next heading
// stands at the top of the window a row steps aside: the heading says it better. A click anywhere on a row goes to its
// heading at once, without a flash, and the heading lands right under what stays stuck. A page that sticks its own headings
// (the game's sections) switches the rows off through Toc's `bar`
defineProps({ wide: Boolean })
const router = useRouter()
const on = computed(() => tocBar.value && tocItems.value.length > 0)
const sub = computed(() => on.value && tocItems.value.some((h, i) => chapterOf(tocItems.value, i)))
const at = (id) => tocItems.value.findIndex((h) => h.id === id)
const rows = computed(() => {
  const i = on.value ? at(tocActive.value) : -1
  if (i < 0) return []
  const h = tocItems.value[i], sec = chapterOf(tocItems.value, i) || h
  const gone = (x, under) => !!under && at(x.id) <= at(under)
  if (!gone(sec, tocUnder.value)) return []
  return sec !== h && gone(h, tocUnderRow.value) ? [sec, h] : [sec]
})
// what is scrolled to lands under the rows, not behind them (style.css: scroll-padding-top; two rows — below)
watchEffect(() => {
  document.documentElement.classList.toggle('toc-bar', on.value)
  document.documentElement.classList.toggle('toc-sub', sub.value)
})
// a sub-section's heading lands under the section's row, which stays; a section's — under the menu
function go(e, h, depth) {
  if (e.target.closest('a') && (e.metaKey || e.ctrlKey || e.shiftKey)) return  // the browser's own: another tab
  e.preventDefault()
  const css = getComputedStyle(document.documentElement)
  goQuiet(h.id, (parseFloat(css.getPropertyValue('--nav-h')) || 0) + (depth ? TOC_ROW * parseFloat(css.fontSize) : 0) + 8, router)
}
</script>

<template>
  <div v-if="rows.length" class="bar">
    <div v-for="(h, i) in rows" :key="i" class="line" :class="{ sub: i }" :title="i ? 'До початку підрозділу' : 'До початку розділу'"
         @click="go($event, h, i)">
      <div class="d-flex align-items-center h-100" :class="wide ? 'container-fluid px-4' : 'page'">
        <span v-if="i" class="sep">›</span>
        <a :href="'#' + h.id" class="name">{{ h.text }}</a>
      </div>
    </div>
  </div>
</template>

<style scoped>
.bar { position: fixed; z-index: 1019; top: var(--nav-h, 0px); left: 0; right: 0; background: var(--bs-body-bg); }
.line { height: 2rem; border-bottom: 1px solid var(--bs-border-color); font-size: .9rem; cursor: pointer; }
.line.sub { height: 1.75rem; font-size: .82rem; }
.line:hover { background: var(--bs-tertiary-bg); }
.name { min-width: 0; overflow: hidden; color: var(--bs-body-color); font-weight: 600; text-decoration: none; text-overflow: ellipsis; white-space: nowrap; }
.sub .name { color: var(--bs-secondary-color); font-weight: 400; }
.line:hover .name { color: var(--bs-body-color); }
.sep { margin: 0 .4rem 0 .6rem; color: var(--bs-tertiary-color); }
@media print { .bar { display: none; } }
</style>

<style>
/* both rows (2rem + 1.75rem) where a sub-section's row can show; style.css: 2rem for one */
html.toc-bar.toc-sub { --stick-h: 3.75rem; }
</style>
