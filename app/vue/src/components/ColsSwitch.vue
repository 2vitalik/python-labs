<script setup>
import { computed } from 'vue'

import Icon from '@core/components/Icon.vue'
import { canCols, modeOf, nextCols, nextOf, own, ownCount } from '../layout.js'

// the columns of a game's description in one button (T291 §1): one → several → dense, its icon is the mode it is in.
// `scope` — a section's heading: the change is this section's own (T294 §2), shown in the colour of «on»; without it —
// every section, and their own looks go. `quiet` — an icon in a heading; `wordy` — the top row: a short line beside the
// button says what it does, and on a narrow window (one column whatever is chosen) the button stays, greyed, saying why.
// `around` — the host's way to make the change without losing the reader's place (SectionHead's `keep`)
const p = defineProps({ quiet: Boolean, wordy: Boolean, scope: String, around: { type: Function, default: (change) => change() } })
const LOOK = { one: ['cols1', 'один стовпець'], some: ['cols2', 'кілька стовпців'], dense: ['cols3', 'щільно — більше вужчих стовпців'] }
const mode = computed(() => modeOf(p.scope))
const mine = computed(() => !!p.scope && !!own[p.scope])
const tip = computed(() => (!canCols.value ? 'Вікно вузьке: один стовпець за будь-якого вибору'
  : p.scope ? `${mine.value ? 'Своє для цієї секції' : 'Як у всіх секцій'}: ${LOOK[mode.value][1]}. Клік — ${LOOK[nextOf(p.scope)][1]} лише тут`
    : `Зараз: ${LOOK[mode.value][1]}. Клік — ${LOOK[nextOf()][1]} у всіх секціях`))
</script>

<template>
  <span v-if="wordy" class="d-inline-flex align-items-center gap-2">
    <button type="button" class="btn btn-sm btn-outline-secondary px-2" :disabled="!canCols" :title="tip" @click="around(() => nextCols())">
      <Icon :name="LOOK[mode][0]" /></button>
    <span class="why">{{ canCols ? `Стовпці: ${LOOK[mode][1]} — у всіх секціях` : 'Стовпці: вікно вузьке — один' }}<template v-if="canCols && ownCount">
      · свої на заголовках: {{ ownCount }}, клік їх скине</template></span>
  </span>
  <button v-else-if="canCols" type="button" :class="quiet ? ['iact', mine ? 'on' : 'dim'] : 'btn btn-sm btn-outline-secondary px-2'" :aria-pressed="mine"
          :title="tip" @click="around(() => nextCols(scope))"><Icon :name="LOOK[mode][0]" /></button>
</template>

<style scoped>
.why { font-size: .78rem; color: var(--bs-secondary-color); }
</style>
