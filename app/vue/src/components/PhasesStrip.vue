<script setup>
import { computed, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import TagInput from '@core/components/TagInput.vue'
import Tip from '@core/components/Tip.vue'
import { putMyGame } from '../api.js'
import { iconOf } from '../catalog.js'
import { useEd } from '../ed.js'
import { jump } from '../jump.js'

// the order of one tick (T270 §4.2, T274 §6): the game's phases as numbered chips, edited in place; the trigger «почалась фаза
// тіку» names them. A phase named as an entity of the game wears its icon and leads to it — a match of names, not a link
const ed = useEd()
const phases = computed(() => ed.game?.phases || [])
const same = (a, b) => a.trim().toLowerCase() === b.trim().toLowerCase()
const items = computed(() => phases.value.map((name) => ({ name, ent: ed.entities.find((p) => same(p.title, name)) })))
const edit = ref(false)
const list = ref([])
const error = ref('')
const TYPICAL = ['ввід', 'гравець', 'вороги', 'снаряди', 'середовище', 'спавн', 'перевірка перемоги', 'рендер']
const known = computed(() => [...new Set([...TYPICAL, ...ed.entities.map((p) => p.title)])])
function open() {
  list.value = [...phases.value]
  error.value = ''
  edit.value = true
}
async function save() {
  const { title, base_game, base_custom, description } = ed.game
  try {
    await putMyGame({ title, base_game, base_custom, description, phases: list.value })
    edit.value = false
    ed.changed()
  } catch (e) {
    error.value = e.message
  }
}
</script>

<template>
  <div v-if="phases.length || ed.editable" class="phases">
    <div v-if="edit" class="vstack gap-2">
      <TagInput v-model="list" :hash="false" placeholder="через кому: ввід, гравець, вороги…" :known />
      <div class="d-flex gap-2">
        <button type="button" class="btn btn-sm btn-success" @click="save"><Icon name="check" /> Зберегти</button>
        <button type="button" class="btn btn-sm btn-outline-secondary" @click="edit = false">Скасувати</button>
      </div>
      <div v-if="error" class="text-danger small">{{ error }}</div>
    </div>
    <div v-else class="d-flex flex-wrap align-items-center gap-1">
      <span class="lead-in">🔁 За один тік:</span>
      <template v-for="({ name, ent }, i) in items" :key="name">
        <Icon v-if="i" name="right" class="sep" />
        <span v-if="ent" class="phase ent" role="button" :title="`показати «${ent.title}»`" @click="jump(`p-${ent.id}`)"><b>{{ i + 1 }}</b> {{ iconOf(ent) }} {{ name }}</span>
        <span v-else class="phase"><b>{{ i + 1 }}</b> {{ name }}</span>
      </template>
      <template v-if="ed.editable">
        <button v-if="phases.length" type="button" class="iact" title="Змінити порядок тіку" @click="open"><Icon name="pencil" /></button>
        <button v-else type="button" class="btn btn-sm btn-add py-0" @click="open"><Icon name="plus" /> фази</button>
      </template>
    </div>
    <Tip id="rules-phases-why" class="why">
      Що за чим відбувається за один крок гри. Фази — назви кроків своїми словами, ні до чого не привʼязуються; порядок потрібен,
      коли правила сперечаються, хто перший. На ці назви посилається подія «почалась фаза тіку»
    </Tip>
  </div>
</template>

<style scoped>
.phases { font-size: .85rem; }
.lead-in { font-weight: 600; margin-right: .15rem; }
.phase { padding: .05rem .5rem; border: 1px solid var(--bs-border-color); border-radius: 1rem; background: var(--bs-body-bg); white-space: nowrap; }
.phase.ent:hover { border-color: var(--bs-secondary-color); }
.phase b { margin-right: .1rem; color: var(--bs-secondary-color); font-variant-numeric: tabular-nums; }
.sep { color: var(--bs-secondary-color); }
.why { margin-top: .25rem; }
</style>
