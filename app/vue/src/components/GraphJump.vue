<script setup>
import { viaText } from '../graphTree.js'
import { jump } from '../jump.js'
import GraphVia from './GraphVia.vue'

// a transition the map's tree has no arrow for, in two lines: «☰ item →» over its target — a dashed copy of a node, in
// that window's colour. The mouse over it tells the map which node to light (`over`), a click goes to the window's card.
// x: { id, via, title, hub }; the sizes come from the view: --by-h, --ghost-h, --ghost-my
defineProps({ x: Object, lit: Boolean })
defineEmits(['over'])
</script>

<template>
  <span class="gjump" role="button" :title="`${[viaText(x.via), x.title].filter(Boolean).join(' → ')} — показати вікно`"
        @mouseenter="$emit('over', x.id)" @mouseleave="$emit('over', '')" @click="jump(`p-${x.id}`)">
    <span class="by"><GraphVia :via="x.via" /><span class="arr"> →</span></span>
    <span class="ghost" :class="[x.hub && `hub-${x.hub}`, { lit }]">{{ x.title }}</span>
  </span>
</template>

<style scoped>
.gjump { display: inline-flex; flex-direction: column; align-items: flex-start; min-width: 0; max-width: 100%; cursor: pointer; }
.by, .ghost { max-width: 100%; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.by { height: var(--by-h); line-height: var(--by-h); }
.arr { font-size: .7rem; color: var(--gg-line); }
.ghost { height: var(--ghost-h); line-height: calc(var(--ghost-h) - 2px); margin: var(--ghost-my, 0) 0; padding: 0 .45rem; border: 1px dashed var(--w-line); border-radius: 6px;
         color: var(--w-ink); font-size: .74rem; }
.gjump:hover .ghost { border-style: solid; }
.ghost.lit { background: var(--bs-warning-bg-subtle); border-color: var(--bs-warning-border-subtle); }
</style>
