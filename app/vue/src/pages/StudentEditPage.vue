<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

import { getStudent, putStudent } from '../api.js'
import ProfileForm from '../components/ProfileForm.vue'
import UserHead from '../components/UserHead.vue'
import { useForm } from '../form.js'
import { user } from '../user.js'

const nick = useRoute().params.nick
const student = ref(null)
const { form, dirty, saved, error, fill, save } = useForm({
  last_name: '', first_name: '', patronymic: '', github: '',
  tg_username: '', group: '', status: 'student',
})

onMounted(async () => fill(student.value = await getStudent(nick)))

const submit = () => save(async (f) => (student.value = await putStudent(nick, f)))
</script>

<template>
  <div v-if="user?.status === 'admin' && student" class="col-lg-8 mx-auto">
    <RouterLink to="/students" class="d-inline-block mb-2">← До списку</RouterLink>
    <UserHead :user="student" />

    <ProfileForm v-model="form" admin :dirty :saved :error @save="submit" />
  </div>
  <p v-else-if="user && user.status !== 'admin'" class="text-center mt-5">Сторінка доступна лише викладачу.</p>
</template>
