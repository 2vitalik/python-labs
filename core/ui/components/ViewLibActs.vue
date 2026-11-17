<script setup>
import { inject, nextTick } from 'vue'

import { flash } from '../anchors.js'
import { archiveView, createView, liveViews, orderViews } from '../viewStore.js'
import Icon from './Icon.vue'
import ViewLibFlag from './ViewLibFlag.vue'

// the right end of a view's row in the library (T315 §8): ⭐ and 📌, then the actions — copy, history, compare, archive —
// grey till the mouse finds them; the one switched on (history open, marked for comparing) keeps its colour
const props = defineProps({ view: { type: Object, required: true } })
const lib = inject('viewsLib')
const picked = () => lib.picks.includes(props.view.slug)

// the copy remembers where it came from, stands right under its source and lights up there
const copy = () => lib.act(async () => {
  const v = props.view
  const c = await createView({ title: `${v.title} (копія)`, emoji: v.emoji, about: v.about, query: v.query, folder: v.folder, tags: v.tags,
                               pinned: v.pinned, parent: v.slug, parent_version: v.version })
  const order = liveViews().map((x) => x.slug).filter((s) => s !== c.slug)
  order.splice(order.indexOf(v.slug) + 1, 0, c.slug)
  await orderViews(order)
  await nextTick()
  flash(`view-${c.slug}`, { near: true })
})
</script>

<template>
  <div class="vacts">
    <ViewLibFlag :view field="etalon" />
    <ViewLibFlag :view field="pinned" />
    <span class="vacts-gap" />
    <button type="button" class="iact" title="Дублювати" @click="copy"><Icon name="copy" /></button>
    <button type="button" class="iact" :class="{ lit: lib.hist[view.slug] }" :aria-expanded="!!lib.hist[view.slug]" title="Історія версій"
            @click="lib.hist[view.slug] = !lib.hist[view.slug]"><Icon name="clock" /></button>
    <button type="button" class="iact" :class="{ lit: picked() }" :aria-pressed="picked()" title="Порівняти — відміть два види чи версії"
            @click="lib.pick(view.slug)"><Icon name="compare" /></button>
    <button type="button" class="iact" title="В архів: зникне з вкладок і звідси, повернути можна з «Архіву» внизу"
            @click="lib.act(() => archiveView(view.slug))"><Icon name="archive" /></button>
  </div>
</template>

<style scoped>
.vacts { display: flex; flex: none; align-items: center; }
.vacts-gap { width: .5rem; }
.iact.lit { background: var(--bs-tertiary-bg); color: var(--bs-primary); }
</style>
