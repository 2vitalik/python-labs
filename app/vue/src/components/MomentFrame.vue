<script setup>
import { ref } from 'vue'

import GrowArea from '@core/components/GrowArea.vue'
import { useMomentEd } from '../momentEd.js'
import MomentPalette from './MomentPalette.vue'
import MomentResize from './MomentResize.vue'
import MomentTools from './MomentTools.vue'

// the frame in work (T276): the caption — written to stand before the picture, as on the page; the tools and the brushes
// right over the field, the field with its size controls (T294 §19: what is chosen sits next to where it is drawn); the
// note — a grey quote under the picture, behind «＋ примітка»
const ed = useMomentEd()
const noting = ref(!!ed.frame.note)  // a note emptied while typing keeps its field
</script>

<template>
  <div class="frame fit-box">
    <div class="label">Кадр {{ ed.at + 1 }} із {{ ed.scenario.frames.length }}</div>
    <GrowArea v-model="ed.frame.caption" class="form-control form-control-sm mb-2" placeholder="Підпис: що сталося на цьому кроці (markdown)" />
    <div class="vstack gap-1 mb-1">
      <MomentTools />
      <MomentPalette />
    </div>
    <div><MomentResize /></div>
    <GrowArea v-if="noting || ed.frame.note" v-model="ed.frame.note" class="form-control form-control-sm mt-2"
              placeholder="Примітка під кадром — сірою цитатою (markdown)" />
    <button v-else type="button" class="more-field mt-2" @click="noting = true">＋ примітка</button>
  </div>
</template>

<style scoped>
.frame { padding: .6rem; border: 1px solid var(--bs-border-color); border-radius: .45rem; }
.label { font-size: .7rem; font-weight: 700; letter-spacing: .04em; text-transform: uppercase; color: var(--bs-secondary-color); margin-bottom: .3rem; }
</style>
