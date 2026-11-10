<script setup>
import { computed } from 'vue'

import Icon from '@core/components/Icon.vue'
import { iconOf, kindOf } from '../catalog.js'
import { useEd } from '../ed.js'
import { sentence } from '../rules.js'

// where a claim may go, by its card's kind (T270 §6): a mechanic — to an entity, an element — to a window, a rule card —
// to a rule…; the current place is marked and cannot be picked. Emits pick({ part, rule })
const props = defineProps({ claim: Object })
const emit = defineEmits(['pick', 'rule'])  // rule — «there is no such rule yet: start one from this card»
const ed = useEd()
const kind = computed(() => kindOf(ed.info(props.claim.task)))
const GROUP = { mechanic: 'Сутності', element: 'Вікна', field: 'Поле', level: 'Рівні', rule: 'Правила' }
const EMPTY = { mechanic: 'Сутностей', element: 'Вікон', field: 'Поля', rule: 'Правил' }
const cut = (s, n = 64) => (s.length > n ? `${s.slice(0, n - 1)}…` : s)
const ruleText = (r) => {
  const s = sentence(r, ed.parts)
  return cut(`коли ${s.when}${s.cond ? `, якщо ${s.cond}` : ''}, то ${s.then}`)
}
const onPart = (p) => ({ key: p.id, text: `${iconOf(p)} ${p.title}`, to: { part: p.id, rule: '' } })
const places = computed(() => {
  switch (kind.value) {
    case 'mechanic': return ed.entities.map(onPart)
    case 'element': return ed.windows.map(onPart)
    case 'field': return ed.field ? [onPart(ed.field)] : []
    case 'level': return [{ key: '', text: '🪜 секція «Рівні»', to: { part: '', rule: '' } }, ...ed.levels.map(onPart)]
    case 'rule': return ed.rules.map((r) => ({ key: r.id, text: ruleText(r), to: { part: '', rule: r.id } }))
    default: return []
  }
})
const now = computed(() => ({ part: props.claim.part || '', rule: props.claim.rule || '' }))
const isNow = (to) => to.part === now.value.part && to.rule === now.value.rule
// for a level card «unanchored» is the section itself, offered above
const unbind = computed(() => (now.value.part || now.value.rule) && kind.value !== 'level')
</script>

<template>
  <div class="move">
    <div v-if="kind === 'game'" class="text-secondary small">Картка гри загалом живе в секції своєї зони — обирати нічого.</div>
    <template v-else-if="GROUP[kind]">
      <div class="grp">{{ GROUP[kind] }}</div>
      <div v-if="!places.length" class="text-secondary small px-2">{{ EMPTY[kind] }} ще нема — спершу додай</div>
    </template>
    <div class="list">
      <button v-for="p in places" :key="p.key" type="button" class="place" :disabled="isNow(p.to)" @click="emit('pick', p.to)">
        <span class="txt">{{ p.text }}</span>
        <span v-if="isNow(p.to)" class="here"><Icon name="done" /> тут</span>
      </button>
    </div>
    <button v-if="kind === 'rule'" type="button" class="place new" @click="emit('rule')"><Icon name="plus" /> нове правило з цієї картки</button>
    <button v-if="unbind" type="button" class="place mt-1" @click="emit('pick', { part: '', rule: '' })">📥 у чернетки — відвʼязати</button>
  </div>
</template>

<style scoped>
.move { padding: .3rem 0; border-radius: .3rem; background: var(--bs-tertiary-bg); }
.grp { margin: 0 .5rem .1rem; font-size: .65rem; font-weight: 700; letter-spacing: .04em; text-transform: uppercase; color: var(--bs-secondary-color); }
.list { max-height: 12rem; overflow-y: auto; }
.place { display: flex; align-items: baseline; gap: .4rem; width: 100%; padding: .2rem .5rem; border: 0; background: none; color: inherit;
         text-align: start; font-size: .82rem; }
.place:hover:not(:disabled) { background: var(--bs-secondary-bg); }
.place:disabled { color: var(--bs-secondary-color); }
.place.new { color: var(--act-add); }
.txt { flex-grow: 1; min-width: 0; }
.here { flex-shrink: 0; font-size: .72rem; color: var(--bs-success); }
</style>
