<script setup>
import GrowArea from '@core/components/GrowArea.vue'
import Tip from '@core/components/Tip.vue'
import { makeMomentEd } from '../momentEd.js'
import MomentFrame from './MomentFrame.vue'
import MomentStrip from './MomentStrip.vue'
import MomentTabs from './MomentTabs.vue'

// the editor of game moments (T276 «Редактор кадрів», T291 §15): a form over the examples text — the scenarios, the strip
// of frames and the frame in work with its brushes (the legend) over the field, drawn with the mouse or a finger. In: Markdown,
// out: the same Markdown (momentsText.js), nothing else is stored. `palette` [{ icon, name }] — brushes ahead of the
// legend (a student's game: its entities), `empty` — what the eraser leaves; then the text before the frames is not
// asked for. Text the frames do not claim is shown grey and left as it is
const text = defineModel({ type: String, default: '' })
const props = defineProps({ palette: Array, empty: String })
const ed = makeMomentEd(text, () => props.palette, () => props.empty)
</script>

<template>
  <div class="vstack gap-3">
    <Tip id="moments-editor">
      Обери значок над полем і малюй мишкою чи пальцем; відро — заливка. «＋ кадр» копіює поточний — зміни клітину-дві й допиши
      підпис. Синя рамка — хто щойно ходив, жовта — що змінилось; з ✦ жовта ставиться сама. Помилився — ↶ або Ctrl+Z.
    </Tip>
    <div v-if="!palette || ed.model.notes">
      <div class="label">Особливості та інше до кадрів</div>
      <GrowArea v-model="ed.model.notes" class="form-control form-control-sm font-monospace" spellcheck="false"
                placeholder="**Особливості** — markdown, як на сторінці гри" />
    </div>
    <div v-if="ed.model.before" class="loose"><div class="label">текст до легенди</div>{{ ed.model.before }}</div>
    <div>
      <MomentTabs />
      <MomentStrip />
    </div>
    <MomentFrame v-if="ed.frame" :key="`${ed.sc}-${ed.at}`" />
    <div v-if="ed.scenario?.tail" class="loose">
      <div class="label">текст після кадрів — править вигляд «текст»</div>{{ ed.scenario.tail }}
    </div>
  </div>
</template>

<style scoped>
.label { font-size: .7rem; font-weight: 700; letter-spacing: .04em; text-transform: uppercase; color: var(--bs-secondary-color); margin-bottom: .2rem; }
.loose { padding: .4rem .6rem; border-radius: .375rem; background: var(--bs-tertiary-bg); color: var(--bs-secondary-color);
         font-size: .8rem; white-space: pre-wrap; }
</style>
