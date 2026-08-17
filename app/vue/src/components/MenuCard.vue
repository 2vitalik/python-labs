<script setup>
import { reactive, ref } from 'vue'

import { deletePart, putPart } from '../api.js'
import ClaimRow from './ClaimRow.vue'
import ShotStrip from './ShotStrip.vue'

const props = defineProps({ part: Object, windows: Array, claims: Array, info: Function })
const emit = defineEmits(['changed'])
const arm = ref(false)
const error = ref('')
const form = reactive({
  title: props.part.title,
  description: props.part.description,
  window: props.part.window,
  items: props.part.items.map((it) => ({ ...it })),
})

const addItem = () => form.items.push({ title: '', window: '', task: '', note: '' })

async function save() {
  error.value = ''
  try {
    const saved = await putPart(props.part.id, form)
    form.items = saved.items.map((it) => ({ ...it }))
    emit('changed')
  } catch (e) {
    error.value = e.message
  }
}

async function remove() {
  error.value = ''
  try {
    await deletePart(props.part.id)
    emit('changed')
  } catch (e) {
    error.value = e.message
  }
}
</script>

<template>
  <div class="card">
    <div class="card-body vstack gap-2">
      <div class="d-flex align-items-center gap-2">
        <input v-model="form.title" class="form-control form-control-sm fw-semibold w-auto">
        <span class="text-secondary small">на вікні</span>
        <select v-model="form.window" class="form-select form-select-sm w-auto">
          <option value="">—</option>
          <option v-for="w in windows" :key="w.id" :value="w.id">{{ w.title }}</option>
        </select>
        <span class="ms-auto"></span>
        <span v-if="!arm" role="button" title="Видалити меню" @click="arm = true">🗑️</span>
        <button v-else class="btn btn-danger btn-sm" @mouseleave="arm = false" @click="remove">Точно видалити?</button>
      </div>
      <div v-for="(it, i) in form.items" :key="i" class="input-group input-group-sm">
        <input v-model="it.title" class="form-control" placeholder="Пункт меню">
        <select v-model="it.window" class="form-select">
          <option value="">→ вікно…</option>
          <option v-for="w in windows" :key="w.id" :value="w.id">→ {{ w.title }}</option>
        </select>
        <input v-model="it.task" class="form-control" placeholder="→ картка (slug)" list="task-cards">
        <input v-model="it.note" class="form-control" placeholder="Нотатка">
        <button class="btn btn-outline-secondary" title="Прибрати пункт" @click="form.items.splice(i, 1)">✕</button>
      </div>
      <div class="d-flex gap-2">
        <button class="btn btn-outline-secondary btn-sm" @click="addItem">＋ пункт</button>
        <button class="btn btn-primary btn-sm" @click="save">💾 Зберегти меню</button>
      </div>
      <ShotStrip :part="part" @changed="emit('changed')" />
      <div v-if="claims.length" class="d-flex flex-wrap gap-1 align-items-start">
        <ClaimRow v-for="c in claims" :key="c.id" :claim="c" :info="info(c.task)" @changed="emit('changed')" />
      </div>
      <div v-if="error" class="text-danger small">{{ error }}</div>
    </div>
  </div>
</template>
