<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

import { getStudent, putStudent } from '../api.js'
import Crumbs from '../components/Crumbs.vue'
import ProfileForm from '../components/ProfileForm.vue'
import UserHead from '../components/UserHead.vue'
import { useForm } from '../form.js'
import { user } from '../user.js'

const nick = useRoute().params.nick
const student = ref(null)
const fio = () => `${student.value.last_name} ${student.value.first_name}`.trim() || student.value.name || nick
const { form, dirty, saved, error, fill, save } = useForm({
  last_name: '', first_name: '', patronymic: '', github: '',
  tg_username: '', group: '', status: 'student',
})

onMounted(async () => fill(student.value = await getStudent(nick)))

const submit = () => save(async (f) => (student.value = await putStudent(nick, f)))
</script>

<template>
  <div v-if="user?.status === 'admin' && student">
    <Crumbs :items="[['/students', 'Студи'], [`/students/${nick}`, fio()], 'Редагування']" />
    <UserHead :user="student" />

    <ProfileForm v-model="form" admin :dirty :saved :error @save="submit" />
  </div>
  <p v-else-if="user && user.status !== 'admin'" class="text-center mt-5">Сторінка доступна лише викладачу.</p>
</template>
