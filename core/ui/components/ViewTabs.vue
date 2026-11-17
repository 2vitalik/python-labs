<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'

import { moved, useDragSort } from '../dragSort.js'
import { useTable } from '../tableCtx.js'
import { drafts } from '../viewDrafts.js'
import { liveViews, orderViews } from '../viewStore.js'
import Icon from './Icon.vue'
import Pop from './Pop.vue'
import ViewCard from './ViewCard.vue'
import ViewIcon from './ViewIcon.vue'
import ViewNew from './ViewNew.vue'

// the tabs of the views (T315 §2.1): the pinned ones in their order, dragged to a new one; the view open, when it is not on
// the tabs, stands last in a dashed frame. A dot — a change waits unsaved. Too many — the row scrolls, it does not wrap.
// The mouse held on a tab brings the view's card under it; it stays while the mouse is on the tab or the card, and half a
// second after — a card that runs from under the cursor annoys. At the end: a new view, the library of all of them
const t = useTable()
const pinned = computed(() => liveViews().filter((v) => v.pinned).sort((a, b) => a.order - b.order))
const loose = computed(() => (t.view && !pinned.value.some((v) => v.slug === t.slug) ? t.view : null))
const tabs = computed(() => (loose.value ? [...pinned.value, loose.value] : pinned.value))
const isLoose = (v) => v.slug === loose.value?.slug
const waits = (v) => (v.slug === t.slug ? t.dirty : !!drafts[v.slug])
const adding = ref(false)
const error = ref('')
const drag = useDragSort((from, to) => {
  orderViews(moved(pinned.value.map((v) => v.slug), from.i, to.i)).catch((e) => (error.value = e.message))
}, { axis: 'x' })
function go(e, v) {
  if (e.metaKey || e.ctrlKey || e.shiftKey) return  // a tab of the browser of its own
  e.preventDefault()
  if (v.slug !== t.slug) t.open(v.slug)
}

const wrap = ref()
const strip = ref()
const card = ref(null)  // { view, x } — x from the row's left edge
let showing, hiding
function enter(v, e) {
  if (e.pointerType !== 'mouse') return  // a finger has no hover: the card would stay after the tap
  clearTimeout(hiding)
  const at = { view: v, x: e.currentTarget.getBoundingClientRect().left - wrap.value.getBoundingClientRect().left }
  if (card.value) card.value = at
  else showing = setTimeout(() => (card.value = at), 400)
}
function leave() {
  clearTimeout(showing)
  hiding = setTimeout(() => (card.value = null), 500)
}
const stay = () => clearTimeout(hiding)
function hide() {
  clearTimeout(showing)
  clearTimeout(hiding)
  card.value = null
}
onBeforeUnmount(hide)
// the view open is in sight in a scrolled row
function reveal() {
  const s = strip.value
  const el = s?.querySelector('.on')
  if (el && (el.offsetLeft < s.scrollLeft || el.offsetLeft + el.offsetWidth > s.scrollLeft + s.clientWidth)) s.scrollLeft = el.offsetLeft - 24
}
onMounted(reveal)
watch(() => t.slug, reveal, { flush: 'post' })
</script>

<template>
  <div ref="wrap" class="vtabs mb-2">
    <div class="d-flex align-items-center gap-1">
      <div ref="strip" class="strip">
        <a v-for="(v, i) in tabs" :key="v.slug" v-bind="isLoose(v) ? {} : drag.item(i)" :href="`?view=${v.slug}`" class="vtab"
           :class="{ on: v.slug === t.slug, loose: isLoose(v) }" @click="go($event, v)" @pointerenter="enter(v, $event)" @pointerleave="leave" @pointerdown="hide">
          <ViewIcon :view="v" /><span class="name">{{ v.title }}</span><span v-if="waits(v)" class="dot" title="Тут є незбережені зміни" />
        </a>
      </div>
      <Pop v-model="adding" width="22rem">
        <template #trigger="{ toggle }">
          <button type="button" class="iact add" title="Новий вид" :aria-expanded="adding" @click="toggle"><Icon name="plus" /></button>
        </template>
        <ViewNew @close="adding = false" />
      </Pop>
      <RouterLink to="/table/views" class="all"><Icon name="grid" /> усі види</RouterLink>
    </div>
    <span v-if="error" class="small text-danger">{{ error }}</span>
    <Transition name="vcard">
      <ViewCard v-if="card" :view="card.view" class="card-at" :style="{ left: `clamp(0px, ${card.x}px, calc(100% - 20rem))` }" @mouseenter="stay" @mouseleave="leave" />
    </Transition>
  </div>
</template>

<style scoped>
.vtabs { position: relative; border-bottom: 1px solid var(--bs-border-color); }
.strip { position: relative; display: flex; min-width: 0; overflow: auto hidden; scrollbar-width: thin; }
.vtab { display: inline-flex; align-items: center; gap: .35rem; flex-shrink: 0; max-width: 16rem; padding: .35rem .65rem; border-bottom: 2px solid transparent;
        color: var(--bs-secondary-color); font-size: .9rem; text-decoration: none; white-space: nowrap; }
.vtab:hover { background: var(--bs-tertiary-bg); color: var(--bs-body-color); }
.vtab.on { border-bottom-color: var(--bs-primary); color: var(--bs-body-color); }
.vtab.loose { border-radius: .4rem .4rem 0 0; outline: 1px dashed var(--bs-border-color); outline-offset: -1px; }
.name { overflow: hidden; text-overflow: ellipsis; }
.dot { width: .45rem; height: .45rem; flex-shrink: 0; border-radius: 50%; background: var(--act-edit); }
.all { display: inline-flex; align-items: center; gap: .3rem; padding: 0 .4rem; color: var(--bs-secondary-color); font-size: .8rem; text-decoration: none; white-space: nowrap; }
.all:hover { color: var(--bs-body-color); }
.card-at { position: absolute; z-index: 35; top: calc(100% + 2px); }
.vcard-enter-active, .vcard-leave-active { transition: opacity .15s ease, transform .15s ease; }
.vcard-enter-from, .vcard-leave-to { opacity: 0; transform: translateY(-.25rem); }
@media (prefers-reduced-motion: reduce) { .vcard-enter-active, .vcard-leave-active { transition: none; } }
</style>
