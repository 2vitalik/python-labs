<script setup>
import Reveal from '@core/components/Reveal.vue'
import { useEd } from '../ed.js'
import PartBlock from './PartBlock.vue'
import StateChips from './StateChips.vue'
import StatList from './StatList.vue'

// an entity's stats as a small table under «Параметри» (StatList) and its states, a pill each after «Стани» (StateChips);
// `auto` — the part's auto-claims. With `can` (the card itself, not a card under the mouse or the helper's proposal) the
// owner changes a value or a state's name where it reads (T306). With `tools` (the card's pencil, T310) both blocks are
// there even while empty: «＋ параметр», «＋ стан»
const props = defineProps({ part: Object, auto: Array, can: Boolean, tools: Boolean })
const ed = useEd()
const setStats = (fn) => ed.save.part(props.part.id, (p) => ({ stats: fn(p.stats || []) }))
</script>

<template>
  <Reveal :show="!!part.stats?.length || tools" gap>
    <PartBlock pic="stats" zone="entities" title="Параметри">
      <StatList :stats="part.stats" :auto :can :tools :save="setStats" />
    </PartBlock>
  </Reveal>
  <Reveal :show="!!part.states?.length || tools" gap>
    <PartBlock pic="half" zone="entities" title="Стани" inline>
      <StateChips :part :can :tools />
    </PartBlock>
  </Reveal>
</template>
