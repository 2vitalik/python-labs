<script setup>
import { computed } from 'vue'

import { useEd } from '../ed.js'
import { clauses } from '../rules.js'
import AiCards from './AiCards.vue'
import Pieces from './Pieces.vue'

// a proposed rule read as RuleText reads (T270 §4.1): КОЛИ / ЯКЩО / ТО in the keyword column, the sentence built by
// rules.js. The node names entities and windows by title, so the renderer gets a stand-in part per name, its id the name
// itself (contract §8). A thing already in the game keeps its own id after — its card under the mouse, a click goes to
// it; a proposed one stays a plain frame, there is nowhere to go yet. `draft` — for the titles proposed beside it
const props = defineProps({ data: Object, draft: Object })
const ed = useEd()
const rule = computed(() => ({ cond: [], then: [], ...props.data }))
const same = (a, b) => String(a).toLowerCase() === String(b).toLowerCase()
const names = computed(() => [rule.value.when, ...rule.value.cond, ...rule.value.then].flatMap((x) => Object.values(x || {})).filter((v) => typeof v === 'string'))
const parts = computed(() => names.value.map((n) => {
  const p = ed.parts.find((x) => x.title && same(x.title, n))
  if (p) return { ...p, id: n, real: p.id }
  const it = props.draft.items.find((x) => (x.group === 'entity' || x.group === 'window') && same(x.data.title || '', n))
  return { kind: it?.group || 'entity', ...it?.data, title: it?.data.title || n, id: n }
}))
const fix = (ps) => ps.map((p) => {
  if (!p.id) return p
  const real = parts.value.find((x) => x.id === p.id)?.real
  return real ? { ...p, id: real } : { ...p, id: undefined, t: 'ent', v: [p.icon, p.v].filter(Boolean).join(' '), tip: 'ще не в грі' }
})
const c = computed(() => {
  const all = clauses(rule.value, parts.value)
  return { when: fix(all.when), cond: all.cond.map(fix), then: all.then.map(fix) }
})
const lead = (ps) => !!ps[0]?.lead
</script>

<template>
  <div class="vstack gap-1">
    <div class="rule-text">
      <span class="kw when">КОЛИ</span><Pieces :list="c.when" />
      <template v-for="(ps, i) in c.cond" :key="`c${i}`">
        <span class="kw if">{{ i ? 'ТА' : 'ЯКЩО' }}<span v-if="lead(ps)" class="kw-not"> НЕ</span></span><Pieces :list="lead(ps) ? ps.slice(1) : ps" />
      </template>
      <template v-for="(ps, i) in c.then" :key="`t${i}`">
        <span class="kw then">{{ i ? '' : 'ТО' }}</span><Pieces :list="ps" />
      </template>
      <template v-if="rule.note">
        <span class="kw note" title="нотатка">💬</span><span class="note-text">{{ rule.note }}</span>
      </template>
    </div>
    <AiCards :list="rule.claims" />
  </div>
</template>
