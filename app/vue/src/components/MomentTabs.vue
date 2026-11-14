<script setup>
import { ref } from 'vue'

import DelButton from '@core/components/DelButton.vue'
import Icon from '@core/components/Icon.vue'
import Pop from '@core/components/Pop.vue'
import { useMomentEd } from '../momentEd.js'

// the scenarios of a game's moments (T276 «Показ»): tabs, each a «### » heading in the text; the tab in work is renamed
// in a panel and deleted with a question. A single untitled scenario shows no tabs — only «＋ сценарій»
const ed = useMomentEd()
const open = ref(false)
const name = ref('')
const pick = (i) => Object.assign(ed, { sc: i, at: 0 })
function rename() {
  const t = name.value.trim()
  if (!t && ed.sc) return  // only the first scenario may go without a heading: another would melt into the one before
  ed.scenario.title = t
  open.value = false
}
const label = (s, i) => s.title || `Сценарій ${i + 1}`
</script>

<template>
  <div class="d-flex flex-wrap align-items-end gap-1 mb-2">
    <template v-if="ed.model.scenarios.length > 1 || ed.scenario?.title">
      <span v-for="(s, i) in ed.model.scenarios" :key="i" class="tab" :class="{ on: i === ed.sc }">
        <button type="button" class="pick" @click="pick(i)">{{ label(s, i) }}</button>
        <template v-if="i === ed.sc">
          <Pop v-model="open" width="18rem">
            <template #trigger>
              <button type="button" class="iact" title="перейменувати сценарій" @click="name = s.title; open = !open"><Icon name="pencil" /></button>
            </template>
            <div class="vstack gap-2" @keydown.enter.prevent="rename">
              <input v-model="name" class="form-control form-control-sm" placeholder="Звичайний хід, глухий кут, перемога…">
              <div class="d-flex gap-2">
                <button type="button" class="btn btn-sm btn-success" :disabled="!name.trim() && ed.sc > 0" @click="rename"><Icon name="check" /> Зберегти</button>
                <button type="button" class="btn btn-sm btn-outline-secondary" @click="open = false">Скасувати</button>
              </div>
            </div>
          </Pop>
          <DelButton :what="`сценарій «${label(s, i)}»`" :note="`разом з його кадрами (${s.frames.length})`" @yes="ed.dropScenario(i)" />
        </template>
      </span>
    </template>
    <button type="button" class="btn btn-sm btn-add ms-1" title="нова історія на тому ж полі: перемога, глухий кут…" @click="ed.addScenario()">
      <Icon name="plus" /> сценарій</button>
  </div>
</template>

<style scoped>
.tab { display: inline-flex; align-items: center; gap: .1rem; padding: .15rem .35rem; border-bottom: 2px solid transparent; }
.tab.on { border-bottom-color: var(--bs-body-color); }
.pick { padding: 0 .2rem; border: 0; background: none; color: var(--bs-secondary-color); font-size: .875rem; }
.tab.on .pick { color: var(--bs-body-color); font-weight: 600; }
.tab .iact { width: 1.35rem; height: 1.35rem; font-size: .75rem; }
</style>
