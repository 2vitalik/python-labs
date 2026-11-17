<script setup>
import { computed } from 'vue'

import Reveal from '@core/components/Reveal.vue'
import { useEd } from '../ed.js'
import { setTools } from '../tools.js'
import PartBlock from './PartBlock.vue'
import StateChips from './StateChips.vue'
import StatList from './StatList.vue'

// an entity's stats as a small table under «Параметри» (StatList) and its states, a pill each after «Стани» (StateChips);
// `auto` — the part's auto-claims. With `can` (the card itself, not a card under the mouse or the helper's proposal) the
// owner changes a value or a state's name where it reads (T306). With `tools` (the card's pencil, T310) both blocks are
// there even while empty: «＋ параметр», «＋ стан». The feature on and nothing in it yet — a quiet «＋» at rest: it turns
// this card's pencil on (T348), no other card's
const props = defineProps({ part: Object, auto: Array, can: Boolean, tools: Boolean })
const ed = useEd()
const setStats = (fn) => ed.save.part(props.part.id, (p) => ({ stats: fn(p.stats || []) }))
const invite = computed(() => props.can && !props.tools && ed.has('stats') && !props.part.stats?.length && !props.part.states?.length)
</script>

<template>
  <button v-if="invite" type="button" class="more-field align-self-start" @click="setTools(part.id, true)">＋ параметри й стани</button>
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
