<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'

import { back, close, leave, peek, peekView, stay } from '../peek.js'
import Icon from './Icon.vue'

// the one floating card of peek.js, drawn where it is mounted — so what a card shows can read what the page provides
// (the game being described). It hangs under its anchor, turned up or shifted left when the window ends; a pinned card
// has a bar: back along the way it came, and a cross. Esc or a click outside closes it
const id = Math.random()
const panel = ref()
const pos = ref(null)
const top = computed(() => (peek.host === id ? peek.stack.at(-1) : null))
const view = computed(() => top.value && peekView(top.value.kind))

async function place() {
  pos.value = null
  await nextTick()
  if (!panel.value || !peek.at) return
  const a = peek.at, p = panel.value.getBoundingClientRect(), gap = 6
  const below = a.top + a.height + gap, above = a.top - p.height - gap
  const fitsBelow = below + p.height < scrollY + innerHeight - 8
  pos.value = {
    left: `${Math.max(scrollX + 8, Math.min(a.left, scrollX + document.documentElement.clientWidth - p.width - 8))}px`,
    top: `${fitsBelow || above < scrollY + 8 ? below : above}px`,
  }
}
watch(() => [peek.at, peek.stack.length, peek.host], () => top.value && place(), { flush: 'post' })

const outside = (e) => peek.pinned && !panel.value?.contains(e.target) && close()
const esc = (e) => e.key === 'Escape' && peek.stack.length && close()
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
    <div v-if="view" ref="panel" class="peek-card shadow border rounded bg-body" :class="{ ready: pos }" :style="pos"
         @mouseenter="stay" @mouseleave="leave" @click="peek.stack.length && (peek.pinned = true)">
      <div v-if="peek.pinned" class="bar">
        <button v-if="peek.stack.length > 1" type="button" class="nav" @click.stop="back"><Icon name="left" /> назад</button>
        <button type="button" class="nav ms-auto" title="Закрити (Esc)" @click.stop="close"><Icon name="x" /></button>
      </div>
      <component :is="view" v-bind="top" :key="`${top.kind}:${top.id}`" />
    </div>
  </Teleport>
</template>

<style>
/* what the cards are made of, whatever they show: a head, rows, a fold, the way to the real place; a v-peek inside is a link */
.peek-card .peek-link { cursor: pointer; text-decoration: underline dotted; text-underline-offset: .2em; }
.peek-card .peek-link:hover { color: var(--bs-link-color); text-decoration-style: solid; }
.pk-head { display: flex; flex-wrap: wrap; align-items: baseline; gap: .15rem .45rem; }
.pk-type { font-size: .78rem; color: var(--bs-secondary-color); }
.pk-shot { align-self: flex-start; max-width: 100%; max-height: 9rem; cursor: zoom-in; }
.pk-row { display: flex; flex-wrap: wrap; gap: 0 .5rem; padding: .05rem 0; font-size: .82rem; }
.pk-fold { display: inline-flex; align-items: center; gap: .35rem; padding: 0; border: 0; background: none; color: var(--bs-secondary-color); font-size: .78rem; }
.pk-fold:hover { color: var(--bs-body-color); }
.pk-go { align-self: flex-start; display: inline-flex; align-items: center; gap: .3rem; padding: 0; border: 0; background: none;
         color: var(--bs-link-color); font-size: .8rem; text-decoration: none; }
.pk-go:hover { text-decoration: underline; }
</style>

<style scoped>
.peek-card { position: absolute; z-index: 1050; width: 21rem; max-width: calc(100vw - 1rem); max-height: min(32rem, 80vh); overflow-y: auto;
             padding: .6rem .7rem; font-size: .875rem; visibility: hidden; }
.peek-card.ready { visibility: visible; }
.bar { display: flex; align-items: center; margin: -.25rem -.25rem .25rem; }
.nav { display: inline-flex; align-items: center; gap: .15rem; padding: .05rem .3rem; border: 0; border-radius: .25rem; background: none;
       color: var(--bs-secondary-color); font-size: .78rem; }
.nav:hover { background: var(--bs-tertiary-bg); color: var(--bs-body-color); }
</style>
