<script setup>
import { ref } from 'vue'

import { getLabLoose, putLabResult } from '../api.js'

// the course's students no card of the lab is pinned to (T375): the cards are the teacher's to pin — a free one of the
// stream, and its number is the student's in every lab. Each student is offered a free card of their own, in order
const props = defineProps({ n: Number })
const emit = defineEmits(['pinned'])
const loose = ref(null)  // {students: [{email, nick, name, group}], free: [vid…]}
const pick = ref({})  // email → vid
const busy = ref(false)
const error = ref('')

async function load() {
  loose.value = await getLabLoose(props.n)
  pick.value = Object.fromEntries(loose.value.students.map((s, i) => [s.email, loose.value.free[i] ?? '']))
}
async function pin(s) {
  busy.value = true
  error.value = ''
  try {
    await putLabResult(props.n, pick.value[s.email], { student: s.email })
    await load()
    emit('pinned')
  } catch (e) {
    error.value = e.message
  } finally {
    busy.value = false
  }
}
load()
</script>

<template>
  <section v-if="loose?.students.length" class="mb-4">
    <h2 class="h6 mb-1">Без картки <span class="fw-normal text-secondary">({{ loose.students.length }})</span></h2>
    <p class="small text-secondary mb-2">Картку закріплюєш ти: її номер стане варіантом студента в усіх лабах.</p>
    <div v-for="s in loose.students" :key="s.email" class="d-flex flex-wrap align-items-center gap-2 mb-1">
      <span>{{ s.name || s.nick }}</span>
      <span class="small text-secondary">{{ s.group }}</span>
      <select v-model="pick[s.email]" class="form-select form-select-sm w-auto" :aria-label="`Картка для ${s.name || s.nick}`">
        <option value="" disabled>вільних карток нема</option>
        <option v-for="vid in loose.free" :key="vid" :value="vid">{{ vid }}</option>
      </select>
      <button type="button" class="btn btn-sm btn-outline-primary" :disabled="!pick[s.email] || busy" @click="pin(s)">Закріпити</button>
    </div>
    <p v-if="error" class="small text-danger mb-0">{{ error }}</p>
  </section>
</template>
