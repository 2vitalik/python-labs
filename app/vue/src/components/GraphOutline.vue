<script setup>
import { computed, ref } from 'vue'

import { useEd } from '../ed.js'
import { forest } from '../graphTree.js'
import { jump } from '../jump.js'

// the map of windows top down (T274 §9): a window per row, its children below it, each on a knee that carries the menu
// item; «↩ target» after the node (the mouse over one lights its target, a click goes to its card). A long row wraps,
// nothing scrolls sideways. A click on a node — `pick(id, its element)`: the map puts the panel under it
defineProps({ open: String })
const emit = defineEmits(['pick'])
const ed = useEd()
const lit = ref('')

// rails: for each level between the root and the row, whether a line passes on down there (that ancestor has a next sibling)
const rows = computed(() => {
  const byId = Object.fromEntries(ed.windows.map((w) => [w.id, w]))
  const { roots, kids, extras, label } = forest(ed.windows, ed.menus, ed.rules)
  const out = []
  const walk = (id, depth, rails, last) => {
    out.push({ w: byId[id], depth, rails, last, label: label[id], extras: extras[id].map((x) => byId[x]) })
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
      <span v-if="r.depth" class="knee" :class="{ last: r.last }" />
      <div class="go-body">
        <span v-if="r.depth" class="go-lbl">{{ r.label }}
          <svg width="16" height="8" viewBox="0 0 16 8" class="go-arr flex-shrink-0"><path d="M0 4H11" /><path d="M9 .5L15.5 4L9 7.5z" class="tip" /></svg>
        </span>
        <button type="button" class="gg-node go-node" :class="{ lit: lit === r.w.id || open === r.w.id }"
                @click="emit('pick', r.w.id, $event.currentTarget)">
          {{ r.w.title || '…' }}<span v-if="r.w.screenshots?.length" class="cam">📷</span>
        </button>
        <span v-for="x in r.extras" :key="x.id" class="go-extra" role="button"
              @mouseenter="lit = x.id" @mouseleave="lit = ''" @click="jump(`p-${x.id}`)">↩&#xFE0E; {{ x.title || '…' }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* --mid: the middle of a row's first line (its padding + half the node), where a knee turns right */
.go { --gg-line: color-mix(in srgb, var(--bs-body-color) 35%, var(--bs-body-bg)); --step: 1rem; --pad: .2rem; --mid: calc(var(--pad) + .8rem); }
.go-row { display: flex; }
.go-row.root:not(:first-child) { margin-top: .6rem; }
.rail, .knee { flex: 0 0 var(--step); position: relative; }
.rail.on::before, .knee::before, .knee:not(.last)::after { content: ''; position: absolute; left: .45rem; border-left: 1px solid var(--gg-line); }
.rail.on::before, .knee:not(.last)::after { top: 0; bottom: 0; }
/* from under the node above (over its row's bottom padding) down to the middle, then right */
.knee::before { top: calc(-1 * var(--pad)); height: calc(var(--mid) + var(--pad)); right: 0; border-bottom: 1px solid var(--gg-line); border-bottom-left-radius: 6px; }
.go-body { flex: 1; min-width: 0; display: flex; flex-wrap: wrap; align-items: center; gap: .15rem .45rem; padding: var(--pad) 0; }
/* as tall as a node: alone on a wrapped line, it still meets its knee in the middle */
.go-lbl { min-height: 1.6rem; display: inline-flex; align-items: center; gap: .25rem; margin-left: .2rem; font-size: .7rem; color: var(--bs-secondary-color); }
.go-arr path { fill: none; stroke: var(--gg-line); stroke-width: 1.3; }
.go-arr .tip { fill: var(--gg-line); stroke: none; }
.go-node { min-height: 1.6rem; display: inline-flex; align-items: center; gap: .3rem; max-width: 100%; padding: 0 .5rem; border: 1px solid var(--bs-border-color);
  border-radius: 6px; background: var(--bs-tertiary-bg); color: var(--bs-body-color); font-size: .8rem; line-height: 1.2; text-align: start; overflow-wrap: anywhere; }
.go-node:hover { border-color: var(--bs-secondary-color); }
.go-node.lit { background: var(--bs-warning-bg-subtle); border-color: var(--bs-warning-border-subtle); }
.cam { font-size: .65rem; }
.go-extra { font-size: .68rem; color: var(--bs-secondary-color); cursor: pointer; }
.go-extra:hover { color: var(--bs-body-color); text-decoration: underline; }
</style>
