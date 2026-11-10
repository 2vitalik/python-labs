<script setup>
import { vocab } from '../catalog.js'

// a rule card's blank (Task.rule) read as the shape of its rule: the vocab's words after the coloured КОЛИ / ЯКЩО / ТО
// of RuleText.vue, whose classes it borrows
defineProps({ rule: Object })
const label = (dic, item) => vocab.value[dic]?.[item.kind]?.label || item.kind
</script>

<template>
  <div v-if="rule?.when || rule?.cond?.length || rule?.then?.length" class="rule-text">
    <template v-if="rule.when"><span class="kw when">КОЛИ</span><span>{{ label('triggers', rule.when) }}</span></template>
    <template v-for="(c, i) in rule.cond || []" :key="`c${i}`">
      <span class="kw if">{{ i ? 'і' : 'ЯКЩО' }}</span><span>{{ c.not ? 'не ' : '' }}{{ label('conditions', c) }}</span>
    </template>
    <template v-for="(e, i) in rule.then || []" :key="`t${i}`">
      <span class="kw then">{{ i ? '' : 'ТО' }}</span><span>{{ label('effects', e) }}</span>
    </template>
  </div>
</template>
