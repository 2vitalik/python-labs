<script setup>
import { computed } from 'vue'

import Clamp from '@core/components/Clamp.vue'
import { kindOf } from '../catalog.js'
import { useEd } from '../ed.js'
import { isFolded, isShort, setShort } from '../fold.js'
import CardPicker from './CardPicker.vue'
import SectionHead from './SectionHead.vue'
import SubzoneRows from './SubzoneRows.vue'

// a section about the game as a whole (T270 §11): the game's own cards of its zones by subzone and «＋ картка» limited
// to them; `z` — the section (sections.js ZONES), `head` — its heading as the editor words it
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
    <SectionHead v-bind="head" />
    <Clamp v-show="!isFolded(head.fold)" :on="isShort(head.fold)" @open="setShort(head.fold, false)">
      <div class="vstack gap-2">
        <SubzoneRows v-if="claims.length" :claims :table="z.table" />
        <div v-else class="text-secondary small">{{ z.hint }}</div>
        <div v-if="noVideo" class="ask">🎬 Відео-демки ще нема: рано чи пізно вона знадобиться — додай картку й посилання, коли запишеш</div>
        <div v-if="ed.editable"><CardPicker :kinds="['game']" :anchor="{}" label="картка" :filter="here" /></div>
      </div>
    </Clamp>
  </section>
</template>

<style scoped>
.ask { padding: .25rem .5rem; border: 1px dashed var(--bs-border-color); border-radius: .3rem; color: var(--bs-secondary-color); font-size: .8rem; }
</style>
