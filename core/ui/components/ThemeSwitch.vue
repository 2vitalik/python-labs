<script setup>
import { ref } from 'vue'

import { mode, nextTheme } from '../theme.js'
import IconTheme from './IconTheme.vue'

// like the flash button of a phone camera: clicks go round three modes, the icon and a note shown for a moment
// say which one is on — so the click that leaves the page as it was (pinned → auto) is not a silent one
const NOTES = { light: 'Завжди світла', dark: 'Завжди темна', auto: 'Авто — як на пристрої' }
const lit = ref(false)
let timer
function click() {
  nextTheme()
  lit.value = true
  clearTimeout(timer)
  timer = setTimeout(() => (lit.value = false), 1200)
}
</script>

<template>
  <!-- the note answers a click only: shown under the cursor as well, it would never leave after one -->
  <button type="button" class="btn btn-sm border-0 p-1 d-inline-flex text-body-secondary position-relative" :class="{ lit }"
          :title="`Тема: ${NOTES[mode].toLowerCase()}`" @click="click" @mouseleave="lit = false">
    <IconTheme :mode="mode" />
    <span class="note" aria-hidden="true">{{ NOTES[mode] }}</span>
  </button>
</template>

<style scoped>
/* a phone keeps :hover after a tap */
@media (hover: hover) { .btn:hover { color: var(--bs-body-color) !important; } }
.note { position: absolute; top: 100%; right: 0; z-index: 1000; margin-top: .4rem; padding: .2rem .5rem; border-radius: .375rem;
        font-size: .8rem; white-space: nowrap; pointer-events: none; opacity: 0; transition: opacity .15s;
        color: var(--bs-body-bg); background: var(--bs-emphasis-color); }
.lit .note { opacity: .9; }
</style>
