<script setup>
import { onBeforeUnmount, watch } from 'vue'

import { box } from '../lightbox.js'
import Icon from './Icon.vue'

// a picture over the whole page (lightbox.js: showShot): a click anywhere or Esc folds it back, ← → walk the list.
// Mounted once by the page that has pictures. Its Esc and its click are its own: a panel the picture was opened from
// (a claim's, a card under the mouse) listens on the document for the same and must stay open
const step = (d) => (box.value.i = (box.value.i + d + box.value.list.length) % box.value.list.length)
function key(e) {
  if (e.key === 'Escape') { e.stopPropagation(); box.value = null }
  else if (e.key === 'ArrowRight') step(1)
  else if (e.key === 'ArrowLeft') step(-1)
}
watch(() => !!box.value, (on) => document[on ? 'addEventListener' : 'removeEventListener']('keydown', key, true))
onBeforeUnmount(() => document.removeEventListener('keydown', key, true))
</script>

<template>
  <Transition name="zoom">
    <div v-if="box" class="lightbox" @click="box = null" @mousedown.stop>
      <img :key="box.i" :src="box.list[box.i]" alt="">
      <button type="button" class="ctl close" title="Закрити (Esc)"><Icon name="x" /></button>
      <template v-if="box.list.length > 1">
        <button type="button" class="ctl prev" title="Попередній" @click.stop="step(-1)"><Icon name="left" /></button>
        <button type="button" class="ctl next" title="Наступний" @click.stop="step(1)"><Icon name="right" /></button>
        <span class="count">{{ box.i + 1 }} / {{ box.list.length }}</span>
      </template>
    </div>
  </Transition>
</template>

<style scoped>
.lightbox { position: fixed; inset: 0; z-index: 2000; display: flex; align-items: center; justify-content: center;
            background: rgba(0, 0, 0, .82); cursor: zoom-out; }
img { max-width: 94vw; max-height: 92vh; border-radius: .35rem; box-shadow: 0 .5rem 2rem rgba(0, 0, 0, .5); image-rendering: auto; }
.ctl { position: absolute; width: 2.5rem; height: 2.5rem; border: 0; border-radius: 50%; background: rgba(255, 255, 255, .14); color: #fff; font-size: 1.2rem; }
.ctl:hover { background: rgba(255, 255, 255, .28); }
.close { top: 1rem; right: 1rem; }
.prev { left: 1rem; }
.next { right: 1rem; }
.count { position: absolute; bottom: 1rem; color: rgba(255, 255, 255, .8); font-size: .85rem; }
.zoom-enter-active, .zoom-leave-active { transition: opacity .15s; }
.zoom-enter-active img, .zoom-leave-active img { transition: transform .15s; }
.zoom-enter-from, .zoom-leave-to { opacity: 0; }
.zoom-enter-from img, .zoom-leave-to img { transform: scale(.85); }
</style>
