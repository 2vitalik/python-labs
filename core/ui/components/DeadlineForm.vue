<script setup>
import { computed, reactive, ref } from 'vue'

import { deleteDeadline, putDeadline } from '../api.js'
import { endOfDay, fmtWhen, fromInput, labName, toInput } from '../labs.js'

// a lab's deadlines: one for everyone and, when a stream runs on another schedule, one per set of groups — the narrower wins.
// The list is what exists; the form below adds or rewrites one (the same set of groups = the same document)
const props = defineProps({ lab: { type: Number, required: true }, deadlines: { type: Array, required: true }, groups: { type: Array, required: true } })
const emit = defineEmits(['saved', 'close'])
const form = reactive({ at: '', groups: [] })
const busy = ref(false)
const error = ref('')
const today = new Date().toISOString().slice(0, 10)
const label = (d) => (d.groups.length ? d.groups.join(', ') : 'для всіх')
const picked = computed(() => new Set(form.groups))
const toggle = (g) => (form.groups = picked.value.has(g) ? form.groups.filter((x) => x !== g) : [...form.groups, g])
const edit = (d) => Object.assign(form, { at: toInput(d.at), groups: [...d.groups] })
if (props.deadlines.length) edit(props.deadlines.find((d) => !d.groups.length) || props.deadlines[0])
else form.at = endOfDay(today)

async function run(action) {
  busy.value = true
  error.value = ''
  try {
    emit('saved', await action())
  } catch (e) {
    error.value = e.message
  } finally {
    busy.value = false
  }
}
const save = () => run(() => putDeadline(props.lab, { at: fromInput(form.at), groups: form.groups }))
const drop = (d) => confirm(`Прибрати дедлайн ${labName(props.lab)} (${label(d)})?`) && run(() => deleteDeadline(d.id))
</script>

<template>
  <div class="card mb-3">
    <div class="card-body">
      <div class="d-flex align-items-center gap-2 mb-2">
        <b>⏰ {{ labName(lab) }} — дедлайн</b>
        <button type="button" class="btn-close btn-sm ms-auto" title="Згорнути" @click="emit('close')"></button>
      </div>
      <ul v-if="deadlines.length" class="list-unstyled small mb-2">
        <li v-for="d in deadlines" :key="d.id" class="d-flex align-items-center gap-2">
          <span>{{ fmtWhen(d.at) }} · {{ label(d) }}</span>
          <a href="#" class="ibtn" title="Редагувати" @click.prevent="edit(d)">✏️</a>
          <a href="#" class="ibtn" title="Прибрати" @click.prevent="drop(d)">🗑</a>
        </li>
      </ul>
      <div class="row g-2 align-items-end">
        <div class="col-sm-4 col-md-3">
          <label class="form-label small mb-0">Дата й час</label>
          <input v-model="form.at" type="datetime-local" class="form-control form-control-sm">
        </div>
        <div class="col-sm">
          <label class="form-label small mb-0">Групи <span class="text-secondary">(жодної = для всіх)</span></label>
          <div class="d-flex flex-wrap gap-1">
            <button v-for="g in groups" :key="g" type="button" class="btn btn-sm chip" :class="picked.has(g) ? 'btn-secondary' : 'btn-outline-secondary'" @click="toggle(g)">{{ g }}</button>
          </div>
        </div>
        <div class="col-auto">
          <button type="button" class="btn btn-primary btn-sm" :disabled="busy || !form.at" @click="save">Зберегти</button>
        </div>
      </div>
      <div v-if="error" class="text-danger small mt-2">{{ error }}</div>
    </div>
  </div>
</template>
