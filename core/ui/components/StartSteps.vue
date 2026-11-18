<script setup>
import { computed, ref } from 'vue'

import { getMyWeek } from '../api.js'
import { site } from '../site.js'
import { user } from '../user.js'

// above a site's home text, for everyone (T136, T214): what a student can already do — sign in, link the bot and, where
// the site asks for it (site.start.week), mark their week (T177); site.start.note — the site's own line under the steps
const COUNT = { 2: 'два', 3: 'три' }
const active = computed(() => !!user.value && user.value.status !== 'pending')
const week = ref(null)
if (site.start.week && active.value) getMyWeek().then((w) => (week.value = w), () => {})
const steps = computed(() => [
  { done: !!user.value, text: 'Увійти з поштою @nure.ua' },
  { done: !!user.value?.tg_linked, text: 'Привʼязати Telegram-бота — кнопка в профілі', to: active.value ? '/my/profile#telegram' : null },
  ...(site.start.week ? [{ done: !!week.value?.done_at, text: 'Позначити свій тиждень — коли можеш бути на спільній парі', to: active.value ? '/my/week' : null }] : []),
])
</script>

<template>
  <div class="steps-box rounded border px-3 py-2 mb-4">
    <p class="mb-2 fw-bold">Перші {{ COUNT[steps.length] }} кроки:</p>
    <ol class="steps">
      <li v-for="s in steps" :key="s.text" :class="{ 'text-secondary': s.done }">
        <span class="me-2">{{ s.done ? '✅' : '⬜' }}</span>
        <RouterLink v-if="s.to && !s.done" :to="s.to">{{ s.text }}</RouterLink>
        <template v-else>{{ s.text }}</template>
      </li>
    </ol>
    <a v-if="!user" class="btn btn-primary" href="/api/auth/login">Увійти з Google</a>
    <p v-else-if="!active" class="text-secondary mb-0">⏳ Тебе ще нема в списку курсу — доступ до профілю відкриє викладач.</p>
    <p v-if="site.start.note" class="text-secondary small mt-3 mb-0">{{ site.start.note }}</p>
  </div>
</template>

<style scoped>
.steps { list-style: none; padding-left: 0; }
.steps li { margin-bottom: .4rem; }
</style>
