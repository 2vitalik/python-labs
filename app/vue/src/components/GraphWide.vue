<script setup>
import { computed, ref } from 'vue'

import { useEd } from '../ed.js'
import { BOX_H, cornerFree, EXTRA_DX, layout } from '../graphLayout.js'
import { useJumps } from '../windowJumps.js'
import GraphJump from './GraphJump.vue'
import GraphNode from './GraphNode.vue'
import GraphVia from './GraphVia.vue'

// the map of windows left to right (graphLayout): the arrows are drawn, the nodes, the labels over them and the other
// transitions under them are HTML laid over the drawing at the layout's places. It scrolls sideways in its box.
// The view switch hangs over its top left corner: when the tree takes that corner, the map steps down a row.
// The colours are the map's (GameGraph)
const ed = useEd()
const jumps = useJumps()
const g = computed(() => layout(ed.windows, ed.menus, jumps.value))
const top = computed(() => (cornerFree(g.value, 170, 38) ? 0 : 36))
const lit = ref('')  // the window under the mouse — its node, or a mention of it under another node: both light up
const px = (o) => Object.fromEntries(Object.entries(o).map(([k, v]) => [k, `${v}px`]))
</script>

<template>
  <div class="overflow-x-auto" :style="{ paddingTop: `${top}px` }">
    <div class="wide" :style="px({ width: g.width, height: g.height })">
      <svg :width="g.width" :height="g.height" class="d-block">
        <defs>
          <marker id="gg-arrow" viewBox="0 0 8 8" refX="8" refY="4" markerWidth="7" markerHeight="7" orient="auto">
            <path d="M0 0L8 4L0 8z" class="tip" />
          </marker>
        </defs>
        <path v-for="e in g.edges" :key="e.to" :d="e.d" class="edge" marker-end="url(#gg-arrow)" />
      </svg>
      <GraphVia v-for="e in g.edges.filter((x) => x.via.length)" :key="`l${e.to}`" :via="e.via" class="lbl" :style="px({ left: e.lx, top: e.ly, maxWidth: e.lw })" />
      <template v-for="n in g.nodes" :key="n.id">
        <GraphNode v-bind="n" :lit="lit === n.id" class="node" :style="px({ left: n.x, top: n.y, width: n.w, height: BOX_H })"
                   @mouseenter="lit = n.id" @mouseleave="lit = ''" />
        <div v-if="n.extras.length" class="jumps" :style="px({ left: n.x + EXTRA_DX, top: n.y + BOX_H + 4, width: n.ew - EXTRA_DX })">
          <GraphJump v-for="x in n.extras" :key="x.id" :x :lit="lit === x.id" @over="lit = $event" />
        </div>
      </template>
    </div>
  </div>
</template>

<style scoped>
.edge { fill: none; stroke: var(--gg-line); stroke-width: 1.3; }
.tip { fill: var(--gg-line); }
/* an extra is EXTRA_H (graphLayout): 13 + 2 + 17 and the gap of 6; the frame GHOST_DX further right */
.wide { position: relative; --by-h: 13px; --by-gap: 2px; --ghost-h: 17px; --ghost-dx: 10px; }
.lbl, .node, .jumps { position: absolute; }
.lbl { height: 16px; font-size: .7rem; line-height: 16px; }
.jumps { display: flex; flex-direction: column; align-items: flex-start; gap: 6px; }
</style>
