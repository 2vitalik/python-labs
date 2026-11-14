<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'

import GuideText from '@core/components/GuideText.vue'
import Icon from '@core/components/Icon.vue'
import { load, save } from '@core/local.js'
import { moments } from '../moments.js'

// a game's examples step by step (T274 §8, T276 «Показ»): the legend on top, then one frame at a time — «◀ 3 з 12 ▶», the
// arrow keys too while the mouse or the focus is here; or the frames one after another; or «грати» — the next frame by
// itself every 1.5 s, for a projector. Scenarios («### …» in the text) are tabs over the frames. A frame is a picture with
// its caption under it (T284 §5). The switch stands where the frames start — after the legend: it rules them only. In
// steps every frame sits in one grid cell, so the block is as tall as the tallest frame and nothing jumps between steps
const props = defineProps({ text: String })
const cut = computed(() => moments(props.text))
const tab = ref(0)
const sc = computed(() => cut.value.scenarios[tab.value] || cut.value.scenarios[0] || { frames: [] })
const n = computed(() => sc.value.frames.length)
const chosen = ref(load('moments-mode'))  // the reader's choice, for every game
const steps = computed(() => n.value > 1 && (chosen.value || (n.value >= 3 ? 'steps' : 'all')) === 'steps')
const at = ref(0)
const go = (i) => (at.value = Math.min(n.value - 1, Math.max(0, i)))
const playing = ref(false)
const setMode = (m) => { chosen.value = m; save('moments-mode', m); playing.value = false }
const pick = (i) => { tab.value = i; at.value = 0; playing.value = false }

// a step by hand restarts the count; the last frame stops the play
let timer = 0
watch([playing, at, tab], () => {
  clearTimeout(timer)
  if (playing.value) timer = setTimeout(() => (at.value < n.value - 1 ? at.value++ : (playing.value = false)), 1500)
})
function play() {
  if (playing.value) return (playing.value = false)
  if (!steps.value) setMode('steps')
  if (at.value >= n.value - 1) at.value = 0
  playing.value = true
}

const root = ref()
const hover = ref(false)
function key(e) {
  if (!steps.value || !(hover.value || root.value?.contains(document.activeElement))) return
  if (e.target.closest?.('input, textarea, select, [contenteditable]')) return
  const d = { ArrowLeft: -1, ArrowRight: 1 }[e.key]
  if (!d) return
  e.preventDefault()
  go(at.value + d)
}
onMounted(() => document.addEventListener('keydown', key))
onBeforeUnmount(() => { document.removeEventListener('keydown', key); clearTimeout(timer) })
</script>

<template>
  <div ref="root" @mouseenter="hover = true" @mouseleave="hover = false">
    <GuideText v-if="cut.legend" :text="cut.legend" class="mb-3" />
    <ul v-if="cut.scenarios.length > 1" class="nav nav-tabs mb-2">
      <li v-for="(s, i) in cut.scenarios" :key="i" class="nav-item">
        <button type="button" class="nav-link" :class="{ active: sc === s }" @click="pick(i)">{{ s.title || `Сценарій ${i + 1}` }}</button>
      </li>
    </ul>
    <!-- the switch and the steps' buttons stay above the frame: frames differ in height, the buttons must not move -->
    <div v-if="n > 1" class="d-flex flex-wrap align-items-center gap-2 mb-2">
      <div class="btn-group btn-group-sm me-2" role="group" aria-label="вигляд прикладів">
        <button type="button" class="btn btn-outline-secondary" :class="{ active: steps && !playing }" @click="setMode('steps')">по кроках</button>
        <button type="button" class="btn btn-outline-secondary" :class="{ active: !steps }" @click="setMode('all')">усе підряд</button>
        <button type="button" class="btn btn-outline-secondary play" :class="{ active: playing }" :title="playing ? 'зупинити' : 'кадри самі, раз на півтори секунди'" @click="play">
          <Icon :name="playing ? 'pause' : 'play'" /> {{ playing ? 'пауза' : 'грати' }}</button>
      </div>
      <template v-if="steps">
        <button type="button" class="btn btn-sm btn-outline-secondary" :disabled="at === 0" title="попередній крок (←)" @click="go(at - 1)"><Icon name="left" /></button>
        <span class="small text-nowrap">крок {{ at + 1 }} з {{ n }}</span>
        <button type="button" class="btn btn-sm btn-outline-secondary" :disabled="at === n - 1" title="наступний крок (→)" @click="go(at + 1)"><Icon name="right" /></button>
        <span class="dots d-flex flex-wrap">
          <button v-for="i in n" :key="i" type="button" class="dot" :class="{ on: i - 1 === at }" :title="`крок ${i}`" @click="go(i - 1)" />
        </span>
      </template>
    </div>
    <div v-if="n" :key="tab" :class="steps ? 'frames' : 'all'">
      <figure v-for="(f, i) in sc.frames" :key="i" class="frame" :class="{ off: steps && i !== at }" :aria-hidden="steps && i !== at">
        <GuideText :text="f.grid" />
        <figcaption v-if="f.caption"><GuideText :text="f.caption" /></figcaption>
        <GuideText v-if="f.after" :text="f.after" class="after" />
      </figure>
    </div>
    <GuideText v-if="sc.tail" :text="sc.tail" />
  </div>
</template>

<style scoped>
.frames { display: grid; }
.frames > * { grid-area: 1 / 1; min-width: 0; }
.frames > .off { visibility: hidden; }
.frame { margin: 0; }
.all > .frame + .frame { margin-top: 1.75rem; }
/* the caption belongs to the picture above it: close to it, smaller and quieter than the page's text */
.frame :deep(pre), .frame > :first-child :deep(> :last-child) { margin-bottom: .35rem; }
figcaption { font-size: .9rem; color: var(--bs-secondary-color); }
figcaption :deep(p) { margin-bottom: .25rem; }
figcaption :deep(strong) { color: var(--bs-body-color); }
.after { margin-top: .75rem; }
.play { min-width: 5.2rem; }  /* «грати» and «пауза» take the same room: the arrows beside do not shift */
.nav-link { padding: .3rem .75rem; font-size: .875rem; }
.dot { width: .9rem; height: .9rem; padding: 0; border: 0; background: none; }
.dot::before { content: ''; display: block; width: .45rem; height: .45rem; margin: auto; border-radius: 50%; background: var(--bs-border-color); }
.dot:hover::before { background: var(--bs-secondary-color); }
.dot.on::before { background: var(--bs-body-color); }
</style>
