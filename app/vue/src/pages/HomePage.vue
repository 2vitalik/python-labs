<script setup>
import { user } from '../user.js'

const statusText = {
  pending: 'Ти в списку. Доступ до курсу надає викладач.',
  student: 'Ти студент курсу.',
  admin: 'Ти викладач.',
}
</script>

<template>
  <div class="col-lg-8 mx-auto text-center mt-5">
    <h1 class="mb-4">Python Labs</h1>
    <template v-if="user">
      <p class="lead">Привіт, {{ user.name || user.email }}!</p>
      <p>{{ statusText[user.status] }}</p>
      <RouterLink v-if="user.status !== 'pending'" to="/profile" class="btn btn-primary">Мій профіль</RouterLink>
    </template>
    <template v-else>
      <p class="lead">Це майбутня система для лабораторних робіт з Python.</p>
      <p>Щоб отримати доступ, авторизуйтесь поштою <b>@nure.ua</b>.</p>
      <a class="btn btn-primary" href="/api/auth/login">Увійти з Google</a>
    </template>
  </div>
</template>
