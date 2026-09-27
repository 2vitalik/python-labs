<script setup>
import { computed } from 'vue'

import { dayMonth } from '../activity.js'

// a bar per day, oldest first, today in the accent. Heights go by square root against a maximum shared by the whole table:
// rows stay comparable, and a day with one action is still visible next to a day with a hundred
const props = defineProps({ values: Array, days: Array, max: Number })
const W = 4
const GAP = 2
const H = 20
const bars = computed(() => props.values.map((n, i) => ({
  n, x: i * (W + GAP), h: n ? Math.max(2, Math.sqrt(n / props.max) * H) : 0, title: `${dayMonth(props.days[i])} · ${n}`,
})))
const total = computed(() => props.values.reduce((a, b) => a + b, 0))
</script>

<template>
  <svg :width="bars.length * (W + GAP) - GAP" :height="H + 1" role="img" :aria-label="`Дій за ${bars.length} днів: ${total}`">
    <g v-for="(b, i) in bars" :key="i">
      <title>{{ b.title }}</title>
      <rect :x="b.x" y="0" :width="W + GAP" :height="H + 1" fill="transparent" />
      <rect v-if="b.n" :x="b.x" :y="H - b.h" :width="W" :height="b.h" rx="1" :class="i === bars.length - 1 ? 'today' : 'day'" />
      <rect v-else :x="b.x" :y="H" :width="W" height="1" class="none" />
    </g>
  </svg>
</template>

<style scoped>
svg { display: block; }
.day { fill: var(--bs-gray-500); }
.today { fill: var(--bs-primary); }
.none { fill: var(--bs-border-color); }
</style>
