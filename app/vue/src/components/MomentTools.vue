<script setup>
import { ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import Pop from '@core/components/Pop.vue'
import { useMomentEd } from '../momentEd.js'
import { paste } from '../momentsEdit.js'

// the tools over the field in one quiet row (T276, T294 §19): paint with the brush, fill a patch of alike cells, the blue
// «хто ходив» and the yellow «що змінилось» frames, the eraser — each a drawing that names itself under the mouse. Then:
// «підсвічувати зміни» (the yellow frame put by itself as you draw), «↶» (Ctrl+Z on the field), «очистити кадр»,
// «вставити текстом» — a ready block of emoji in place of this frame's field. A level's map (`single`) has no marks
const ed = useMomentEd()
const TOOLS = [['paint', 'малювати пензлем'], ['fill', 'заливка: клітина й усі такі самі поруч'], ['who', 'синя рамка: хто ходив'], ['new', 'жовта рамка: що змінилось'], ['erase', 'гумка']]
const open = ref(false)
const text = ref('')
const bad = ref(false)
function save() {
  ed.snap()
  bad.value = !paste(ed.frame, text.value)
  if (bad.value) return
  open.value = false
  text.value = ''
}
</script>

<template>
  <div class="tools">
    <span class="seg" role="group" aria-label="інструмент">
      <button v-for="[k, label] in TOOLS.filter(([t]) => !ed.single || (t !== 'who' && t !== 'new'))" :key="k" type="button" class="tool qtip"
              :class="{ on: ed.tool === k }" :aria-pressed="ed.tool === k" :data-tip="k === 'erase' ? `${label}: лишає ${ed.empty}` : label" @click="ed.tool = k">
        <span class="sw" :class="k">
          <Icon v-if="k === 'erase'" name="eraser" /><Icon v-else-if="k === 'fill'" name="bucket" /><template v-else-if="k === 'paint'">{{ ed.brush }}</template>
        </span>
      </button>
    </span>
    <span class="sep" />
    <button v-if="!ed.single" type="button" class="iact qtip" :class="{ on: ed.highlight }" :aria-pressed="ed.highlight"
            :data-tip="ed.highlight ? 'зміни підсвічуються самі — вимкнути' : 'підсвічувати зміни жовтим самому'" @click="ed.setHighlight(!ed.highlight)"><Icon name="spark" /></button>
    <button type="button" class="iact qtip" :disabled="!ed.steps" data-tip="крок назад (Ctrl+Z)" aria-label="крок назад" @click="ed.undo()"><Icon name="back" /></button>
    <button type="button" class="iact qtip" data-tip="очистити кадр — лишаються порожні клітини" aria-label="очистити кадр" @click="ed.clear()"><Icon name="broom" /></button>
    <Pop v-model="open" width="22rem">
      <template #trigger="{ toggle }">
        <button type="button" class="more-field ms-1" @click="toggle">вставити текстом</button>
      </template>
      <div class="vstack gap-2">
        <textarea v-model="text" class="form-control form-control-sm font-monospace" rows="6" spellcheck="false"
                  placeholder="⬛ ⬛ ⬛&#10;⬛ 😎 ⬛&#10;емодзі через пробіл, ряд — рядок"></textarea>
        <div class="small text-secondary">Замінить поле цього кадру; [😎] — хто ходив, (✨) — що змінилось.</div>
        <div v-if="bad" class="text-danger small">Тут не видно жодного ряду клітин</div>
        <div class="d-flex gap-2">
          <button type="button" class="btn btn-sm btn-success" :disabled="!text.trim()" @click="save"><Icon name="check" /> Зберегти</button>
          <button type="button" class="btn btn-sm btn-outline-secondary" @click="open = false">Скасувати</button>
        </div>
      </div>
    </Pop>
  </div>
</template>

<style scoped>
.tools { display: flex; flex-wrap: wrap; align-items: center; gap: .15rem; }
.seg { display: inline-flex; padding: .1rem; border: 1px solid var(--bs-border-color); border-radius: .45rem; gap: .1rem; }
.tool { display: inline-flex; align-items: center; justify-content: center; width: 1.9rem; height: 1.75rem; padding: 0; border: 0; border-radius: .3rem;
        background: none; color: var(--bs-secondary-color); }
.tool:hover { background: var(--bs-tertiary-bg); color: var(--bs-body-color); }
.tool.on { background: color-mix(in srgb, var(--bs-primary) 14%, transparent); color: var(--bs-body-color); }
.sw { display: inline-flex; align-items: center; justify-content: center; width: 1.25rem; height: 1.25rem; border-radius: .25rem; font-size: .95rem; line-height: 1; }
.sw.who { box-shadow: inset 0 0 0 2px var(--bs-primary); }
.sw.new { box-shadow: inset 0 0 0 2px var(--bs-warning); }
.sep { width: 1px; height: 1.3rem; margin: 0 .3rem; background: var(--bs-border-color); }
.iact.on { background: color-mix(in srgb, var(--bs-warning) 22%, transparent); color: var(--bs-warning-text-emphasis); }
.iact:disabled { opacity: .35; }
</style>
