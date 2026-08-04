<script setup>
import { reactive, ref, watch } from 'vue'

import { putProfile } from '../api.js'
import ProfileForm from '../components/ProfileForm.vue'
import { user } from '../user.js'

const form = reactive({ last_name: '', first_name: '', patronymic: '', github: '', tg_username: '' })
const saved = ref(false)
const error = ref('')

watch(user, (u) => {
  if (u) for (const k in form) form[k] = u[k]
}, { immediate: true })

async function save() {
  error.value = ''
  try {
    Object.assign(user.value, await putProfile(form))
    saved.value = true
    setTimeout(() => (saved.value = false), 2000)
  } catch (e) {
    error.value = e.message
  }
}
</script>

<template>
  <div v-if="user && user.status !== 'pending'" class="col-lg-8 mx-auto">
    <h1 class="h3 mb-1">Мій профіль</h1>
    <p class="text-secondary mb-4">{{ user.email }}</p>

    <ProfileForm v-model="form" hints @save="save">
      <template #telegram>
        <div class="mt-3">
          <span v-if="user.tg_linked" class="badge text-bg-success">✅ Бот привʼязаний</span>
          <template v-else-if="user.tg_link">
            <a :href="user.tg_link" target="_blank" class="btn btn-outline-primary btn-sm">
              Привʼязати бота
            </a>
            <div class="form-text mt-2">
              Натисни кнопку і в чаті з ботом натисни <b>Start</b> — він упізнає тебе і привʼяже акаунт.
            </div>
          </template>
        </div>
      </template>
    </ProfileForm>

    <div v-if="saved" class="alert alert-success mt-3">Збережено ✓</div>
    <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
  </div>
  <p v-else-if="user" class="text-center mt-5">Доступ до профілю зʼявиться, коли викладач додасть тебе до курсу.</p>
  <p v-else class="text-center mt-5">Спочатку <a href="/api/auth/login">увійди</a>.</p>
</template>
