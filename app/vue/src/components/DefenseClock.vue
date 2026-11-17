<script setup>
import { computed, onBeforeUnmount, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import Pop from '@core/components/Pop.vue'
import { fromInput, toInput } from '@core/labs.js'
import { clock, dayOf, mins, span } from '../defense.js'
import '../defense.css'

// the time of a defense (T327 §3): when it started, how long it runs, a button to end it; a click on the time opens both
// to change. Past the usual length the counter turns warm — a reminder with no sound and no window
const props = defineProps({ d: Object })
const emit = defineEmits(['set'])
const USUAL = 30  // minutes
const now = ref(Date.now())
const timer = setInterval(() => (now.value = Date.now()), 15000)
onBeforeUnmount(() => clearInterval(timer))
const m = computed(() => (props.d.started_at ? mins(props.d.started_at, props.d.ended_at || now.value) : 0))
const open = ref(false)
const set = (key, e) => e.target.value && emit('set', { [key]: fromInput(e.target.value) })
</script>

<template>
  <div class="drow">
    <span class="dlbl">Час</span>
    <span class="d-flex flex-wrap align-items-center gap-2">
      <Pop v-model="open" width="17rem">
        <template #trigger="{ toggle }">
          <button type="button" class="time" title="Клік — змінити початок і кінець" @click="toggle">
            <Icon name="clock" /> {{ dayOf(d.started_at) }}, {{ clock(d.started_at) }}<template v-if="d.ended_at"> – {{ clock(d.ended_at) }}</template>
          </button>
        </template>
        <label class="form-label small mb-1">Початок</label>
        <input type="datetime-local" class="form-control form-control-sm mb-2" :value="toInput(d.started_at)" @change="set('started_at', $event)">
        <label class="form-label small mb-1">Кінець</label>
        <input type="datetime-local" class="form-control form-control-sm" :value="d.ended_at ? toInput(d.ended_at) : ''" @change="set('ended_at', $event)">
        <button v-if="d.ended_at" type="button" class="more-field mt-2" @click="emit('set', { ended_at: null })">захист ще триває — прибрати кінець</button>
      </Pop>
      <span class="len" :class="{ long: !d.ended_at && m > USUAL }">{{ d.ended_at ? '' : 'триває ' }}{{ span(m) }}</span>
      <button v-if="!d.ended_at" type="button" class="btn btn-sm btn-outline-secondary ms-auto" @click="emit('set', { ended_at: new Date().toISOString() })"><Icon name="stop" /> Завершити</button>
    </span>
  </div>
</template>

<style scoped>
.time { padding: 0 .3rem; border: 0; border-radius: .3rem; background: none; color: inherit; }
.time:hover { background: var(--bs-tertiary-bg); }
.len { font-variant-numeric: tabular-nums; color: var(--bs-secondary-color); }
.len.long { color: var(--bs-warning-text-emphasis); font-weight: 600; }
</style>
