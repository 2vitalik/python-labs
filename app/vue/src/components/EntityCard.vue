<script setup>
import { reactive, ref } from 'vue'

import { deletePart, postClaim, putPart } from '../api.js'
import { ROLES } from '../catalog.js'
import ClaimPicker from './ClaimPicker.vue'
import ClaimRow from './ClaimRow.vue'
import ShotStrip from './ShotStrip.vue'

const props = defineProps({ part: Object, claims: Array, info: Function })
const emit = defineEmits(['changed'])
const edit = ref(false)
const arm = ref(false)
const error = ref('')
const form = reactive({ title: props.part.title, role: props.part.role, description: props.part.description })

async function run(fn) {
  error.value = ''
  try {
    await fn()
    emit('changed')
  } catch (e) {
    error.value = e.message
  }
}
const save = () => run(async () => { await putPart(props.part.id, form); edit.value = false })
const remove = () => run(() => deletePart(props.part.id))
const addClaim = (task) => run(() => postClaim({ task, part: props.part.id }))
</script>

<template>
  <div class="card h-100">
    <div class="card-body vstack gap-2">
      <div class="d-flex align-items-center gap-2">
        <template v-if="!edit">
          <span class="fw-semibold">{{ ROLES[part.role]?.icon }} {{ part.title }}</span>
          <span class="badge text-bg-light border text-secondary fw-normal">{{ ROLES[part.role]?.label || part.role }}</span>
          <span class="ms-auto" role="button" title="Редагувати" @click="edit = true">✏️</span>
          <span v-if="!arm" role="button" title="Видалити сутність (разом з її правилами)" @click="arm = true">🗑️</span>
          <button v-else class="btn btn-danger btn-sm" @mouseleave="arm = false" @click="remove">Точно видалити?</button>
        </template>
        <template v-else>
          <select v-model="form.role" class="form-select form-select-sm w-auto">
            <option v-for="(r, k) in ROLES" :key="k" :value="k">{{ r.icon }} {{ r.label }}</option>
          </select>
          <input v-model="form.title" class="form-control form-control-sm">
          <button class="btn btn-primary btn-sm" @click="save">💾</button>
          <button class="btn btn-outline-secondary btn-sm" @click="edit = false">✕</button>
        </template>
      </div>
      <textarea v-if="edit" v-model="form.description" class="form-control form-control-sm" rows="2"
                placeholder="Опис сутності"></textarea>
      <div v-else-if="part.description" class="text-secondary small">{{ part.description }}</div>
      <ShotStrip :part="part" @changed="emit('changed')" />
      <div v-if="claims.length" class="d-flex flex-wrap gap-1 align-items-start">
        <ClaimRow v-for="c in claims" :key="c.id" :claim="c" :info="info(c.task)" @changed="emit('changed')" />
      </div>
      <ClaimPicker placeholder="＋ механіка цієї сутності…" @pick="addClaim" />
      <div v-if="error" class="text-danger small">{{ error }}</div>
    </div>
  </div>
</template>
