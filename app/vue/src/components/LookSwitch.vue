<script setup>
import { computed } from 'vue'

import { ALL_HOW, toAll } from '@core/allkey.js'
import Icon from '@core/components/Icon.vue'

// a look of the description in one button (T296 §6–7), as ColsSwitch: its icon is the look it is in, a click — the next.
// `look` — a store of looks.js, `modes` — [value, icon, what it is] in the order a click goes; `scope` — a section's
// heading: the change is this section's own, blue while it differs from the top (T298), ⌥-click — the next for every
// section; without it — every section, their own looks dropped. `quiet` — an icon in a heading; `wordy` — the top row,
// a line of what it does. `off` — why it can do nothing now: greyed with that line; `label` — the line's first word
const p = defineProps({ look: Object, modes: Array, label: String, scope: String, quiet: Boolean, wordy: Boolean, off: String,
                        around: { type: Function, default: (change) => change() } })
const word = (v) => (p.modes.find((m) => m[0] === v) || p.modes[0])[2]
const cur = computed(() => p.modes.find(([v]) => v === p.look.of(p.scope)) || p.modes[0])
const next = computed(() => p.modes[(p.modes.indexOf(cur.value) + 1) % p.modes.length])
const top = computed(() => p.look.all.value)
const mine = computed(() => !!p.scope && !!p.look.own[p.scope])
const count = computed(() => p.look.count.value)
const tip = computed(() => p.off || (p.scope
  ? `${p.label} — ${mine.value ? `своє: ${cur.value[2]} (угорі — ${word(top.value)})` : `як угорі: ${cur.value[2]}`}. `
    + `Клік — ${next.value[2]}${next.value[0] === top.value ? ', як угорі' : ' лише тут'} · ${ALL_HOW} — у всіх секціях`
  : `${p.label} зараз: ${cur.value[2]}. Клік — ${next.value[2]} у всіх секціях`))
const go = (e) => p.around(() => p.look.set(next.value[0], toAll(e) ? undefined : p.scope))
</script>

<template>
  <span v-if="wordy" class="d-inline-flex align-items-center gap-2">
    <button type="button" class="btn btn-sm btn-outline-secondary px-2" :disabled="!!off" :title="tip" @click="go"><Icon :name="cur[1]" /></button>
    <span class="why">{{ label }}: {{ off || `${cur[2]} — у всіх секціях` }}<template v-if="!off && count"> · свої (сині на заголовках): {{ count }}, клік їх скине</template></span>
  </span>
  <button v-else type="button" :class="quiet ? ['iact every', mine ? 'on' : 'dim'] : 'btn btn-sm btn-outline-secondary px-2'" :aria-pressed="mine"
          :disabled="!!off" :title="tip" :data-all="`у всіх секціях: ${next[2].split(' — ')[0]}`" @click="go"><Icon :name="cur[1]" /></button>
</template>

<style scoped>
.why { font-size: .78rem; color: var(--bs-secondary-color); }
</style>
