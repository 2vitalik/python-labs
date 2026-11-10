<script setup>
import { computed } from 'vue'

import Icon from '@core/components/Icon.vue'
import { iconOf, vocab } from '../catalog.js'
import { useEd } from '../ed.js'
import { clauses, plain, specOf } from '../rules.js'

// the contacts table (T270 §4.2): who (А) in rows × with whom (Б) in columns, a cell says what happens — ТО, and ЯКЩО in small
// type. A click on a rule emits show(id); in the editor a click on an empty cell emits add(prefill) for that pair
const props = defineProps({ rules: Array })
const emit = defineEmits(['show', 'add'])
const ed = useEd()
const rank = (v) => {
  const i = ed.entities.findIndex((p) => p.id === v)
  return i < 0 ? 1e6 + (v === '*') : i  // the game's order; «будь-хто» last
}
const axis = (side) => [...new Set(props.rules.map((r) => r.when[side]))].sort((x, y) => rank(x) - rank(y))
const rows = computed(() => axis('a'))
const cols = computed(() => axis('b'))
const cells = computed(() => {
  const m = {}
  for (const r of props.rules) {
    const c = clauses(r, ed.parts)
    const key = `${r.when.a} ${r.when.b}`
    m[key] = [...(m[key] || []), {
      id: r.id, trigger: r.when.kind === 'contact' ? '' : specOf('triggers', r.when.kind)?.label,
      cond: c.cond.map(plain).join(' і '), then: c.then.map(plain),
    }]
  }
  return m
})
const cell = (a, b) => cells.value[`${a} ${b}`]
function who(v) {
  if (vocab.value.sides[v]) return vocab.value.sides[v]
  const p = ed.parts.find((x) => x.id === v)
  return p ? `${iconOf(p)} ${p.title}` : '?'
}
</script>

<template>
  <div>
    <div class="mx-box">
      <table class="mx">
        <thead>
          <tr>
            <th class="corner text-secondary">А ＼ Б</th>
            <th v-for="b in cols" :key="b" scope="col">{{ who(b) }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="a in rows" :key="a">
            <th scope="row">{{ who(a) }}</th>
            <td v-for="b in cols" :key="b">
              <button v-for="r in cell(a, b)" :key="r.id" type="button" class="mrule" title="показати в списку" @click="emit('show', r.id)">
                <span v-if="r.trigger" class="small-line">{{ r.trigger }}</span>
                <span v-if="r.cond" class="small-line">якщо {{ r.cond }}</span>
                <span v-for="(t, i) in r.then" :key="i" class="d-block">{{ t }}</span>
              </button>
              <button v-if="ed.editable && !cell(a, b)" type="button" class="iact add free" :title="`Нове правило: ${who(a)} × ${who(b)}`"
                      @click="emit('add', { when: { kind: 'contact', a, b } })"><Icon name="plus" /></button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="small text-secondary mt-1">
      Рядок — хто (А), стовпець — з ким (Б). Клік по правилу — перейти до нього в списку{{ ed.editable ? '; по «＋» у порожній клітині — нове правило для цієї пари' : '' }}.
    </div>
  </div>
</template>

<style scoped>
.mx-box { max-width: 100%; max-height: 75vh; overflow: auto; border: 1px solid var(--bs-border-color); border-radius: .375rem; }
.mx { border-collapse: separate; border-spacing: 0; font-size: .78rem; }
.mx th, .mx td { padding: .25rem .4rem; border: solid var(--bs-border-color); border-width: 0 1px 1px 0; vertical-align: top; background: var(--bs-body-bg); }
.mx td { min-width: 9rem; max-width: 15rem; }
.mx th { background: var(--bs-tertiary-bg); font-weight: 600; white-space: nowrap; }
/* the header row and the first column stay put while the table scrolls under them */
.mx thead th { position: sticky; top: 0; z-index: 2; }
.mx tbody th, .mx .corner { position: sticky; left: 0; z-index: 1; }
.mx .corner { z-index: 3; font-weight: 400; }
.mrule { display: block; width: 100%; padding: .1rem .2rem; border: 0; border-radius: .25rem; background: none; color: inherit; text-align: start; }
.mrule + .mrule { margin-top: .2rem; border-top: 1px dashed var(--bs-border-color); border-radius: 0; }
.mrule:hover { background: var(--bs-tertiary-bg); }
.small-line { display: block; font-size: .7rem; color: var(--bs-secondary-color); }
.free { width: 100%; opacity: .3; }
.free:hover, .free:focus-visible { opacity: 1; }
</style>
