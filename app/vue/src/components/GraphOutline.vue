<script setup>
import { computed, ref } from 'vue'

import { useEd } from '../ed.js'
import { forest } from '../graphTree.js'
import { jump } from '../jump.js'

// the map of windows top down (T274 §9, T278 §8): a window per row, its children below it, each on a knee into the
// node's middle; «→ menu item» stands over the node, so the nodes of one level line up; «↩ target · item» after the
// node (the mouse over one lights its target, a click goes to its card). A long row wraps, nothing scrolls sideways.
// A click on a node — `pick(id, its element)`: the map puts the panel under it. The colours are the map's (GameGraph)
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
    out.push({ w: byId[id], depth, rails, last, label: label[id], extras: extras[id].map((x) => ({ ...x, title: byId[x.id].title })) })
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
      <span v-if="r.depth" class="knee" :class="{ last: r.last }"><i class="go-tip" /></span>
      <div class="go-body">
        <div v-if="r.depth" class="go-lbl" :title="r.label"><span class="go-arr">→</span> {{ r.label }}</div>
        <div class="go-line">
          <button type="button" class="gg-node go-node" :class="{ lit: lit === r.w.id || open === r.w.id }"
                  @click="emit('pick', r.w.id, $event.currentTarget)">
            {{ r.w.title || '…' }}<span v-if="r.w.screenshots?.length" class="cam">📷</span>
          </button>
          <span v-for="x in r.extras" :key="x.id" class="go-extra" role="button"
                @mouseenter="lit = x.id" @mouseleave="lit = ''" @click="jump(`p-${x.id}`)">↩&#xFE0E; {{ x.title || '…' }}<span v-if="x.label" class="go-via"> · {{ x.label }}</span></span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* --mid: the middle of a node — under its row's padding and its label's line — where a knee turns into it */
.go { --step: 1rem; --pad: .3rem; --lbl: 1rem; --node: 1.6rem; --mid: calc(var(--pad) + var(--lbl) + var(--node) / 2); }
.go-row { display: flex; }
.go-row.root:not(:first-child) { margin-top: .6rem; }
.rail, .knee { flex: 0 0 var(--step); position: relative; }
.rail.on::before, .knee::before, .knee:not(.last)::after { content: ''; position: absolute; left: .45rem; border-left: 1px solid var(--gg-line); }
.rail.on::before, .knee:not(.last)::after { top: 0; bottom: 0; }
/* from under the node above (over its row's bottom padding), past the label, down to the node's middle, then into it */
.knee::before { top: calc(-1 * var(--pad)); height: calc(var(--mid) + var(--pad)); right: 0; border-bottom: 1px solid var(--gg-line); border-bottom-left-radius: 6px; }
.go-tip { position: absolute; right: 0; top: calc(var(--mid) - 4px); border: 3.5px solid transparent; border-right: 0; border-left: 6px solid var(--gg-line); }
.go-body { flex: 1; min-width: 0; padding: var(--pad) 0; }
.go-lbl { height: var(--lbl); line-height: var(--lbl); padding-left: .1rem; font-size: .7rem; font-weight: 500; color: var(--gg-lbl);
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.go-arr { color: var(--gg-line); }
.go-line { display: flex; flex-wrap: wrap; align-items: center; gap: .15rem .45rem; }
.go-node { min-height: var(--node); display: inline-flex; align-items: center; gap: .3rem; max-width: 100%; padding: 0 .5rem; border: 1px solid var(--bs-border-color);
  border-radius: 6px; background: var(--bs-tertiary-bg); color: var(--bs-body-color); font-size: .8rem; line-height: 1.2; text-align: start; overflow-wrap: anywhere; }
.go-node:hover { border-color: var(--bs-secondary-color); }
.go-node.lit { background: var(--bs-warning-bg-subtle); border-color: var(--bs-warning-border-subtle); }
.cam { font-size: .65rem; }
.go-extra { font-size: .68rem; color: var(--bs-secondary-color); cursor: pointer; }
.go-extra:hover { color: var(--bs-body-color); text-decoration: underline; }
.go-via { color: var(--gg-pale); }
</style>
