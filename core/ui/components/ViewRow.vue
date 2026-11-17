<script setup>
import { computed, inject } from 'vue'

import { describe } from '../tableDiff.js'
import { originLine, workLine, worked } from '../viewStats.js'
import { saveView } from '../viewStore.js'
import Icon from './Icon.vue'
import InlineText from './InlineText.vue'
import Reveal from './Reveal.vue'
import ViewIcon from './ViewIcon.vue'
import ViewLibActs from './ViewLibActs.vue'
import ViewLibTags from './ViewLibTags.vue'
import ViewVersions from './ViewVersions.vue'

// one view in the library (T315 §8), two levels of text: its icon and name (both changed in place), and under them,
// smaller and greyer, «для чого», then one line — what it is made of, how it was used (in plain colour once worked
// with), where it came from, its tags. The switches and actions stand grey on the right; the history opens under the row.
// The grip says `grab` — the folder makes the row draggable while it is held
const props = defineProps({ view: { type: Object, required: true }, canDrag: Boolean })
const emit = defineEmits(['grab'])
const lib = inject('viewsLib')
const save = (patch) => saveView(props.view.slug, patch)
const made = computed(() => describe(props.view.query, lib.cols).map((x) => x.text).join(' · '))
</script>

<template>
  <li :id="`view-${view.slug}`" class="vrow">
    <div class="vrow-main">
      <span class="vrow-grip" :class="{ off: !canDrag }" :title="canDrag ? 'Потягни — переставити чи перенести в іншу папку' : 'Переставляти можна в порядку «свій»'"
            @mousedown="canDrag && emit('grab')"><Icon name="grip" /></span>
      <ViewIcon :view can class="vrow-icon" />
      <div class="vrow-body">
        <div class="vrow-l1">
          <InlineText class="vrow-title" :value="view.title" :save="(title) => save({ title })" can required />
          <RouterLink :to="`/table?view=${view.slug}`" class="iact mini" title="Відкрити в таблиці"><Icon name="open" /></RouterLink>
        </div>
        <InlineText class="vrow-about" :value="view.about" :save="(about) => save({ about })" can multi block placeholder="Для чого цей вид">
          <template #empty><span class="more-field">＋ для чого</span></template>
        </InlineText>
        <div class="vrow-meta">
          <span class="part" :title="made">{{ made }}</span>
          <span class="part" :class="{ worked: worked(view) }" :title="workLine(view)">{{ workLine(view) }}</span>
          <span v-if="originLine(view)" class="part" :title="originLine(view)">{{ originLine(view) }}</span>
          <ViewLibTags :view />
        </div>
      </div>
      <ViewLibActs :view />
    </div>
    <Reveal :show="!!lib.hist[view.slug]"><ViewVersions :view class="vrow-vers" /></Reveal>
  </li>
</template>

<style scoped>
.vrow { padding: .4rem .3rem .45rem; border-bottom: 1px solid var(--bs-border-color-translucent); border-radius: .3rem; }
.vrow:hover { background: color-mix(in srgb, var(--bs-tertiary-bg) 70%, transparent); }
.vrow-main { display: flex; align-items: flex-start; gap: .45rem; }
.vrow-grip { display: inline-flex; padding-top: .2rem; color: var(--bs-secondary-color); opacity: .35; cursor: grab; }
.vrow:hover .vrow-grip { opacity: .8; }
.vrow-grip.off, .vrow:hover .vrow-grip.off { opacity: .2; cursor: not-allowed; }
.vrow-icon { padding-top: .05rem; font-size: 1.1rem; }
.vrow-body { flex: 1; min-width: 0; }
.vrow-l1 { display: flex; align-items: center; gap: .3rem; min-width: 0; }
.vrow-title { font-weight: 600; }
.vrow-title:not(.open) { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.vrow-l1 .iact { opacity: .6; }
.vrow:hover .vrow-l1 .iact { opacity: 1; }
.vrow-about { margin-top: .05rem; font-size: .85rem; color: var(--bs-secondary-color); }
.vrow:not(:hover):not(:focus-within) .vrow-about .more-field { opacity: .55; }
/* each part stays whole and goes to the next line when the row is short; one longer than the row ends in «…» */
.vrow-meta { display: flex; flex-wrap: wrap; align-items: center; min-width: 0; margin-top: .1rem; font-size: .76rem; color: var(--bs-secondary-color); white-space: nowrap; }
.part { max-width: 100%; overflow: hidden; text-overflow: ellipsis; opacity: .8; }
.part.worked { color: var(--bs-body-color); opacity: 1; }
.part + .part::before { content: '·'; margin: 0 .4rem; }
.vrow:not(:hover):not(:focus-within) .vtags.empty:not(.open) { visibility: hidden; }  /* «＋ теги» — only where the mouse is */
.vrow-vers { margin: .35rem 0 .1rem 2.6rem; }
</style>
