<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'

import { back, close, leave, peek, peekView, pin, stay } from '../peek.js'
import Icon from './Icon.vue'
import PeekPace from './PeekPace.vue'

// one floating card of the chain in peek.js: it hangs under its anchor, turned up or shifted left where the window ends;
// clicked, it has a bar — back along the way it came, and a cross that closes it with the cards opened from it;
// at its foot — how fast the cards come (PeekPace)
const props = defineProps({ card: Object, k: Number })
const panel = ref()
const pos = ref(null)
const top = computed(() => props.card.stack.at(-1))
const view = computed(() => top.value && peekView(top.value.kind))

// `again` — the card on screen changed its height (clicked, it got its bar; its pace row opened): it is placed anew
// without a blink — still in the window, still off its anchor
async function place(again = false) {
  if (!again) pos.value = null
  await nextTick()
  if (!panel.value) return
  const a = props.card.at, p = panel.value.getBoundingClientRect(), gap = 6
  const below = a.top + a.height + gap, above = a.top - p.height - gap
  const fitsBelow = below + p.height < scrollY + innerHeight - 8
  pos.value = {
    left: `${Math.max(scrollX + 8, Math.min(a.left, scrollX + document.documentElement.clientWidth - p.width - 8))}px`,
    top: `${fitsBelow || above < scrollY + 8 ? below : above}px`,
  }
}
watch(() => [props.card.at, props.card.stack.length], () => place(), { immediate: true, flush: 'post' })
const sized = new ResizeObserver(() => pos.value && place(true))
onMounted(() => panel.value && sized.observe(panel.value))
onBeforeUnmount(() => sized.disconnect())
</script>

<template>
  <div v-if="view" ref="panel" class="peek-card shadow border rounded bg-body" :class="{ ready: pos }" :style="{ ...pos, zIndex: 1050 + k }" :data-k="k"
       @mouseenter="stay(k)" @mouseleave="leave" @click="pin(k)">
    <div v-if="k < peek.pinned" class="bar">
      <button v-if="card.stack.length > 1" type="button" class="nav" @click.stop="back(k)"><Icon name="left" /> назад</button>
      <button type="button" class="nav ms-auto" title="Закрити (Esc)" @click.stop="close(k)"><Icon name="x" /></button>
    </div>
    <component :is="view" v-bind="top" :key="`${top.kind}:${top.id}`" />
    <PeekPace />
  </div>
</template>

<style scoped>
.peek-card { position: absolute; width: 21rem; max-width: calc(100vw - 1rem); max-height: min(32rem, 80vh); overflow-y: auto;
             padding: .6rem .7rem; font-size: .875rem; visibility: hidden; }
.peek-card.ready { visibility: visible; }
.bar { display: flex; align-items: center; margin: -.25rem -.25rem .25rem; }
.nav { display: inline-flex; align-items: center; gap: .15rem; padding: .05rem .3rem; border: 0; border-radius: .25rem; background: none;
       color: var(--bs-secondary-color); font-size: .78rem; }
.nav:hover { background: var(--bs-tertiary-bg); color: var(--bs-body-color); }
</style>
