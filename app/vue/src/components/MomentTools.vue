<script setup>
import { ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import Pop from '@core/components/Pop.vue'
import { useMomentEd } from '../momentEd.js'
import { paste } from '../momentsEdit.js'

// the tools beside the field (T276): paint with the brush, the blue «хто ходив» and the yellow «що змінилось» frames, the
// eraser — the empty cell; «підсвітити зміни» puts the yellow frame by itself as you draw; «вставити текстом» takes a
// ready block of emoji (from Notion, from the game's console) in place of this frame's field. A level's map (`single`) has
// no marks: only the brush and the eraser
const ed = useMomentEd()
const TOOLS = [['paint', 'малювати'], ['who', 'хто ходив'], ['new', 'що змінилось'], ['erase', 'гумка']]
const open = ref(false)
const text = ref('')
const bad = ref(false)
function save() {
  bad.value = !paste(ed.frame, text.value)
  if (bad.value) return
  open.value = false
  text.value = ''
}
</script>

<template>
  <div class="tools vstack gap-2">
    <div class="btn-group-vertical btn-group-sm" role="group" aria-label="інструмент">
      <button v-for="[k, label] in TOOLS.filter(([t]) => !ed.single || t === 'paint' || t === 'erase')" :key="k" type="button"
              class="btn btn-outline-secondary tool" :class="{ active: ed.tool === k }" :title="k === 'erase' ? `лишає порожню клітину ${ed.empty}` : ''" @click="ed.tool = k">
        <span class="sw" :class="k"><Icon v-if="k === 'erase'" name="eraser" /><template v-else-if="k === 'paint'">{{ ed.brush }}</template></span> {{ label }}
      </button>
    </div>
    <label v-if="!ed.single" class="form-check small mb-0" title="клітина, що не така, як у попередньому кадрі, сама бере жовту рамку; та, що стала порожньою, — ні">
      <input type="checkbox" class="form-check-input" :checked="ed.highlight" @change="ed.setHighlight($event.target.checked)"> підсвітити зміни
    </label>
    <Pop v-model="open" width="22rem">
      <template #trigger="{ toggle }">
        <button type="button" class="more-field" @click="toggle">вставити текстом</button>
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
.tools { width: 10rem; }
.tool { display: flex; align-items: center; gap: .4rem; text-align: start; }
.sw { display: inline-flex; align-items: center; justify-content: center; width: 1.3rem; height: 1.3rem; flex-shrink: 0; border-radius: .25rem; font-size: .85rem; line-height: 1; }
.sw.who { box-shadow: inset 0 0 0 2px var(--bs-primary); }
.sw.new { box-shadow: inset 0 0 0 2px var(--bs-warning); }
</style>
