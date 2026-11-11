<script setup>
import { statOf } from '../catalog.js'
import JudgeMark from './JudgeMark.vue'
import PartLabel from './PartLabel.vue'

// an entity's stats as a small table under «Параметри» — name on the left, value and unit on the right, the teacher's mark
// on the stat's claim — and its states, a pill each after «Стани»; `auto` — the part's auto-claims
const props = defineProps({ part: Object, auto: Array })
const claimOf = (s) => {
  const slug = statOf(s.key)?.slug
  return slug ? props.auto.find((c) => c.task === slug) : null
}
</script>

<template>
  <div v-if="part.stats?.length || part.states?.length" class="vstack gap-1">
    <PartLabel v-if="part.stats?.length" icon="🔢" zone="entities">Параметри</PartLabel>
    <div v-if="part.stats?.length" class="stats">
      <div v-for="s in part.stats" :key="s.key" class="stat" :title="statOf(s.key)?.desc || 'свій параметр'">
        <span class="name">{{ statOf(s.key)?.icon || '•' }} {{ s.label || s.key }}</span>
        <span class="text-nowrap"><b>{{ s.value }}</b><span v-if="s.unit" class="unit">{{ s.unit }}</span> <JudgeMark :claim="claimOf(s)" /></span>
      </div>
    </div>
    <div v-if="part.states?.length" class="d-flex flex-wrap align-items-center gap-1">
      <PartLabel icon="◐" zone="entities" class="me-1">Стани</PartLabel>
      <span v-for="st in part.states" :key="st" class="state">{{ st }}</span>
    </div>
  </div>
</template>

<style scoped>
.stats { display: grid; grid-template-columns: repeat(auto-fill, minmax(10.5rem, 1fr)); column-gap: 1.25rem; font-size: .8rem; }
.stat { display: flex; justify-content: space-between; align-items: baseline; gap: .5rem; padding: .1rem 0; border-bottom: 1px dotted var(--bs-border-color); }
.name { min-width: 0; overflow-wrap: anywhere; color: var(--bs-secondary-color); }
.stat b { font-weight: 600; font-variant-numeric: tabular-nums; }
.unit { margin-left: .25em; color: var(--bs-secondary-color); }
.state { padding: 0 .45rem; border: 1px solid var(--bs-info-border-subtle); border-radius: 1rem; background: color-mix(in srgb, var(--bs-info) 14%, var(--bs-body-bg)); font-size: .76rem; }
</style>
