<script setup>
import { ref } from 'vue'

import { deleteField, orderFields } from '../api.js'
import FieldForm from './FieldForm.vue'

// the teacher's own columns (T240): the list with its order, a form for a new one or an edit, deletion in two clicks (the values go with it)
const props = defineProps({ fields: { type: Array, required: true } })
const emit = defineEmits(['changed', 'close'])
const editing = ref(null)  // a field, or {} for a new one
const sure = ref('')
const error = ref('')
const TYPES = { bool: 'чекбокс', select: 'вибір', multi: 'кілька', number: 'число', text: 'текст', date: 'дата' }
const SCOPES = { student: 'на студента', lab: 'на лабу' }
async function run(action) {
  error.value = ''
  try {
    await action()
    emit('changed')
  } catch (e) {
    error.value = e.message
  }
}
const drop = (f) => run(async () => {
  await deleteField(f.key)
  sure.value = ''
})
function move(f, by) {
  const keys = props.fields.map((x) => x.key)
  const i = keys.indexOf(f.key)
  if (i + by < 0 || i + by >= keys.length) return
  ;[keys[i], keys[i + by]] = [keys[i + by], keys[i]]
  run(() => orderFields(keys))
}
</script>

<template>
  <div class="card mb-3">
    <div class="card-body py-2">
      <div class="d-flex align-items-center gap-2 mb-2">
        <b>⚙️ Мої поля</b>
        <span class="small text-secondary">колонки, яких сайт не знає: чекбокс, вибір з варіантами, число, текст, дата — на студента або на кожну лабу</span>
        <button type="button" class="btn-close btn-sm ms-auto" title="Згорнути" @click="emit('close')"></button>
      </div>
      <div v-for="(f, i) in fields" :key="f.key" class="d-flex flex-wrap align-items-center gap-2 py-1 border-bottom small">
        <span>{{ f.emoji }} <b>{{ f.title }}</b></span>
        <span class="text-secondary">{{ TYPES[f.type] }} · {{ SCOPES[f.scope] }}<template v-if="f.options.length"> · {{ f.options.map((o) => o.emoji || o.text).join(' ') }}</template></span>
        <span class="ms-auto d-flex gap-1">
          <a href="#" class="ibtn" :class="{ invisible: !i }" title="Вище" @click.prevent="move(f, -1)">↑</a>
          <a href="#" class="ibtn" :class="{ invisible: i === fields.length - 1 }" title="Нижче" @click.prevent="move(f, 1)">↓</a>
          <a href="#" class="ibtn" title="Редагувати" @click.prevent="editing = f">✏️</a>
          <a v-if="sure !== f.key" href="#" class="ibtn" title="Видалити поле з усіма значеннями" @click.prevent="sure = f.key">🗑</a>
          <template v-else>
            <button type="button" class="btn btn-sm btn-outline-danger py-0" @click="drop(f)">видалити</button>
            <button type="button" class="btn btn-sm btn-outline-secondary py-0" @click="sure = ''">ні</button>
          </template>
        </span>
      </div>
      <p v-if="!fields.length" class="small text-secondary mb-1">Полів ще нема.</p>
      <div v-if="error" class="text-danger small mt-1">{{ error }}</div>
      <button v-if="!editing" type="button" class="btn btn-sm btn-outline-primary mt-2" @click="editing = {}">＋ Нове поле</button>
      <FieldForm v-else :field="editing" class="mt-2" @saved="editing = null; emit('changed')" @close="editing = null" />
    </div>
  </div>
</template>
