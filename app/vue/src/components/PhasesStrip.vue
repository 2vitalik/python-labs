<script setup>
import { computed, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import TagInput from '@core/components/TagInput.vue'
import { putMyGame } from '../api.js'
import { useEd } from '../ed.js'

// the order of one tick (T270 §4.2): the game's phases as numbered chips, edited in place; the trigger «почалась фаза тіку» names them
const ed = useEd()
const phases = computed(() => ed.game?.phases || [])
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
      <TagInput v-model="list" :hash="false" placeholder="фаза і Enter" :known />
      <div class="d-flex gap-2">
        <button type="button" class="btn btn-sm btn-success" @click="save"><Icon name="check" /> Зберегти</button>
        <button type="button" class="btn btn-sm btn-outline-secondary" @click="edit = false">Скасувати</button>
      </div>
      <div v-if="error" class="text-danger small">{{ error }}</div>
    </div>
    <div v-else class="d-flex flex-wrap align-items-center gap-1">
      <span class="lead-in">🔁 За один тік:</span>
      <template v-for="(p, i) in phases" :key="p">
        <Icon v-if="i" name="right" class="sep" />
        <span class="phase"><b>{{ i + 1 }}</b> {{ p }}</span>
      </template>
      <template v-if="ed.editable">
        <button v-if="phases.length" type="button" class="iact" title="Змінити порядок тіку" @click="open"><Icon name="pencil" /></button>
        <button v-else type="button" class="btn btn-sm btn-add py-0" @click="open"><Icon name="plus" /> фази</button>
      </template>
    </div>
    <div class="why">
      що за чим відбувається за один крок гри; потрібно, коли правила сперечаються, хто перший. На ці назви посилається подія «почалась фаза тіку»
    </div>
  </div>
</template>

<style scoped>
.phases { font-size: .85rem; }
.lead-in { font-weight: 600; margin-right: .15rem; }
.phase { padding: .05rem .5rem; border: 1px solid var(--bs-border-color); border-radius: 1rem; background: var(--bs-body-bg); white-space: nowrap; }
.phase b { margin-right: .1rem; color: var(--bs-secondary-color); font-variant-numeric: tabular-nums; }
.sep { color: var(--bs-secondary-color); }
.why { margin-top: .2rem; font-size: .75rem; color: var(--bs-secondary-color); }
</style>
