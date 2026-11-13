<script setup>
import { computed, onMounted, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import { load, save } from '@core/local.js'
import { zones } from '../catalog.js'
import { useEd } from '../ed.js'
import { layout } from '../graphLayout.js'
import { forest } from '../graphTree.js'
import GraphOutline from './GraphOutline.vue'
import GraphPanel from './GraphPanel.vue'
import GraphWide from './GraphWide.vue'

// the map of windows (T270 §10.4, T274 §9, T278 §8): a tree from the root, «вшир» — left to right (GraphWide), «вглиб» —
// top down in rows (GraphOutline). Two colours tell what is what: a window is blue, what leads to one — «☰ item» of
// «Переходи й дії» — is orange, «⚡ rule» violet; an arrow's label sits in its elbow. The transitions the tree has no
// arrow for stand by their node, «☰ item →» over the window in a dashed frame (GraphJump). A window many of them lead
// to is a hub with a colour of its own, and so are the mentions of it. A node opens its panel
const ed = useEd()
const still = computed(() => {
  const { kids, extras } = forest(ed.windows, ed.menus, ed.rules)
  return ![...Object.values(kids), ...Object.values(extras)].some((list) => list.length)
})
const hues = computed(() => ({ '--gg-win': zones.value.interface?.color, '--gg-by-rule': zones.value['game-logic']?.color }))
const root = ref()
const mode = ref(load('graph-mode'))  // 'wide' | 'deep'; not chosen yet — «вшир» if it fits without scrolling sideways
const at = ref(null)  // the open panel: { id, left, top } over the map, so it is placed outside the scrolling box
const win = computed(() => at.value && ed.windows.find((w) => w.id === at.value.id))

onMounted(() => {
  const room = root.value.clientWidth || window.innerWidth
  mode.value ||= room < 700 || layout(ed.windows, ed.menus, ed.rules).width > room ? 'deep' : 'wide'
})
function choose(m) {
  mode.value = m
  save('graph-mode', m)
  at.value = null
}
const place = (id, left, top) => (at.value = at.value?.id === id ? null : { id, left, top })
const under = (id, el) => place(id, el.offsetLeft, el.offsetTop + el.offsetHeight + 4)
</script>

<template>
  <div ref="root" class="graph" :style="hues">
    <div v-if="!still" class="d-flex justify-content-end mb-1">
      <div class="btn-group btn-group-sm" role="group" aria-label="вигляд схеми">
        <button type="button" class="btn btn-outline-secondary" :class="{ active: mode === 'wide' }" @click="choose('wide')"><Icon name="right" /> вшир</button>
        <button type="button" class="btn btn-outline-secondary" :class="{ active: mode === 'deep' }" @click="choose('deep')"><Icon name="down" /> вглиб</button>
      </div>
    </div>
    <GraphOutline v-if="mode === 'deep'" :open="at?.id" @pick="under" />
    <GraphWide v-else-if="mode" :open="at?.id" @pick="place" @moved="at = null" />
    <GraphPanel v-if="win" :win :style="{ left: `max(0px, min(${at.left}px, 100% - 18rem))`, top: `${at.top}px` }" @close="at = null" />
    <div v-if="still" class="small text-secondary">Стрілки зʼявляться, коли переходи вестимуть до інших вікон</div>
    <div v-else class="legend">
      <span><Icon name="menu" class="by-item" /> пункт із «Переходів і дій»</span>
      <span><span class="by-rule">⚡&#xFE0E;</span> перехід за правилом</span>
      <span><span class="ghost">вікно</span> — перехід до вікна, що вже є на схемі</span>
    </div>
  </div>
</template>

<style scoped>
/* both views. --w: a window's hue — the map's blue, or a hub's own; the box, its frame and its name's ink come from it */
.graph { position: relative; --gg-line: color-mix(in srgb, var(--bs-body-color) 35%, var(--bs-body-bg));
  --gg-win: #0288d1; --gg-by-rule: #8e24aa; --gg-item: color-mix(in srgb, #e8590c 82%, var(--bs-body-color));
  --gg-rule: color-mix(in srgb, var(--gg-by-rule) 78%, var(--bs-body-color)); --w: var(--gg-win); }
.graph, .graph :deep([class*=hub-]) { --w-bg: color-mix(in srgb, var(--w) 9%, var(--bs-body-bg)); --w-line: color-mix(in srgb, var(--w) 50%, var(--bs-body-bg));
  --w-ink: color-mix(in srgb, var(--w) 72%, var(--bs-body-color)); }
.graph :deep(.hub-1) { --w: #0f9d76; }
.graph :deep(.hub-2) { --w: #d6336c; }
.graph :deep(.hub-3) { --w: #8d6e63; }
.legend { display: flex; flex-wrap: wrap; gap: .1rem 1rem; margin-top: .5rem; font-size: .7rem; color: var(--bs-secondary-color); }
.legend .by-item { color: var(--gg-item); }
.legend .by-rule { color: var(--gg-rule); }
.legend .ghost { padding: 0 .3rem; border: 1px dashed var(--w-line); border-radius: 5px; color: var(--w-ink); }
</style>
