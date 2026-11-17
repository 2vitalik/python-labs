<script setup>
import { computed, nextTick, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import Pop from '@core/components/Pop.vue'
import { vHint } from '@core/hint.js'
import { useEd } from '../ed.js'
import { BASE, FEATURES } from '../features.js'
import { SECTIONS } from '../sections.js'
import FeatureCheck from './FeatureCheck.vue'

// «Можливості» (T319): what the game page holds beyond its base — all of it, none, or one by one. Turning off takes away
// only the empty: what has data stays, so nothing filled is ever hidden. The owner's only (GameEditor).
// A map of the page (T348): the base on a line of its own, then the page from top to bottom — its own switches, then the
// sections in the page's order: one that is a feature of its own is a box with its name, a base one is its name with the
// features inside it on its line. What a thing means comes under the mouse (hint.js)
const ed = useEd()
const open = ref(false)
const busy = ref(false)
const ROWS = [
  { title: 'Сторінка', opts: FEATURES.filter((f) => f.place === 'page') },
  ...SECTIONS.map((id) => ({ self: FEATURES.find((f) => f.section === id), base: BASE.find((b) => b.place === id), opts: FEATURES.filter((f) => f.place === id) }))
    .filter((r) => r.self || r.opts.length),
]
const count = computed(() => FEATURES.filter((f) => ed.has(f.id)).length)
const ids = (fn) => FEATURES.filter(fn).map((f) => f.id)
const more = computed(() => ids((f) => !ed.has(f.id) && ed.offers(f.id)))
const less = computed(() => ids((f) => ed.has(f.id) && !ed.filled(f.id)))
const button = ref()
// a tile above may come or go with a feature: the page scrolls by as much, and the panel stays under the mouse
async function run(fn) {
  busy.value = true
  const was = button.value.getBoundingClientRect().top
  await fn()
  await nextTick()
  const shift = button.value.getBoundingClientRect().top - was
  if (shift) scrollBy({ top: shift, behavior: 'instant' })
  busy.value = false
}
</script>

<template>
  <Pop v-model="open" width="36.5rem">
    <template #trigger="{ toggle }">
      <button ref="button" type="button" class="btn btn-sm btn-outline-secondary" :aria-expanded="open" title="Що ще описати в грі: усе одразу чи галочками" @click="toggle">
        <Icon name="layers" /> Можливості <span class="cnt">{{ count ? `основа + ${count}` : 'основа' }}</span>
      </button>
    </template>
    <div class="fp vstack">
      <div class="base">
        <div class="cap">Основа — є завжди</div>
        <div class="line">
          <div class="items">
            <span v-for="b in BASE" :key="b.title" v-hint="{ title: b.title, text: b.text }" class="b">{{ b.icon }} {{ b.title }}</span>
          </div>
        </div>
      </div>
      <div class="head">
        <span class="cap add">Можна додати</span>
        <span v-hint="more.length ? 'Увімкнути все, що можна' : 'Усе вже ввімкнено'" class="ms-auto">
          <button type="button" class="btn btn-sm btn-outline-secondary bulk" :disabled="busy || !more.length" @click="run(() => ed.turn(more, true))">
            <Icon name="boxcheck" class="tick" /> Усе</button>
        </span>
        <span v-hint="less.length ? 'Вимкнути все порожнє — заповнене лишається' : 'Вимикати нічого: лишилось тільки заповнене'">
          <button type="button" class="btn btn-sm btn-outline-secondary bulk" :disabled="busy || !less.length" @click="run(() => ed.turn(ids((f) => !ed.filled(f.id)), false))">
            <Icon name="box" /> Нічого</button>
        </span>
      </div>
      <div class="map">
        <template v-for="r in ROWS" :key="r.self?.id || r.base?.place || r.title">
          <div class="where" :class="{ wide: !r.opts.length }">
            <FeatureCheck v-if="r.self" :f="r.self" :busy :run />
            <span v-else-if="r.base" v-hint="{ title: r.base.title, text: `${r.base.text} — є завжди` }" class="place">{{ r.base.icon }} {{ r.base.title }}</span>
            <span v-else class="place">{{ r.title }}</span>
          </div>
          <div v-if="r.opts.length" class="opts">
            <FeatureCheck v-for="f in r.opts" :key="f.id" :f :busy :run />
          </div>
        </template>
      </div>
    </div>
  </Pop>
</template>

<style scoped>
.cnt { font-size: .75rem; opacity: .7; font-variant-numeric: tabular-nums; }
.fp { gap: .6rem; font-size: .82rem; }
/* a caption apart from the names: grey for what is always there, the boxes' blue for what may be added */
.cap { font-size: .68rem; font-weight: 600; letter-spacing: .05em; text-transform: uppercase; color: var(--bs-secondary-color); }
.cap.add { color: var(--bs-primary-text-emphasis); }
.base { padding: .3rem .55rem .35rem; border-radius: .375rem; background: var(--bs-tertiary-bg); }
/* a dot between the names: each name's own, in the gap before it — the first of a line has its dot cut off at the edge */
.line { margin-top: .1rem; overflow-x: clip; }
.items { display: flex; flex-wrap: wrap; row-gap: .1rem; margin-left: -1.1rem; }
.b { position: relative; margin-left: 1.1rem; font-weight: 500; white-space: nowrap; cursor: default; }
.b::before { content: '·'; position: absolute; left: -.68rem; color: var(--bs-secondary-color); }
.head { display: flex; align-items: center; gap: .35rem; margin-bottom: -.2rem; }
.bulk { padding: 0 .45rem; font-size: .78rem; }
.tick { color: var(--bs-primary); }
.bulk:disabled .tick { color: inherit; }
.map { display: grid; grid-template-columns: max-content 1fr; align-items: start; column-gap: 1.1rem; row-gap: .15rem; }
.where.wide { grid-column: 1 / -1; }
/* a base section has no box: its name stands where the boxed names begin, level with the first line of its features */
.place { display: inline-block; padding: .1rem 0 .1rem calc(1em + .4rem); font-weight: 600; cursor: default; }
.where :deep(.name) { font-weight: 600; }
.opts { display: flex; flex-wrap: wrap; column-gap: .9rem; row-gap: .1rem; min-width: 0; }
/* a phone has one column, and its sheet (Pop) scrolls: the features go under their section's name */
@media (max-width: 575px) {
  .map { grid-template-columns: 1fr; }
  .opts { padding-left: calc(1em + .4rem); margin-bottom: .25rem; }
}
</style>
