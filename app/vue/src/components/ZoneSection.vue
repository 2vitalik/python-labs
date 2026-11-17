<script setup>
import { computed } from 'vue'

import Clamp from '@core/components/Clamp.vue'
import Tip from '@core/components/Tip.vue'
import { kindOf } from '../catalog.js'
import { useEd } from '../ed.js'
import { isFolded, isShort, setShort } from '../fold.js'
import CardPicker from './CardPicker.vue'
import SectionHead from './SectionHead.vue'
import SubzoneRows from './SubzoneRows.vue'
import VideoSlots from './VideoSlots.vue'

// a section about the game as a whole (T270 §11): the game's own cards of its zones by subzone and «＋ картка» limited
// to them — on the heading, as every section's «＋» (T294 §8); `z` — the section (sections.js ZONES), `head` — its heading as the editor words it.
// «Супровід» opens with the videos every game is asked for (T318, VideoSlots) — without its cards (T319) they are all of it
const p = defineProps({ z: Object, head: Object })
const ed = useEd()
const here = (t) => p.z.zones.includes(t?.zone)
const claims = computed(() => ed.claims.filter((c) => {
  const t = ed.info(c.task)
  return !c.part && !c.rule && kindOf(t) === 'game' && here(t)
}))
const videos = computed(() => p.z.zones.includes('support') && !!ed.videos)
const cards = computed(() => !p.z.zones.includes('support') || ed.has('support'))
</script>

<template>
  <section :id="z.id" class="mb-4">
    <SectionHead v-bind="head">
      <CardPicker v-if="ed.editable && cards" :kinds="['game']" :anchor="{}" label="картка" :filter="here" :catalog="head.catalog" />
    </SectionHead>
    <Clamp v-show="!isFolded(head.fold)" :on="isShort(head.fold)" @open="setShort(head.fold, false)">
      <div class="vstack gap-3 align-items-start">
        <VideoSlots v-if="videos" class="align-self-stretch" />
        <template v-if="cards">
          <SubzoneRows v-if="claims.length" class="align-self-stretch" :claims :table="z.table" cols :scope="z.id" />
          <Tip v-else>{{ z.hint }}</Tip>
        </template>
      </div>
    </Clamp>
  </section>
</template>
