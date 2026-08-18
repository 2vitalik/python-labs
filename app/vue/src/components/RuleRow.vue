<script setup>
import { computed, reactive, ref } from 'vue'

import { deleteRule, postRule, putRule } from '../api.js'
import { ROLES } from '../catalog.js'
import { EFFECTS, TRIGGERS, effectText, whenText } from '../rules.js'

const props = defineProps({ rule: Object, parts: Array, editable: Boolean })
const emit = defineEmits(['changed', 'cancel'])
const edit = ref(!props.rule)
const error = ref('')
const form = reactive({
  kind: props.rule?.when.kind || 'contact',
  a: props.rule?.when.a || '',
  b: props.rule?.when.b || '',
  every: props.rule?.when.every || 20,
  effects: props.rule ? props.rule.then.map((e) => ({ ...e })) : [],
  note: props.rule?.note || '',
})
const ne = reactive({ kind: '', n: 1, part: '', text: '' }) // new-effect draft

const entities = computed(() => props.parts.filter((p) => p.kind === 'entity'))
const windows = computed(() => props.parts.filter((p) => p.kind === 'window'))
const name = (id) => {
  const p = props.parts.find((x) => x.id === id)
  return p ? `${ROLES[p.role]?.icon || ''}${p.title}` : '?'
}
const arg = computed(() => EFFECTS[ne.kind]?.arg)
const ready = computed(() => form.effects.length &&
  (form.kind === 'timer' ? form.every > 0 : form.a && form.b))

function addEffect() {
  const e = { kind: ne.kind }
  if (arg.value === 'n') e.n = ne.n
  if (arg.value === 'entity' || arg.value === 'window') e.part = ne.part
  if (arg.value === 'text') e.text = ne.text
  form.effects.push(e)
  Object.assign(ne, { kind: '', n: 1, part: '', text: '' })
}

async function save() {
  error.value = ''
  const when = form.kind === 'contact'
    ? { kind: 'contact', a: form.a, b: form.b } : { kind: 'timer', every: form.every }
  const data = { when, then: form.effects, note: form.note }
  try {
    await (props.rule ? putRule(props.rule.id, data) : postRule(data))
    edit.value = false
    emit('changed')
  } catch (e) {
    error.value = e.message
  }
}
const cancel = () => (props.rule ? (edit.value = false) : emit('cancel'))
const remove = async () => { await deleteRule(props.rule.id); emit('changed') }
</script>

<template>
  <div v-if="!edit" class="d-flex flex-wrap align-items-center gap-1 border rounded px-2 py-1">
    <span class="text-secondary small fw-semibold">КОЛИ</span>
    <span>{{ whenText(rule.when, name) }}</span>
    <span class="text-secondary small fw-semibold">→ ТО</span>
    <span>{{ rule.then.map((e) => effectText(e, name)).join(' · ') }}</span>
    <span v-if="rule.note" class="text-secondary small" :title="rule.note">💬</span>
    <template v-if="editable">
      <span class="ms-auto" role="button" title="Редагувати" @click="edit = true">✏️</span>
      <span class="text-secondary" role="button" title="Видалити правило" @click="remove">✕</span>
    </template>
  </div>

  <div v-else class="border rounded p-2 vstack gap-2">
    <div class="d-flex flex-wrap align-items-center gap-2">
      <span class="text-secondary small fw-semibold">КОЛИ</span>
      <select v-model="form.kind" class="form-select form-select-sm w-auto">
        <option v-for="(label, k) in TRIGGERS" :key="k" :value="k">{{ label }}</option>
      </select>
      <template v-if="form.kind === 'contact'">
        <select v-model="form.a" class="form-select form-select-sm w-auto">
          <option value="">сутність А…</option>
          <option v-for="p in entities" :key="p.id" :value="p.id">{{ name(p.id) }}</option>
        </select>
        ×
        <select v-model="form.b" class="form-select form-select-sm w-auto">
          <option value="">сутність Б…</option>
          <option v-for="p in entities" :key="p.id" :value="p.id">{{ name(p.id) }}</option>
        </select>
      </template>
      <template v-else>
        кожні <input v-model.number="form.every" type="number" min="1" class="form-control form-control-sm num"> тіків
      </template>
    </div>
    <div class="d-flex flex-wrap align-items-center gap-2">
      <span class="text-secondary small fw-semibold">ТО</span>
      <span v-for="(e, i) in form.effects" :key="i" class="badge text-bg-light border text-dark fw-normal">
        {{ effectText(e, name) }} <span role="button" @click="form.effects.splice(i, 1)">✕</span>
      </span>
      <select v-model="ne.kind" class="form-select form-select-sm w-auto">
        <option value="">＋ ефект…</option>
        <option v-for="(d, k) in EFFECTS" :key="k" :value="k">{{ d.label }}</option>
      </select>
      <input v-if="arg === 'n'" v-model.number="ne.n" type="number" class="form-control form-control-sm num">
      <select v-else-if="arg === 'entity' || arg === 'window'" v-model="ne.part" class="form-select form-select-sm w-auto">
        <option value="">ціль…</option>
        <option v-for="p in arg === 'entity' ? entities : windows" :key="p.id" :value="p.id">{{ name(p.id) }}</option>
      </select>
      <input v-else-if="arg === 'text'" v-model="ne.text" class="form-control form-control-sm w-auto" placeholder="опиши словами">
      <button v-if="ne.kind" class="btn btn-outline-primary btn-sm" @click="addEffect">＋</button>
    </div>
    <div class="d-flex gap-2">
      <input v-model="form.note" class="form-control form-control-sm" placeholder="Нотатка">
      <button class="btn btn-primary btn-sm" :disabled="!ready" @click="save">💾</button>
      <button class="btn btn-outline-secondary btn-sm" @click="cancel">✕</button>
    </div>
    <div v-if="error" class="text-danger small">{{ error }}</div>
  </div>
</template>

<style scoped>
.num { width: 5rem; }
</style>
