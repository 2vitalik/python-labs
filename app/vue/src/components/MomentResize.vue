<script setup>
import { computed, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import Pop from '@core/components/Pop.vue'
import { useMomentEd } from '../momentEd.js'
import { resize } from '../momentsEdit.js'
import MomentGrid from './MomentGrid.vue'

// the field with its size around it (T276): «＋ / −» a row or a column at each side. With more frames in the scenario a
// panel under the field asks whether they all change — the frames of one story usually share one field
const ed = useMomentEd()
const SIDES = { top: 'зверху', bottom: 'знизу', left: 'ліворуч', right: 'праворуч' }
const ask = ref(null)  // { side, d } waiting for the answer
const open = computed({ get: () => !!ask.value, set: (v) => !v && (ask.value = null) })
const size = computed(() => `${Math.max(0, ...ed.frame.grid.map((row) => row.length))} × ${ed.frame.grid.length}`)
function go(side, d) {
  if (ed.scenario.frames.length > 1) return (ask.value = { side, d })
  ed.snap()
  resize(ed.frame, side, d, ed.empty)
}
function apply(all) {
  const { side, d } = ask.value
  ed.snap()
  for (const f of all ? ed.scenario.frames : [ed.frame]) resize(f, side, d, ed.empty)
  ask.value = null
}
const what = (a) => `${a.d > 0 ? 'Додати' : 'Прибрати'} ${a.side === 'top' || a.side === 'bottom' ? 'ряд' : 'стовпець'} ${SIDES[a.side]}`
</script>

<template>
  <Pop v-model="open" width="19rem">
    <template #trigger>
      <div class="sized">
        <div v-for="(label, side) in SIDES" :key="side" class="side" :class="side">
          <button type="button" class="sz" :title="`＋ ${side === 'top' || side === 'bottom' ? 'ряд' : 'стовпець'} ${label}`" @click="go(side, 1)"><Icon name="plus" /></button>
          <button type="button" class="sz" :title="`− ${side === 'top' || side === 'bottom' ? 'ряд' : 'стовпець'} ${label}`" @click="go(side, -1)"><Icon name="minus" /></button>
          <span v-if="side === 'bottom'" class="dim">{{ size }}</span>
        </div>
        <MomentGrid class="mid" />
      </div>
    </template>
    <template v-if="ask">
      <div class="mb-2">{{ what(ask) }} — усім кадрам сценарію ({{ ed.scenario.frames.length }}) чи лише цьому?</div>
      <div class="d-flex flex-wrap gap-2">
        <button type="button" class="btn btn-sm btn-success" @click="apply(true)"><Icon name="check" /> усім кадрам</button>
        <button type="button" class="btn btn-sm btn-outline-success" @click="apply(false)">лише цьому</button>
        <button type="button" class="btn btn-sm btn-outline-secondary" @click="open = false">Скасувати</button>
      </div>
    </template>
  </Pop>
</template>

<style scoped>
.sized { display: grid; grid-template: '. top .' auto 'left mid right' auto '. bottom .' auto / auto auto auto; gap: .15rem; }
.mid { grid-area: mid; }
.side { display: flex; align-items: center; justify-content: center; gap: .1rem; }
.top { grid-area: top; }
.bottom { grid-area: bottom; }
.left, .right { flex-direction: column; }
.left { grid-area: left; }
.right { grid-area: right; }
.sz { display: inline-flex; align-items: center; justify-content: center; width: 1.25rem; height: 1.25rem; padding: 0; border: 0; border-radius: .25rem;
      background: none; color: var(--bs-secondary-color); font-size: .7rem; opacity: .6; }
.sz:hover { background: var(--bs-tertiary-bg); color: var(--bs-body-color); opacity: 1; }
.dim { margin-left: .4rem; font-size: .7rem; color: var(--bs-secondary-color); font-variant-numeric: tabular-nums; }
</style>
