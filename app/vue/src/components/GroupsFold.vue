<script setup>
import { computed } from 'vue'

import Icon from '@core/components/Icon.vue'
import { groups, rulesView } from '../looks.js'

// on the heading of «Правила» (T304): every group of rules folded to its head or open — as «усе / згорнуто» does for the
// sections; its icon is the state now, blue while a group differs (its own fold, RuleGroup), a click sets all and drops
// those. Grey with the reason while the section shows a table. `around` — the heading's way to keep the reader's place
const p = defineProps({ around: { type: Function, default: (change) => change() } })
const shut = computed(() => groups.all.value === 'shut')
const own = computed(() => groups.count.value)
const off = computed(() => rulesView.value !== 'list')
const tip = computed(() => (off.value ? 'Групи правил — у вигляді «Список»'
  : `Групи правил: ${shut.value ? 'згорнуті до заголовків' : 'розгорнуті'}${own.value ? ` (інакше — у ${own.value})` : ''}. Клік — ${shut.value ? 'розгорнути' : 'згорнути'} всі`))
</script>

<template>
  <button type="button" class="iact" :class="own ? 'on' : 'dim'" :disabled="off" :title="tip" :aria-pressed="shut"
          @click="p.around(() => groups.set(shut ? 'open' : 'shut'))"><Icon :name="shut ? 'fold' : 'unfold'" /></button>
</template>
