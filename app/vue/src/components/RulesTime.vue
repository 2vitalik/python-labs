<script setup>
import { computed } from 'vue'

import Icon from '@core/components/Icon.vue'
import { useEd } from '../ed.js'
import { clauses, plain } from '../rules.js'
import { isTimed, spans, TIME_KINDS } from '../ruleViews.js'
import Pieces from './Pieces.vue'
import RulesLasting from './RulesLasting.vue'
import './ruleTable.css'

// «Час» (T274 §6): what happens when — the rules time starts, from the tick's phases to a turn's end, the shorter period
// first — and below it what lasts how long. A row emits show(id); in the editor «＋ правило за часом» emits add(prefill)
const emit = defineEmits(['show', 'add'])
const ed = useEd()
const phases = computed(() => ed.game?.phases || [])
const phaseAt = (name) => {
  const i = phases.value.findIndex((p) => p.toLowerCase() === String(name ?? '').trim().toLowerCase())
  return i < 0 ? phases.value.length : i
}
// within one trigger: phases in the game's order, the shorter period first, the likelier first
const WITHIN = { phase_start: (w) => phaseAt(w.phase), timer: (w) => +w.every || 0, idle: (w) => +w.n || 0, rng: (w) => -w.p || 0 }
const rank = (w) => [TIME_KINDS.indexOf(w.kind), WITHIN[w.kind]?.(w) ?? 0]
const rows = computed(() => {
  const list = ed.rules.filter(isTimed).map((r) => ({ r, c: clauses(r, ed.parts), k: rank(r.when) }))
  list.sort((x, y) => x.k[0] - y.k[0] || x.k[1] - y.k[1])
  return spans(list, (x) => plain(x.c.when))
})
</script>

<template>
  <div>
    <div class="rtab-cap">Що коли відбувається</div>
    <div v-if="phases.length" class="rtab-note">🔁 За один тік: {{ phases.map((p, i) => `${i + 1} ${p}`).join(' → ') }}</div>
    <div v-if="rows.length" class="rtab-box">
      <table class="rtab">
        <thead>
          <tr><th scope="col">коли</th><th scope="col">якщо</th><th scope="col">то</th></tr>
        </thead>
        <tbody>
          <tr v-for="(x, i) in rows" :key="x.r.id" class="go" tabindex="0" title="показати в списку"
              @click="emit('show', x.r.id)" @keydown.enter="emit('show', x.r.id)">
            <td v-if="x.span" :rowspan="x.span" :class="{ last: i + x.span === rows.length }"><Pieces :list="x.c.when" /></td>
            <td class="wide"><Pieces v-for="(ps, j) in x.c.cond" :key="j" :list="ps" class="d-block" /></td>
            <td class="wide"><Pieces v-for="(ps, j) in x.c.then" :key="j" :list="ps" class="d-block" /></td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else class="rtab-note">Правил, які запускає час, поки нема.</div>
    <button v-if="ed.editable" type="button" class="btn btn-sm btn-add mt-2" @click="emit('add', { when: { kind: 'timer' } })"><Icon name="plus" /> правило за часом</button>
    <RulesLasting class="mt-3" @show="(id) => emit('show', id)" />
  </div>
</template>
