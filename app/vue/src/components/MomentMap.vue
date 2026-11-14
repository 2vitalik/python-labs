<script setup>
import { makeMapEd } from '../momentMap.js'
import MomentPalette from './MomentPalette.vue'
import MomentResize from './MomentResize.vue'
import MomentTools from './MomentTools.vue'

// «намалювати рівень» (T276 «Те саме студентам»): the level's map in one frame — the brushes of the game's entities, the
// field with its size around it, the brush and the eraser. In and out — the map's text (a level's `props.map`)
const map = defineModel({ type: String, default: '' })
const props = defineProps({ palette: Array })
makeMapEd(map, () => props.palette)
</script>

<template>
  <div class="fit-box vstack gap-2">
    <MomentPalette />
    <div class="d-flex flex-wrap align-items-start gap-3">
      <MomentResize />
      <MomentTools />
    </div>
  </div>
</template>
