<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { flash, guideClick } from '../anchors.js'
import { renderMd } from '../md.js'

const props = defineProps({ text: String, prefix: { type: String, default: '' }, editable: Boolean })
const emit = defineEmits(['edit'])
const route = useRoute()
const router = useRouter()
const root = ref()
const html = computed(() => renderMd(props.text, props.prefix, props.editable))

// ✏️ on a heading (admin) opens the editor for that section; everything else is guideClick's
function click(e) {
  const edit = e.target.closest('a.edit')
  if (!edit) return guideClick(e, router)
  e.preventDefault()
  emit('edit', edit.dataset.id)
}

// the #target may live in this text: light it once the html is in the DOM (page load, section change)
function lightHash() {
  const el = route.hash && document.getElementById(route.hash.slice(1))
  if (el && root.value.contains(el)) flash(el.id)
}
onMounted(lightHash)
watch(html, lightHash, { flush: 'post' })
</script>

<template>
  <div ref="root" class="guide" v-html="html" @click="click"></div>
</template>

<style>
/* global: v-html content lives outside scoped styles; .flash is JS-added and may land on a section outside .guide (/all) */
.guide > :last-child { margin-bottom: 0; }
.guide h2 { font-size: 1.35rem; margin-top: 1.75rem; }
.guide h3 { font-size: 1.1rem; margin-top: 1.25rem; }
.guide h2, .guide h3, .guide h4, .guide li, .guide p, .guide tr { scroll-margin-top: 1rem; }
/* Notion-like: the bullet sits about where a paragraph starts, a nested bullet under its parent's text */
.guide ul { padding-left: 1.25rem; }
.guide ol { padding-left: 1.5rem; }
.guide li { margin-bottom: .2rem; }
.guide li > p { margin-bottom: .25rem; }
.guide .anchor { position: absolute; }
.guide .link, .guide .edit { text-decoration: none; font-size: .7em; opacity: 0; margin-left: .1rem; transition: opacity .15s; }
.guide :is(h1, h2, h3, h4):hover :is(.link, .edit), .guide :is(.link, .edit):focus { opacity: .6; }
.guide blockquote { border-left: 4px solid var(--bs-border-color); padding: .5rem 1rem; color: var(--bs-secondary-color); }
.guide blockquote > :last-child { margin-bottom: 0; }  /* the paragraph's own margin made the bottom gap bigger than the top */
/* callout: a paler yellow than the flash, so a flashed callout still lights up */
.guide blockquote.callout { border-color: var(--bs-warning-border-subtle); color: inherit; border-radius: .375rem;
                            background: color-mix(in srgb, var(--bs-warning-bg-subtle) 55%, var(--bs-body-bg)); }
.guide .table-responsive { margin-bottom: 1rem; }
/* ```field: cells sized by CSS, so the grid lines up whatever emoji font the OS has; [x] = just moved, (x) = effect */
.guide .field { width: fit-content; max-width: 100%; overflow-x: auto; margin-bottom: 1rem; padding: .35rem; line-height: 1;
                border: 1px solid var(--bs-border-color); border-radius: .375rem; background: var(--bs-tertiary-bg); }
.guide .field > div { display: flex; }
.guide .field .c { display: inline-flex; align-items: center; justify-content: center; width: 1.7em; height: 1.7em; flex-shrink: 0; }
.guide .field .mark-a { box-shadow: inset 0 0 0 2px var(--bs-primary); border-radius: .3rem; }
.guide .field .mark-b { box-shadow: inset 0 0 0 2px var(--bs-warning); border-radius: .3rem; }
.guide details { border: 1px solid var(--bs-border-color); border-radius: .375rem; padding: .5rem 1rem; margin-bottom: 1rem; }
.guide summary { cursor: pointer; }
.guide details[open] > summary { margin-bottom: .75rem; }
.guide table { margin-bottom: 0; }
.flash { animation: guide-flash 2.5s ease-out; border-radius: .25rem; }
@keyframes guide-flash {
  0%, 45% { background-color: var(--bs-warning-bg-subtle); box-shadow: -.6rem 0 0 var(--bs-warning-bg-subtle), .4rem 0 0 var(--bs-warning-bg-subtle); }
  100% { background-color: transparent; box-shadow: none; }
}
@media (prefers-reduced-motion: reduce) {
  .flash { animation: none; background-color: var(--bs-warning-bg-subtle); }
}
@media print { .navbar, .guide .link, .toc { display: none !important; } }
</style>
