<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

import { getStudent, putStudent } from '../api.js'
import Crumbs from '../components/Crumbs.vue'
import ProfileForm from '../components/ProfileForm.vue'
import UserHead from '../components/UserHead.vue'
import { useForm } from '../form.js'
import { useTitle } from '../title.js'
import { lookAs, user } from '../user.js'

const nick = useRoute().params.nick
const student = ref(null)
const fio = () => `${student.value.last_name} ${student.value.first_name}`.trim() || student.value.name || nick
useTitle(() => student.value && `Студент: ${fio()}`)
const { form, dirty, saved, error, fill, save } = useForm({
  last_name: '', first_name: '', patronymic: '', github: '',
  tg_username: '', group: '', status: 'student', test: false,
})

onMounted(async () => fill(student.value = await getStudent(nick)))

const submit = () => save(async (f) => (student.value = await putStudent(nick, f)))
</script>

<template>
  <div v-if="user?.status === 'admin' && student">
    <Crumbs :items="[['/students', 'Студи'], [`/students/${nick}`, fio()], 'Редагування']">
      <button v-if="student.status !== 'admin'" class="btn btn-outline-secondary btn-sm ms-auto"
              :title="student.test ? null : 'Лише перегляд'" @click="lookAs(nick)">👁 Очима студента</button>
      <RouterLink :to="{ path: '/activity', query: { user: nick } }" class="btn btn-outline-secondary btn-sm">📈 Активність</RouterLink>
    </Crumbs>
    <UserHead :user="student" />

    <ProfileForm v-model="form" admin :dirty :saved :error @save="submit" />
  </div>
  <p v-else-if="user && user.status !== 'admin'" class="text-center mt-5">Сторінка доступна лише викладачу.</p>
</template>
