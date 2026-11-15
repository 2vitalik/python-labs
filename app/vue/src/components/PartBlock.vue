<script setup>
import PartLabel from './PartLabel.vue'

// a block inside a card (T284 §4): its caption (PartLabel) and, under it, the block's content shifted right under the
// caption's word — so the eye sees where «Параметри» end and «Механіки» begin. `inline` — short content stays on the
// caption's line (an entity's states); the `after` slot sits right of the caption (a count, a chevron, a «＋»); an
// explanation put away inside leaves its icon there too (Tip.vue)
defineProps({ pic: String, zone: String, title: String, inline: Boolean })
</script>

<template>
  <div class="pblock" :class="{ inline }" data-dock>
    <div class="cap"><PartLabel :pic :zone>{{ title }}</PartLabel><slot name="after" /><span class="tip-dock" /></div>
    <div class="body"><slot /></div>
  </div>
</template>

<style scoped>
/* a card stacks its pieces .5rem apart: a block keeps a little more air above itself */
.pblock { margin-top: .25rem; }
.cap { display: flex; align-items: center; gap: .4rem; min-height: 1.6rem; }  /* a «＋» beside it changes nothing */
.body { margin-top: .25rem; padding-left: 1.25rem; }  /* the sign (PartLabel .pic) and its gap */
.body:empty { display: none; }
.inline { display: flex; flex-wrap: wrap; align-items: center; gap: .25rem .5rem; }
.inline > .body { margin: 0; padding: 0; }
</style>
