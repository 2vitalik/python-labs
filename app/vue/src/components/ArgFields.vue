<script setup>
import { computed, useId } from 'vue'

import { iconOf, statOf, vocab } from '../catalog.js'
import { useEd } from '../ed.js'
import { sideName } from '../ruleSides.js'

// inputs for a word's arguments, writing straight into `item`: the game's entities and windows, numbers, choices, texts with
// hints (states of the entity the clause names, counters, typical inputs, the game's phases); `when` resolves А / Б to an entity.
// «кого» lists the trigger's sides first, named by what they stand for (T278 §7), then «будь-хто» and the game's entities
const props = defineProps({ spec: Object, item: Object, sides: { type: Array, default: () => ['*'] }, when: Object })
const ed = useEd()
const uid = useId()
const ACTIONS = ['стрілки', 'пробіл', 'Enter', 'Esc', 'клік по клітині', 'правий клік', 'подвійний клік', 'свайп', 'перетягування', 'колесо миші', 'клавіша дії']
const label = (a) => vocab.value.args[a.name] || a.name
const whenSides = computed(() => props.sides.filter((s) => s.startsWith('@')))
const miss = (a) => a.required && [undefined, null, ''].includes(props.item[a.name])
const states = computed(() => {
  const v = String(props.item.a || '')
  const id = v.startsWith('@') ? props.when?.[v.slice(1)] : v
  const own = ed.entities.find((p) => p.id === id)?.states
  return own?.length ? own : [...new Set(ed.entities.flatMap((p) => p.states || []))]
})
const counters = computed(() => [...new Set([
  ...ed.entities.flatMap((p) => (p.stats || []).map((s) => s.label || statOf(s.key)?.label || s.key)), 'очки', 'час', 'рівень', 'комбо'])])
const hints = (name) => ({ s: states.value, name: counters.value, action: ACTIONS, phase: ed.game?.phases || [] })[name]
const set = (a, e) => (props.item[a.name] = e.target.value)
</script>

<template>
  <template v-for="a in spec.args" :key="a.name">
    <select v-if="a.type === 'entity' || a.type === 'window'" :value="item[a.name] ?? ''" class="form-select form-select-sm sel"
            :class="{ miss: miss(a) }" :title="label(a)" @change="set(a, $event)">
      <option value="">{{ label(a) }}…</option>
      <template v-if="a.type === 'entity'">
        <optgroup v-if="whenSides.length" label="з КОЛИ">
          <option v-for="s in whenSides" :key="s" :value="s">{{ sideName(s, when, ed.parts) }}</option>
        </optgroup>
        <option v-if="sides.includes('*')" value="*">{{ vocab.sides['*'] }}</option>
      </template>
      <option v-for="p in a.type === 'entity' ? ed.entities : ed.windows" :key="p.id" :value="p.id">{{ iconOf(p) }} {{ p.title }}</option>
    </select>
    <select v-else-if="a.type.startsWith('choice:')" :value="item[a.name] ?? ''" class="form-select form-select-sm sel"
            :class="{ miss: miss(a) }" :title="label(a)" @change="set(a, $event)">
      <option value="">{{ label(a) }}…</option>
      <option v-for="(text, v) in vocab.options[a.type.slice(7)]" :key="v" :value="v">{{ text }}</option>
    </select>
    <input v-else-if="a.type === 'int'" v-model.number="item[a.name]" type="number" class="form-control form-control-sm num"
           :class="{ miss: miss(a) }" :placeholder="label(a)" :title="label(a)">
    <label v-else-if="a.type === 'bool'" class="form-check form-check-inline small m-0">
      <input v-model="item[a.name]" type="checkbox" class="form-check-input"> {{ label(a) }}
    </label>
    <template v-else>
      <input v-model="item[a.name]" class="form-control form-control-sm txt" :class="{ miss: miss(a), wide: a.name === 'text' }"
             :placeholder="label(a)" :title="label(a)" :list="hints(a.name) ? `${uid}-${a.name}` : null">
      <datalist v-if="hints(a.name)" :id="`${uid}-${a.name}`"><option v-for="h in hints(a.name)" :key="h" :value="h" /></datalist>
    </template>
  </template>
</template>

<style scoped>
.sel { width: auto; max-width: 16rem; }  /* fits «👻 Привид — той, що в КОЛИ (Б)» */
.num { width: 5.5rem; }
.txt { width: 9rem; }
.txt.wide { flex: 1 1 14rem; width: auto; }
.miss { border-color: var(--bs-form-invalid-border-color); }
</style>
