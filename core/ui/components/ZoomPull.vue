<script setup>
import { ref } from 'vue'

import { pullZoom, uploadAttendance } from '../api.js'
import Icon from './Icon.vue'

// «Оновити із Zoom»: the lesson's meeting ID (typed once, remembered on the lesson) → the attendance rows; the result in one line.
// Without Zoom's keys — the participants report the host exports from Zoom's site, as a CSV (T336)
const props = defineProps({ lesson: Object })
const emit = defineEmits(['pulled'])
const meeting = ref(props.lesson.meeting || '')
const sources = ref(false)
const busy = ref(false)
const said = ref('')
const error = ref('')

async function run(job) {
  busy.value = true
  error.value = said.value = ''
  try {
    const a = await job()
    said.value = `${a.pulled} рядків · ${a.people.length} студентів · ${a.unknown.length} невідомих`
    emit('pulled')
  } catch (e) {
    error.value = e.message
  }
  busy.value = false
}
const pull = () => run(() => pullZoom(props.lesson.slug, { meeting: meeting.value.trim(), sources: sources.value }))
const csv = (e) => e.target.files[0] && run(() => uploadAttendance(props.lesson.slug, e.target.files[0])).then(() => (e.target.value = ''))
</script>

<template>
  <form class="d-flex flex-wrap align-items-center gap-2 small" @submit.prevent="pull">
    <input v-model="meeting" class="form-control form-control-sm meeting" placeholder="ID зустрічі Zoom або UUID" required>
    <label class="d-flex align-items-center gap-1 text-secondary"><input v-model="sources" type="checkbox" class="form-check-input mt-0"> + транскрипт, чат і запис</label>
    <button class="btn btn-outline-primary btn-sm d-inline-flex align-items-center gap-1" :disabled="busy"><Icon v-if="!busy" name="refresh" /> {{ busy ? 'Питаю Zoom…' : 'Оновити із Zoom' }}</button>
    <label class="more-field mb-0" role="button" title="Zoom → Reports → Meeting and webinar history → число в колонці Participants → Export (без «Show unique users»)">
      або CSV зі звіту Zoom<input type="file" accept=".csv,text/csv" hidden @change="csv">
    </label>
    <span v-if="said" class="text-success">{{ said }}</span>
    <span v-if="error" class="text-danger">{{ error }}</span>
  </form>
</template>

<style scoped>
.meeting { max-width: 17rem; }
</style>
