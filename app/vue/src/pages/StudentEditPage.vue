<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useRoute } from 'vue-router'

import { getStudent, putStudent } from '../api.js'
import ProfileForm from '../components/ProfileForm.vue'
import { user } from '../user.js'

const nick = useRoute().params.nick
const student = ref(null)
const form = reactive({
  last_name: '', first_name: '', patronymic: '', github: '',
  tg_username: '', group: '', status: 'student',
})
const saved = ref(false)
const error = ref('')

onMounted(async () => {
  student.value = await getStudent(nick)
  for (const k in form) form[k] = student.value[k]
})

async function save() {
  error.value = ''
  try {
    student.value = await putStudent(nick, form)
    saved.value = true
    setTimeout(() => (saved.value = false), 2000)
  } catch (e) {
    error.value = e.message
  }
}
</script>

<template>
  <div v-if="user?.status === 'admin' && student" class="col-lg-8 mx-auto">
    <RouterLink to="/students" class="d-inline-block mb-2">← До списку</RouterLink>
    <h1 class="h3 mb-1">{{ student.last_name }} {{ student.first_name }}</h1>
    <p class="text-secondary mb-4">{{ student.email }}</p>

    <ProfileForm v-model="form" admin @save="save" />

    <div v-if="saved" class="alert alert-success mt-3">Збережено ✓</div>
    <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
  </div>
  <p v-else-if="user && user.status !== 'admin'" class="text-center mt-5">Сторінка доступна лише викладачу.</p>
</template>
