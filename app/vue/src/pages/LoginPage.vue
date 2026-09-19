<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

import { safeNext, user } from '../user.js'

const route = useRoute()
const isDev = import.meta.env.DEV
const next = computed(() => safeNext(route.query.next))
const query = computed(() => `?next=${encodeURIComponent(next.value)}`)
const errorText = {
  domain: 'Вхід можливий лише з поштою @nure.ua.',
  verify: 'Google не підтвердив цю пошту.',
  oauth: 'Вхід не завершено. Спробуй ще раз.',
  session: 'Сесія завершилась. Увійди знову.',
}
</script>

<template>
  <div class="col-lg-6 mx-auto text-center mt-5">
    <div v-if="errorText[route.query.error]" class="alert alert-warning">{{ errorText[route.query.error] }}</div>
    <template v-if="!user">
      <h1 class="h3 mb-3">Потрібен вхід</h1>
      <p v-if="next !== '/'">Сторінка <code>{{ next }}</code> відкриється після входу з поштою <b>@nure.ua</b>.</p>
      <p v-else>Увійди з поштою <b>@nure.ua</b>.</p>
      <a class="btn btn-primary" :href="'/api/auth/login' + query">Увійти з Google</a>
      <a v-if="isDev" class="btn btn-outline-secondary ms-2" :href="'/api/auth/dev-login' + query">Dev-вхід</a>
    </template>
    <template v-else-if="user.status === 'pending'">
      <h1 class="h3 mb-3">Доступ ще не відкрито</h1>
      <p>Ти в списку. Доступ до курсу надає викладач, після цього сторінка відкриється.</p>
      <RouterLink to="/" class="btn btn-outline-secondary">На головну</RouterLink>
    </template>
    <template v-else>
      <h1 class="h3 mb-3">Лише для викладача</h1>
      <p>Сторінка <code>{{ next }}</code> студентам поки недоступна.</p>
      <RouterLink to="/" class="btn btn-outline-secondary">На головну</RouterLink>
    </template>
  </div>
</template>
