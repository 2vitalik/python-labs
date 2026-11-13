<script setup>
import { computed, ref } from 'vue'

import { useEd } from '../ed.js'
import { BOX_H, layout } from '../graphLayout.js'
import GraphJump from './GraphJump.vue'

// the map of windows left to right (graphLayout): the arrows and the nodes are drawn, an arrow's label — «☰ item»,
// «⚡ rule» — in its elbow; the other transitions are HTML blocks laid under their node (GraphJump). It scrolls sideways
// in its box. A click on a node — `pick(id, left, top)`: where the map hangs the panel. The colours are the map's (GameGraph)
defineProps({ open: String })
const emit = defineEmits(['pick', 'moved'])
const ed = useEd()
const g = computed(() => layout(ed.windows, ed.menus, ed.rules))
const labelled = computed(() => g.value.edges.filter((e) => e.full))
const box = ref()
const lit = ref('')  // the window under the mouse — its node, or a mention of it under another node: both light up
const titleOf = (id) => ed.windows.find((w) => w.id === id)?.title || '…'
const ham = (x, y) => `M${x} ${y - 7.5}h8M${x} ${y - 4.5}h8M${x} ${y - 1.5}h8`  // «☰» before a label whose baseline is y
const hubOf = (n) => (n ? `hub-${n}` : '')
const pick = (n) => emit('pick', n.id, box.value.offsetLeft + n.x - box.value.scrollLeft, box.value.offsetTop + n.y + BOX_H + 4)
</script>

<template>
  <div ref="box" class="overflow-x-auto" @scroll="emit('moved')">
    <div class="wide" :style="{ width: `${g.width}px` }">
      <svg :width="g.width" :height="g.height" class="d-block">
        <defs>
          <marker id="gg-arrow" viewBox="0 0 8 8" refX="8" refY="4" markerWidth="7" markerHeight="7" orient="auto">
            <path d="M0 0L8 4L0 8z" class="tip" />
          </marker>
        </defs>
        <path v-for="e in g.edges" :key="e.to" :d="e.d" class="edge" marker-end="url(#gg-arrow)" />
        <g v-for="e in labelled" :key="`l${e.to}`" class="lbl">
          <title>{{ e.full }}</title>
          <path v-if="e.item" :d="ham(e.lx, e.ly)" class="ham" />
          <text :x="e.lx + (e.item ? 12 : 0)" :y="e.ly">{{ e.item }}<tspan v-if="e.rule" class="by-rule">{{ e.item ? ' ' : '' }}⚡&#xFE0E; {{ e.rule }}</tspan></text>
        </g>
        <g v-for="n in g.nodes" :key="n.id" class="gg-node" :class="[hubOf(n.hub), { lit: lit === n.id || open === n.id }]" role="button"
           @mouseenter="lit = n.id" @mouseleave="lit = ''" @click="pick(n)">
          <title>{{ titleOf(n.id) }}</title>
          <rect :x="n.x + .5" :y="n.y + .5" :width="n.w - 1" :height="BOX_H - 1" rx="6" />
          <text :x="n.x + 10" :y="n.y + BOX_H / 2" dominant-baseline="central" class="ttl">{{ n.title }}</text>
          <text v-if="n.shot" :x="n.x + n.w - 7" :y="n.y + BOX_H / 2" dominant-baseline="central" text-anchor="end" class="cam">📷</text>
        </g>
      </svg>
      <template v-for="n in g.nodes" :key="n.id">
        <div v-if="n.extras.length" class="jumps" :style="{ left: `${n.x + 2}px`, top: `${n.y + BOX_H + 2}px`, width: `${n.ew - 2}px` }">
          <GraphJump v-for="x in n.extras" :key="x.id" :x :lit="lit === x.id" @over="lit = $event" />
        </div>
      </template>
    </div>
  </div>
</template>

<style scoped>
.edge { fill: none; stroke: var(--gg-line); stroke-width: 1.3; }
.tip { fill: var(--gg-line); }
.lbl text { font-size: .7rem; font-weight: 500; fill: var(--gg-item); }
.ham { fill: none; stroke: var(--gg-item); stroke-width: 1.4; stroke-linecap: round; }
.lbl .by-rule { fill: var(--gg-rule); }
.gg-node { cursor: pointer; }
.gg-node rect { fill: var(--w-bg); stroke: var(--w-line); }
.gg-node:hover rect { stroke: var(--w-ink); }
.gg-node.lit rect { fill: var(--bs-warning-bg-subtle); stroke: var(--bs-warning-border-subtle); }
.ttl { font-size: .8rem; fill: var(--bs-body-color); }
.cam { font-size: .65rem; }
/* the extras over the drawing, EXTRA_H each (graphLayout): 14 + 18 and the gap */
.wide { position: relative; --by-h: 14px; --ghost-h: 18px; }
.jumps { position: absolute; display: flex; flex-direction: column; align-items: flex-start; gap: 2px; }
</style>
