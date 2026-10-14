<script setup>
import { ref } from 'vue'

import { pullZoom } from '../api.js'

// «Оновити із Zoom»: the lesson's meeting ID (typed once, remembered on the lesson) → the attendance rows; the result in one line
const props = defineProps({ lesson: Object })
const emit = defineEmits(['pulled'])
const meeting = ref(props.lesson.meeting || '')
const sources = ref(false)
const busy = ref(false)
const said = ref('')
const error = ref('')

async function pull() {
  busy.value = true
  error.value = said.value = ''
  try {
    const a = await pullZoom(props.lesson.slug, { meeting: meeting.value.trim(), sources: sources.value })
    said.value = `${a.pulled} рядків · ${a.people.length} студентів · ${a.unknown.length} невідомих`
    emit('pulled')
  } catch (e) {
    error.value = e.message
  }
  busy.value = false
}
</script>

<template>
  <form class="d-flex flex-wrap align-items-center gap-2 small" @submit.prevent="pull">
    <input v-model="meeting" class="form-control form-control-sm meeting" placeholder="ID зустрічі Zoom або UUID" required>
    <label class="d-flex align-items-center gap-1 text-secondary"><input v-model="sources" type="checkbox" class="form-check-input mt-0"> + транскрипт, чат і запис</label>
    <button class="btn btn-outline-primary btn-sm" :disabled="busy">{{ busy ? 'Питаю Zoom…' : '⟳ Оновити із Zoom' }}</button>
    <span v-if="said" class="text-success">{{ said }}</span>
    <span v-if="error" class="text-danger">{{ error }}</span>
  </form>
</template>

<style scoped>
.meeting { max-width: 17rem; }
</style>
