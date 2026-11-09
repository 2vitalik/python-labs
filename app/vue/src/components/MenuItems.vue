<script setup>
import { computed, reactive, ref, watch } from 'vue'

import { deletePart, postPart, putPart } from '../api.js'
import { taskIndex } from '../catalog.js'

// the menu of a window, edited in place: a row per item — title and where it leads (another window, a card, nothing);
// the menu is a Part of its own (kind=menu) hosted on this window, created on the first save
const props = defineProps({ window: Object, menu: Object, windows: Array, info: Function, editable: Boolean })
const emit = defineEmits(['changed'])
const edit = ref(false)
const error = ref('')
const form = reactive({ items: [] })
const items = computed(() => props.menu?.items || [])
const target = (it) => (it.window ? `→ ${props.windows.find((w) => w.id === it.window)?.title || '?'}` : it.task ? `→ ${props.info(it.task)?.title || it.task}` : '')
const taskTitle = (slug) => taskIndex.value[slug]?.title
watch(edit, (on) => on && (form.items = items.value.length ? items.value.map((it) => ({ ...it, to: it.window ? `w:${it.window}` : it.task ? 't' : '' })) : [blank()]))
const blank = () => ({ title: '', window: '', task: '', note: '', to: '' })

function retarget(it) {
  it.window = it.to.startsWith('w:') ? it.to.slice(2) : ''
  if (it.to !== 't') it.task = ''
}
async function save() {
  error.value = ''
  const rows = form.items.map(({ to, ...it }) => it)
  try {
    if (props.menu) await putPart(props.menu.id, { title: props.menu.title, description: props.menu.description, window: props.window.id, items: rows })
    else await postPart({ kind: 'menu', title: `Меню «${props.window.title}»`, window: props.window.id, items: rows })
    edit.value = false
    emit('changed')
  } catch (e) {
    error.value = e.message
  }
}
async function remove() {
  await deletePart(props.menu.id)
  edit.value = false
  emit('changed')
}
</script>

<template>
  <div v-if="items.length || editable" class="menu small">
    <div v-if="!edit" class="d-flex align-items-start gap-2">
      <ul v-if="items.length" class="mb-0 ps-3 flex-grow-1">
        <li v-for="(it, i) in items" :key="i">
          {{ it.title }} <span class="text-secondary">{{ target(it) }}</span>
          <span v-if="it.note" class="text-secondary">· {{ it.note }}</span>
        </li>
      </ul>
      <button v-if="editable" class="btn btn-link btn-sm p-0 text-decoration-none text-nowrap" @click="edit = true">{{ items.length ? '✏️ меню' : '＋ пункти меню' }}</button>
    </div>
    <div v-else class="vstack gap-1">
      <div v-for="(it, i) in form.items" :key="i" class="input-group input-group-sm">
        <input v-model="it.title" class="form-control" placeholder="Пункт меню">
        <select v-model="it.to" class="form-select" style="max-width: 11rem" @change="retarget(it)">
          <option value="">нікуди (текст)</option>
          <option value="t">→ картка…</option>
          <option v-for="w in windows" :key="w.id" :value="`w:${w.id}`" :disabled="w.id === window.id">→ {{ w.title }}</option>
        </select>
        <input v-if="it.to === 't'" v-model="it.task" class="form-control" placeholder="slug картки" list="task-cards" :title="taskTitle(it.task)">
        <input v-model="it.note" class="form-control" placeholder="нотатка" style="max-width: 9rem">
        <button class="btn btn-outline-secondary" title="Прибрати пункт" @click="form.items.splice(i, 1)">✕</button>
      </div>
      <div class="d-flex gap-2 align-items-center">
        <button class="btn btn-outline-secondary btn-sm" @click="form.items.push(blank())">＋ пункт</button>
        <button class="btn btn-primary btn-sm" @click="save">💾 Зберегти меню</button>
        <button class="btn btn-outline-secondary btn-sm" @click="edit = false">✕</button>
        <button v-if="menu" class="btn btn-link btn-sm text-danger text-decoration-none ms-auto" @click="remove">прибрати меню</button>
      </div>
      <div v-if="error" class="text-danger">{{ error }}</div>
    </div>
  </div>
</template>
