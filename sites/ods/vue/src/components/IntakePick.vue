<script setup>
import { ref, watch } from 'vue'

import Picker from '@core/components/Picker.vue'
import Pop from '@core/components/Pop.vue'

import { students } from '../intake.js'

// a student picked from the list with a search, in a panel by the word that opened it — nothing around moves;
// the list is fetched the first time a panel opens
defineProps({ label: String, busy: Boolean })
const emit = defineEmits(['pick'])
const open = ref(false)
const items = ref(null)
const error = ref('')
watch(open, async (on) => {
  if (!on || items.value) return
  error.value = ''
  try {
    items.value = await students()
  } catch (e) {
    error.value = e.message
  }
})
function pick(it) {
  open.value = false
  emit('pick', it.key)
}
</script>

<template>
  <Pop v-model="open" width="20rem">
    <template #trigger="{ toggle }">
      <button type="button" class="dot" :disabled="busy" :aria-expanded="open" @click="toggle">{{ label }}</button>
    </template>
    <p v-if="error" class="text-danger small mb-0">{{ error }}</p>
    <p v-else-if="!items" class="text-secondary small mb-0">Беру список студентів…</p>
    <Picker v-else inline autofocus small :items placeholder="прізвище, нік, група…" @pick="pick" />
  </Pop>
</template>
