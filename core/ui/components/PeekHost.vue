<script setup>
import { computed, onBeforeUnmount, onMounted } from 'vue'

import { close, peek } from '../peek.js'
import PeekCard from './PeekCard.vue'

// the floating cards of peek.js, drawn where this is mounted — so what a card shows can read what the page provides
// (the game being described). Esc closes the last card of the chain, a click outside them all — every one
const id = Math.random()
const cards = computed(() => (peek.host === id ? peek.cards : []))
const outside = (e) => peek.pinned && !e.target.closest?.('.peek-card') && close()
const esc = (e) => e.key === 'Escape' && peek.cards.length && close(peek.cards.length - 1)
onMounted(() => {
  peek.host = id
  document.addEventListener('mousedown', outside)
  document.addEventListener('keydown', esc)
})
onBeforeUnmount(() => {
  if (peek.host === id) { peek.host = 0; close() }
  document.removeEventListener('mousedown', outside)
  document.removeEventListener('keydown', esc)
})
</script>

<template>
  <Teleport to="body">
    <PeekCard v-for="(card, k) in cards" :key="k" :card :k />
  </Teleport>
</template>

<style>
/* what the cards are made of, whatever they show: a head, rows, a fold, the way to the real place; a v-peek inside is a link */
.peek-card .peek-link { cursor: pointer; text-decoration: underline dotted; text-underline-offset: .2em; }
.peek-card .peek-link:hover { color: var(--bs-link-color); text-decoration-style: solid; }
.pk-head { display: flex; flex-wrap: wrap; align-items: baseline; gap: .15rem .45rem; }
/* a sign, a name, a price: one line — a long name wraps inside itself and never leaves its sign alone on a row (T296 §10) */
.pk-one { flex-wrap: nowrap; }
.pk-one > .fw-semibold { flex: 1 1 auto; min-width: 0; }
.pk-sign { align-self: center; }
.pk-hint { padding-top: .35rem; border-top: 1px dashed var(--bs-border-color); font-size: .75rem; color: var(--bs-secondary-color); }
.pk-type { font-size: .78rem; color: var(--bs-secondary-color); }
.pk-shot { align-self: flex-start; max-width: 100%; max-height: 9rem; cursor: zoom-in; }
.pk-row { display: flex; flex-wrap: wrap; gap: 0 .5rem; padding: .05rem 0; font-size: .82rem; }
.pk-fold { display: inline-flex; align-items: center; gap: .35rem; padding: 0; border: 0; background: none; color: var(--bs-secondary-color); font-size: .78rem; }
.pk-fold:hover { color: var(--bs-body-color); }
.pk-go { align-self: flex-start; display: inline-flex; align-items: center; gap: .3rem; padding: 0; border: 0; background: none;
         color: var(--bs-link-color); font-size: .8rem; text-decoration: none; }
.pk-go:hover { text-decoration: underline; }
</style>
