<script setup>
import { vPeek } from '@core/peek.js'
import { statOf } from '../catalog.js'
import JudgeMark from './JudgeMark.vue'
import PartBlock from './PartBlock.vue'

// an entity's stats as a small table under «Параметри» — name on the left, value and unit on the right, the teacher's mark
// on the stat's claim — and its states, a pill each after «Стани»; `auto` — the part's auto-claims. A stat from the
// catalog shows its card under the mouse
const props = defineProps({ part: Object, auto: Array })
const claimOf = (s) => {
  const slug = statOf(s.key)?.slug
  return slug ? props.auto.find((c) => c.task === slug) : null
}
const peek = (s) => (statOf(s.key)?.slug ? { kind: 'task', id: statOf(s.key).slug } : null)
</script>

<template>
  <PartBlock v-if="part.stats?.length" pic="stats" zone="entities" title="Параметри">
    <div class="stats">
      <div v-for="s in part.stats" :key="s.key" v-peek="peek(s)" class="stat" :title="statOf(s.key) ? null : 'свій параметр'">
        <span class="name">{{ statOf(s.key)?.icon || '•' }} {{ s.label || s.key }}</span>
        <span class="val"><b>{{ s.value }}</b><span v-if="s.unit" class="unit">{{ s.unit }}</span> <JudgeMark :claim="claimOf(s)" /></span>
      </div>
    </div>
  </PartBlock>
  <PartBlock v-if="part.states?.length" pic="half" zone="entities" title="Стани" inline>
    <span class="d-flex flex-wrap gap-1"><span v-for="st in part.states" :key="st" class="state">{{ st }}</span></span>
  </PartBlock>
</template>

<style scoped>
.stats { display: grid; grid-template-columns: repeat(auto-fill, minmax(10.5rem, 1fr)); column-gap: 1.25rem; font-size: .8rem; }
/* a long value («≤ 4 (20 на рівень) шт.») wraps under itself instead of squeezing the name into a column of letters */
.stat { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: baseline; gap: 0 .5rem; padding: .1rem 0; border-bottom: 1px dotted var(--bs-border-color); }
.name { color: var(--bs-secondary-color); }
.val { margin-left: auto; text-align: end; }
.stat b { font-weight: 600; font-variant-numeric: tabular-nums; }
.unit { margin-left: .25em; color: var(--bs-secondary-color); }
.state { padding: 0 .45rem; border: 1px solid var(--bs-info-border-subtle); border-radius: 1rem; background: color-mix(in srgb, var(--bs-info) 14%, var(--bs-body-bg)); font-size: .76rem; }
</style>
