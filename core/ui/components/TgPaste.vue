<script setup>
import { ref, watch } from 'vue'

import { importMessages } from '../api.js'

// a chat with the student pasted from Telegram (T230): the bot never gets history, so the teacher's copy of it goes in by hand.
// «Розібрати» shows who wrote how much and guesses which name is the student; «Імпортувати» writes the rows
const props = defineProps({ nick: { type: String, required: true } })
const text = ref('')
const look = ref(null)  // authors with counts, the guessed student, header lines with a date we could not read
const student = ref('')
const done = ref(null)
const error = ref('')
const busy = ref(false)

watch(text, () => { look.value = done.value = null; error.value = '' })

async function call(body) {
  busy.value = true
  error.value = ''
  try {
    return await importMessages(props.nick, body)
  } catch (e) {
    error.value = e.message
  } finally {
    busy.value = false
  }
}

async function parse() {
  const r = await call({ text: text.value })
  if (r) { look.value = r; student.value = r.student }
}

async function save() {
  const r = await call({ text: text.value, student: student.value })
  if (r) { done.value = r; look.value = null }
}
</script>

<template>
  <div class="card mb-3">
    <div class="card-header">Telegram: вставити листування</div>
    <div class="card-body">
      <textarea v-model="text" class="form-control font-monospace small" rows="6"
                placeholder="Віталій Ляпота, [24.10.2026 12:34]&#10;Текст повідомлення&#10;&#10;Імʼя студента, [24.10.2026 12:36]&#10;Відповідь"></textarea>
      <div class="form-text">Бот бачить лише те, що написано після підключення. Старе: виділи повідомлення в чаті зі студентом → Копіювати → встав сюди. Те, що вже є, вдруге не додається.</div>
      <div v-if="look" class="mt-3">
        <div v-if="look.errors.length" class="text-danger small mb-2">
          Не розібрав дату в рядках — прибери їх або виправ:
          <div v-for="l in look.errors" :key="l" class="font-monospace">{{ l }}</div>
        </div>
        <template v-if="look.authors.length">
          <div class="small text-secondary mb-1">Хто з них студент? Решта рядків — твої.</div>
          <div v-for="a in look.authors" :key="a.name" class="form-check">
            <input :id="`tg-${a.name}`" v-model="student" class="form-check-input" type="radio" :value="a.name">
            <label :for="`tg-${a.name}`" class="form-check-label">{{ a.name }} <span class="text-secondary">· {{ a.n }}</span></label>
          </div>
          <div class="form-check">
            <input id="tg-none" v-model="student" class="form-check-input" type="radio" value="">
            <label for="tg-none" class="form-check-label text-secondary">ніхто — усе моє</label>
          </div>
        </template>
        <div v-else class="text-secondary small">Не знайшов жодного рядка виду «Імʼя, [дата час]».</div>
      </div>
      <div class="d-flex align-items-center gap-3 mt-3">
        <button v-if="!look" class="btn btn-outline-primary" :disabled="busy || !text.trim()" @click="parse">Розібрати</button>
        <button v-else class="btn btn-primary" :disabled="busy || look.errors.length > 0 || !look.authors.length" @click="save">Імпортувати</button>
        <span v-if="done" class="text-success small">
          ✓ Додано {{ done.added }} · студента {{ done.student }}, твоїх {{ done.teacher }}<template v-if="done.skipped"> · вже було {{ done.skipped }}</template>
        </span>
        <span v-if="error" class="text-danger small">{{ error }}</span>
      </div>
    </div>
  </div>
</template>
