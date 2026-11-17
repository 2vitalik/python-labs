<script setup>
import { computed } from 'vue'

import { fmtWhen } from '../labs.js'

// a date that reads as a date (T315 §6): «27.11» — the day plain, the month smaller and grey, in a thin frame; the year only
// when it is not this one; the whole of it under the mouse. `plain` — no frame (a line under a cell), `pre` — a mark before («→»)
const props = defineProps({ at: { type: String, required: true }, plain: Boolean, pre: { type: String, default: '' } })
const p2 = (n) => String(n).padStart(2, '0')
const d = computed(() => new Date(props.at))
const year = computed(() => (d.value.getFullYear() === new Date().getFullYear() ? '' : `.${p2(d.value.getFullYear() % 100)}`))
const full = computed(() => fmtWhen(props.at, props.at.length <= 10))  // a bare day has no hour to show
</script>

<template>
  <span class="datechip" :class="{ plain }" :title="full">{{ pre }}<span>{{ p2(d.getDate()) }}</span><i>.{{ p2(d.getMonth() + 1) }}{{ year }}</i></span>
</template>

<style scoped>
.datechip { display: inline-block; padding: 0 .28rem; border: 1px solid var(--bs-border-color); border-radius: .35rem; line-height: 1.35;
            font-variant-numeric: tabular-nums; white-space: nowrap; }
.datechip i { font-style: normal; font-size: .72em; color: var(--bs-secondary-color); }
.datechip.plain { padding: 0; border: 0; line-height: inherit; }
.datechip.plain i { font-size: .88em; }  /* already small where it stands */
</style>
