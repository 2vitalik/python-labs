<script setup>
import { ref, watch } from 'vue'

import Icon from '@core/components/Icon.vue'

import { turn } from '../slideKeys.js'

// «далі ↓» at the foot of a slide that still scrolls (slideFit.js), until it is read to its end; a click turns a screen.
// `body` — the slide's body: it says `fit` once fitted (slideFit.js), and it scrolls
const props = defineProps({ body: Object })
const more = ref(false)
function look() {
  const b = props.body
  more.value = b.classList.contains('scroll') && b.scrollHeight - b.clientHeight - b.scrollTop > 2
}
watch(() => props.body, (b, old) => ['fit', 'scroll'].forEach((e) => {
  old?.removeEventListener(e, look)
  b?.addEventListener(e, look, { passive: true })
}), { immediate: true })
</script>

<template>
  <button v-if="more" type="button" class="slide-more" title="Прокрутити слайд (→, пробіл)" @click="turn(body, 1)">далі<Icon name="arrowdown" /></button>
</template>

<style>
/* over the fade (slides.css: .scroll) */
.slide-more { position: absolute; left: 50%; bottom: 1.6cqh; translate: -50% 0; display: inline-flex; align-items: center; gap: .3em;
              padding: .1em .8em; font-size: max(12px, 1.2cqw); line-height: 1.5; color: var(--lec-accent);
              background: color-mix(in srgb, var(--lec-paper) 85%, transparent); border: 1px solid var(--lec-rule); border-radius: 1em; }
.slide-more:hover { border-color: currentColor; }
.lec-author .slide-more { color: var(--au-n); }
</style>
