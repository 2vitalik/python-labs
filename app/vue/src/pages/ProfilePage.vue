<script setup>
import { onUnmounted, ref, watch } from 'vue'

import { getMe, putProfile, unlinkTelegram } from '../api.js'
import Crumbs from '../components/Crumbs.vue'
import ProfileForm from '../components/ProfileForm.vue'
import UserHead from '../components/UserHead.vue'
import { useForm } from '../form.js'
import { user } from '../user.js'

const { form, dirty, saved, error, fill, save } = useForm({
  last_name: '', first_name: '', patronymic: '', github: '', tg_username: '',
})

watch(user, (u) => u && fill(u), { immediate: true })

function apply(u) {  // patch in place: replacing user.value would reset the form
  Object.assign(user.value, u)
  fill({ tg_username: u.tg_username })
}

let poll
function watchLink() {  // student went to Telegram: poll until the bot writes chat_id, up to 3 min
  let left = 90
  clearInterval(poll)
  poll = setInterval(async () => {
    const u = await getMe().catch(() => null)
    if (u?.tg_linked) apply(u)
    if (u?.tg_linked || !--left) clearInterval(poll)
  }, 2000)
}
onUnmounted(() => clearInterval(poll))

const asking = ref(false)  // «відвʼязати» is one tap away from a thumb: ask first
const unlink = async () => { asking.value = false; apply(await unlinkTelegram()) }

const submit = () => save(async (f) => {
  const u = await putProfile(f)
  Object.assign(user.value, u)
  return u
})
</script>

<template>
  <div v-if="user && user.status !== 'pending'">
    <Crumbs :items="['Профіль']" />
    <UserHead :user title="Мій профіль" />

    <ProfileForm v-model="form" hints :dirty :saved :error @save="submit">
      <template #telegram>
        <div class="mt-3">
          <template v-if="user.tg_linked">
            <span class="badge text-bg-success">✅ Бот привʼязаний</span>
            <template v-if="asking">
              <span class="ms-2 small">Відвʼязати бота?</span>
              <button type="button" class="btn btn-outline-danger btn-sm ms-2" @click="unlink">Так, відвʼязати</button>
              <a href="#" class="ms-2 small text-secondary" @click.prevent="asking = false">ні</a>
            </template>
            <a v-else href="#" class="ms-2 small text-secondary" @click.prevent="asking = true">відвʼязати</a>
          </template>
          <template v-else-if="user.tg_link">
            <a :href="user.tg_link" target="_blank" class="btn btn-outline-primary btn-sm" @click="watchLink">
              Привʼязати бота
            </a>
            <div class="form-text mt-2">
              <ul class="mb-0 ps-3">
                <li>Кнопка відкриє чат з ботом і передасть йому код привʼязки:
                  <ul class="ps-3">
                    <li>у новому чаті — натисни <b>Start</b></li>
                    <li>у знайомому — нічого не треба, код піде сам</li>
                  </ul>
                </li>
                <li>Бот відповість «✔️ Записав тебе», а сторінка помітить це сама</li>
              </ul>
            </div>
          </template>
        </div>
      </template>
    </ProfileForm>
  </div>
  <p v-else-if="user" class="text-center mt-5">Доступ до профілю зʼявиться, коли викладач додасть тебе до курсу.</p>
  <p v-else class="text-center mt-5">Спочатку <a href="/api/auth/login">увійди</a>.</p>
</template>
