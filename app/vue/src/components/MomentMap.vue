<script setup>
import { makeMapEd } from '../momentMap.js'
import MomentPalette from './MomentPalette.vue'
import MomentResize from './MomentResize.vue'
import MomentTools from './MomentTools.vue'

// «намалювати рівень» (T276 «Те саме студентам»): the level's map in one frame — the tools and the brushes of the game's
// entities right over the field with its size around it (T294 §19). In and out — the map's text (a level's `props.map`)
const map = defineModel({ type: String, default: '' })
const props = defineProps({ palette: Array })
makeMapEd(map, () => props.palette)
</script>

<template>
  <div class="fit-box vstack gap-1">
    <MomentTools />
    <MomentPalette />
    <MomentResize />
  </div>
</template>
