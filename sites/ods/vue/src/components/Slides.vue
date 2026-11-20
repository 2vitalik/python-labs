<script setup>
import { computed, nextTick, onMounted, onUnmounted, ref, watch } from 'vue'

import GuideText from '@core/components/GuideText.vue'
import Icon from '@core/components/Icon.vue'
import Lightbox from '@core/components/Lightbox.vue'
import { showShot } from '@core/lightbox.js'

import { author } from '../lecLook.js'
import { fit } from '../slideFit.js'
import { useSlideKeys } from '../slideKeys.js'
import '../slides.css'
import { COURSE, coverOf, headHtml } from '../slides.js'
import SlideMore from './SlideMore.vue'
import SlideOrig from './SlideOrig.vue'

// one slide at a time on a 16:9 sheet (T359 §4); `v-model` is the slide's own number, «у тексті» sends it back (`text`).
// A slide shows only once its type is fitted (slideFit.js). The keys, the swipe and the whole screen are slideKeys.js'.
// The lightbox is its own: on the whole screen nothing outside this element is seen. `slug` — the lecture's: «оригінал»
// shows the lecturer's own slide (SlideOrig) in place of ours; the look — his colours or calm — is lecLook.js'
const props = defineProps({ slides: Array, title: String, slug: String })
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
const orig = ref(false), hasOrig = ref(false)
const { idle, canFull, full, wake, touchDown, touchUp } = useSlideKeys(root, body, go, orig)

// the sheet and its bar take the window from the sheet's own top down (slides.css: --top): scrolling the page to them would
// not hold — the router takes the page to its top at every slide. On the whole screen the sheet is the window's
const measure = () => document.fullscreenElement || root.value.style.setProperty('--top', `${Math.round(root.value.getBoundingClientRect().top + scrollY)}px`)
let runs = 0
async function place(hide) {
  const run = ++runs
  if (hide) ready.value = false
  measure()
  await nextTick()
  if (hide) body.value.scrollTop = 0  // the body stays the same element: a new slide starts from its top
  await fit(body.value)
  if (run === runs) ready.value = true
}
watch(text, () => place(true))
const refit = () => place(false)
const sized = new ResizeObserver(refit)
// opened from deep in the text the page stays scrolled as far as it still goes: the sheet's top comes out from under the shelf
// (--nav-h), by as little as it takes — a shelf scrolled to the very top grows, and its buttons would move
function inSight() {
  const shelf = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--nav-h')) || 0
  const top = root.value.getBoundingClientRect().top
  if (top < shelf + 8) scrollBy({ top: top - shelf - 8, behavior: 'instant' })
}
onMounted(() => (inSight(), place(true), sized.observe(sheet.value), document.fonts.addEventListener('loadingdone', refit)))
onUnmounted(() => (sized.disconnect(), document.fonts.removeEventListener('loadingdone', refit)))

function zoom(e) {
  const all = [...body.value.querySelectorAll('img')]
  if (all.includes(e.target)) showShot(all.map((i) => i.src), all.indexOf(e.target))
}
</script>

<template>
  <div ref="root" class="slides" :class="{ idle, 'lec-author': author }" @mousemove="wake">
    <div ref="sheet" class="slide" :class="{ cover, wait: !ready, orig }" :style="{ '--at': last ? at / last : 1 }"
         @touchstart.passive="touchDown" @touchend="touchUp">
      <div v-if="!cover" class="slide-head"><span class="sec" v-html="headHtml(cur.sec)"></span><span class="num">{{ cur.n }}</span></div>
      <div ref="body" class="slide-body" @click="zoom">
        <template v-if="cover">
          <div class="eyebrow">{{ COURSE }}</div>
          <div class="title"><span v-if="cover.topic" class="topic">{{ cover.topic }}</span>{{ cover.name }}</div>
        </template>
        <GuideText v-if="text" :key="cur.n" :text />
      </div>
      <SlideMore :body />
      <SlideOrig v-model="orig" v-model:has="hasOrig" :slug :n="cur.n" />
      <div class="slide-progress"></div>
    </div>
    <div class="slide-bar">
      <button class="btn btn-sm btn-outline-secondary" :disabled="!at" title="Попередній (←)" @click="go(-1)"><Icon name="left" /></button>
      <span class="count" title="Номер слайда / останній">{{ cur.n }} / {{ slides[last].n }}</span>
      <button class="btn btn-sm btn-outline-secondary" :disabled="at === last" title="Наступний (→)" @click="go(1)"><Icon name="right" /></button>
      <span class="grow"></span>
      <span :title="hasOrig ? 'Слайд лектора, як на лекції (O)' : 'Знімки слайдів лектора ще не залито'">
        <button class="btn btn-sm btn-outline-secondary" :class="{ active: orig }" :aria-pressed="orig" :disabled="!hasOrig" @click="orig = !orig"><Icon name="image" /><span class="word">оригінал</span></button>
      </span>
      <button class="btn btn-sm btn-outline-secondary" title="Це місце в тексті" @click="emit('text', cur.n)"><Icon name="book" /><span>у тексті</span></button>
      <button class="btn btn-sm btn-outline-secondary" :disabled="!canFull" title="На весь екран (F)" @click="full"><Icon name="full" /></button>
    </div>
    <Lightbox />
  </div>
</template>
