<script setup>
import { computed, inject, nextTick, ref } from 'vue'

import { flash } from '../anchors.js'
import { useDragSort } from '../dragSort.js'
import { liveViews, load, orderViews, saveView, setFolders, store, viewOf } from '../viewStore.js'
import Icon from './Icon.vue'
import InlineText from './InlineText.vue'
import ViewFolder from './ViewFolder.vue'

// the library in folders (T315 §8): the views in no folder first, then the folders in their order. A view is dragged within
// a folder and between them; its new place is told for all the live views at once (the tabs of /table keep the same order).
// A search hides the folders it finds nothing in; «＋ папка» — a new folder is named right where it will stand
const props = defineProps({ views: { type: Array, required: true }, filtering: Boolean, canDrag: Boolean })
const lib = inject('viewsLib')
const folderOf = (v) => v.folder || ''
const names = computed(() => [...new Set(['', ...store.data.prefs.folders, ...liveViews().map(folderOf)])])
const sections = computed(() => names.value
  .map((name) => ({ name, list: props.views.filter((v) => folderOf(v) === name), total: liveViews().filter((v) => folderOf(v) === name).length }))
  .filter((s) => s.list.length || (!props.filtering && (s.name || names.value.length > 1))))  // «no folder» stays, empty, as a place to drop on

function move(from, to) {
  const zone = (name) => sections.value.find((s) => s.name === name)?.list || []
  const v = zone(from.zone)[from.i]
  const before = zone(to.zone)[to.i]
  const rest = zone(to.zone).filter((x) => x !== v)
  const order = liveViews().map((x) => x.slug).filter((s) => s !== v.slug)
  // before a row · after the folder's last one · at the very end (an empty folder)
  const at = before ? order.indexOf(before.slug) : rest.length ? order.indexOf(rest.at(-1).slug) + 1 : order.length
  order.splice(at, 0, v.slug)
  if (to.zone === from.zone) return lib.act(() => orderViews(order))
  // the row lands at once, in its folder and place; the server hears the folder first, so the order's answer has it
  v.folder = to.zone
  order.forEach((s, i) => (viewOf(s).order = i))
  store.data.views.sort((a, b) => a.order - b.order)
  lib.act(async () => {
    try {
      await saveView(v.slug, { folder: to.zone })
      await orderViews(order)
    } catch (e) {
      load()
      throw e
    }
  })
}
const drag = useDragSort(move)

const adding = ref(false)
async function add(name) {
  await setFolders({ folders: [...store.data.prefs.folders, name] })
  adding.value = false
  await nextTick()
  flash(`folder-${name}`, { near: true })
}
</script>

<template>
  <div class="vfolders">
    <ViewFolder v-for="s in sections" :key="s.name" v-bind="s" :drag :can-drag />
    <div class="vfolders-add">
      <h2 v-if="adding" class="vfolders-new"><Icon name="folder" /><InlineText :save="add" can fresh required placeholder="Назва папки" @drop="adding = false" /></h2>
      <button v-else type="button" class="btn btn-sm btn-add" :disabled="filtering" :title="filtering ? 'Спершу скинь пошук — нова папка порожня, її не буде видно' : 'Нова папка'"
              @click="adding = true"><Icon name="plus" /> папка</button>
    </div>
  </div>
</template>

<style scoped>
.vfolders-add { margin-top: .75rem; }
.vfolders-new { display: flex; align-items: center; gap: .4rem; margin: 0; font-size: 1rem; font-weight: 600; }
.vfolders-new .icon { color: var(--bs-secondary-color); }
</style>
