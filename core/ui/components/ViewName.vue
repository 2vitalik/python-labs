<script setup>
import { computed, onMounted, ref } from 'vue'

import { parseOption } from '../polls.js'

// the name of a new view, typed in a panel; an emoji at its start becomes the icon. Enter or «Створити» awaits
// `go({ title, emoji })`, its error stays here; «Скасувати» — `cancel`. `blocked` — why it cannot be made yet: the button greys
const p = defineProps({ go: { type: Function, required: true }, blocked: { type: String, default: '' } })
const emit = defineEmits(['cancel'])
const name = ref('')
const busy = ref(false)
const error = ref('')
const field = ref()
const why = computed(() => p.blocked || (parseOption(name.value).text ? '' : 'Назви вид'))
onMounted(() => field.value?.focus())

async function make() {
  if (busy.value || why.value) return
  const { emoji, text } = parseOption(name.value)
  busy.value = true
  error.value = ''
  try {
    await p.go({ title: text, emoji })
  } catch (e) {
    error.value = e.message
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <form class="d-flex flex-wrap gap-2" @submit.prevent="make">
    <input ref="field" v-model="name" class="form-control form-control-sm" placeholder="🚫 Без репозиторію" aria-label="Назва виду"
           title="Назва; емодзі на початку стане значком" :readonly="busy">
    <button type="submit" class="btn btn-sm btn-add" :disabled="busy || !!why" :title="why || null">Створити</button>
    <button type="button" class="btn btn-sm btn-outline-secondary" @click="emit('cancel')">Скасувати</button>
    <div v-if="error" class="w-100 small text-danger">{{ error }}</div>
  </form>
</template>
