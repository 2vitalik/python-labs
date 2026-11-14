<script setup>
import { computed, ref } from 'vue'

import { useCellFit } from '../cellFit.js'
import { parseGrid } from '../momentsText.js'

// a level's map on its card (T276): the cells as the game's moments show them, never wider than the card
const props = defineProps({ text: String })
const grid = computed(() => parseGrid(props.text || ''))
const cols = computed(() => Math.max(1, ...grid.value.map((row) => row.length)))
const root = ref()
const cell = useCellFit(root, cols, { max: 22 })
</script>

<template>
  <div ref="root" class="cells" :style="{ '--cell': `${cell}px` }" role="img" aria-label="мапа рівня">
    <div v-for="(row, r) in grid" :key="r" class="line">
      <span v-for="(c, k) in row" :key="k" class="c" :class="c.mark">{{ c.icon }}</span>
    </div>
  </div>
</template>

<style scoped>
.cells { width: fit-content; padding: .25rem; border: 1px solid var(--bs-border-color); border-radius: .375rem; background: var(--bs-tertiary-bg);
         font-size: calc(var(--cell) * .62); line-height: 1; }
.line { display: flex; }
.c { display: inline-flex; align-items: center; justify-content: center; width: var(--cell); height: var(--cell); flex-shrink: 0; border-radius: .25rem; }
.who { box-shadow: inset 0 0 0 2px var(--bs-primary); }
.new { box-shadow: inset 0 0 0 2px var(--bs-warning); }
</style>
