<script setup>
import PartLabel from './PartLabel.vue'

// a block inside a card (T284 §4): its caption (PartLabel) and, under it, the block's content shifted right under the
// caption's word — so the eye sees where «Параметри» end and «Механіки» begin. `inline` — short content stays on the
// caption's line (an entity's states); the `after` slot sits right of the caption (a count, a chevron)
defineProps({ icon: String, zone: String, title: String, inline: Boolean })
</script>

<template>
  <div class="pblock" :class="{ inline }">
    <div class="cap"><PartLabel :icon :zone>{{ title }}</PartLabel><slot name="after" /></div>
    <div class="body"><slot /></div>
  </div>
</template>

<style scoped>
/* a card stacks its pieces .5rem apart: a block keeps a little more air above itself */
.pblock { margin-top: .25rem; }
.cap { display: flex; align-items: center; gap: .4rem; }
.body { margin-top: .25rem; padding-left: 1.1rem; }
.body:empty { display: none; }
.inline { display: flex; flex-wrap: wrap; align-items: center; gap: .25rem .5rem; }
.inline > .body { margin: 0; padding: 0; }
</style>
