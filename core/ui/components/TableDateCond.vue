<script setup>
import { ref, watch } from 'vue'

// a date column's condition (T315 §5, §12.1): from a day or up to it (>2026-11-01 · <2026-11-01), within the last N days or
// older than N (~7 · ^7). A day picked with no side chosen means «from»; N with no side — «the last N days»
const props = defineProps({ spec: { type: String, default: '' } })
const emit = defineEmits(['set'])
const QUICK = ['7', '14', '30']
const day = ref('')
const n = ref('')
const side = (ops) => (props.spec.length > 1 && ops.includes(props.spec[0]) ? props.spec[0] : '')
watch(() => props.spec, () => {
  if (side('<>')) day.value = props.spec.slice(1)
  if (side('~^')) n.value = props.spec.slice(1)
}, { immediate: true })
const toggle = (o, value) => emit('set', props.spec === o + value ? '' : o + value)
const onDay = () => emit('set', day.value ? (side('<>') || '>') + day.value : '')
function onDays(value) {
  n.value = String(value).replace(/\D/g, '')
  emit('set', n.value ? (side('~^') || '~') + n.value : '')
}
</script>

<template>
  <div class="dc">
    <div class="d-flex align-items-center gap-1">
      <button v-for="[o, word] in [['>', 'від'], ['<', 'до']]" :key="o" type="button" class="opt" :class="{ on: side('<>') === o }" :disabled="!day"
              :title="day ? '' : 'Спершу вибери дату'" @click="toggle(o, day)">{{ word }}</button>
      <input v-model="day" type="date" class="form-control form-control-sm" @change="onDay">
    </div>
    <div class="d-flex align-items-center gap-1 mt-1">
      <button v-for="[o, word] in [['~', 'за останні'], ['^', 'давніше']]" :key="o" type="button" class="opt" :class="{ on: side('~^') === o }"
              @click="toggle(o, n || '7')">{{ word }}</button>
    </div>
    <div class="d-flex align-items-center gap-1 mt-1 mb-1">
      <button v-for="q in QUICK" :key="q" type="button" class="opt" :class="{ on: !!side('~^') && n === q }" @click="onDays(q)">{{ q }}</button>
      <input v-model.trim="n" type="text" inputmode="numeric" class="form-control form-control-sm days" placeholder="N" @input="onDays(n)"> днів
    </div>
  </div>
</template>

<style scoped>
.opt { border: 1px solid var(--bs-border-color); border-radius: .35rem; background: none; color: var(--bs-body-color); padding: .1rem .5rem; white-space: nowrap; }
.opt:hover:not(:disabled) { background: var(--bs-tertiary-bg); }
.opt:disabled { color: var(--bs-tertiary-color); }
.opt.on { background: var(--bs-warning-bg-subtle); border-color: var(--bs-warning-border-subtle); }
.days { width: 3.2rem; }
</style>
