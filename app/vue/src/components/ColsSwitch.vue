<script setup>
import { computed } from 'vue'

import Icon from '@core/components/Icon.vue'
import { canCols, canDense, colsMode, nextCols } from '../layout.js'

// the columns of a game's description in one button (T291 §1): one → several → dense, its icon is the mode it is in.
// Nothing to switch (a phone: one column whatever is chosen) — no button. `quiet` — an icon in a section's heading;
// `around` — the host's way to make the change without losing the reader's place (SectionHead's `keep`)
defineProps({ quiet: Boolean, around: { type: Function, default: (change) => change() } })
const LOOK = { one: ['cols1', 'один стовпець'], some: ['cols2', 'кілька стовпців'], dense: ['cols3', 'щільно — більше вужчих стовпців'] }
const next = computed(() => (colsMode.value === 'one' ? 'some' : colsMode.value === 'some' && canDense.value ? 'dense' : 'one'))
</script>

<template>
  <button v-if="canCols" type="button" :class="quiet ? 'iact dim' : 'btn btn-sm btn-outline-secondary px-2'"
          :title="`Зараз: ${LOOK[colsMode][1]}. Клік: ${LOOK[next][1]}`" @click="around(nextCols)"><Icon :name="LOOK[colsMode][0]" /></button>
</template>
