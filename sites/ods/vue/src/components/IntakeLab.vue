<script setup>
import { vHint } from '@core/hint.js'

import { putIntakeRow } from '../api.js'
import { LAB_NUMS } from '../intake.js'

// which lab a notebook is, picked on the spot: «лаба?» while the site could not tell; or, while the file is not a version
// yet, the lab it read — the very text «Лаба N» with a see-through list laid over it, so it is exactly as wide as the
// text it turns into. A failed save puts the old lab back
const props = defineProps({ id: String, lab: Number, busy: Boolean })
const emit = defineEmits(['act'])
function pick(e) {
  const el = e.target, lab = Number(el.value)
  if (lab) emit('act', () => putIntakeRow(props.id, { lab }).catch((err) => { el.value = props.lab ?? ''; throw err }))
}
</script>

<template>
  <span v-if="lab" v-hint="'не та лаба? — вибери іншу'" class="in-text">Лаба {{ lab }}<select class="over" :value="lab" :disabled="busy"
    aria-label="Яка це лаба" @change="pick"><option v-for="n in LAB_NUMS" :key="n" :value="n">Лаба {{ n }}</option></select></span>
  <select v-else class="form-select form-select-sm lab" value="" :disabled="busy" aria-label="Яка це лаба" @change="pick">
    <option value="">лаба?</option>
    <option v-for="n in LAB_NUMS" :key="n" :value="n">лаба {{ n }}</option>
  </select>
</template>

<style scoped>
.lab { width: auto; height: 1.4rem; min-height: 0; padding: 0 1.6rem 0 .45rem; background-position: right .35rem center; font-size: .78rem; }
.in-text { position: relative; border-bottom: 1px dotted var(--bs-secondary-color); color: var(--bs-body-color); cursor: pointer; }
.in-text:hover { background: var(--bs-tertiary-bg); }
.in-text:has(.over:disabled) { opacity: .5; }
.in-text:has(.over:focus-visible) { outline: 2px solid var(--bs-primary); outline-offset: 1px; }
.over { position: absolute; inset: 0; width: 100%; opacity: 0; cursor: pointer; font: inherit; appearance: none; }
</style>
