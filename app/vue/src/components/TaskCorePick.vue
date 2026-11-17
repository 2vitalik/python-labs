<script setup>
import { computed, ref } from 'vue'

import { saveTask } from '../taskForm.js'

// the teacher's word «в основі» / «за запитом» of a card where its status reads (T319): a click flips it and saves at once,
// as a pick of the status does (T306); the history keeps it, «↩» there takes it back
const props = defineProps({ task: Object })
const busy = ref(false)
const saved = ref(false)
const error = ref('')
const tip = computed(() => (props.task.core
  ? 'В основі: студенти заявляють одразу.\nКлік — зробити «за запитом»'
  : 'За запитом: студенти додають з одним реченням, монетка — коли картка в основі.\nКлік — відкрити для всіх'))

async function flip() {
  if (busy.value) return
  busy.value = true
  error.value = ''
  try {
    await saveTask(props.task, { core: !props.task.core })
    saved.value = true
    setTimeout(() => (saved.value = false), 1400)
  } catch (e) {
    error.value = e.message
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <span class="inl can pick" :class="{ saved, 'opacity-50': busy }" role="button" tabindex="0" :title="tip"
        @click.stop="flip" @keydown.enter.prevent="flip">{{ task.core ? 'в основі' : 'за запитом' }}</span>
  <span v-if="error" class="text-danger"> {{ error }}</span>
</template>
