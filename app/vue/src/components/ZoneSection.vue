<script setup>
import { computed } from 'vue'

import { kindOf } from '../catalog.js'
import { useEd } from '../ed.js'
import CardPicker from './CardPicker.vue'
import SubzoneRows from './SubzoneRows.vue'

// the body of a section about the game as a whole (T270 §11): the game's own cards of these zones by subzone and
// «＋ картка» limited to them; `hint` — what goes here, while nothing does. The heading is the editor's.
const p = defineProps({ zones: Array, title: String, hint: String })
const ed = useEd()
const here = (t) => p.zones.includes(t?.zone)
const claims = computed(() => ed.claims.filter((c) => {
  const t = ed.info(c.task)
  return !c.part && !c.rule && kindOf(t) === 'game' && here(t)
}))
</script>

<template>
  <div class="vstack gap-2">
    <SubzoneRows v-if="claims.length" :claims />
    <div v-else class="text-secondary small">{{ hint }}</div>
    <div v-if="ed.editable"><CardPicker :kinds="['game']" :anchor="{}" label="картка" :filter="here" /></div>
  </div>
</template>
