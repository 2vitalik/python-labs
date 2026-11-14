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

// a section about the game as a whole (T270 §11): the game's own cards of its zones by subzone and «＋ картка» limited
// to them — on the heading, as every section's «＋» (T294 §8); `z` — the section (sections.js ZONES), `head` — its heading as the editor words it
const p = defineProps({ z: Object, head: Object })
const ed = useEd()
const here = (t) => p.z.zones.includes(t?.zone)
const claims = computed(() => ed.claims.filter((c) => {
  const t = ed.info(c.task)
  return !c.part && !c.rule && kindOf(t) === 'game' && here(t)
}))
// a demo is wanted sooner or later (T278 §10): the support section asks for it until one is claimed
const noVideo = computed(() => ed.editable && p.z.zones.includes('support')
  && !ed.claims.some((c) => ed.info(c.task)?.zone === 'support' && ed.info(c.task)?.subzone === 'video'))
</script>

<template>
  <section :id="z.id" class="mb-4">
    <SectionHead v-bind="head">
      <CardPicker v-if="ed.editable" :kinds="['game']" :anchor="{}" label="картка" :filter="here" />
    </SectionHead>
    <Clamp v-show="!isFolded(head.fold)" :on="isShort(head.fold)" @open="setShort(head.fold, false)">
      <div class="vstack gap-2 align-items-start">
        <SubzoneRows v-if="claims.length" class="align-self-stretch" :claims :table="z.table" cols :scope="z.id" />
        <Tip v-else>{{ z.hint }}</Tip>
        <Tip v-if="noVideo" id="ask-video">🎬 Відео-демки ще нема: рано чи пізно вона знадобиться — додай картку й посилання, коли запишеш</Tip>
      </div>
    </Clamp>
  </section>
</template>
