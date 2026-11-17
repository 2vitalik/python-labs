<script setup>
import { computed } from 'vue'

import { columns } from '../tableCols.js'
import { describe } from '../tableDiff.js'
import { originLine, workLine } from '../viewStats.js'
import { store } from '../viewStore.js'
import Icon from './Icon.vue'
import ViewIcon from './ViewIcon.vue'

// a view at a glance (T315 §2.1, §9), under the mouse on its tab: what it is for, what it is made of part by part, its folder
// and tags, where it comes from, how much it was worked with. The columns come from the store, not the table's context:
// the card reads the same in the library. A line with nothing to say is not drawn
const p = defineProps({ view: { type: Object, required: true } })
const WHAT = { lab: 'лаба', cols: 'колонки', group: 'групи', filters: 'фільтри', sort: 'сортування' }
const parts = computed(() => (store.data ? describe(p.view.query, columns(store.data)) : []))
const bare = (d) => (d.what === 'lab' || d.what === 'cols' ? d.text.match(/\d+/)?.[0] || d.text : d.text)  // «лаба 2» by «лаба» is 2
const origin = computed(() => originLine(p.view))
</script>

<template>
  <div class="vcard shadow border rounded bg-body">
    <div class="head">
      <ViewIcon :view /><b class="text-truncate">{{ view.title }}</b>
      <span v-if="view.etalon" class="star" title="Еталон"><Icon name="starfill" /></span>
    </div>
    <p v-if="view.about" class="about">{{ view.about }}</p>
    <dl v-if="parts.length" class="parts">
      <template v-for="d in parts" :key="d.what">
        <dt>{{ WHAT[d.what] }}</dt>
        <dd :title="d.text">{{ bare(d) }}</dd>
      </template>
    </dl>
    <div v-if="view.folder" class="line"><Icon name="folder" /><span class="text-truncate">{{ view.folder }}</span></div>
    <div v-if="view.tags?.length" class="line"><Icon name="tag" /><span class="text-truncate">{{ view.tags.join(', ') }}</span></div>
    <div v-if="origin" class="line"><Icon name="branch" /><span class="text-truncate">{{ origin }}</span></div>
    <div class="line"><Icon name="clock" /><span class="text-truncate">{{ workLine(view) }}</span></div>
  </div>
</template>

<style scoped>
.vcard { width: 20rem; max-width: calc(100vw - 1rem); padding: .55rem .75rem .6rem; font-size: .82rem; }
.head { display: flex; align-items: center; gap: .4rem; font-size: .92rem; }
.star { color: var(--bs-warning); }
.about { display: -webkit-box; margin: .25rem 0 0; overflow: hidden; -webkit-box-orient: vertical; -webkit-line-clamp: 3; }
.parts { display: grid; grid-template-columns: auto minmax(0, 1fr); gap: .05rem .6rem; align-items: baseline; margin: .45rem 0 .35rem; }
.parts dt { font-size: .72rem; font-weight: 400; color: var(--bs-secondary-color); }
.parts dd { margin: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.line { display: flex; align-items: center; gap: .35rem; min-width: 0; margin-top: .1rem; color: var(--bs-secondary-color); }
</style>
