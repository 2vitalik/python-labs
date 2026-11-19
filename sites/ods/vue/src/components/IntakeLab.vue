<script setup>
import { vHint } from '@core/hint.js'

import { putIntakeRow } from '../api.js'
import { LAB_NUMS } from '../intake.js'

// which lab a notebook is, picked on the spot: «лаба?» while the site could not tell; or the lab it read, while the
// file is not a version yet — a word like the text around it and as wide (every option is «Лаба N»). A failed save
// puts the old lab back
const props = defineProps({ id: String, lab: Number, busy: Boolean })
const emit = defineEmits(['act'])
function pick(e) {
  const el = e.target, lab = Number(el.value)
  if (lab) emit('act', () => putIntakeRow(props.id, { lab }).catch((err) => { el.value = props.lab ?? ''; throw err }))
}
</script>

<template>
  <select v-hint="lab ? 'не та лаба? — вибери іншу' : ''" class="lab" :class="lab ? 'in-text' : 'form-select form-select-sm'"
          :value="lab ?? ''" :disabled="busy" aria-label="Яка це лаба" @change="pick">
    <option v-if="!lab" value="">лаба?</option>
    <option v-for="n in LAB_NUMS" :key="n" :value="n">{{ lab ? 'Лаба' : 'лаба' }} {{ n }}</option>
  </select>
</template>

<style scoped>
.form-select.lab { width: auto; height: 1.4rem; min-height: 0; padding: 0 1.6rem 0 .45rem; background-position: right .35rem center; font-size: .78rem; }
.in-text { appearance: none; padding: 0; border: 0; border-bottom: 1px dotted var(--bs-secondary-color); border-radius: 0; background: none;
           color: var(--bs-body-color); font: inherit; line-height: 1.2; vertical-align: baseline; cursor: pointer; }  /* lower than the line: no taller than the text it turns into */
.in-text:hover:not(:disabled) { background: var(--bs-tertiary-bg); }
.in-text:disabled { opacity: .5; cursor: default; }
</style>
