<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

import { guideClick } from '../anchors.js'
import { renderMd } from '../md.js'

const props = defineProps({ text: String, prefix: { type: String, default: '' } })
const router = useRouter()
const html = computed(() => renderMd(props.text, props.prefix))
</script>

<template>
  <div class="guide" v-html="html" @click="guideClick($event, router)"></div>
</template>

<style>
/* global: v-html content and the JS-added .flash class live outside scoped styles */
.guide > :last-child { margin-bottom: 0; }
.guide h2 { font-size: 1.35rem; margin-top: 1.75rem; }
.guide h3 { font-size: 1.1rem; margin-top: 1.25rem; }
.guide h2, .guide h3, .guide h4, .guide li, .guide p, .guide tr { scroll-margin-top: 1rem; }
.guide li { margin-bottom: .2rem; }
.guide li > p { margin-bottom: .25rem; }
.guide .anchor { position: absolute; }
.guide .link { text-decoration: none; font-size: .7em; opacity: 0; margin-left: .1rem; transition: opacity .15s; }
.guide h1:hover .link, .guide h2:hover .link, .guide h3:hover .link, .guide h4:hover .link, .guide .link:focus { opacity: .6; }
.guide blockquote { border-left: 4px solid var(--bs-border-color); padding: .25rem 1rem; color: var(--bs-secondary-color); }
.guide blockquote.callout { border-color: var(--bs-info-border-subtle); background: var(--bs-info-bg-subtle); color: inherit; border-radius: .375rem; }
.guide .table-responsive { margin-bottom: 1rem; }
.guide table { margin-bottom: 0; }
.guide .flash { animation: guide-flash 2.5s ease-out; border-radius: .25rem; }
@keyframes guide-flash {
  0%, 45% { background-color: var(--bs-warning-bg-subtle); box-shadow: -.6rem 0 0 var(--bs-warning-bg-subtle), .4rem 0 0 var(--bs-warning-bg-subtle); }
  100% { background-color: transparent; box-shadow: none; }
}
@media (prefers-reduced-motion: reduce) {
  .guide .flash { animation: none; background-color: var(--bs-warning-bg-subtle); }
}
@media print { .navbar, .guide .link, .toc { display: none !important; } }
</style>
