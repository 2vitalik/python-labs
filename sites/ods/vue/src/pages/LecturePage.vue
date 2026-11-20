<script setup>
import { computed, nextTick, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { getGuidePage } from '@core/api.js'
import Crumbs from '@core/components/Crumbs.vue'
import GuideBody from '@core/components/GuideBody.vue'
import Lightbox from '@core/components/Lightbox.vue'
import Toc from '@core/components/Toc.vue'
import { textOf } from '@core/drafts.js'
import { loadGuide } from '@core/guide.js'
import { tocOf } from '@core/md.js'
import { problem } from '@core/problem.js'
import { site } from '@core/site.js'
import { useTitle } from '@core/title.js'

import '../labColors.css'
import FoundBar from '../components/FoundBar.vue'
import LecLook from '../components/LecLook.vue'
import LectureAnchors from '../components/LectureAnchors.vue'
import Slides from '../components/Slides.vue'
import { author } from '../lecLook.js'
import { labsOf, withMarks } from '../lectures.js'
import { vRich } from '../rich.js'
import { slidesOf } from '../slides.js'

// a lecture: the text with its contents and the slides' numbers on its margin, or its slides one at a time (?slide=N);
// a number in the text opens its slide, «Текст» / «у тексті» of a slide comes back to the slide's place in the text
const route = useRoute()
const router = useRouter()
const list = computed(() => site.guide.filter((s) => s.kind === 'lectures'))
const doc = computed(() => list.value.find((s) => String(s.n) === route.params.n))
const prev = computed(() => list.value[list.value.indexOf(doc.value) - 1])
const next = computed(() => list.value[list.value.indexOf(doc.value) + 1])
const labs = computed(() => labsOf(doc.value?.n))
const page = ref(null)
const body = ref()
const slides = computed(() => slidesOf(page.value?.public ?? textOf(page.value)))  // no drafts on a slide: it may be on a projector
const plain = (text) => text.replace(/\$([^$]+)\$/g, (_, tex) => tex.replace(/[{}\\]/g, ''))  // the contents are text: $R^{2}$ → R^2
const toc = computed(() => tocOf(textOf(page.value)).map((h) => ({ ...h, text: plain(h.text) })))
const slide = computed({
  get: () => (route.query.slide === undefined ? null : Number(route.query.slide)),
  set: (n) => router.replace({ query: { ...kept(), ...(n === null ? {} : { slide: n }) } }),
})
const kept = () => (route.query.find ? { find: route.query.find } : {})  // a search stays lit in both views; its place does not
const fmt = (d) => new Date(d).toLocaleDateString('uk-UA')
useTitle(() => page.value?.title)

const marks = () => [...(body.value?.querySelectorAll('.slide-mark') || [])]
// the slide the reader has got to: the last number above the upper third of the window
const reading = () => Number(marks().filter((a) => a.getBoundingClientRect().top < innerHeight / 3).at(-1)?.textContent ?? slides.value[0].n)

function clickMark(e) {
  const a = e.target.closest('a.slide-mark')
  if (!a || e.metaKey || e.ctrlKey || e.shiftKey) return  // with a key — the browser's own: ?slide=N in a new tab
  e.preventDefault()
  if (!a.closest('.editor')) slide.value = Number(a.textContent)  // in the editor's preview it would drop the edit
}

// back to the text at slide n's number (or the nearest before it — a mark inside a list stays a comment); its blocks light up
let timer
async function toText(n) {
  await router.replace({ query: kept() })
  await nextTick()
  // the text is drawn anew: its pictures have no height until decoded, and the place would slide away under the scroll
  await Promise.all([...body.value.querySelectorAll('img')].map((img) => img.decode().catch(() => null)))
  const at = marks().filter((a) => Number(a.textContent) <= n).at(-1)?.parentElement
  if (!at) return window.scrollTo({ top: 0 })
  const blocks = []
  for (let el = at.nextElementSibling; el && !el.classList.contains('slide-at'); el = el.nextElementSibling) blocks.push(el)
  ;(blocks[0] || at).scrollIntoView({ block: 'start' })
  clearTimeout(timer)
  blocks.forEach((el) => el.classList.add('flash'))
  timer = setTimeout(() => blocks.forEach((el) => el.classList.remove('flash')), 2500)
}

// the guide's list comes with the text: «Потрібна для» names only the labs this reader has pages of, and nothing moves after
async function load() {
  page.value = null
  if (!doc.value) return (problem.value = 'lost')
  const [p] = await Promise.all([getGuidePage(doc.value.slug), loadGuide()])
  page.value = p
}
watch(doc, load, { immediate: true })
</script>

<template>
  <Crumbs :items="[['/lectures', 'Лекції'], doc?.nav]">
    <LecLook v-if="page" class="me-2" />
    <div v-if="slides.length > 1" class="btn-group btn-group-sm">
      <button class="btn btn-outline-secondary" :class="{ active: slide === null }" @click="slide !== null && toText(slide)">Текст</button>
      <button class="btn btn-outline-secondary" :class="{ active: slide !== null }" @click="slide === null && (slide = reading())">Слайди</button>
    </div>
  </Crumbs>
  <div v-if="page">
    <h1 class="h2 mb-3">{{ page.title }}</h1>
    <div v-if="labs.length" class="needs small text-body-tertiary">
      Потрібна для:
      <RouterLink v-for="lab in labs" :key="lab" :to="`/labs/${lab}`" class="lab lab-tint badge rounded-pill border fw-normal text-body-secondary"
                  :class="`lab-c${lab}`">Лаба {{ lab }}</RouterLink>
    </div>
    <FoundBar v-if="route.query.find || route.query.at" :root="body" :slides="slide !== null" />
    <Slides v-if="slide !== null && slides.length" v-model="slide" :slides :title="page.title" :slug="doc.slug" @text="toText" />
    <template v-else>
      <div ref="body" v-rich="doc.slug" class="lecture" :class="{ 'lec-author': author }" @click="clickMark">
        <GuideBody v-model:page="page" :view="withMarks" />
      </div>
      <LectureAnchors :root="body" />
      <Toc :items="toc" />
      <Lightbox />  <!-- the text's own: the slides have theirs, and two at once would both take ← → -->
    </template>
    <nav class="docs-nav mt-4 pt-3 border-top">
      <RouterLink v-if="prev" :to="prev.path">← {{ prev.nav }}</RouterLink><span v-else></span>
      <RouterLink to="/lectures" class="text-secondary">Лекції</RouterLink>
      <RouterLink v-if="next" :to="next.path">{{ next.nav }} →</RouterLink><span v-else></span>
    </nav>
    <div class="small text-body-tertiary text-end mt-3">Оновлено {{ fmt(page.updated) }}</div>
  </div>
</template>

<style scoped>
/* equal side columns keep the middle link centred whatever the neighbours' widths (or absence) */
.docs-nav { display: grid; grid-template-columns: 1fr auto 1fr; gap: 1rem; }
.docs-nav > :nth-child(3) { text-align: right; }
.needs { display: flex; flex-wrap: wrap; align-items: baseline; gap: .25rem; margin: -.5rem 0 1rem; }
.needs .lab { text-decoration: none; }
.needs .lab:hover { color: var(--bs-body-color) !important; }
/* the slides' numbers (withMarks) are out of the flow — the text keeps its place: on a narrow screen at the right end of the
   gap above the slide's first block, on a wide one on the right margin beside its first line (the contents start further) */
.lecture :deep(.slide-at) { position: relative; height: 0; }
.lecture :deep(.slide-mark) { position: absolute; right: 0; bottom: .1rem; min-width: 1.5rem; padding: 0 .3rem; font-size: .7rem; line-height: 1.4;
                              text-align: center; text-decoration: none; color: var(--bs-tertiary-color);
                              border: 1px solid var(--bs-border-color-translucent); border-radius: .25rem; }
.lecture :deep(.slide-mark:hover) { color: var(--bs-body-color); border-color: var(--bs-border-color); }
@media (min-width: 56rem) {
  .lecture :deep(.slide-mark) { right: -1.8rem; top: .2rem; bottom: auto; }
  .lecture :deep(.slide-at:has(+ h2) .slide-mark) { top: 1rem; }  /* a heading's own top margin is below the mark's line */
  .lecture :deep(.slide-at:has(+ h3) .slide-mark) { top: .4rem; }
  .lecture :deep(.slide-at:first-child .slide-mark) { top: .25rem; }  /* the first heading's margin is outside the text */
  .lecture :deep(.editor .slide-at .slide-mark) { right: 0; top: auto; bottom: .1rem; }  /* the preview has no margin */
}
@media print { .lecture :deep(.slide-mark) { display: none; } }
</style>
