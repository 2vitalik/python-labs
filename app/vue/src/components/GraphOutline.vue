<script setup>
import { computed, ref } from 'vue'

import { useEd } from '../ed.js'
import { forest, toneOf } from '../graphTree.js'
import { useJumps } from '../windowJumps.js'
import GraphJump from './GraphJump.vue'
import GraphNode from './GraphNode.vue'
import GraphVia from './GraphVia.vue'

// the map of windows top down (T274 §9, T284 §1): a window per row, its children below it a step to the right, so the
// nodes of one level line up. An arrow comes down from its parent and turns into the node; its label — «☰ item →» —
// stands over the node, from its left edge. The other transitions stand right of the node's box and are as tall as the
// box itself (GraphJump, in a smaller type): the mouse over one lights the real node, and the other way round. A long
// row wraps, nothing scrolls sideways. The colours are the map's (GameGraph)
const ed = useEd()
const jumps = useJumps()
const lit = ref('')

// rails: for each level between the root and the row, whether a line passes on down there (that ancestor has a next sibling)
const rows = computed(() => {
  const byId = Object.fromEntries(ed.windows.map((w) => [w.id, w]))
  const { roots, kids, extras, via } = forest(ed.windows, ed.menus, jumps.value)
  const out = []
  const walk = (id, depth, rails, last) => {
    const w = byId[id]
    out.push({ w, depth, rails, last, via: via[id] || [], tone: toneOf(w),
      extras: extras[id].map((x) => ({ ...x, title: byId[x.id].title || '…', tone: toneOf(byId[x.id]) })) })
    kids[id].forEach((k, i) => walk(k, depth + 1, depth ? [...rails, !last] : [], i === kids[id].length - 1))
  }
  roots.forEach((r) => walk(r, 0, [], true))
  return out
})
</script>

<template>
  <div class="go">
    <div v-for="r in rows" :key="r.w.id" class="go-row" :class="{ root: !r.depth }">
      <span v-for="(on, i) in r.rails" :key="i" class="rail" :class="{ on }" />
      <div class="go-body" :class="{ kid: r.depth, more: r.depth && !r.last }">
        <div class="go-main">
          <template v-if="r.depth">
            <span class="knee"><i class="go-tip" /></span>
            <span class="go-lbl"><GraphVia :via="r.via" /></span>
          </template>
          <GraphNode :id="r.w.id" :title="r.w.title || '…'" :shot="!!r.w.screenshots?.length" :tone="r.tone" :lit="lit === r.w.id" class="go-node"
                     @mouseenter="lit = r.w.id" @mouseleave="lit = ''" />
        </div>
        <GraphJump v-for="x in r.extras" :key="x.id" :x :lit="lit === x.id" @over="lit = $event" />
      </div>
    </div>
  </div>
</template>

<style scoped>
/* --step: a level's shift right, the length of an arrow's last stretch; --rx: where in the step the line comes down;
   an extra's two lines and the gap between them make --node: 12 + 1 + 17 */
.go { --step: 2.4rem; --rx: .85rem; --pad: .3rem; --lbl: 1.05rem; --node: 30px;
  --by-h: 12px; --by-gap: 1px; --ghost-h: 17px; --ghost-dx: 8px; --by-font: .62rem; --ghost-font: .68rem; }
@media (max-width: 575px) { .go { --step: 1.5rem; --rx: .55rem; } }
.go-row { display: flex; }
.go-row.root:not(:first-child) { margin-top: .6rem; }
.go-row:first-child { padding-right: 10.5rem; }  /* the view switch hangs over this corner */
.rail { flex: 0 0 var(--step); position: relative; }
.rail.on::before, .go-body.more::before, .knee::before { content: ''; position: absolute; left: var(--rx); border-left: 1px solid var(--gg-line); }
.rail.on::before, .go-body.more::before { top: 0; bottom: 0; }
/* the node with its arrow, then the extras beside its box; a wrapped line of extras starts under the node, clear of the line going down */
.go-body { position: relative; flex: 1; min-width: 0; display: flex; flex-wrap: wrap; align-items: flex-end; gap: .3rem .8rem; padding: var(--pad) 0; }
.go-body.kid { padding-left: var(--step); }
.go-main { display: grid; min-width: 0; max-width: 100%; }
.kid > .go-main { grid-template: var(--lbl) auto / var(--step) minmax(0, auto); margin-left: calc(-1 * var(--step)); }
/* from under the node above (over the row's top padding) down to the node's middle, then into it */
.knee { grid-area: 1 / 1 / 3 / 2; position: relative; }
.knee::before { top: calc(-1 * var(--pad)); height: calc(var(--pad) + var(--lbl) + var(--node) / 2); right: 0; border-bottom: 1px solid var(--gg-line); border-bottom-left-radius: 7px; }
.go-tip { position: absolute; right: 0; top: calc(var(--lbl) + var(--node) / 2 - 4px); border: 3.5px solid transparent; border-right: 0; border-left: 6px solid var(--gg-line); }
/* the label takes no width of its own: a long one runs on over the extras' row instead of pushing them away from the box */
.go-lbl { grid-area: 1 / 2; width: 0; padding-left: 2px; font-size: .7rem; line-height: var(--lbl); }
.go-lbl > * { max-width: min(24rem, 60vw); }
.go-node { justify-self: start; height: var(--node); }
.kid > .go-main > .go-node { grid-area: 2 / 2; }
</style>
