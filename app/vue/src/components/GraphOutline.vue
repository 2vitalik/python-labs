<script setup>
import { computed, ref } from 'vue'

import { useEd } from '../ed.js'
import { forest, viaText } from '../graphTree.js'
import GraphJump from './GraphJump.vue'
import GraphVia from './GraphVia.vue'

// the map of windows top down (T274 §9, T278 §8): a window per row, its children below it a step to the right, so the
// nodes of one level line up. An arrow comes down from its parent and turns into the node; its label — «☰ item»,
// «⚡ rule» — sits in the elbow, by the arrow itself. The other transitions stand after the node (GraphJump): the mouse
// over one lights the real node, and the other way round. A long row wraps, nothing scrolls sideways. A click on a
// node — `pick(id, its element)`: the map puts the panel under it. The colours are the map's (GameGraph)
defineProps({ open: String })
const emit = defineEmits(['pick'])
const ed = useEd()
const lit = ref('')

// rails: for each level between the root and the row, whether a line passes on down there (that ancestor has a next sibling)
const rows = computed(() => {
  const byId = Object.fromEntries(ed.windows.map((w) => [w.id, w]))
  const { roots, kids, extras, via, hub } = forest(ed.windows, ed.menus, ed.rules)
  const out = []
  const walk = (id, depth, rails, last) => {
    out.push({ w: byId[id], depth, rails, last, via: via[id] || [], hub: hub[id],
      extras: extras[id].map((x) => ({ ...x, title: byId[x.id].title || '…', hub: hub[x.id] })) })
    kids[id].forEach((k, i) => walk(k, depth + 1, depth ? [...rails, !last] : [], i === kids[id].length - 1))
  }
  roots.forEach((r) => walk(r, 0, [], true))
  return out
})
const hubOf = (n) => (n ? `hub-${n}` : '')
</script>

<template>
  <div class="go">
    <div v-for="r in rows" :key="r.w.id" class="go-row" :class="{ root: !r.depth }">
      <span v-for="(on, i) in r.rails" :key="i" class="rail" :class="{ on }" />
      <div class="go-body" :class="{ kid: r.depth, more: r.depth && !r.last }">
        <div class="go-main">
          <template v-if="r.depth">
            <span class="knee"><i class="go-tip" /></span>
            <GraphVia :via="r.via" class="go-lbl" :title="viaText(r.via)" />
          </template>
          <button type="button" class="gg-node go-node" :class="[hubOf(r.hub), { lit: lit === r.w.id || open === r.w.id }]"
                  @mouseenter="lit = r.w.id" @mouseleave="lit = ''" @click="emit('pick', r.w.id, $event.currentTarget)">
            {{ r.w.title || '…' }}<span v-if="r.w.screenshots?.length" class="cam">📷</span>
          </button>
        </div>
        <GraphJump v-for="x in r.extras" :key="x.id" :x :lit="lit === x.id" @over="lit = $event" />
      </div>
    </div>
  </div>
</template>

<style scoped>
/* --step: a level's shift right, the length of an arrow's last stretch; --rx: where in the step the line comes down */
.go { --step: 2.4rem; --rx: .85rem; --pad: .3rem; --lbl: 1.05rem; --node: 1.6rem;
  --by-h: var(--lbl); --ghost-h: 1.3rem; --ghost-my: calc((var(--node) - var(--ghost-h)) / 2); }
@media (max-width: 575px) { .go { --step: 1.5rem; --rx: .55rem; } }
.go-row { display: flex; }
.go-row.root:not(:first-child) { margin-top: .6rem; }
.rail { flex: 0 0 var(--step); position: relative; }
.rail.on::before, .go-body.more::before, .knee::before { content: ''; position: absolute; left: var(--rx); border-left: 1px solid var(--gg-line); }
.rail.on::before, .go-body.more::before { top: 0; bottom: 0; }
/* the node with its arrow, then the extras; a wrapped line of extras starts under the node, clear of the line going down */
.go-body { position: relative; flex: 1; min-width: 0; display: flex; flex-wrap: wrap; align-items: flex-end; gap: .25rem 1rem; padding: var(--pad) 0; }
.go-body.kid { padding-left: var(--step); }
.go-main { display: grid; min-width: 0; max-width: 100%; }
.kid > .go-main { grid-template: var(--lbl) auto / var(--step) minmax(0, auto); margin-left: calc(-1 * var(--step)); }
/* from under the node above (over the row's top padding) down to the node's middle, then into it */
.knee { grid-area: 1 / 1 / 3 / 2; position: relative; }
.knee::before { top: calc(-1 * var(--pad)); height: calc(var(--pad) + var(--lbl) + var(--node) / 2); right: 0; border-bottom: 1px solid var(--gg-line); border-bottom-left-radius: 7px; }
.go-tip { position: absolute; right: 0; top: calc(var(--lbl) + var(--node) / 2 - 4px); border: 3.5px solid transparent; border-right: 0; border-left: 6px solid var(--gg-line); }
.go-lbl { grid-area: 1 / 1 / 2 / 3; padding-left: calc(var(--rx) + .4rem); line-height: var(--lbl); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.go-node { justify-self: start; min-height: var(--node); display: inline-flex; align-items: center; gap: .3rem; max-width: 100%; padding: 0 .55rem;
  border: 1px solid var(--w-line); border-radius: 6px; background: var(--w-bg); color: var(--bs-body-color); font-size: .8rem; line-height: 1.2; text-align: start; overflow-wrap: anywhere; }
.kid > .go-main > .go-node { grid-area: 2 / 2; }
.go-node:hover { border-color: var(--w-ink); }
.go-node.lit { background: var(--bs-warning-bg-subtle); border-color: var(--bs-warning-border-subtle); }
.cam { font-size: .65rem; }
</style>
