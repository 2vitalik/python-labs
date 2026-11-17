<script setup>
import { computed, ref } from 'vue'

import Tip from '@core/components/Tip.vue'
import { kindOf } from '../catalog.js'
import { useEd } from '../ed.js'
import CardPicker from './CardPicker.vue'
import ClaimRow from './ClaimRow.vue'
import LevelCard from './LevelCard.vue'
import LevelDraft from './LevelDraft.vue'
import StableColumns from './StableColumns.vue'

// the «Рівні» section's body (T270 §9): a new level's draft on top (T310), the levels in two steady columns, then the cards
// about the levels in general (format, generation, editor…) that sit on no level
const ed = useEd()
const adding = ref(0)  // the draft's number while it is open: add() again starts a fresh one
let n = 0
const general = computed(() => ed.claims.filter((c) => !c.part && !c.rule && kindOf(ed.info(c.task)) === 'level'))
defineExpose({ add: () => (adding.value = ++n) })
</script>

<template>
  <div class="vstack gap-2">
    <LevelDraft v-if="adding" :key="adding" @done="adding = 0" @cancel="adding = 0" />
    <template v-if="!ed.levels.length && !adding">
      <Tip v-if="ed.editable">
        <div>Опиши кожен рівень або групу схожих: звідки він береться, розмір і параметри, скриншот. Генератор рівнів — теж рівень.</div>
        <div>Розмір і властивості поля на різних рівнях можуть відрізнятись — це пишеться в самому рівні.</div>
      </Tip>
      <div v-else class="text-secondary small">Рівні не описані.</div>
    </template>
    <StableColumns v-if="ed.levels.length" v-slot="{ item }" :items="ed.levels" scope="levels">
      <LevelCard :part="item" />
    </StableColumns>
    <div v-if="general.length || ed.editable" id="levels-general" class="vstack gap-1">
      <div class="d-flex align-items-center gap-1 small text-secondary">Про рівні загалом
        <CardPicker plus :kinds="['level']" :anchor="{}" label="картка про рівні загалом" /></div>
      <ClaimRow v-for="c in general" :key="c.id" :claim="c" />
    </div>
  </div>
</template>
