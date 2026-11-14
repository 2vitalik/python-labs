<script setup>
import { computed } from 'vue'

import { vPeek } from '@core/peek.js'
import { roleOf, statOf } from '../catalog.js'
import AiCards from './AiCards.vue'
import EntityStats from './EntityStats.vue'

// a proposed entity read as its card reads (EntityCard): icon, name, type; the description, stats and states
// (the card's own EntityStats), the mechanics. `data` — the reference node: {title, role, icon, description, stats, states, claims}
const props = defineProps({ data: Object })
const role = computed(() => roleOf(props.data.role))
// a stat of the catalog is named by its card, as the form names it on saving
const stats = computed(() => (props.data.stats || []).map((s) => ({ ...s, label: statOf(s.key)?.label || s.key, unit: s.unit || statOf(s.key)?.unit || '' })))
</script>

<template>
  <div class="vstack gap-1">
    <div class="ai-line">
      <span class="ai-ico">{{ data.icon || role.icon }}</span>
      <span class="ai-t">{{ data.title }}</span>
      <span v-peek="role.slug ? { kind: 'task', id: role.slug } : null" class="ai-ty">{{ (role.label || '').toLowerCase() }}</span>
    </div>
    <div v-if="data.description" class="ai-d">{{ data.description }}</div>
    <EntityStats v-if="stats.length || data.states?.length" :part="{ stats, states: data.states || [] }" :auto="[]" />
    <AiCards :list="data.claims" />
  </div>
</template>
