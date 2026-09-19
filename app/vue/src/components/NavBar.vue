<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

import { canAccess, user } from '../user.js'

const isDev = import.meta.env.DEV
const router = useRouter()
const links = [
  ['/games', 'Ігри'], ['/tasks', 'Завдання'], ['/students', 'Студенти'],
  ['/refs', 'Знахідки'], ['/my/game', 'Моя гра'], ['/profile', 'Профіль'],
]
// menu follows route access, so a page and its link open together
const visible = computed(() => links.filter(([to]) => canAccess(router.resolve(to).meta.access)))
</script>

<template>
  <nav class="navbar navbar-expand bg-body-tertiary border-bottom">
    <div class="container">
      <RouterLink class="navbar-brand" to="/">Python Labs</RouterLink>
      <ul class="navbar-nav me-auto">
        <li v-for="[to, text] in visible" :key="to" class="nav-item">
          <RouterLink class="nav-link" :to="to">{{ text }}</RouterLink>
        </li>
      </ul>
      <div class="d-flex align-items-center gap-2">
        <template v-if="user">
          <img v-if="user.picture" :src="user.picture" class="rounded-circle" width="32" height="32" :alt="user.name">
          <span>{{ user.name || user.email }}</span>
          <a class="btn btn-outline-secondary btn-sm" href="/api/auth/logout">Вийти</a>
        </template>
        <template v-else>
          <a v-if="isDev" class="btn btn-outline-secondary btn-sm" href="/api/auth/dev-login">Dev-вхід</a>
          <a class="btn btn-primary btn-sm" href="/api/auth/login">Увійти з Google</a>
        </template>
      </div>
    </div>
  </nav>
</template>
