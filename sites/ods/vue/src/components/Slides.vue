<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'

import GuideText from '@core/components/GuideText.vue'

// one slide at a time: ← → (and PgUp/PgDn, the clicker's keys) walk, F — the whole screen; `v-model` is the slide's own number
const props = defineProps({ slides: Array })
const n = defineModel({ type: Number })
const box = ref()
const at = computed(() => Math.max(0, props.slides.findIndex((s) => s.n === n.value)))
const go = (step) => {
  const s = props.slides[at.value + step]
  if (s) n.value = s.n
}
const full = () => (document.fullscreenElement ? document.exitFullscreen() : box.value.requestFullscreen())

function key(e) {
  if (e.altKey || e.ctrlKey || e.metaKey || e.target.closest('input, textarea')) return
  const step = { ArrowRight: 1, PageDown: 1, ' ': 1, ArrowLeft: -1, PageUp: -1 }[e.key]
  if (step) {
    e.preventDefault()
    go(step)
  } else if (e.key === 'f' || e.key === 'а') full()  // а — the same key on the Ukrainian layout
}
onMounted(() => document.addEventListener('keydown', key))
onUnmounted(() => document.removeEventListener('keydown', key))
</script>

<template>
  <div ref="box" class="slide border rounded">
    <GuideText :key="slides[at].n" :text="slides[at].text" class="slide-text" />
    <div class="bar d-flex align-items-center gap-2 small text-secondary">
      <button class="btn btn-sm btn-outline-secondary" :disabled="!at" title="Попередній (←)" @click="go(-1)">←</button>
      <span class="count">{{ at + 1 }} / {{ slides.length }}</span>
      <button class="btn btn-sm btn-outline-secondary" :disabled="at === slides.length - 1" title="Наступний (→)" @click="go(1)">→</button>
      <button class="btn btn-sm btn-outline-secondary ms-auto" title="На весь екран (F)" @click="full">⛶</button>
    </div>
  </div>
</template>

<style scoped>
.slide { display: flex; flex-direction: column; min-height: 65vh; padding: 1.5rem 2rem 1rem; background: var(--bs-body-bg); }
.slide-text { flex: 1; font-size: 1.1rem; }
.bar { margin-top: 1.5rem; }
.count { min-width: 4rem; text-align: center; }
.slide:fullscreen { padding: 3rem 5vw 1.5rem; overflow-y: auto; }
.slide:fullscreen .slide-text { font-size: 1.5rem; }
</style>
