<script setup>
import { ref } from 'vue'

import { openLabDemo } from '../api.js'

// no card for this reader (T375): the teacher pins the cards by the stream's list, so a student has nothing to pick
// here — `why` are the API's words on what to do. The teacher and a test student are not in the list: `demo` — the
// demo card they open by a click
const props = defineProps({ n: Number, why: String, demo: String })
const emit = defineEmits(['got'])
const busy = ref(false)
const error = ref('')

async function open() {
  busy.value = true
  error.value = ''
  try {
    emit('got', await openLabDemo(props.n))
  } catch (e) {
    error.value = e.message
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <section v-if="demo">
    <h2 class="h5">Студент бачить тут свою картку</h2>
    <p>Варіант закріплено за кожним студентом зі списку потоку: він відкриває цю сторінку — і картка вже на ній. У викладача
      й тестового студента своєї картки нема, тож сторінку можна пройти на демо-варіанті.</p>
    <button type="button" class="btn btn-primary" :disabled="busy" @click="open">Відкрити демо-варіант {{ demo }}</button>
    <p v-if="error" class="text-danger mt-2 mb-0">{{ error }}</p>
  </section>
  <section v-else>
    <h2 class="h5">Варіант ще не закріплено</h2>
    <p class="mb-0">{{ why }}</p>
  </section>
</template>
