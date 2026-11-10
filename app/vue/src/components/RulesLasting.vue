<script setup>
import { computed } from 'vue'

import { statOf } from '../catalog.js'
import { useEd } from '../ed.js'
import { jump } from '../jump.js'
import { lasting, timedStats, whenText, whoPiece } from '../ruleViews.js'
import Pieces from './Pieces.vue'
import './ruleTable.css'

// «Що скільки триває» (T274 §6): the effects that last, from any rule, then the entities' stats measured in time.
// A rule's row emits show(id), a stat's leads to its entity; nothing to say — nothing shown
const emit = defineEmits(['show'])
const ed = useEd()
const rows = computed(() => [
  ...ed.rules.flatMap((r) => r.then.filter(lasting).map((e, i) => ({
    key: `r${r.id}-${i}`, go: () => emit('show', r.id), tip: 'показати правило в списку', who: whoPiece(e.a, r.when, ed.parts),
    what: e.kind === 'stun' ? [{ t: 'word', v: 'завмирає' }] : [{ t: 'word', v: 'стає' }, { t: 'state', v: e.s }],
    n: e.kind === 'stun' ? e.n : e.dur, unit: 'тіків', from: `КОЛИ ${whenText(r, ed.parts)}`,
  }))),
  ...timedStats(ed.entities).map(({ p, s, unit }) => ({
    key: `p${p.id}-${s.key}`, go: () => jump(`p-${p.id}`), tip: 'показати сутність', who: whoPiece(p.id, null, ed.parts),
    what: [{ t: 'name', v: `${statOf(s.key)?.icon || ''} ${s.label || s.key}`.trim() }], n: s.value, unit, from: 'параметр сутності',
  })),
])
</script>

<template>
  <div v-if="rows.length">
    <div class="rtab-cap">Що скільки триває</div>
    <div class="rtab-box">
      <table class="rtab">
        <thead>
          <tr><th scope="col">хто</th><th scope="col">що</th><th scope="col">скільки</th><th scope="col">звідки</th></tr>
        </thead>
        <tbody>
          <tr v-for="x in rows" :key="x.key" class="go" tabindex="0" :title="x.tip" @click="x.go()" @keydown.enter="x.go()">
            <td><Pieces :list="[x.who]" /></td>
            <td><Pieces :list="x.what" /></td>
            <td class="text-nowrap"><span class="num">{{ x.n }}</span> {{ x.unit }}</td>
            <td class="muted">{{ x.from }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
