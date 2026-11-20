<script setup>
import { computed, onMounted, onUnmounted, ref, shallowRef, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import Icon from '@core/components/Icon.vue'
import { box as shot } from '@core/lightbox.js'

import { blocksOf } from '../lectureAnchors.js'
import '../lectureFind.css'
import { paint, rangesOf, unpaint } from '../lectureFound.js'
import { firstOf, flash, nextOf, standOn } from '../lectureFoundPlace.js'

// a search's place in a lecture (?find=a|b&at=N, T374 §6.3): once the text is drawn it stands on slide N's first match (none —
// on the slide's start), lights every term — bright at first, calm after — and walks them ‹ ›; ✕ or Esc lets go of it all.
// `root` — the text, or the slides (`slides`: the terms of the slide shown, no walk). A strip under the menu (#top-shelf);
// a phone's text — a pill at the bottom, beside the page's own buttons
const props = defineProps({ root: Object, slides: Boolean })
const route = useRoute()
const router = useRouter()
const terms = computed(() => String(route.query.find || '').split('|').map((t) => t.trim()).filter(Boolean))
const ranges = shallowRef([])
const cur = ref(-1)
const hot = ref(true)
const narrow = matchMedia('(max-width: 575.98px)'), phone = ref(narrow.matches)
const pill = computed(() => phone.value && !props.slides)
watch([ranges, cur, hot], () => paint(ranges.value, cur.value, hot.value))

// the slides are found on the page: their component is not this page's to reach into
const target = () => (props.slides ? document.querySelector('.slides .slide-body') : props.root)
let landed = false, runs = 0, cool
async function measure() {
  const el = target()
  if (!el) return
  const run = ++runs
  await Promise.all([...el.querySelectorAll('img')].map((img) => img.decode().catch(() => null)))  // else the place slides away
  if (run !== runs) return
  ranges.value = rangesOf(el, terms.value)
  if (cur.value >= ranges.value.length) cur.value = -1
  if (landed) return
  landed = true  // once: opened on the slides, the text's place later is «у тексті»'s, not the search's
  if (!props.slides) land(el)
  cool = setTimeout(() => (hot.value = false), 4000)
}
function land(el) {
  const { i, mark } = firstOf(el, ranges.value, route.query.at)
  if (i >= 0) return go(i, true)
  if (!mark) return
  mark.scrollIntoView({ block: 'start', behavior: 'instant' })
  flash(blocksOf(mark))
}
function go(i, force) {
  cur.value = i
  standOn(ranges.value[i], force)
  flash([ranges.value[i].startContainer])
}
const step = (d) => ranges.value.length && go(nextOf(ranges.value, cur.value, d))
function close() {
  const query = { ...route.query }
  delete query.find
  delete query.at
  router.replace({ query, hash: route.hash })
}
function key(e) {
  if (e.key !== 'Escape' || shot.value || e.defaultPrevented || e.target.closest?.('input, textarea, select, [contenteditable]')) return
  close()
}

// the text is drawn anew (the admin's drafts, a slide turned): its ranges are counted again; the place is kept
const seen = new MutationObserver(() => measure())
watch(() => [props.root, props.slides], () => {
  const el = target()
  seen.disconnect()
  if (el) (seen.observe(el, { childList: true, subtree: true, characterData: true }), measure())
}, { immediate: true, flush: 'post' })
const fit = () => (phone.value = narrow.matches)
onMounted(() => (document.addEventListener('keydown', key), narrow.addEventListener('change', fit)))
onUnmounted(() => {
  seen.disconnect()
  clearTimeout(cool)
  unpaint()
  document.removeEventListener('keydown', key)
  narrow.removeEventListener('change', fit)
})
</script>

<template>
  <Teleport defer to="#top-shelf" :disabled="pill">
    <div v-if="terms.length" class="found" :class="{ pill }" role="region" aria-label="Знайдене в лекції">
      <div class="in" :class="{ page: !pill }">
        <Icon name="search" class="ico" />
        <span class="what"><span class="lbl">знайдено: </span><b>{{ terms.join(', ') }}</b></span>
        <span v-if="slides" class="count">на слайді: {{ ranges.length || 'нема' }}</span>
        <template v-else>
          <span class="count" :title="ranges.length ? 'Котрий збіг / усього в лекції' : 'У тексті лекції цих слів не видно'">{{ cur >= 0 ? cur + 1 : '–' }} / {{ ranges.length }}</span>
          <button type="button" class="nav" :disabled="!ranges.length" title="Попередній збіг" @click="step(-1)"><Icon name="left" /></button>
          <button type="button" class="nav" :disabled="!ranges.length" title="Наступний збіг" @click="step(1)"><Icon name="right" /></button>
        </template>
        <button type="button" class="nav x" title="Прибрати підсвітку (Esc)" @click="close"><Icon name="x" /></button>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
.found { border-bottom: 1px solid var(--bs-border-color); background: color-mix(in srgb, #ffc107 9%, var(--bs-body-bg)); font-size: .875rem; }
.in { display: flex; align-items: center; gap: .5rem; height: 2.25rem; }
.ico { flex-shrink: 0; color: var(--bs-secondary-color); }
.what { min-width: 0; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; color: var(--bs-secondary-color); }
.what b { font-weight: 600; color: var(--bs-body-color); }
.count { flex-shrink: 0; margin-left: auto; font-variant-numeric: tabular-nums; color: var(--bs-secondary-color); }
.nav { display: inline-flex; align-items: center; justify-content: center; flex-shrink: 0; width: 1.75rem; height: 1.75rem; padding: 0;
       color: var(--bs-secondary-color); background: none; border: 1px solid transparent; border-radius: .3rem; }
.nav:hover:not(:disabled) { color: var(--bs-body-color); border-color: var(--bs-border-color); background: var(--bs-body-bg); }
.nav:disabled { opacity: .4; }
.x { margin-left: .25rem; }
/* a phone: the text's pill floats at the bottom, clear of the page's own buttons on the right (PageJump) */
.found.pill { position: fixed; z-index: 1029; left: .75rem; right: 3.75rem; bottom: .75rem; border: 1px solid var(--bs-border-color);
              border-radius: 1.25rem; box-shadow: 0 .25rem 1rem rgba(0, 0, 0, .15); }
.pill .in { padding: 0 .35rem 0 .75rem; height: 2.5rem; }
.pill .lbl { display: none; }  /* the magnifier says it; the terms get the room */
@media print { .found { display: none; } }
</style>
