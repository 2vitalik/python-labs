<script setup>
import { useTable } from '../tableCtx.js'
import DateChip from './DateChip.vue'

// which lab «this lab» of the view is: the labs in rows with their deadline (the one for everyone, else the first), the
// current one lit; a click turns the view to that lab
const emit = defineEmits(['done'])
const t = useTable()
const due = (l) => (l.deadlines.find((d) => !d.groups?.length) || l.deadlines[0])?.at
function pick(n) {
  t.set({ lab: n })
  emit('done')
}
</script>

<template>
  <div>
    <button v-for="l in t.data.labs" :key="l.n" type="button" class="sl-row" :class="{ on: l.n === t.state.lab }" @click="pick(l.n)">
      <span>Лаба {{ l.n }}</span>
      <template v-if="due(l)"><span class="sl-due">дедлайн</span><DateChip :at="due(l)" /></template>
    </button>
  </div>
</template>

<style scoped>
.sl-row { display: flex; align-items: center; gap: .4rem; width: 100%; padding: .25rem .45rem; border: 0; border-radius: .3rem; background: none; color: inherit; text-align: start; }
.sl-row:hover { background: var(--bs-tertiary-bg); }
.sl-row.on { background: color-mix(in srgb, var(--bs-primary) 12%, transparent); font-weight: 600; }
.sl-due { margin-left: auto; color: var(--bs-secondary-color); font-size: .75rem; font-weight: 400; }
</style>
