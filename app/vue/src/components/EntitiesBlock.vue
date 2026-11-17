<script setup>
import { ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import Tip from '@core/components/Tip.vue'
import { useEd } from '../ed.js'
import EntityCard from './EntityCard.vue'
import EntityDraft from './EntityDraft.vue'
import StableColumns from './StableColumns.vue'

// the body of «Сутності» (T270 §7): a new entity's draft on top (T310), the cards in two stable columns, one toggle for all
// their rule lists. add(prefill?) opens the draft, the type (and the name) already chosen: { role?, title? }
const ed = useEd()
const adding = ref(null)  // { n, prefill } while the draft is open; n starts a fresh one when add() comes again
let n = 0
const add = (prefill = {}) => (adding.value = { n: ++n, prefill })
defineExpose({ add })
</script>

<template>
  <div>
    <div v-if="ed.entities.length" class="d-flex justify-content-end mb-1">
      <button type="button" class="toggle" @click="ed.showRules = !ed.showRules">
        <Icon :name="ed.showRules ? 'fold' : 'unfold'" /> {{ ed.showRules ? 'згорнути правила' : 'розгорнути правила' }}
      </button>
    </div>
    <EntityDraft v-if="ed.editable && adding" :key="adding.n" :prefill="adding.prefill" class="mb-2" @done="adding = null" @cancel="adding = null" />
    <StableColumns v-if="ed.entities.length" v-slot="{ item }" :items="ed.entities" scope="entities">
      <EntityCard :part="item" />
    </StableColumns>
    <Tip v-else-if="!adding">
      <div>Мешканці поля: гравець, вороги, предмети, стіни, підлога.</div>
      <div>У кожної — {{ ['тип, опис, скриншот', ed.has('stats') && 'параметри, стани', ed.has('mechanics') && 'механіки'].filter(Boolean).join(', ') }} і правила.</div>
    </Tip>
  </div>
</template>

<style scoped>
.toggle { display: inline-flex; align-items: center; gap: .25rem; padding: 0; border: 0; background: none; color: var(--bs-secondary-color); font-size: .78rem; }
.toggle:hover { color: var(--bs-body-color); }
</style>
