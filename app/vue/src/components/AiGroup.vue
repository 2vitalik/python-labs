<script setup>
import { computed } from 'vue'

import Icon from '@core/components/Icon.vue'
import { addable } from '../ai.js'
import { zones } from '../catalog.js'
import AiItem from './AiItem.vue'

// one group of a draft's proposals under the heading of its section in the description — its icon, its category's colour
// (T278 §9), how many — and «додати всі» for the open ones. `group` — {key, icon, title, zone, items}
const props = defineProps({ group: Object, draft: Object, busy: Boolean })
const emit = defineEmits(['add', 'mark'])
const ready = computed(() => props.group.items.filter((it) => addable(props.draft, it)).map((it) => it.key))
const color = computed(() => zones.value[props.group.zone]?.color || (props.group.key === 'unknown' ? 'var(--bs-warning)' : 'var(--bs-secondary-color)'))
</script>

<template>
  <div class="vstack gap-1">
    <div class="ghead" :style="{ '--c': color }">
      <span>{{ group.icon }} {{ group.title }}</span><span class="n">{{ group.items.length }}</span>
      <button v-if="ready.length > 1" type="button" class="iact add all" :disabled="busy" @click="emit('add', ready)"><Icon name="plus" /> додати всі ({{ ready.length }})</button>
    </div>
    <div class="vstack gap-1 items">
      <AiItem v-for="it in group.items" :key="it.key" :item="it" :draft :busy @add="emit('add', $event)" @mark="(keys, state) => emit('mark', keys, state)" />
    </div>
  </div>
</template>

<style scoped>
.ghead { display: flex; align-items: center; gap: .5rem; min-height: 1.6rem; padding: 0 0 0 .5rem; border-left: 4px solid var(--c); font-weight: 700; }
.n { font-weight: 400; opacity: .55; }
.all { width: auto; gap: .2rem; margin-left: auto; padding: 0 .4rem; font-size: .78rem; font-weight: 400; }
.items { padding-left: .75rem; }
@media (max-width: 575px) { .items { padding-left: 0; } }
</style>
