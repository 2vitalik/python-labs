<script setup>
import { reactive, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import { judgeClaim } from '../api.js'
import { CLAIM_STATUSES } from '../catalog.js'
import { useEd } from '../ed.js'

// the teacher's part of a claim's panel: заявлено · зараховано · повернуто and a word to the student
const props = defineProps({ claim: Object })
const emit = defineEmits(['close'])
const ed = useEd()
const form = reactive({ status: props.claim.status || 'claimed', verdict: props.claim.verdict || '' })
const error = ref('')
const TONE = { accepted: 'btn-success', returned: 'btn-danger', claimed: 'btn-secondary' }

async function save() {
  error.value = ''
  try {
    await judgeClaim(ed.nick, props.claim.id, form)
    ed.changed()
    emit('close')
  } catch (e) {
    error.value = e.message
  }
}
</script>

<template>
  <div class="vstack gap-2 pt-2 border-top">
    <div class="btn-group btn-group-sm align-self-start">
      <button v-for="(label, k) in CLAIM_STATUSES" :key="k" type="button" class="btn"
              :class="form.status === k ? TONE[k] : 'btn-outline-secondary'" @click="form.status = k">{{ label }}</button>
    </div>
    <input v-model="form.verdict" class="form-control form-control-sm" placeholder="Слово студентові (за бажанням)" @keydown.enter="save">
    <div class="d-flex gap-2">
      <button type="button" class="btn btn-sm btn-success" @click="save"><Icon name="check" /> Зберегти</button>
      <button type="button" class="btn btn-sm btn-outline-secondary" @click="emit('close')">Скасувати</button>
    </div>
    <div v-if="error" class="text-danger small">{{ error }}</div>
  </div>
</template>
