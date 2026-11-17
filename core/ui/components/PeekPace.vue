<script setup>
import { ref, watch } from 'vue'

import { pace, PACES, setPace } from '../peek.js'
import Icon from './Icon.vue'

// the reader's pace of the cards under the mouse (T344), at the foot of every card: a quiet sign opens the choice right
// there — so whoever is annoyed by the cards, or waits for them too long, finds the setting where the cards are.
// `grew` — the card is taller now: it finds its place again
const emit = defineEmits(['grew'])
const open = ref(false)
watch(open, () => emit('grew'), { flush: 'post' })
</script>

<template>
  <div class="pace">
    <template v-if="open">
      <span class="say">Картка зʼявляється, коли мишка зупинилась на слові:</span>
      <span class="btn-group btn-group-sm">
        <button v-for="([ms, word], k) in PACES" :key="k" type="button" class="btn" :class="pace === k ? 'btn-secondary' : 'btn-outline-secondary'"
                :title="`через ${ms / 1000} с`.replace('.', ',')" @click="setPace(k)">{{ word }}</button>
      </span>
    </template>
    <button type="button" class="sign" :class="{ on: open }" :aria-expanded="open" title="Як швидко зʼявляються картки під мишкою" @click="open = !open"><Icon name="sliders" /></button>
  </div>
</template>

<style scoped>
/* tucked into the card's own bottom padding: a card grows by a hair, not by a row */
.pace { display: flex; flex-wrap: wrap; align-items: center; justify-content: flex-end; gap: .3rem .4rem; margin: .1rem -.45rem -.4rem 0; }
.say { flex: 1 1 100%; font-size: .72rem; color: var(--bs-secondary-color); }
.btn { --bs-btn-padding-y: 0; --bs-btn-padding-x: .4rem; --bs-btn-font-size: .72rem; }
.sign { display: inline-flex; align-items: center; justify-content: center; width: 1.1rem; height: 1.1rem; padding: 0; border: 0; border-radius: .25rem; background: none;
        color: var(--bs-secondary-color); font-size: .75rem; opacity: .35; }
.sign:hover, .sign.on { background: var(--bs-tertiary-bg); color: var(--bs-body-color); opacity: 1; }
</style>
