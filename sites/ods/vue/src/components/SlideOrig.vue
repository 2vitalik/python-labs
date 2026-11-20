<script setup>
import { ref, watch } from 'vue'

import { showShot } from '@core/lightbox.js'

// the lecturer's own slide over ours (T374 §5): /api/media/<slug>/orig/sKK.webp, the whole of it on the sheet, a click —
// the lightbox. A lecture's pictures are uploaded all at once: its first one says whether there are any (`has` — the bar's
// button greys out without them, and `on` does not hold)
const props = defineProps({ slug: String, n: Number })
const on = defineModel({ type: Boolean })
const has = defineModel('has', { type: Boolean })
const src = (n) => `/api/media/${props.slug}/orig/s${String(n).padStart(2, '0')}.webp`
const lost = ref(false)  // this one slide has none

watch(() => props.slug, (slug) => {
  has.value = false
  const probe = new Image()
  probe.onload = () => (has.value = slug === props.slug)
  if (slug) probe.src = src(1)
}, { immediate: true })
watch([on, has], () => on.value && !has.value && (on.value = false))
watch(() => props.n, () => (lost.value = false))
</script>

<template>
  <div v-if="on && has" class="slide-orig">
    <img v-if="!lost" :src="src(n)" :alt="`Слайд ${n} лектора`" @click="showShot([src(n)])" @error="lost = true">
    <span v-else>Знімка слайда {{ n }} у лектора нема</span>
  </div>
</template>

<style>
/* over the whole sheet; his 4:3 slide as high as the sheet, on its paper */
.slide-orig { position: absolute; inset: 0; display: grid; place-items: center; color: var(--lec-muted); }
.slide-orig img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: contain; cursor: zoom-in; }
</style>
