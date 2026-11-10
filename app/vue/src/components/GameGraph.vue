<script setup>
import { computed, ref } from 'vue'

import { useEd } from '../ed.js'
import { BOX_H, EXTRA_H, layout } from '../graphLayout.js'
import { jump } from '../jump.js'
import GraphPanel from './GraphPanel.vue'

// the map of windows (T270 §10.4): a tree from the root, menu items as labelled arrows; the other transitions are
// «↩ target» lines under a node (the mouse over one lights its target, a click goes to its card); a node opens its panel
const ed = useEd()
const g = computed(() => layout(ed.windows, ed.menus, ed.rules))
const still = computed(() => !g.value.edges.length && !g.value.nodes.some((n) => n.extras.length))
const box = ref()
const lit = ref('')  // the node an «↩» line under the mouse points at
const at = ref(null)  // the open panel: { id, left, top } over the map, so it is placed outside the scrolling box
const win = computed(() => at.value && ed.windows.find((w) => w.id === at.value.id))
const titleOf = (id) => ed.windows.find((w) => w.id === id)?.title

function toggle(n) {
  at.value = at.value?.id === n.id ? null : { id: n.id, left: n.x - box.value.scrollLeft, top: n.y + BOX_H + 4 }
}
</script>

<template>
  <div class="graph">
    <div ref="box" class="overflow-x-auto" @scroll="at = null">
      <svg :width="g.width" :height="g.height" class="d-block">
        <defs>
          <marker id="gg-arrow" viewBox="0 0 8 8" refX="8" refY="4" markerWidth="7" markerHeight="7" orient="auto">
            <path d="M0 0L8 4L0 8z" class="tip" />
          </marker>
        </defs>
        <path v-for="e in g.edges" :key="e.to" :d="e.d" class="edge" marker-end="url(#gg-arrow)" />
        <text v-for="e in g.edges" :key="`l${e.to}`" :x="e.lx" :y="e.ly" text-anchor="end" class="lbl">{{ e.label }}</text>
        <template v-for="n in g.nodes" :key="n.id">
          <g class="gg-node" :class="{ lit: lit === n.id || at?.id === n.id }" role="button" @click="toggle(n)">
            <title>{{ titleOf(n.id) }}</title>
            <rect :x="n.x + .5" :y="n.y + .5" :width="n.w - 1" :height="BOX_H - 1" rx="6" />
            <text :x="n.x + 10" :y="n.y + BOX_H / 2" dominant-baseline="central" class="ttl">{{ n.title }}</text>
            <text v-if="n.shot" :x="n.x + n.w - 7" :y="n.y + BOX_H / 2" dominant-baseline="central" text-anchor="end" class="cam">📷</text>
          </g>
          <text v-for="(x, i) in n.extras" :key="x.id" :x="n.x + 4" :y="n.y + BOX_H + 11 + i * EXTRA_H" class="extra" role="button"
                @mouseenter="lit = x.id" @mouseleave="lit = ''" @click="jump(`p-${x.id}`)">↩&#xFE0E; {{ x.title }}</text>
        </template>
      </svg>
    </div>
    <GraphPanel v-if="win" :win :style="{ left: `max(0px, min(${at.left}px, 100% - 18rem))`, top: `${at.top}px` }" @close="at = null" />
    <div v-if="still" class="small text-secondary">Стрілки зʼявляться, коли пункти меню вестимуть до інших вікон</div>
  </div>
</template>

<style scoped>
.graph { position: relative; --gg-line: color-mix(in srgb, var(--bs-body-color) 35%, var(--bs-body-bg)); }
.edge { fill: none; stroke: var(--gg-line); stroke-width: 1.3; }
.tip { fill: var(--gg-line); }
/* a halo in the page colour under a label: a line passing below never cuts a word */
.lbl { font-size: .7rem; fill: var(--bs-secondary-color); paint-order: stroke; stroke: var(--bs-body-bg); stroke-width: 4px; stroke-linejoin: round; }
.gg-node { cursor: pointer; }
.gg-node rect { fill: var(--bs-tertiary-bg); stroke: var(--bs-border-color); }
.gg-node:hover rect { stroke: var(--bs-secondary-color); }
.gg-node.lit rect { fill: var(--bs-warning-bg-subtle); stroke: var(--bs-warning-border-subtle); }
.ttl { font-size: .8rem; fill: var(--bs-body-color); }
.cam { font-size: .65rem; }
.extra { font-size: .68rem; fill: var(--bs-secondary-color); cursor: pointer; }
.extra:hover { fill: var(--bs-body-color); text-decoration: underline; }
</style>
