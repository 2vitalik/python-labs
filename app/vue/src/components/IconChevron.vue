<script setup>
// chevron of fold/unfold controls (the ▴▾ glyphs were too small); `dir` down · up · right
const ROT = { down: 0, up: 180, right: -90 }
defineProps({ dir: { type: String, default: 'down' }, size: { type: Number, default: 14 } })
</script>

<template>
  <svg :width="size" :height="size" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2"
       stroke-linecap="round" stroke-linejoin="round" :style="{ transform: `rotate(${ROT[dir]}deg)`, transition: 'transform .15s' }" aria-hidden="true">
    <path d="M3 5.5 8 10.5l5-5" />
  </svg>
</template>
