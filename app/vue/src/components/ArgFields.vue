<script setup>
import { computed } from 'vue'

import { roleOf, vocab } from '../catalog.js'

// inputs for a word's arguments, writing straight into `item`: entities and windows of the game, numbers, choices,
// texts with hints (states of the named entity, stat names, typical inputs, the game's phases)
const props = defineProps({ spec: Object, item: Object, parts: Array, sides: { type: Array, default: () => ['*'] }, game: Object })
const entities = computed(() => props.parts.filter((p) => p.kind === 'entity'))
const windows = computed(() => props.parts.filter((p) => p.kind === 'window'))
const ACTIONS = ['стрілки', 'пробіл', 'Enter', 'Esc', 'клік по клітині', 'правий клік', 'подвійний клік', 'свайп', 'перетягування', 'колесо миші', 'клавіша дії']
const stateNames = computed(() => {
  const ref = props.item.a
  const own = entities.value.find((p) => p.id === ref)?.states
  return own?.length ? own : [...new Set(entities.value.flatMap((p) => p.states))]
})
const counterNames = computed(() => [...new Set([...entities.value.flatMap((p) => p.stats.map((s) => s.label || s.key)), 'очки', 'час', 'рівень', 'комбо'])])
const hints = (name) => ({ s: stateNames.value, name: counterNames.value, action: ACTIONS, phase: props.game?.phases || [] }[name] || null)
const id = (name) => `hints-${name}-${Math.random().toString(36).slice(2, 7)}`
const ids = Object.fromEntries(['s', 'name', 'action', 'phase'].map((n) => [n, id(n)]))
const PLACE = { text: 'словами', where: 'де саме', list: 'тік 100, 250, 400…', options: 'варіанти через кому', prop: 'колір / значення', v: 'значення', color: 'колір', side: 'чия' }
</script>

<template>
  <template v-for="a in spec.args" :key="a.name">
    <select v-if="a.type === 'entity'" v-model="item[a.name]" class="form-select form-select-sm w-auto" :class="{ 'is-invalid': a.required && !item[a.name] }">
      <option value="">{{ a.name === 'a' ? 'А…' : a.name === 'b' ? 'Б…' : `${a.name}…` }}</option>
      <option v-for="s in sides" :key="s" :value="s">{{ vocab.sides[s] }}</option>
      <option v-for="p in entities" :key="p.id" :value="p.id">{{ roleOf(p.role).icon }} {{ p.title }}</option>
    </select>
    <select v-else-if="a.type === 'window'" v-model="item[a.name]" class="form-select form-select-sm w-auto">
      <option value="">вікно…</option>
      <option v-for="p in windows" :key="p.id" :value="p.id">🪟 {{ p.title }}</option>
    </select>
    <select v-else-if="a.type.startsWith('choice:')" v-model="item[a.name]" class="form-select form-select-sm w-auto">
      <option value="">{{ a.name }}…</option>
      <option v-for="(label, v) in vocab.options[a.type.slice(7)]" :key="v" :value="v">{{ label }}</option>
    </select>
    <input v-else-if="a.type === 'int'" v-model.number="item[a.name]" type="number" class="form-control form-control-sm num" :placeholder="a.name">
    <label v-else-if="a.type === 'bool'" class="form-check form-check-inline small m-0 align-self-center">
      <input v-model="item[a.name]" type="checkbox" class="form-check-input"> {{ a.name }}
    </label>
    <template v-else>
      <input v-model="item[a.name]" class="form-control form-control-sm w-auto txt" :placeholder="PLACE[a.name] || a.name" :list="hints(a.name) ? ids[a.name] : null">
      <datalist v-if="hints(a.name)" :id="ids[a.name]"><option v-for="h in hints(a.name)" :key="h" :value="h" /></datalist>
    </template>
  </template>
</template>

<style scoped>
.num { width: 4.5rem; }
.txt { min-width: 9rem; }
</style>
