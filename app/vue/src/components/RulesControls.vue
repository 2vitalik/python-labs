<script setup>
import { computed } from 'vue'

import Icon from '@core/components/Icon.vue'
import { vocab } from '../catalog.js'
import { useEd } from '../ed.js'
import { clauses } from '../rules.js'
import { marks } from '../ruleSides.js'
import { isControl, spans, whoPiece } from '../ruleViews.js'
import Pieces from './Pieces.vue'
import './ruleTable.css'

// «Керування» (T274 §6): the rules a player's action starts — the action, for whom, if what, then what; the rows of one
// action side by side under one cell. A row emits show(id); in the editor «＋ дія» emits add(prefill) of an input rule
const emit = defineEmits(['show', 'add'])
const ed = useEd()
const action = (r) => String(r.when.action ?? '').trim().toLowerCase()
const rows = computed(() => {
  const list = ed.rules.filter(isControl)
  const order = [...new Set(list.map(action))]
  const out = list.map((r) => ({ r, c: clauses(r, ed.parts), who: r.when.a ? [{ ...whoPiece(r.when.a, r.when, ed.parts), sub: marks(r).a, sd: 'a' }] : [] }))
  return spans(out.sort((x, y) => order.indexOf(action(x.r)) - order.indexOf(action(y.r))), (x) => action(x.r))
})
// the field's own «Керування», by its options' names
const control = computed(() => {
  const spec = vocab.value.field.find((s) => s.key === 'control')
  return [].concat(ed.field?.props?.control || []).map((v) => {
    const o = spec?.options?.[v]
    return o?.label ? [o.icon, o.label].filter(Boolean).join(' ') : o || v
  }).join(' · ')
})
</script>

<template>
  <div>
    <div v-if="control" class="rtab-note">Керування в полі: <span class="text-body">{{ control }}</span></div>
    <div class="rtab-box">
      <table class="rtab">
        <thead>
          <tr><th scope="col">дія гравця</th><th scope="col">для кого</th><th scope="col">якщо</th><th scope="col">то</th></tr>
        </thead>
        <tbody>
          <tr v-for="(x, i) in rows" :key="x.r.id" class="go" tabindex="0" title="показати в списку"
              @click="emit('show', x.r.id)" @keydown.enter="emit('show', x.r.id)">
            <td v-if="x.span" :rowspan="x.span" :class="{ last: i + x.span === rows.length }"><span class="key">{{ x.r.when.action }}</span></td>
            <td><Pieces :list="x.who" /></td>
            <td class="wide"><Pieces v-for="(ps, j) in x.c.cond" :key="j" :list="ps" class="d-block" /></td>
            <td class="wide"><Pieces v-for="(ps, j) in x.c.then" :key="j" :list="ps" class="d-block" /></td>
          </tr>
        </tbody>
      </table>
    </div>
    <button v-if="ed.editable" type="button" class="btn btn-sm btn-add mt-2" @click="emit('add', { when: { kind: 'input' } })"><Icon name="plus" /> дія</button>
  </div>
</template>

<style scoped>
/* what the player presses, as a key */
.key { display: inline-block; padding: 0 .4rem; border: 1px solid var(--bs-border-color); border-bottom-width: 2px; border-radius: .3rem;
       background: var(--bs-body-bg); font-weight: 600; line-height: 1.6; }
</style>
