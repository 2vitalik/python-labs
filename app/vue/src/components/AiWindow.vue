<script setup>
import { computed } from 'vue'

import Icon from '@core/components/Icon.vue'
import { vPeek } from '@core/peek.js'
import { taskIndex } from '../catalog.js'
import { useEd } from '../ed.js'
import AiCards from './AiCards.vue'
import CoinBadge from './CoinBadge.vue'

// a proposed window read as WindowCard reads: its sign, name and type with the type's coin, the menu's items with where
// each leads, the elements. `data` — the reference node: {title, task, description, items: [{title, window, task, note}], claims}
const props = defineProps({ data: Object })
const ed = useEd()
const card = (slug) => ed.info(slug) || taskIndex.value[slug]
const type = computed(() => card(props.data.task))
const to = (i) => (i.window ? ` → ${i.window}` : i.task ? ` → ${card(i.task)?.title || i.task}` : '')
</script>

<template>
  <div class="vstack gap-1">
    <div class="ai-line">
      <Icon name="win" class="ai-ico" />
      <span class="ai-t">{{ data.title }}</span>
      <span v-peek="type ? { kind: 'task', id: data.task } : null" class="ai-ty"><CoinBadge :coin="type?.coin" :amount="type?.amount" /> {{ type?.title || data.task }}</span>
    </div>
    <div v-if="data.description" class="ai-d">{{ data.description }}</div>
    <div v-if="data.items?.length" class="ai-sub">
      <template v-for="(i, k) in data.items" :key="k">{{ k ? ' · ' : '' }}<span class="text-nowrap">☰ {{ i.title }}{{ to(i) }}</span></template>
    </div>
    <AiCards :list="data.claims" />
  </div>
</template>
