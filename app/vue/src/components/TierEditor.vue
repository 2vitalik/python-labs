<script setup>
import { computed } from 'vue'

import Icon from '@core/components/Icon.vue'
import Tip from '@core/components/Tip.vue'
import { ladder } from '../tiers.js'

// a card's price steps (T291 §13): a row a step «до [N]-ї — × [множник]», the last one may go on with no end; under them —
// the ladder as the card will show it. v-model — the [[upto, factor], …] list, written in place; [] — no steps any more
const tiers = defineModel({ type: Array, required: true })
defineProps({ amount: Number })
const last = (i) => i === tiers.value.length - 1
const topN = (skip) => Math.max(0, ...tiers.value.filter((t) => t !== skip).map((t) => Number(t[0]) || 0))
const lines = computed(() => ladder({ tiers: tiers.value.map(([u, f]) => [Number(u) || 0, Number(f) || 0]) }))

function add() {
  const end = tiers.value.at(-1)
  const step = [topN() + 3, end?.[1] ?? 1]
  if (end && end[0] === 0) tiers.value.splice(-1, 0, step)
  else tiers.value.push(step)
}
function setEndless(t, on) {
  t[0] = on ? 0 : topN(t) + 3
}
</script>

<template>
  <div class="vstack gap-1">
    <Tip id="tiers-how">Картку можна заявити кілька разів, і що далі — то дешевше: перші N за повну ціну, наступні — за частку.
      Остання сходинка без номера — «далі без межі».</Tip>
    <div v-for="(t, i) in tiers" :key="i" class="step">
      <template v-if="last(i) && t[0] === 0"><span class="far">далі</span></template>
      <template v-else>до <input v-model.number="t[0]" type="number" min="1" class="form-control form-control-sm n">-ї</template>
      <span>— ×</span>
      <input v-model.number="t[1]" type="number" min="0.05" max="1" step="0.05" class="form-control form-control-sm n">
      <label v-if="last(i)" class="endless">
        <input type="checkbox" class="form-check-input m-0" :checked="t[0] === 0" @change="setEndless(t, $event.target.checked)"> далі без межі
      </label>
      <button type="button" class="iact del" title="Прибрати сходинку" @click="tiers.splice(i, 1)"><Icon name="minus" /></button>
    </div>
    <div class="d-flex align-items-center gap-3">
      <button type="button" class="iact add" title="＋ сходинка" @click="add"><Icon name="plus" /></button>
      <button type="button" class="more-field" @click="tiers = []">прибрати сходинки</button>
    </div>
    <div class="sum">
      <div v-for="l in lines" :key="l">{{ l }}</div>
    </div>
  </div>
</template>

<style scoped>
.step { display: flex; flex-wrap: wrap; align-items: center; gap: .3rem; }
.n { width: 4rem; }
/* «далі» stands where the number would: the multipliers stay in one column */
.far { display: inline-block; width: calc(4rem + 2.4em); }
.endless { display: inline-flex; align-items: center; gap: .25rem; margin: 0 0 0 .3rem; font-size: .75rem; color: var(--bs-secondary-color); }
.sum { font-size: .75rem; line-height: 1.3; color: var(--bs-secondary-color); }
</style>
