<script setup>
import { computed } from 'vue'

import { vHint } from '@core/hint.js'

import { WAYS } from '../labText.js'

// the hint by the levels (T228, GRADE): the level the work reaches capped by the form of defence; «Поставити» hands the
// number to the points field (`put`) — saving stays the teacher's step
const props = defineProps({ grade: { type: Object, default: () => ({}) } })
defineEmits(['put'])
const g = computed(() => props.grade || {})
const ready = computed(() => typeof g.value.hint === 'number')
const wayWords = computed(() => ({ '': 'форму захисту не названо', none: 'без захисту' })[g.value.way ?? ''] ?? `захист ${WAYS[g.value.way]}`)
</script>

<template>
  <div class="group-box">
    <div class="group-cap">Підказка</div>
    <div class="d-flex align-items-center gap-3">
      <span class="hn-big">{{ g.hint ?? '—' }}</span>
      <span class="small">робота — {{ g.work ?? 'ще не 12' }}, {{ wayWords }}<template v-if="g.cap"> — до {{ g.cap }}</template></span>
    </div>
    <span v-hint="ready ? 'вписати в бали — зберігаєш сам' : 'робота ще не сягає рівня 12'" class="d-inline-block mt-1">
      <button type="button" class="btn btn-sm btn-outline-primary" :disabled="!ready" @click="$emit('put', g.hint)">Поставити {{ g.hint ?? '' }}</button>
    </span>
  </div>
</template>

<style scoped>
.hn-big { font-size: 2.2rem; font-weight: 700; line-height: 1; font-variant-numeric: tabular-nums; }
</style>
