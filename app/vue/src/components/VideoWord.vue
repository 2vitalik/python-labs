<script setup>
import { reactive, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import { judgeVideo } from '../api.js'
import { CLAIM_STATUSES } from '../catalog.js'
import { useEd } from '../ed.js'

// the teacher's word on a video of «Супровід» (T318): is it wanted from this student — with a line why the student reads —
// and the check itself, as on a claim: заявлено · зараховано · повернуто
const props = defineProps({ v: Object })
const emit = defineEmits(['close'])
const ed = useEd()
const form = reactive({ need: props.v.need, why: props.v.why, status: props.v.status, verdict: props.v.verdict })
const error = ref('')
const NEEDS = { '': 'як у всіх', must: 'обовʼязково', skip: 'не потрібно' }
const TONE = { accepted: 'btn-success', returned: 'btn-danger', claimed: 'btn-secondary' }

async function save() {
  error.value = ''
  try {
    await judgeVideo(ed.nick, props.v.slot, form)
    await ed.changed()
    emit('close')
  } catch (e) {
    error.value = e.message
  }
}
</script>

<template>
  <div class="vstack gap-2">
    <div class="cap">Чи потрібне це відео від студента</div>
    <div class="btn-group btn-group-sm align-self-start">
      <button v-for="(label, k) in NEEDS" :key="k" type="button" class="btn" :class="form.need === k ? 'btn-secondary' : 'btn-outline-secondary'" @click="form.need = k">{{ label }}</button>
    </div>
    <input v-if="form.need" v-model="form.why" class="form-control form-control-sm" placeholder="Чому — студент побачить: «показав на онлайн-захисті»" @keydown.enter="save">
    <div class="cap">Перевірка</div>
    <div class="btn-group btn-group-sm align-self-start">
      <button v-for="(label, k) in CLAIM_STATUSES" :key="k" type="button" class="btn" :class="form.status === k ? TONE[k] : 'btn-outline-secondary'" @click="form.status = k">{{ label }}</button>
    </div>
    <input v-model="form.verdict" class="form-control form-control-sm" placeholder="Слово студентові (за бажанням)" @keydown.enter="save">
    <div class="d-flex gap-2">
      <button type="button" class="btn btn-sm btn-success" @click="save"><Icon name="check" /> Зберегти</button>
      <button type="button" class="btn btn-sm btn-outline-secondary" @click="emit('close')">Скасувати</button>
    </div>
    <div v-if="error" class="text-danger small">{{ error }}</div>
  </div>
</template>

<style scoped>
.cap { font-size: .7rem; color: var(--bs-secondary-color); }
</style>
