<script setup>
import { nextTick, onBeforeUnmount, ref, watch } from 'vue'

import Icon from './Icon.vue'

// a roomy window over the page (T318): the page stays underneath as it was, and closing the window is coming back to it.
// ✕, Esc or a click beside it closes; a floating panel or a field open inside takes its own Esc first.
// <Sheet v-model="open" title="…"> <template #head> beside the title </template> <template #bar> a fixed row under it </template> the body </Sheet>
const open = defineModel({ type: Boolean, default: false })
defineProps({ title: String, width: { type: String, default: '76rem' } })
const box = ref()
let back = null  // what had the focus: it gets it again

function key(e) {
  if (e.key !== 'Escape' || box.value?.querySelector('.pop-panel, .inl.open')) return
  e.stopPropagation()  // the page's own Esc is about the page
  open.value = false
}
// the wheel beside the window, or inside it with nothing to scroll, must not move the page underneath
function wheel(e) {
  for (let n = e.target; n && n !== box.value; n = n.parentElement) {
    if (n.scrollHeight > n.clientHeight + 1 && /auto|scroll/.test(getComputedStyle(n).overflowY)) return
  }
  e.preventDefault()
}
watch(open, async (on) => {
  document[on ? 'addEventListener' : 'removeEventListener']('keydown', key, true)
  if (!on) return back?.focus?.({ preventScroll: true })
  back = document.activeElement
  await nextTick()
  // the search field takes the keys at once — where there are keys: on a phone it would only raise the keyboard
  const field = matchMedia('(hover: hover)').matches && box.value?.querySelector('input:not([type=checkbox]), textarea')
  ;(field || box.value)?.focus({ preventScroll: true })
})
onBeforeUnmount(() => document.removeEventListener('keydown', key, true))
</script>

<template>
  <Teleport to="body">
    <Transition name="sheet">
      <div v-if="open" class="sheet-back" @mousedown.self="open = false" @wheel="wheel">
        <div ref="box" class="sheet shadow-lg border rounded bg-body" :style="{ width }" role="dialog" aria-modal="true" :aria-label="title" tabindex="-1">
          <header class="sheet-head">
            <span class="sheet-title">{{ title }}</span>
            <slot name="head" />
            <button type="button" class="iact ms-auto" title="Закрити — Esc" @click="open = false"><Icon name="x" /></button>
          </header>
          <div v-if="$slots.bar" class="sheet-bar"><slot name="bar" /></div>
          <div class="sheet-body"><slot /></div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style>
/* over the menu and the page's stuck headings; a tip under the mouse (1080) still shows over it */
.sheet-back { position: fixed; inset: 0; z-index: 1050; display: flex; align-items: flex-start; justify-content: center; padding: 2.5vh 1rem;
              background: rgb(0 0 0 / .32); }
/* roomy from the start: a search that leaves two cards does not shrink it under the hand */
.sheet { display: flex; flex-direction: column; max-width: 100%; min-height: min(38rem, 95vh); max-height: 95vh; outline: 0; }
.sheet-head { display: flex; flex-wrap: wrap; align-items: center; gap: .25rem .75rem; padding: .5rem .75rem; border-bottom: 1px solid var(--bs-border-color); }
.sheet-title { font-weight: 700; }
.sheet-bar { padding: .5rem .75rem 0; }
.sheet-body { flex: 1 1 auto; min-height: 8rem; overflow-y: auto; overscroll-behavior: contain; padding: .5rem .75rem .75rem; }
.sheet-enter-active, .sheet-leave-active { transition: opacity .16s ease; }
.sheet-enter-active > .sheet, .sheet-leave-active > .sheet { transition: transform .16s ease; }
.sheet-enter-from, .sheet-leave-to { opacity: 0; }
.sheet-enter-from > .sheet, .sheet-leave-to > .sheet { transform: translateY(.6rem); }
@media (prefers-reduced-motion: reduce) { .sheet-enter-active, .sheet-leave-active, .sheet-enter-active > .sheet, .sheet-leave-active > .sheet { transition: none; } }
/* a phone has no room for a frame: the window is the screen */
@media (max-width: 575px) {
  .sheet-back { padding: 0; }
  .sheet { width: 100% !important; height: 100%; max-height: none; border: 0 !important; border-radius: 0 !important; }
}
</style>
