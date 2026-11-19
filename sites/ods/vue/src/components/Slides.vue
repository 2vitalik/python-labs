<script setup>
import { computed, nextTick, onMounted, onUnmounted, ref, watch } from 'vue'

import GuideText from '@core/components/GuideText.vue'
import Icon from '@core/components/Icon.vue'
import Lightbox from '@core/components/Lightbox.vue'
import { showShot } from '@core/lightbox.js'

import { fit } from '../slideFit.js'
import { useSlideKeys } from '../slideKeys.js'
import '../slides.css'
import { COURSE, coverOf, headHtml } from '../slides.js'

// one slide at a time on a 16:9 sheet (T359 §4); `v-model` is the slide's own number, «у тексті» sends it back (`text`).
// A slide shows only once its type is fitted (slideFit.js). The keys, the swipe and the whole screen are slideKeys.js'.
// The lightbox is its own: on the whole screen nothing outside this element is seen
const props = defineProps({ slides: Array, title: String })
const emit = defineEmits(['text'])
const n = defineModel({ type: Number })
const root = ref(), sheet = ref(), body = ref(), ready = ref(false)
const at = computed(() => Math.max(0, props.slides.findIndex((s) => s.n === n.value)))
const cur = computed(() => props.slides[at.value])
const last = computed(() => props.slides.length - 1)
const cover = computed(() => (at.value ? null : coverOf(cur.value, props.title)))
const text = computed(() => (cover.value ? cover.value.text : cur.value.text))
function go(step) {
  const s = props.slides[at.value + step]
  if (s) n.value = s.n
}
const { idle, canFull, full, wake, touchDown, touchUp } = useSlideKeys(root, go)

let runs = 0
async function place(hide) {
  const run = ++runs
  if (hide) ready.value = false
  await nextTick()
  await fit(body.value)
  if (run === runs) ready.value = true
}
watch(text, () => place(true))
const refit = () => place(false)
const sized = new ResizeObserver(refit)
onMounted(() => {
  place(true)
  sized.observe(sheet.value)
  document.fonts.addEventListener('loadingdone', refit)
})
onUnmounted(() => {
  sized.disconnect()
  document.fonts.removeEventListener('loadingdone', refit)
})

function zoom(e) {
  const all = [...body.value.querySelectorAll('img')]
  if (all.includes(e.target)) showShot(all.map((i) => i.src), all.indexOf(e.target))
}
</script>

<template>
  <div ref="root" class="slides" :class="{ idle }" @mousemove="wake">
    <div ref="sheet" class="slide" :class="{ cover, wait: !ready }" :style="{ '--at': last ? at / last : 1 }"
         @touchstart.passive="touchDown" @touchend="touchUp">
      <div v-if="!cover" class="slide-head"><span class="sec" v-html="headHtml(cur.sec)"></span><span class="num">{{ cur.n }}</span></div>
      <div ref="body" class="slide-body" @click="zoom">
        <template v-if="cover">
          <div class="eyebrow">{{ COURSE }}</div>
          <div class="title"><span v-if="cover.topic" class="topic">{{ cover.topic }}</span>{{ cover.name }}</div>
        </template>
        <GuideText v-if="text" :key="cur.n" :text />
      </div>
      <div class="slide-progress"></div>
    </div>
    <div class="slide-bar">
      <button class="btn btn-sm btn-outline-secondary" :disabled="!at" title="Попередній (←)" @click="go(-1)"><Icon name="left" /></button>
      <span class="count">{{ at + 1 }} / {{ slides.length }}</span>
      <button class="btn btn-sm btn-outline-secondary" :disabled="at === last" title="Наступний (→)" @click="go(1)"><Icon name="right" /></button>
      <span class="grow"></span>
      <button class="btn btn-sm btn-outline-secondary" title="Це місце в тексті" @click="emit('text', cur.n)"><Icon name="book" /><span>у тексті</span></button>
      <button class="btn btn-sm btn-outline-secondary" :disabled="!canFull" title="На весь екран (F)" @click="full"><Icon name="full" /></button>
    </div>
    <Lightbox />
  </div>
</template>
