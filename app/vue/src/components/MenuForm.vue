<script setup>
import { reactive, ref } from 'vue'

import DelButton from '@core/components/DelButton.vue'
import Icon from '@core/components/Icon.vue'
import { deletePart, postPart, putPart } from '../api.js'
import { useEd } from '../ed.js'
import MenuTarget from './MenuTarget.vue'

// the menu of a window, edited in place: a row per item — title, where it leads, a note. The menu is a Part of its own
// (kind menu) hosted on the window, made on the first save; an item is { title, window, task, note }
const props = defineProps({ window: Object, menu: Object })
const emit = defineEmits(['done', 'cancel'])
const ed = useEd()
const blank = () => ({ title: '', window: '', task: '', note: '' })
const rows = reactive((props.menu?.items || []).map((it) => ({ ...blank(), ...it })))
if (!rows.length) rows.push(blank())
const busy = ref(false)
const error = ref('')

async function run(fn) {
  error.value = ''
  busy.value = true
  try {
    await fn()
    ed.changed()
    emit('done')
  } catch (e) {
    error.value = e.message
  } finally {
    busy.value = false
  }
}
const save = () => run(() => (props.menu
  ? putPart(props.menu.id, { title: props.menu.title, description: props.menu.description, window: props.window.id, items: rows })
  : postPart({ kind: 'menu', title: `Меню «${props.window.title}»`, window: props.window.id, items: rows })))
const remove = () => run(() => deletePart(props.menu.id))
</script>

<template>
  <div class="vstack gap-2">
    <div v-for="(it, i) in rows" :key="i" class="item">
      <input v-model="it.title" class="form-control form-control-sm" placeholder="Пункт меню">
      <MenuTarget v-model:window="it.window" v-model:task="it.task" :host="window.id" />
      <input v-model="it.note" class="form-control form-control-sm" placeholder="нотатка">
      <button type="button" class="iact del" title="Прибрати пункт" @click="rows.splice(i, 1)"><Icon name="minus" /></button>
    </div>
    <div class="text-secondary">Дія — пункт, що не відкриває вікно, а щось робить: рестарт рівня, гучність, збереження.</div>
    <div class="d-flex flex-wrap align-items-center gap-2">
      <button type="button" class="btn btn-sm btn-add" @click="rows.push(blank())"><Icon name="plus" /> пункт</button>
      <button type="button" class="btn btn-sm btn-success" :disabled="busy" @click="save"><Icon name="check" /> Зберегти</button>
      <button type="button" class="btn btn-sm btn-outline-secondary" @click="emit('cancel')">Скасувати</button>
      <DelButton v-if="menu" class="ms-auto" what="меню цього вікна" @yes="remove" />
    </div>
    <div v-if="error" class="text-danger">{{ error }}</div>
  </div>
</template>

<style scoped>
/* title · target · note in a row; in a narrow card the note wraps under them */
.item { display: flex; flex-wrap: wrap; align-items: center; gap: .25rem; }
.item > input { flex: 1 1 8rem; min-width: 0; }
.item + .item { padding-top: .5rem; border-top: 1px dashed var(--bs-border-color); }
</style>
