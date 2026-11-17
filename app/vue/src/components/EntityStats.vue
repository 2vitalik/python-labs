<script setup>
import InlineText from '@core/components/InlineText.vue'
import Reveal from '@core/components/Reveal.vue'
import { useEd } from '../ed.js'
import PartBlock from './PartBlock.vue'
import StatList from './StatList.vue'

// an entity's stats as a small table under «Параметри» (StatList) and its states, a pill each after «Стани»; `auto` — the
// part's auto-claims. With `can` (the card itself, not a card under the mouse or the helper's proposal) the owner changes
// a value and the states where they read (T306) — the states as one line «через кому». With `tools` (the card's pencil,
// T310) both blocks are there even while empty: «＋ параметр», «＋ стани»
const props = defineProps({ part: Object, auto: Array, can: Boolean, tools: Boolean })
const ed = useEd()
const setStats = (fn) => ed.save.part(props.part.id, (p) => ({ stats: fn(p.stats || []) }))
const setStates = (line) => ed.save.part(props.part.id, { states: line.split(',').map((s) => s.trim()).filter(Boolean) })
</script>

<template>
  <Reveal :show="!!part.stats?.length || tools" gap>
    <PartBlock pic="stats" zone="entities" title="Параметри">
      <StatList :stats="part.stats" :auto :can :tools :save="setStats" />
    </PartBlock>
  </Reveal>
  <Reveal :show="!!part.states?.length || tools" gap>
    <PartBlock pic="half" zone="entities" title="Стани" inline>
      <InlineText :value="(part.states || []).join(', ')" :can placeholder="через кому: звичайний, посилений, спить…" class="d-inline-flex flex-wrap gap-1" :save="setStates">
        <span v-for="st in part.states" :key="st" class="state">{{ st }}</span>
        <template #empty><span class="more-field">＋ стани</span></template>
      </InlineText>
    </PartBlock>
  </Reveal>
</template>

<style scoped>
.state { padding: 0 .45rem; border: 1px solid var(--bs-info-border-subtle); border-radius: 1rem; background: color-mix(in srgb, var(--bs-info) 14%, var(--bs-body-bg)); font-size: .76rem; }
</style>
