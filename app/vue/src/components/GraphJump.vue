<script setup>
import Icon from '@core/components/Icon.vue'
import { vPeek } from '@core/peek.js'
import { jump } from '../jump.js'
import GraphVia from './GraphVia.vue'

// a transition the map's tree has no arrow for, in two lines read as a child of its node: «☰ item ↓» over its target —
// a dashed copy of a node with the window's sign, smaller, in that window's colour (T296 §13), right under the caption as a
// child window stands under its own (T301 §6). The mouse over it tells the map which node to light (`over`) and brings the
// window's card; a click goes to the window's own card on the page. x: { id, via, title, tone }; the sizes come from the
// view: --by-h, --by-gap, --ghost-h
defineProps({ x: Object, lit: Boolean })
defineEmits(['over'])
</script>

<template>
  <span class="gjump" @mouseenter="$emit('over', x.id)" @mouseleave="$emit('over', '')">
    <GraphVia :via="x.via" class="by" />
    <span v-peek="{ kind: 'window', id: x.id }" class="ghost gg-w" :class="[x.tone && `tone-${x.tone}`, { lit }]" role="button" @click="jump(`p-${x.id}`)"><Icon name="win" class="wsign" />{{ x.title }}</span>
  </span>
</template>

<style scoped>
.gjump { display: inline-flex; flex-direction: column; align-items: flex-start; min-width: 0; max-width: 100%; }
.by { height: var(--by-h); margin-bottom: var(--by-gap, 0); font-size: var(--by-font, .64rem); line-height: var(--by-h); }
.ghost { max-width: 100%; height: var(--ghost-h); padding: 0 .4rem; overflow: hidden; border: 1px dashed var(--w-line);
         border-radius: 5px; color: var(--w-ink); font-size: var(--ghost-font, .7rem); line-height: calc(var(--ghost-h) - 2px); text-overflow: ellipsis; white-space: nowrap; cursor: pointer; }
.ghost:hover { border-style: solid; }
.wsign { margin-right: .25rem; vertical-align: -.15em; }
.ghost.lit { background: var(--bs-warning-bg-subtle); border-color: var(--bs-warning-border-subtle); }
</style>
