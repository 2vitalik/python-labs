<script setup>
import { computed } from 'vue'

import { user } from '../user.js'

// home page while the guide is closed (T136): what a student can already do — sign in, fill the profile, link the bot
const active = computed(() => !!user.value && user.value.status !== 'pending')
const profile = computed(() => (active.value ? '/my/profile' : null))
const steps = computed(() => [
  { done: !!user.value, text: 'Увійти з поштою @nure.ua' },
  { done: active.value && !!user.value.github, text: 'Заповнити профіль: ПІБ, GitHub, Telegram', to: profile.value },
  { done: !!user.value?.tg_linked, text: 'Привʼязати Telegram-бота — кнопка в профілі', to: profile.value },
])
</script>

<template>
  <div>
    <p class="lead">Лабораторні з Python — одна гра на весь семестр 🎮</p>
    <div class="alert alert-light border">🚧 Методичка ще пишеться й відкриється тут пізніше. Поки що — реєстрація:</div>
    <ol class="steps">
      <li v-for="s in steps" :key="s.text" :class="{ 'text-secondary': s.done }">
        <span class="me-2">{{ s.done ? '✅' : '⬜' }}</span>
        <RouterLink v-if="s.to && !s.done" :to="s.to">{{ s.text }}</RouterLink>
        <template v-else>{{ s.text }}</template>
      </li>
    </ol>
    <a v-if="!user" class="btn btn-primary" href="/api/auth/login">Увійти з Google</a>
    <p v-else-if="!active" class="text-secondary mb-0">⏳ Тебе ще нема в списку курсу — доступ до профілю відкриє викладач.</p>
  </div>
</template>

<style scoped>
.steps { list-style: none; padding-left: 0; }
.steps li { margin-bottom: .4rem; }
</style>
