<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { flash, guideClick } from '../anchors.js'
import { renderMd } from '../md.js'

const props = defineProps({ text: String, prefix: { type: String, default: '' } })
const route = useRoute()
const router = useRouter()
const root = ref()
const html = computed(() => renderMd(props.text, props.prefix))

// the #target may live in this text: light it once the html is in the DOM (page load, section change)
function lightHash() {
  const el = route.hash && document.getElementById(route.hash.slice(1))
  if (el && root.value.contains(el)) flash(el.id)
}
onMounted(lightHash)
watch(html, lightHash, { flush: 'post' })
</script>

<template>
  <div ref="root" class="guide" v-html="html" @click="guideClick($event, router)"></div>
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
.guide .link { text-decoration: none; font-size: .7em; opacity: 0; margin-left: .1rem; transition: opacity .15s; }
.guide h1:hover .link, .guide h2:hover .link, .guide h3:hover .link, .guide h4:hover .link, .guide .link:focus { opacity: .6; }
.guide blockquote { border-left: 4px solid var(--bs-border-color); padding: .5rem 1rem; color: var(--bs-secondary-color); }
.guide blockquote > :last-child { margin-bottom: 0; }  /* the paragraph's own margin made the bottom gap bigger than the top */
/* callout: a paler yellow than the flash, so a flashed callout still lights up */
.guide blockquote.callout { border-color: var(--bs-warning-border-subtle); color: inherit; border-radius: .375rem;
                            background: color-mix(in srgb, var(--bs-warning-bg-subtle) 55%, var(--bs-body-bg)); }
.guide .table-responsive { margin-bottom: 1rem; }
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
