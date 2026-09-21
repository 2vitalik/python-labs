<script setup>
// width toggle: arrows from a bar outward (`out` — make it wide) or back inward (return to the column)
defineProps({ out: Boolean, size: { type: Number, default: 16 } })
</script>

<template>
  <svg :width="size" :height="size" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"
       stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
    <path d="M8 3v10" />
    <path v-if="out" d="M6 8H1m2.5-2.5L1 8l2.5 2.5M10 8h5m-2.5-2.5L15 8l-2.5 2.5" />
    <path v-else d="M1 8h5M3.5 5.5 6 8l-2.5 2.5M15 8h-5m2.5-2.5L10 8l2.5 2.5" />
  </svg>
</template>
