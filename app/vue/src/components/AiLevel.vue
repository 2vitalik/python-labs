<script setup>
import { computed } from 'vue'

import { vocab } from '../catalog.js'
import AiCards from './AiCards.vue'
import PropsList from './PropsList.vue'

// a proposed level read as LevelCard reads: where it comes from and how many, its size and the field's properties it
// overrides (the cards' own PropsList), its parameters, the level's cards. `data` — the reference node
const props = defineProps({ data: Object })
const OWN = ['title', 'description', 'mode', 'count', 'stats', 'claims']
const mode = computed(() => {
  const o = vocab.value.level.find((s) => s.key === 'mode')?.options?.[props.data.mode]
  return typeof o === 'string' ? o : o?.label || props.data.mode || ''
})
const values = computed(() => Object.fromEntries(Object.entries(props.data).filter(([k]) => !OWN.includes(k))))
const specs = computed(() => [...vocab.value.level.filter((s) => s.key === 'size'), ...vocab.value.field.filter((s) => s.key !== 'size')])
</script>

<template>
  <div class="vstack gap-1">
    <div class="ai-line">
      <span>🪜</span>
      <span class="ai-t">{{ data.title }}</span>
      <span class="ai-ty">{{ mode }}<template v-if="data.count"> {{ /^\d+$/.test(data.count) ? '×' : '·' }} {{ data.count }}</template></span>
    </div>
    <PropsList :props="values" :specs />
    <div v-if="data.stats?.length" class="ai-sub">параметри: {{ data.stats.map((s) => `${s.key} ${s.value}${s.unit ? ` ${s.unit}` : ''}`).join(' · ') }}</div>
    <div v-if="data.description" class="ai-d">{{ data.description }}</div>
    <AiCards :list="data.claims" />
  </div>
</template>
