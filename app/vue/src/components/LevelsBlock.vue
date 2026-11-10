<script setup>
import { computed, ref } from 'vue'

import { kindOf } from '../catalog.js'
import { useEd } from '../ed.js'
import CardPicker from './CardPicker.vue'
import ClaimRow from './ClaimRow.vue'
import LevelCard from './LevelCard.vue'
import LevelForm from './LevelForm.vue'
import StableColumns from './StableColumns.vue'

// the «Рівні» section's body (T270 §9): a new level's form on top, the levels in two steady columns, then the cards
// about the levels in general (format, generation, editor…) that sit on no level
const ed = useEd()
const adding = ref(false)
const general = computed(() => ed.claims.filter((c) => !c.part && !c.rule && kindOf(ed.info(c.task)) === 'level'))
defineExpose({ add: () => (adding.value = true) })
</script>

<template>
  <div class="vstack gap-2">
    <div v-if="adding" class="card">
      <div class="card-body p-2"><LevelForm @done="adding = false" @cancel="adding = false" /></div>
    </div>
    <div v-if="!ed.levels.length && !adding" class="text-secondary small">
      <template v-if="ed.editable">
        <div>Опиши кожен рівень або групу схожих: звідки він береться, розмір і параметри, скриншот. Генератор рівнів — теж рівень.</div>
        <div>Розмір і властивості поля на різних рівнях можуть відрізнятись — це пишеться в самому рівні.</div>
      </template>
      <template v-else>Рівні не описані.</template>
    </div>
    <StableColumns v-if="ed.levels.length" v-slot="{ item }" :items="ed.levels">
      <LevelCard :part="item" />
    </StableColumns>
    <div v-if="general.length || ed.editable" class="vstack gap-1">
      <div class="small text-secondary">Про рівні загалом</div>
      <ClaimRow v-for="c in general" :key="c.id" :claim="c" />
      <div v-if="ed.editable"><CardPicker :kinds="['level']" :anchor="{}" label="картка про рівні" /></div>
    </div>
  </div>
</template>
